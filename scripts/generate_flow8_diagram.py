# -*- coding: utf-8 -*-
import os
import unicodedata

# Content to write
content = """# Flow 8 設備連接規劃分析圖

以下是針對您即將舉辦的活動所規劃的設備連接分析圖，包含了麥克風、電腦訊號輸入，以及針對卡拉 OK 擴大機的輸出建議。

```mermaid
graph TD
    %% 節點定義
    subgraph 麥克風輸入 (Microphones)
        M1["Mipro ACT-589 (無線麥克風接收機)"]
        M2["Mipro MA-300D (無線擴音機/接收機)"]
    end

    subgraph 電腦輸入 (Computers)
        C1["第一臺電腦"]
        C2["第二臺電腦"]
        Cable2["20米 3.5mm 對 3.5mm 延長線"]
        Adapter2["母 3.5mm 轉 2TS 轉接頭"]
    end

    Flow8{"Behringer Flow 8<br/>數位混音器"}

    subgraph 擴音輸出 (Output)
        Amp["現場卡拉 OK 擴大機<br/>(僅支援 RCA 輸入)"]
        Speakers["現場喇叭"]
    end

    %% 連接關係 - 輸入
    M1 -- "XLR 或 6.3mm 線材" --> Flow8
    M2 -- "6.3mm 線材 (Line Out)" --> Flow8
    
    C1 -- "3.5mm 轉 2TS 線材" --> Flow8
    
    C2 -- "3.5mm 輸出" --> Cable2
    Cable2 --> Adapter2
    Adapter2 -- "2TS 輸出" --> Flow8

    %% 連接關係 - 輸出 (解決方案)
    Flow8 -- "方案一：XLR(母) 轉 RCA 線材<br/>方案二：6.3mm TS 轉 RCA 線材" --> Amp
    Amp -- "喇叭線" --> Speakers

    %% 樣式設定
    classDef mixer fill:#ffcc00,stroke:#333,stroke-width:2px,color:#000;
    classDef audio fill:#66ccff,stroke:#333,stroke-width:1px,color:#000;
    classDef device fill:#99ff99,stroke:#333,stroke-width:1px,color:#000;
    classDef warning fill:#ff9999,stroke:#333,stroke-width:2px,stroke-dasharray: 5 5,color:#000;

    class Flow8 mixer;
    class M1,M2,C1,C2 audio;
    class Cable2,Adapter2 device;
    class Amp warning;
```

### 💡 針對擴大機 RCA 輸入的解決方案

Behringer Flow 8 的主要輸出為 **XLR (Main Out)** 與 **6.3mm (Monitor Out)**，要接入僅有 RCA 輸入的卡拉 OK 擴大機，建議採用以下兩種方式之一：

1. **方案一：使用 XLR 轉 RCA 線材（推薦）**
   - **接法**：從 Flow 8 的 `MAIN OUT L/R` (XLR 公頭) 接出，使用一條 **雙 XLR (母) 轉 雙 RCA (公)** 的音源線，直接接入擴大機的 RCA 輸入孔。
   - **優點**：Main Out 是主要輸出，控制最直覺。

2. **方案二：使用 6.3mm (TS) 轉 RCA 線材**
   - **接法**：從 Flow 8 的 `MONITOR SEND 1/2` (6.3mm 孔) 接出，使用 **雙 6.3mm (TS 單聲道) 轉 雙 RCA (公)** 的音源線，接入擴大機。
   - **注意**：這會佔用 Monitor 輸出，且音量需透過 Monitor 旋鈕控制，若沒有要接監聽喇叭的話也可以這樣使用。

> [!TIP]
> **電腦二的長距離傳輸建議**
> 第二臺電腦使用 20 米的 3.5mm 線材傳輸非平衡訊號，距離較長可能會有些許底噪或訊號衰減。如果現場有雜音問題，建議可以在電腦端加上一個 DI Box (直接輸出盒) 轉成平衡訊號傳輸，或是確保線材品質良好且盡量避開電源線走線。
"""

def main():
    # 建立輸出路徑
    base_path = r"C:\Users\kevin\Desktop\Taospace\output"
    filename = "設備連接規劃_115年.md"
    
    # NFC 正規化含中文檔名的路徑 (遵循 Windows Python 腳本編碼標準)
    filename = unicodedata.normalize('NFC', filename)
    target_path = os.path.join(base_path, filename)
    
    # 確保資料夾存在
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        
    # 以 UTF-8 with BOM 寫入檔案 (遵循 Windows Python 腳本編碼標準)
    with open(target_path, 'w', encoding='utf-8-sig') as f:
        f.write(content)
        
    print(f"成功建立檔案：{target_path}")

    # 用一個含中文字的真實路徑執行一次驗證
    try:
        with open(target_path, 'r', encoding='utf-8-sig') as f:
            test_content = f.read()
            if "Behringer Flow 8" in test_content:
                print("中文路徑驗證成功！")
            else:
                print("驗證失敗：內容不符。")
    except Exception as e:
        print(f"驗證失敗：{e}")

if __name__ == "__main__":
    main()
