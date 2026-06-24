import asyncio
import edge_tts
import re
import unicodedata
import os

async def generate_audio():
    in_file = unicodedata.normalize('NFC', r"C:\Users\kevin\Desktop\Taospace\output\美安事業執行重點逐字稿_115年.md")
    out_file = unicodedata.normalize('NFC', r"C:\Users\kevin\Desktop\Taospace\output\美安事業執行重點逐字稿_純淨版_115年.mp3")
    
    with open(in_file, 'r', encoding='utf-8-sig') as f:
        lines = f.readlines()

    clean_lines = []
    for line in lines:
        if line.startswith('  > '):
            clean_line = line[4:].strip()
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
