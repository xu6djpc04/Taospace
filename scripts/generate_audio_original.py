import asyncio
import edge_tts
import re
import unicodedata
import os

async def generate_audio():
    in_file = unicodedata.normalize('NFC', r"C:\Users\kevin\Desktop\Taospace\output\美安事業原音逐字稿_115年.md")
    out_file = unicodedata.normalize('NFC', r"C:\Users\kevin\Desktop\Taospace\output\美安事業原音逐字稿_純淨版_115年.mp3")
    
    with open(in_file, 'r', encoding='utf-8-sig') as f:
        text = f.read()

    # --- 修正發音與替換邏輯 ---
    text = text.replace('SHOP.COM', 'Shop dot com')
    text = text.replace('7-11', 'Seven Eleven')
    
    # 數字區間
    text = re.sub(r'(\d+)-(\d+)', r'\1 到 \2', text)
    
    # 修正「2」的語氣讀音為「兩」
    text = text.replace('2 到 3', '兩到三')
    text = text.replace('2 到 4', '兩到四')
    text = text.replace('2 個', '兩個')
    
    # 修正 622 法則唸法 (拆開來唸，避免被唸成 六百二十二)
    text = text.replace('622法則', '六二二法則')
    text = text.replace('662法則', '六二二法則') # 預防錯字

    # --- 移除所有 markdown 與特殊符號 ---
    text = text.replace('*', '')  # 徹底移除所有半形星號
    text = text.replace('＊', '') # 徹底移除所有全形星號
    text = re.sub(r'-{3,}', '', text)  # 移除分隔線 ---
    text = text.replace('→', '，也就是') 
    
    clean_lines = [line.strip() for line in text.split('\n') if line.strip()]
    text = '\n\n'.join(clean_lines)

    voice = 'zh-TW-YunJheNeural'
    
    if os.path.exists(out_file):
        os.remove(out_file)
        
    communicate = edge_tts.Communicate(text, voice, rate="+0%")
    await communicate.save(out_file)

if __name__ == "__main__":
    asyncio.run(generate_audio())
    print("Audio generation complete.")
