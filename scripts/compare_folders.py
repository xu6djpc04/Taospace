import os
import hashlib
import sys

sys.stdout.reconfigure(encoding='utf-8')

dir1 = r'C:\Users\kevin\Desktop\Taospace\Taofiles\班務組\暑期班務研習\雲端研習資料下載'
dir2 = r'C:\Users\kevin\Desktop\Taospace\Taofiles\班務組\暑期班務研習\雲端下載_1150615'

def get_files(directory):
    files = []
    if not os.path.exists(directory):
        print(f'Error: Directory not found - {directory}')
        return files
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(root, filename)
            rel_path = os.path.relpath(filepath, directory)
            files.append({
                'name': filename,
                'path': filepath,
                'rel_path': rel_path,
                'size': os.path.getsize(filepath)
            })
    return files

files1 = get_files(dir1)
files2 = get_files(dir2)

if not files1 and not files2:
    print('Both directories are empty or not found.')
    sys.exit()

by_name1 = {}
for f in files1:
    by_name1.setdefault(f['name'], []).append(f)

by_name2 = {}
for f in files2:
    by_name2.setdefault(f['name'], []).append(f)

exact_duplicates = []
name_duplicates = []

for name, list2 in by_name2.items():
    if name in by_name1:
        list1 = by_name1[name]
        for f2 in list2:
            matched_exact = False
            for f1 in list1:
                if f1['size'] == f2['size']:
                    with open(f1['path'], 'rb') as fp1, open(f2['path'], 'rb') as fp2:
                        if fp1.read() == fp2.read():
                            exact_duplicates.append((f1, f2))
                            matched_exact = True
                            break
            if not matched_exact:
                for f1 in list1:
                    name_duplicates.append((f1, f2))

print('=== 檢查結果 ===')
if exact_duplicates:
    print(f'\n【完全相同的檔案】(檔名與內容皆相同，共 {len(exact_duplicates)} 筆):')
    for f1, f2 in exact_duplicates:
        print(f'- 檔名: {f1["name"]}')
        print(f'  位於 1: 雲端研習資料下載\\{f1["rel_path"]}')
        print(f'  位於 2: 雲端下載_1150615\\{f2["rel_path"]}')
else:
    print('\n沒有找到【完全相同】的檔案。')

if name_duplicates:
    print(f'\n【同名但內容/大小不同的檔案】(共 {len(name_duplicates)} 筆):')
    for f1, f2 in name_duplicates:
        print(f'- 檔名: {f1["name"]}')
        print(f'  位於 1: 雲端研習資料下載\\{f1["rel_path"]} (大小: {f1["size"]} bytes)')
        print(f'  位於 2: 雲端下載_1150615\\{f2["rel_path"]} (大小: {f2["size"]} bytes)')

print('\n【只存在於 雲端研習資料下載 的檔案】:')
unique1 = 0
for name, list1 in by_name1.items():
    if name not in by_name2:
        for f in list1:
            print(f'- {f["rel_path"]}')
            unique1 += 1
if unique1 == 0: print('  (無)')

print('\n【只存在於 雲端下載_1150615 的檔案】:')
unique2 = 0
for name, list2 in by_name2.items():
    if name not in by_name1:
        for f in list2:
            print(f'- {f["rel_path"]}')
            unique2 += 1
if unique2 == 0: print('  (無)')
