# -*- coding: utf-8 -*-
import os
import unicodedata

xml_content = """<mxfile host="Electron">
  <diagram name="Flow 8 連接圖" id="flow8-diagram">
    <mxGraphModel dx="1212" dy="736" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1100" pageHeight="600" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        
        <!-- Title -->
        <mxCell id="title" parent="1" style="text;html=1;fontSize=17;fontStyle=1;align=center;verticalAlign=middle;" value="&lt;font style=&quot;font-size: 24px;&quot;&gt;Flow 8 設備連接規劃圖&lt;/font&gt;" vertex="1">
          <mxGeometry height="28" width="1040" x="30" y="20" as="geometry" />
        </mxCell>
        
        <!-- Zones -->
        <mxCell id="zone_src" parent="1" style="rounded=0;whiteSpace=wrap;html=1;dashed=1;fillColor=none;strokeColor=#6c8ebf;verticalAlign=top;fontStyle=1;fontSize=13;" value="&lt;font style=&quot;font-size: 18px;&quot;&gt;訊號源&lt;/font&gt;" vertex="1">
          <mxGeometry height="420" width="270" x="30" y="60" as="geometry" />
        </mxCell>
        <mxCell id="zone_core" parent="1" style="rounded=0;whiteSpace=wrap;html=1;dashed=1;fillColor=none;strokeColor=#82b366;verticalAlign=top;fontStyle=1;fontSize=13;" value="&lt;font style=&quot;font-size: 18px;&quot;&gt;混音控台&lt;/font&gt;" vertex="1">
          <mxGeometry height="420" width="300" x="320" y="60" as="geometry" />
        </mxCell>
        <mxCell id="zone_out" parent="1" style="rounded=0;whiteSpace=wrap;html=1;dashed=1;fillColor=none;strokeColor=#d6b656;verticalAlign=top;fontStyle=1;fontSize=13;" value="&lt;font style=&quot;font-size: 18px;&quot;&gt;擴音輸出&lt;/font&gt;" vertex="1">
          <mxGeometry height="420" width="430" x="640" y="60" as="geometry" />
        </mxCell>
        
        <!-- Sources -->
        <mxCell id="mic1" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" value="Mipro ACT-589&#xa;(無線麥克風接收機)" vertex="1">
          <mxGeometry height="50" width="230" x="50" y="110" as="geometry" />
        </mxCell>
        <mxCell id="mic2" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;" value="Mipro MA-300D&#xa;(無線擴音機/接收機)" vertex="1">
          <mxGeometry height="50" width="230" x="50" y="190" as="geometry" />
        </mxCell>
        <mxCell id="pc1" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" value="第一臺電腦" vertex="1">
          <mxGeometry height="50" width="230" x="50" y="270" as="geometry" />
        </mxCell>
        <mxCell id="pc2" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;" value="第二臺電腦&#xa;(20米 3.5延長線 ＋ 轉2TS頭)" vertex="1">
          <mxGeometry height="60" width="230" x="50" y="350" as="geometry" />
        </mxCell>
        
        <!-- Console -->
        <mxCell id="flow8" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;fontStyle=1;fontSize=16;" value="Behringer Flow 8&#xa;數位混音器" vertex="1">
          <mxGeometry height="160" width="160" x="390" y="180" as="geometry" />
        </mxCell>
        
        <!-- Outputs -->
        <mxCell id="amp" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;" value="現場卡拉 OK 擴大機&#xa;(僅支援 RCA 輸入)" vertex="1">
          <mxGeometry height="60" width="160" x="730" y="230" as="geometry" />
        </mxCell>
        <mxCell id="speakers" parent="1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#666666;" value="現場喇叭" vertex="1">
          <mxGeometry height="60" width="100" x="950" y="230" as="geometry" />
        </mxCell>
        
        <!-- Edges: Sources to Console -->
        <mxCell id="e_mic1" edge="1" parent="1" source="mic1" target="flow8" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#6c8ebf;endArrow=block;fontSize=11;" value="XLR 或 6.3mm">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="340" y="135" />
              <mxPoint x="340" y="210" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="e_mic2" edge="1" parent="1" source="mic2" target="flow8" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#6c8ebf;endArrow=block;fontSize=11;" value="6.3mm (Line Out)">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="340" y="215" />
              <mxPoint x="340" y="240" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="e_pc1" edge="1" parent="1" source="pc1" target="flow8" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#82b366;endArrow=block;fontSize=11;" value="3.5mm 轉 2TS">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="340" y="295" />
              <mxPoint x="340" y="270" />
            </Array>
          </mxGeometry>
        </mxCell>
        <mxCell id="e_pc2" edge="1" parent="1" source="pc2" target="flow8" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#82b366;endArrow=block;fontSize=11;" value="2TS 輸入">
          <mxGeometry relative="1" as="geometry">
            <Array as="points">
              <mxPoint x="340" y="380" />
              <mxPoint x="340" y="300" />
            </Array>
          </mxGeometry>
        </mxCell>
        
        <!-- Edges: Console to Output -->
        <mxCell id="e_amp" edge="1" parent="1" source="flow8" target="amp" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#d6b656;endArrow=block;fontSize=11;" value="方案一：XLR(母) 轉 RCA 線材&#xa;方案二：6.3mm TS 轉 RCA 線材">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
        
        <!-- Edges: Amp to Speakers -->
        <mxCell id="e_speakers" edge="1" parent="1" source="amp" target="speakers" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;strokeColor=#666666;endArrow=block;fontSize=11;" value="喇叭線">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>

        <!-- Legend -->
        <mxCell id="legend" parent="1" style="text;html=1;align=left;verticalAlign=top;fillColor=#f8f8f8;strokeColor=#cccccc;spacingLeft=8;spacingTop=6;fontSize=11;" value="&lt;font style=&quot;font-size: 14px;&quot;&gt;&lt;b&gt;重點提示與解決方案：&lt;/b&gt;&lt;br&gt;1. 【擴大機 RCA 輸入】：Behringer Flow 8 的主要輸出為 XLR (Main Out)。建議使用一條「雙 XLR (母) 轉 雙 RCA (公)」線材直接接入擴大機，控制最直覺。&lt;br&gt;2. 【長距離電腦音訊】：電腦二使用 20 米的 3.5mm 非平衡線傳輸容易有底噪。若現場測試有雜音，建議在電腦端加 DI Box (直接輸出盒) 轉成平衡訊號。&lt;/font&gt;" vertex="1">
          <mxGeometry height="80" width="1040" x="30" y="500" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>"""

def main():
    base_path = r"C:\Users\kevin\Desktop\Taospace\output"
    filename = "設備連接規劃_115年.drawio"
    
    filename = unicodedata.normalize('NFC', filename)
    target_path = os.path.join(base_path, filename)
    
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        
    with open(target_path, 'w', encoding='utf-8-sig') as f:
        f.write(xml_content)
        
    print(f"成功建立檔案：{target_path}")

    # 用一個含中文字的真實路徑執行一次驗證
    try:
        with open(target_path, 'r', encoding='utf-8-sig') as f:
            test_content = f.read()
            if "Flow 8 設備連接規劃圖" in test_content:
                print("中文路徑驗證成功！")
            else:
                print("驗證失敗：內容不符。")
    except Exception as e:
        print(f"驗證失敗：{e}")

if __name__ == "__main__":
    main()
