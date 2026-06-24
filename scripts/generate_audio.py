import asyncio
import edge_tts
import re
import unicodedata
import os

async def generate_audio():
    in_file = unicodedata.normalize('NFC', r"C:\Users\kevin\Desktop\Taospace\output\中庸心得分享逐字稿_115年.md")
    out_file = unicodedata.normalize('NFC', r"C:\Users\kevin\Desktop\Taospace\output\中庸心得分享逐字稿_純淨版_115年.mp3")
    
    with open(in_file, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()

    clean_lines = []
    for line in lines:
        # 只抓取真正要唸出來的逐字稿段落 (以兩個空白加一個大於符號開頭的行)
        if line.startswith('  > '):
            clean_line = line[4:].strip()
            # 移除講者註記，例如：(註：講者可擇一發揮，以下以師母的故事為例)
            clean_line = re.sub(r'\(註：.*?\)', '', clean_line)
            if clean_line:
                clean_lines.append(clean_line)
                
    text = '\n\n'.join(clean_lines)

    # Use YunJheNeural
    voice = 'zh-TW-YunJheNeural'
    
    communicate = edge_tts.Communicate(text, voice, rate="+0%")
    await communicate.save(out_file)

if __name__ == "__main__":
    asyncio.run(generate_audio())
    print("Audio generation complete.")
