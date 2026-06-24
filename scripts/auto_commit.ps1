Set-Location "C:\Users\kevin\Desktop\Taospace"
git add -A
git diff --staged --quiet
if ($LASTEXITCODE -ne 0) {
    $timestamp = Get-Date -Format "yyyyMMdd-HHmmss"
    git commit -m "auto: $timestamp"
    git push origin main
}
