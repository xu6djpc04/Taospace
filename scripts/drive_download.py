# -*- coding: utf-8 -*-
"""可重用的 Google Drive 下載工具。

把過往踩過的雷一次內建處理：
  - 中文終端機編碼（cp950 UnicodeEncodeError）→ 強制 stdout 用 UTF-8。
  - Google 原生不可下載檔（表單、繪圖等）→ 自動跳過並列出，不中斷。
  - 簡報／文件／試算表 → 透過 API export 成 .pptx/.docx/.xlsx。
  - 單檔下載失敗 → 清掉半成品、記錄、繼續下一個，不讓整批掛掉。
  - 已存在的檔 → 跳過（可重跑、可續傳）。
  - 資料夾遞迴並以 id 去重，避免母／子資料夾重複下載。
  - 平行下載（預設 8 條）加速大量小檔。
  - 影音大檔可用 --max-media-mb 設上限先略過。

用法範例：
  # 依名稱抓資料夾（遞迴），存到 references/
  python drive_download.py --folder "114 班務傳題講師研習" --dest references/114班務傳題

  # 依關鍵字（name contains）抓所有符合的檔與資料夾
  python drive_download.py --keyword 暑期 --dest references/暑期

  # 只列出不下載（驗證用，不耗流量）
  python drive_download.py --folder "114 班務傳題講師研習" --dest x --list

  # 影音檔超過 80MB 先略過、用 12 條平行
  python drive_download.py --folder X --dest Y --max-media-mb 80 --workers 12
"""
import os
import io
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# 雷①：中文輸出。Python 3.7+ 直接 reconfigure，遇到無法編的字也不炸。
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from google_drive import get_service, EXPORT_MIME  # noqa: E402
from googleapiclient.http import MediaIoBaseDownload  # noqa: E402

FOLDER_MIME = "application/vnd.google-apps.folder"
MEDIA_EXT = (".mp4", ".wav", ".m4a", ".aac", ".mov", ".mp3", ".avi", ".mkv")


def list_children(service, folder_id):
    files, page_token = [], None
    while True:
        resp = service.files().list(
            q=f"'{folder_id}' in parents and trashed = false",
            pageSize=200, pageToken=page_token,
            fields="nextPageToken, files(id,name,mimeType,size)",
        ).execute()
        files.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return files


def search(service, keyword, exact=False):
    op = "=" if exact else "contains"
    files, page_token = [], None
    while True:
        resp = service.files().list(
            q=f"name {op} '{keyword}' and trashed = false",
            pageSize=200, pageToken=page_token,
            fields="nextPageToken, files(id,name,mimeType,size)",
        ).execute()
        files.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return files


def collect_tasks(service, item, dest_dir, tasks, visited, max_media_bytes, nondl):
    """遞迴展開資料夾，把所有「要下載的單檔」攤平成 (file, dest_dir) 清單。"""
    mime = item["mimeType"]
    if mime == FOLDER_MIME:
        if item["id"] in visited:          # 雷⑤：母/子資料夾去重
            return
        visited.add(item["id"])
        sub_dest = os.path.join(dest_dir, _safe(item["name"]))
        for child in list_children(service, item["id"]):
            collect_tasks(service, child, sub_dest, tasks, visited, max_media_bytes, nondl)
        return
    # 雷②：Google 原生但不可匯出（表單、繪圖、網站…）→ 跳過
    if mime.startswith("application/vnd.google-apps") and mime not in EXPORT_MIME:
        nondl.append((item["name"], "不可匯出：" + mime.split(".")[-1]))
        return
    # 影音上限
    if max_media_bytes and item["name"].lower().endswith(MEDIA_EXT):
        size = int(item.get("size", 0) or 0)
        if size > max_media_bytes:
            nondl.append((item["name"], f"影音 {round(size/1048576,1)}MB 超過上限，略過"))
            return
    tasks.append((item, dest_dir))


def _safe(name):
    for ch in '<>:"/\\|?*':
        name = name.replace(ch, "_")
    return name.strip()


def download_one(service, item, dest_dir):
    name, mime = item["name"], item["mimeType"]
    if mime in EXPORT_MIME:
        export_mime, ext = EXPORT_MIME[mime]
        if not name.endswith(ext):
            name += ext
        request = service.files().export_media(fileId=item["id"], mimeType=export_mime)
    else:
        request = service.files().get_media(fileId=item["id"])

    os.makedirs(dest_dir, exist_ok=True)
    path = os.path.join(dest_dir, _safe(name))
    if os.path.exists(path):                 # 雷④：已存在跳過（可重跑）
        return ("exist", name)
    try:                                     # 雷③：失敗清半成品、不中斷
        with io.FileIO(path, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request, chunksize=8 * 1024 * 1024)
            done = False
            while not done:
                _, done = downloader.next_chunk()
        return ("ok", name)
    except Exception as e:
        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass
        return ("fail", f"{name}　（{str(e)[:80]}）")


def main():
    ap = argparse.ArgumentParser(description="可重用的 Google Drive 下載工具")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--folder", help="資料夾名稱（精確比對，遞迴下載）")
    g.add_argument("--keyword", help="名稱關鍵字（name contains，檔與資料夾都抓）")
    ap.add_argument("--dest", required=True, help="下載目的地（相對於專案根或絕對路徑）")
    ap.add_argument("--max-media-mb", type=float, default=0,
                    help="影音檔大小上限(MB)，超過先略過；0=不限制")
    ap.add_argument("--workers", type=int, default=8, help="平行下載條數（預設 8）")
    ap.add_argument("--list", action="store_true", help="只列出要下載什麼，不實際下載")
    args = ap.parse_args()

    base = os.path.dirname(os.path.abspath(__file__))
    dest = args.dest if os.path.isabs(args.dest) else os.path.join(base, args.dest)
    max_media = int(args.max_media_mb * 1048576) if args.max_media_mb else 0

    service = get_service()

    if args.folder:
        roots = [f for f in search(service, args.folder, exact=True) if f["mimeType"] == FOLDER_MIME]
        if not roots:
            print(f"找不到資料夾：{args.folder}")
            return
    else:
        roots = search(service, args.keyword, exact=False)
        if not roots:
            print(f"找不到符合「{args.keyword}」的項目")
            return

    tasks, visited, nondl = [], set(), []
    for r in roots:
        collect_tasks(service, r, dest, tasks, visited, max_media, nondl)

    print(f"展開完成：{len(tasks)} 個檔待下載；{len(nondl)} 個略過。\n")
    if args.list:
        for item, d in tasks:
            print(f"  [下載] {os.path.relpath(d, base)}\\{item['name']}")
        for n, why in nondl:
            print(f"  [略過] {n}　（{why}）")
        return

    ok = exist = 0
    fails = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:   # 雷⑥：平行
        futs = {pool.submit(download_one, service, it, d): it for it, d in tasks}
        for fut in as_completed(futs):
            status, msg = fut.result()
            if status == "ok":
                ok += 1
                print(f"  下載：{msg}")
            elif status == "exist":
                exist += 1
            else:
                fails.append(msg)

    print("\n========== 結果 ==========")
    print(f"新下載 {ok}　已存在略過 {exist}　失敗 {len(fails)}　不可下載 {len(nondl)}")
    for n, why in nondl:
        print(f"  [不可下載] {n}　（{why}）")
    for m in fails:
        print(f"  [失敗] {m}")


if __name__ == "__main__":
    main()
