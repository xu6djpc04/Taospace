$htmlPath = "C:\Users\kevin\Desktop\Taospace\output\細胞活化開啟青春密碼筆記.html"
$docxPath = "C:\Users\kevin\Desktop\Taospace\output\細胞活化開啟青春密碼筆記.docx"

if (Test-Path $docxPath) {
    Remove-Item $docxPath
}

Write-Host "Starting Word Application..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false

Write-Host "Opening HTML file..."
$doc = $word.Documents.Open($htmlPath)

Write-Host "Saving as DOCX..."
# 16 is wdFormatDocumentDefault (docx)
$doc.SaveAs([ref]$docxPath, [ref]16)

$doc.Close()
$word.Quit()

Write-Host "Conversion complete. Saved to: $docxPath"
