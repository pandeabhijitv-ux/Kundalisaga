# Test APK v1.0.8 and Capture Crash Logs
# This script will install the app and monitor for crashes in real-time

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  APK v1.0.8 Installation & Test" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

$apkPath = "C:\AstroKnowledge\mobile\android\app\build\outputs\apk\release\app-release.apk"
$packageName = "com.kundalii.saga"
$logFile = "C:\AstroKnowledge\mobile\crash_log_v1.0.8.txt"

# Step 1: Check if APK exists
Write-Host "[1/6] Checking APK..." -ForegroundColor Yellow
if (!(Test-Path $apkPath)) {
    Write-Host "ERROR: APK not found at $apkPath" -ForegroundColor Red
    exit 1
}
$size = (Get-Item $apkPath).Length / 1MB
Write-Host ">> APK found: $([math]::Round($size, 2)) MB`n" -ForegroundColor Green

# Step 2: Check device connection
Write-Host "[2/6] Checking device connection..." -ForegroundColor Yellow
$devices = adb devices 2>&1
if ($devices -match "device$") {
    Write-Host ">> Device connected`n" -ForegroundColor Green
} else {
    Write-Host "ERROR: No device connected!" -ForegroundColor Red
    Write-Host "`nPlease:" -ForegroundColor Yellow
    Write-Host "1. Enable USB debugging on your Android device" -ForegroundColor White
    Write-Host "2. Connect device via USB cable" -ForegroundColor White
    Write-Host "3. Accept USB debugging prompt on device" -ForegroundColor White
    Write-Host "4. Run this script again`n" -ForegroundColor White
    exit 1
}

# Step 3: Uninstall old version (if exists)
Write-Host "[3/6] Uninstalling old version..." -ForegroundColor Yellow
adb uninstall $packageName 2>&1 | Out-Null
Write-Host ">> Old version removed`n" -ForegroundColor Green

# Step 4: Install new APK
Write-Host "[4/6] Installing v1.0.8 APK..." -ForegroundColor Yellow
$installResult = adb install $apkPath 2>&1
if ($installResult -match "Success") {
    Write-Host ">> APK installed successfully`n" -ForegroundColor Green
} else {
    Write-Host "ERROR: Installation failed!" -ForegroundColor Red
    Write-Host $installResult
    exit 1
}

# Step 5: Clear logcat and start monitoring
Write-Host "[5/6] Starting crash monitor..." -ForegroundColor Yellow
Write-Host "Clearing old logs..." -ForegroundColor Gray
adb logcat -c 2>&1 | Out-Null

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  READY TO TEST!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nNow I will:" -ForegroundColor Yellow
Write-Host "1. Launch the app on your device" -ForegroundColor White
Write-Host "2. Monitor for crashes in real-time" -ForegroundColor White
Write-Host "3. Save crash log to: $logFile" -ForegroundColor White
Write-Host "`nPress CTRL+C to stop monitoring`n" -ForegroundColor Gray

# Step 6: Launch app and monitor
Write-Host "[6/6] Launching app and monitoring..." -ForegroundColor Yellow
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  LIVE CRASH MONITOR" -ForegroundColor Green  
Write-Host "========================================`n" -ForegroundColor Cyan

# Launch the app
adb shell am start -n "$packageName/.MainActivity" 2>&1 | Out-Null
Write-Host ">> App launched on device!" -ForegroundColor Green
Write-Host ">> Watching for crashes...`n" -ForegroundColor Yellow

# Monitor logcat for crashes and errors
Start-Transcript -Path $logFile -Append
Write-Host "=== Crash Log Started at $(Get-Date) ===`n"

# Start logcat with filters for errors, crashes, and our app
$logcatProcess = Start-Process -FilePath "adb" -ArgumentList "logcat", "-v", "time", "*:E", "AndroidRuntime:E", "ReactNativeJS:*", "kundalii:*" -NoNewWindow -PassThru

Write-Host "`n>> Watch your device screen now!" -ForegroundColor Cyan
Write-Host "If the app crashes, the error will appear below..." -ForegroundColor Yellow
Write-Host "`nMonitoring for 60 seconds (or press CTRL+C to stop)...`n" -ForegroundColor Gray

# Wait 60 seconds while monitoring
Start-Sleep -Seconds 60

# Stop monitoring
Write-Host "`n`n========================================" -ForegroundColor Cyan
Write-Host "  MONITORING COMPLETE" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Stop-Process -Id $logcatProcess.Id -Force 2>&1 | Out-Null
Stop-Transcript

Write-Host ">> Crash log saved to: $logFile`n" -ForegroundColor Green
Write-Host "What happened on your device?" -ForegroundColor Yellow
Write-Host "1. Did the app open successfully? (Y/N)" -ForegroundColor White
Write-Host "2. Did you see any screens? (Which ones?)" -ForegroundColor White  
Write-Host "3. Did it crash immediately or after some action?`n" -ForegroundColor White

# Show summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  NEXT STEPS" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan
Write-Host "If the app WORKED:" -ForegroundColor Green
Write-Host "  >> Great! Upload the AAB to Play Store" -ForegroundColor White
Write-Host "  >> AAB: mobile\android\app\build\outputs\bundle\release\app-release.aab`n" -ForegroundColor Gray

Write-Host "If the app CRASHED:" -ForegroundColor Red
Write-Host "  >> Share the crash log: $logFile" -ForegroundColor White
Write-Host "  >> I'll analyze it and fix the issue`n" -ForegroundColor White
