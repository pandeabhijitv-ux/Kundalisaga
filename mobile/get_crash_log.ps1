# Get Crash Log from Android Device
# Requires: ADB (Android Debug Bridge)

param(
    [string]$AdbPath = ""
)

Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   KundaliSaga - Crash Log Capture" -ForegroundColor White
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Find ADB
if ($AdbPath -eq "") {
    $possiblePaths = @(
        "C:\android-sdk\platform-tools\adb.exe",
        "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe",
        "$env:USERPROFILE\AppData\Local\Android\Sdk\platform-tools\adb.exe",
        "C:\Program Files (x86)\Android\android-sdk\platform-tools\adb.exe"
    )
    
    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            $AdbPath = $path
            break
        }
    }
}

if ($AdbPath -eq "" -or !(Test-Path $AdbPath)) {
    Write-Host "❌ ADB not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Android SDK Platform Tools:" -ForegroundColor Yellow
    Write-Host "1. Download from: https://developer.android.com/tools/releases/platform-tools" -ForegroundColor Cyan
    Write-Host "2. Extract to: C:\android-sdk\platform-tools" -ForegroundColor Cyan
    Write-Host "3. Run this script again" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Or provide path manually:" -ForegroundColor Yellow
    Write-Host "  .\get_crash_log.ps1 -AdbPath 'C:\path\to\adb.exe'" -ForegroundColor Gray
    exit 1
}

Write-Host "✓ ADB found: $AdbPath" -ForegroundColor Green
Write-Host ""

# Check devices
Write-Host "📱 Checking connected devices..." -ForegroundColor Cyan
$devices = & $AdbPath devices | Select-Object -Skip 1 | Where-Object { $_ -match "device$" }

if ($devices.Count -eq 0) {
    Write-Host "❌ No devices connected!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please:" -ForegroundColor Yellow
    Write-Host "1. Enable USB Debugging on your phone:" -ForegroundColor Cyan
    Write-Host "   Settings → About Phone → Tap 'Build Number' 7 times" -ForegroundColor Gray
    Write-Host "   Settings → Developer Options → Enable 'USB Debugging'" -ForegroundColor Gray
    Write-Host "2. Connect phone via USB cable" -ForegroundColor Cyan
    Write-Host "3. Accept 'Allow USB Debugging' prompt on phone" -ForegroundColor Cyan
    Write-Host "4. Run this script again" -ForegroundColor Cyan
    exit 1
}

Write-Host "✓ Device connected: $($devices[0])" -ForegroundColor Green
Write-Host ""

# Clear old logs
Write-Host "🧹 Clearing old logs..." -ForegroundColor Cyan
& $AdbPath logcat -c
Start-Sleep -Seconds 1

# Prepare log file
$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$logFile = "$PSScriptRoot\crash_log_$timestamp.txt"

Write-Host "✓ Ready to capture" -ForegroundColor Green
Write-Host ""
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host "   INSTRUCTIONS" -ForegroundColor White
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Now launch the KundaliSaga app on your phone" -ForegroundColor Cyan
Write-Host "2. Wait for it to crash" -ForegroundColor Cyan
Write-Host "3. Press Ctrl+C here to stop logging" -ForegroundColor Cyan
Write-Host ""
Write-Host "Capturing logs... (Press Ctrl+C when done)" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host ""

try {
    # Capture full logcat with filtering
    & $AdbPath logcat -v time "*:E" | Tee-Object -FilePath $logFile | ForEach-Object {
        if ($_ -match "kundalii|saga|crash|fatal|exception|AndroidRuntime") {
            Write-Host $_ -ForegroundColor Red
        } elseif ($_ -match "error|ERROR") {
            Write-Host $_ -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "`n`n✓ Logging stopped" -ForegroundColor Green
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "   LOG SAVED" -ForegroundColor White
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "File: $logFile" -ForegroundColor Cyan
Write-Host ""

# Try to extract crash info
if (Test-Path $logFile) {
    $crashLines = Get-Content $logFile | Select-String -Pattern "FATAL EXCEPTION|AndroidRuntime|com.kundalii.saga" -Context 10
    
    if ($crashLines.Count -gt 0) {
        Write-Host "🔍 CRASH DETECTED:" -ForegroundColor Red
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Red
        $crashLines | Select-Object -First 30 | ForEach-Object { Write-Host $_.Line -ForegroundColor Yellow }
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Red
    } else {
        Write-Host "⚠️  No obvious crash found in logs" -ForegroundColor Yellow
        Write-Host "   Check the full log file for details" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Review $logFile for crash details" -ForegroundColor Gray
Write-Host "2. Look for 'FATAL EXCEPTION' or error messages" -ForegroundColor Gray
Write-Host "3. Share the crash details for further debugging" -ForegroundColor Gray
Write-Host ""
Write-Host "Jai Sriram! 🙏" -ForegroundColor Magenta
