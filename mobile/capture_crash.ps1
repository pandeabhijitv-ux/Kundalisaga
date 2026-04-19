# 📱 Automated Crash Log Capture
# Usage: .\capture_crash.ps1

param(
    [switch]$ClearOnly,
    [switch]$DeviceInfo
)

$ErrorActionPreference = "Continue"
$logFile = "kundalii_crash_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"

Write-Host "`n🔍 KundaliSaga Crash Log Capture Tool`n" -ForegroundColor Cyan

# Check if ADB is available
try {
    $null = adb version 2>&1
} catch {
    Write-Host "❌ ADB not found!" -ForegroundColor Red
    Write-Host "   Please install Android SDK Platform Tools" -ForegroundColor Yellow
    Write-Host "   Download: https://developer.android.com/tools/releases/platform-tools" -ForegroundColor Yellow
    exit 1
}

# Device Info
if ($DeviceInfo) {
    Write-Host "📱 Connected Devices:" -ForegroundColor Cyan
    adb devices -l
    Write-Host "`n📊 Device Properties:" -ForegroundColor Cyan
    adb shell getprop ro.product.model
    adb shell getprop ro.build.version.release
    exit 0
}

# Wait for device
Write-Host "📱 Waiting for phone connection..." -ForegroundColor Yellow
Write-Host "   (Make sure USB Debugging is enabled)" -ForegroundColor Gray
adb wait-for-device

# Get device name
$deviceModel = adb shell getprop ro.product.model 2>$null
$androidVer = adb shell getprop ro.build.version.release 2>$null
Write-Host "✅ Connected: $deviceModel (Android $androidVer)" -ForegroundColor Green

# Clear old logs
Write-Host "🧹 Clearing old logs..." -ForegroundColor Yellow
adb logcat -c
Start-Sleep -Seconds 1

if ($ClearOnly) {
    Write-Host "✅ Logs cleared! Exiting..." -ForegroundColor Green
    exit 0
}

# Check if app is installed
$packageCheck = adb shell pm list packages | Select-String "kundalii.saga"
if ($packageCheck) {
    $appVersion = adb shell dumpsys package com.kundalii.saga | Select-String "versionName"
    Write-Host "📦 App installed: $appVersion" -ForegroundColor Green
} else {
    Write-Host "⚠️  App not found (com.kundalii.saga)" -ForegroundColor Yellow
    Write-Host "   Please install the AAB/APK first" -ForegroundColor Yellow
}

# Start recording
Write-Host "`n🎬 Recording crash logs..." -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
Write-Host "👉 Now OPEN THE APP on your phone" -ForegroundColor Yellow -BackgroundColor DarkMagenta
Write-Host "   Press Ctrl+C after it crashes" -ForegroundColor Yellow
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor DarkGray

# Record all logs and filter for errors
try {
    adb logcat -v time `*:W | Tee-Object -FilePath $logFile
} catch {
    Write-Host "`n✅ Recording stopped" -ForegroundColor Green
}

Write-Host "`n✅ Crash log saved to: $logFile" -ForegroundColor Green

# Analyze the crash
Write-Host "`n🔍 Analyzing crash..." -ForegroundColor Cyan

$crashPatterns = @(
    "FATAL EXCEPTION",
    "AndroidRuntime",
    "com.kundalii.saga",
    "ReactNative",
    "JavascriptException",
    "NativeModule"
)

$foundCrash = $false
foreach ($pattern in $crashPatterns) {
    $matches = Select-String -Path $logFile -Pattern $pattern -Context 0,5
    if ($matches) {
        $foundCrash = $true
        Write-Host "`n━━━ Found: $pattern ━━━" -ForegroundColor Red
        $matches | ForEach-Object { $_.Line } | Select-Object -First 10
    }
}

if (-not $foundCrash) {
    Write-Host "⚠️  No obvious crash found in logs" -ForegroundColor Yellow
    Write-Host "   The app might not have crashed yet, or crash wasn't logged" -ForegroundColor Gray
    Write-Host "`n   Full log available in: $logFile" -ForegroundColor Cyan
} else {
    Write-Host "`n✅ Crash detected! See details above ⬆️" -ForegroundColor Green
    Write-Host "   Send this file to developer: $logFile" -ForegroundColor Cyan
}

# Create summary
$summary = @"

CRASH LOG SUMMARY
=================
Date: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
Device: $deviceModel
Android: $androidVer
App: com.kundalii.saga $appVersion
Log File: $logFile

"@

Add-Content -Path $logFile -Value $summary
Write-Host "`n📄 Full log: $logFile" -ForegroundColor Cyan
