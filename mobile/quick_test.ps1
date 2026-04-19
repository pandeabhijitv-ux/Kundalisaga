# Quick Test Script for v1.0.8 APK
# Run this after connecting your Android device with USB debugging enabled

$adb = "C:\Users\abhijit.pande\AppData\Local\Android\Sdk\platform-tools\adb.exe"  
$apk = "C:\AstroKnowledge\mobile\android\app\build\outputs\apk\release\app-release.apk"
$pkg = "com.kundalii.saga"

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Testing v1.0.8 APK" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

# Check device
Write-Host "[1/5] Checking device..." -ForegroundColor Yellow
$devices = & $adb devices 2>&1
if ($devices -match "device$") {
    Write-Host ">> Device connected!`n" -ForegroundColor Green
} else {
    Write-Host "ERROR: No device found!" -ForegroundColor Red
    Write-Host "`nPlease:" -ForegroundColor Yellow
    Write-Host "1. Enable USB debugging (Settings → Developer Options)" -ForegroundColor White
    Write-Host "2. Connect phone via USB" -ForegroundColor White
    Write-Host "3. Accept USB debugging popup on phone`n" -ForegroundColor White
    exit 1
}

# Uninstall old version
Write-Host "[2/5] Removing old version..." -ForegroundColor Yellow
& $adb uninstall $pkg 2>&1 | Out-Null
Write-Host ">> Done`n" -ForegroundColor Green

# Install new APK
Write-Host "[3/5] Installing v1.0.8..." -ForegroundColor Yellow
$result = & $adb install $apk 2>&1
if ($result -match "Success") {
    Write-Host ">> Installed successfully!`n" -ForegroundColor Green
} else {
    Write-Host "ERROR: Installation failed!`n$result" -ForegroundColor Red
    exit 1
}

# Clear logs
Write-Host "[4/5] Clearing old logs..." -ForegroundColor Yellow
& $adb logcat -c 2>&1 | Out-Null
Write-Host ">> Done`n" -ForegroundColor Green

# Launch app
Write-Host "[5/5] Launching app..." -ForegroundColor Yellow
& $adb shell am start -n "$pkg/.MainActivity" 2>&1 | Out-Null
Write-Host ">> App launched!`n" -ForegroundColor Green

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  WATCH YOUR PHONE NOW!" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "What happened on your phone?`n" -ForegroundColor Yellow

Write-Host "A) App opened successfully?" -ForegroundColor White
Write-Host "   >> GREAT! The app works! Upload v1.0.8 AAB to Play Store`n" -ForegroundColor Green

Write-Host "B) App crashed immediately?" -ForegroundColor White
Write-Host "   >> Run this to get crash log:" -ForegroundColor Red
Write-Host "   & `"$adb`" logcat -d > crash_log.txt`n" -ForegroundColor Gray

Write-Host "C) Need to see live crash logs now?" -ForegroundColor White
Write-Host "   >> Monitoring for 30 seconds...`n" -ForegroundColor Yellow

# Monitor for crashes
Write-Host "CRASH MONITOR (Press CTRL+C to stop):" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

& $adb logcat -v time "*:E" "AndroidRuntime:E" "ReactNative:*"
