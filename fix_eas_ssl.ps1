# Fix EAS SSL Certificate Issue on Windows

Write-Host "`nFixing EAS SSL certificate issue...`n" -ForegroundColor Yellow

# Set environment variable to disable SSL verification (not recommended for production)
$env:NODE_TLS_REJECT_UNAUTHORIZED = "0"

Write-Host "✅ SSL verification temporarily disabled for this session`n" -ForegroundColor Green
Write-Host "Now run: .\build_apk.ps1`n" -ForegroundColor Cyan

# Alternative: Update npm config
Write-Host "Updating npm config for strict SSL...`n" -ForegroundColor Yellow
npm config set strict-ssl false

Write-Host "✅ npm strict-ssl disabled`n" -ForegroundColor Green
Write-Host "Try running: .\build_apk.ps1 again`n" -ForegroundColor Cyan
