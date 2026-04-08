# Build Status Check Script
# Run this anytime to check if your APK build completed

$ErrorActionPreference = "SilentlyContinue"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "KundaliSaga APK Build Status" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check if build is currently running
$gradleProcess = Get-Process | Where-Object { $_.ProcessName -like "*java*" -and $_.CommandLine -like "*gradle*" }

if ($gradleProcess) {
    Write-Host "STATUS: Build is currently RUNNING" -ForegroundColor Yellow
    Write-Host "Process ID: $($gradleProcess.Id)" -ForegroundColor Gray
    Write-Host "Please wait for completion (5-10 minutes total)`n" -ForegroundColor Yellow
} else {
    Write-Host "STATUS: No active build process detected" -ForegroundColor Gray
}

# Check for completed APK
$apkPath = "C:\AstroKnowledge\mobile\android\app\build\outputs\apk\release\app-release.apk"
$aabPath = "C:\AstroKnowledge\mobile\android\app\build\outputs\bundle\release\app-release.aab"

Write-Host "Checking for build outputs...`n" -ForegroundColor Cyan

if (Test-Path $apkPath) {
    $apkInfo = Get-Item $apkPath
    $apkSize = [math]::Round($apkInfo.Length / 1MB, 2)
    Write-Host "✓ APK FOUND!" -ForegroundColor Green
    Write-Host "  Location: $apkPath" -ForegroundColor White
    Write-Host "  Size: $apkSize MB" -ForegroundColor White
    Write-Host "  Created: $($apkInfo.LastWriteTime)" -ForegroundColor White
    Write-Host ""
    Write-Host "Your APK is ready to install on Android devices!" -ForegroundColor Green
} else {
    Write-Host "✗ APK not found yet" -ForegroundColor Red
    Write-Host "  Expected location: $apkPath" -ForegroundColor Gray
}

Write-Host ""

if (Test-Path $aabPath) {
    $aabInfo = Get-Item $aabPath
    $aabSize = [math]::Round($aabInfo.Length / 1MB, 2)
    Write-Host "✓ AAB FOUND (Play Store format)!" -ForegroundColor Green
    Write-Host "  Location: $aabPath" -ForegroundColor White
    Write-Host "  Size: $aabSize MB" -ForegroundColor White
    Write-Host "  Created: $($aabInfo.LastWriteTime)" -ForegroundColor White
} else {
    Write-Host "✗ AAB not found (only created after APK build)" -ForegroundColor Gray
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "1. If APK found: Copy to your Android device" -ForegroundColor White
Write-Host "2. Enable 'Unknown Sources' on your device" -ForegroundColor White
Write-Host "3. Install the APK" -ForegroundColor White
Write-Host "4. Launch KundaliSaga app" -ForegroundColor White
Write-Host "`nFor errors: Check logs in mobile\android\app\build\outputs\logs\" -ForegroundColor Yellow
Write-Host ""
