# -*- coding: utf-8 -*-
"""整個『暑期班務研習』統一按年度攤平、保留影音、114 去重。
做法：以已整理好的『雲端研習資料下載』為底（111年/114年/報名與統計表/獨立專題與實務資料），
補進 109年、113年兩個年度與兩個保留影音，最後攤平到頂層、刪除舊散檔與雲端夾。
"""
import os, sys, io, glob, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = r"C:\Users\kevin\Desktop\Taospace\Taofiles\班務組\暑期班務研習"
CLOUD = os.path.join(ROOT, "雲端研習資料下載")
STAGING = os.path.join(ROOT, "_整理暫存")
IGNORE = shutil.ignore_patterns("~$*")

def p(*a):
    return os.path.join(ROOT, *a)

if os.path.exists(STAGING):
    shutil.rmtree(STAGING)

# 1) 以雲端研習資料下載為底 → 暫存（四組現成：111年/114年/報名與統計表/獨立專題與實務資料）
shutil.copytree(CLOUD, STAGING, ignore=IGNORE)

# 2) 109年
d109 = os.path.join(STAGING, "109年 學界傳題講師研習")
os.makedirs(d109, exist_ok=True)
shutil.copy2(p("109 台中道場學界傳題講師研習_0713.0720.docx"), d109)

# 3) 113年（同心同德 + 帶班講師的使命與職責，含鮭魚影片）
d113 = os.path.join(STAGING, "113年 帶班講師研習")
os.makedirs(d113, exist_ok=True)
shutil.copy2(p("1130820帶班講師 同心同德.pptx"), d113)
shutil.copytree(p("帶班講師的使命與職責"),
                os.path.join(d113, "帶班講師的使命與職責"), ignore=IGNORE)

# 4) 王陽明影片 → 併入 114年 德字班 黃愛智（保留影音）
dezi = os.path.join(STAGING, "114年 班務傳題講師研習", "德字班 - 黃愛智講師")
for mp4 in glob.glob(os.path.join(p("深入經藏 淺出妙諦 20250812"), "*.mp4")):
    shutil.copy2(mp4, dezi)

# 核對
total = sum(len([f for f in fs if not f.startswith("~$")])
            for _, _, fs in os.walk(STAGING))
print(f"暫存夾共 {total} 個檔（預期 25）")
if total != 25:
    print("!! 檔數不符，中止，不刪任何舊檔。")
    sys.exit(1)

# 5) 刪舊散檔與雲端夾
for item in ["109 台中道場學界傳題講師研習_0713.0720.docx",
             "1130820帶班講師 同心同德.pptx",
             "114.08.12_崇元研習(學)_古典智慧的現代實踐【如何培養經典詮釋能力與講述技巧】",
             "帶班講師的使命與職責",
             "新民班傳題研習20250812.pptx",
             "深入經藏 淺出妙諦 20250812",
             "雲端研習資料下載"]:
    tgt = p(item)
    if os.path.isdir(tgt):
        shutil.rmtree(tgt)
    elif os.path.exists(tgt):
        os.remove(tgt)

# 6) 攤平：暫存內各年度夾移到頂層，移除暫存殼
for name in os.listdir(STAGING):
    shutil.move(os.path.join(STAGING, name), p(name))
os.rmdir(STAGING)

print("整理完成。\n")
print("======== 暑期班務研習（整理後）========")
for dp, dns, fs in os.walk(ROOT):
    dns.sort(); fs.sort()
    depth = dp.replace(ROOT, "").count(os.sep)
    indent = "  " * depth
    name = os.path.basename(dp) if depth else "暑期班務研習"
    print(f"{indent}{name}/")
    for fn in fs:
        if not fn.startswith("~$"):
            print(f"{indent}  {fn}")
fin = sum(len([f for f in fs if not f.startswith('~$')]) for _, _, fs in os.walk(ROOT))
print(f"\n合計 {fin} 個檔。")
