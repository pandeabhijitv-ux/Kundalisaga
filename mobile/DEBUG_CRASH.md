# Android App Crash Debugging Guide

## Method 1: Using Google Play Console (Easiest - Recommended)

If you've uploaded to Google Play:

1. **Go to Play Console**: https://play.google.com/console
2. **Navigate to**: Your App → Quality → Android vitals → Crashes & ANRs
3. **View crash reports**: Automatic crash logs from users
4. **Stack trace**: Shows exact line where crash occurred

## Method 2: Using ADB (Local Device)

### Step 1: Install Android SDK Platform Tools

```powershell
# Download from: https://developer.android.com/tools/releases/platform-tools
# Extract to: C:\android-sdk\platform-tools
# Add to PATH or use full path
```

### Step 2: Connect Device

```powershell
# Enable USB Debugging on your Android device:
# Settings → About Phone → Tap "Build Number" 7 times
# Settings → Developer Options → Enable "USB Debugging"
# Connect phone via USB
```

### Step 3: Check Connection

```powershell
C:\android-sdk\platform-tools\adb.exe devices
# Should show: List of devices attached
#              <device-id>    device
```

### Step 4: Clear Logs and Launch App

```powershell
# Clear previous logs
C:\android-sdk\platform-tools\adb.exe logcat -c

# Start capturing logs
C:\android-sdk\platform-tools\adb.exe logcat > crash_log.txt

# NOW: Open the app on your phone
# When it crashes, press Ctrl+C to stop logging
```

### Step 5: Filter for Crashes

```powershell
# Look for errors related to your app
C:\android-sdk\platform-tools\adb.exe logcat -s AndroidRuntime:E KundaliSaga:E
```

## Method 3: Install APK with Logcat (Quick Debug)

### Build APK instead of AAB

```powershell
cd C:\AstroKnowledge\mobile\android
.\gradlew.bat assembleRelease
# Output: app/build/outputs/apk/release/app-release.apk
```

### Install and Monitor

```powershell
# Install APK
C:\android-sdk\platform-tools\adb.exe install -r app/build/outputs/apk/release/app-release.apk

# Monitor in real-time while launching app
C:\android-sdk\platform-tools\adb.exe logcat | Select-String -Pattern "kundalii|crash|error|exception" -Context 5
```

## Method 4: Create Debug Build with Logs

### Temporary Debug Build

Edit `mobile/android/app/build.gradle`:

```gradle
buildTypes {
    release {
        debuggable true  // ← Add this temporarily
        signingConfig signingConfigs.release
        minifyEnabled false  // ← Set to false for debugging
        ...
    }
}
```

Then rebuild and check logs.

## Common Crash Causes & Solutions

### 1. **JavaScript/React Native Crashes**

**Symptom**: App crashes immediately on launch  
**Cause**: JS bundle not loaded or syntax error  
**Solution**: Check if `index.android.bundle` exists

```powershell
# Build JS bundle manually
cd C:\AstroKnowledge\mobile
npx react-native bundle --platform android --dev false --entry-file index.js --bundle-output android/app/src/main/assets/index.android.bundle
```

### 2. **Python/Chaquopy Crashes**

**Symptom**: Crashes when trying to use Python features  
**Cause**: Python modules not initialized  
**Solution**: Check MainApplication.java initialization

### 3. **Missing Permissions**

**Symptom**: Crashes when accessing features  
**Cause**: Runtime permissions not requested  
**Solution**: Add to AndroidManifest.xml:

```xml
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
```

### 4. **Native Library Crashes**

**Symptom**: "UnsatisfiedLinkError" in logs  
**Cause**: Missing .so files for architecture  
**Solution**: Ensure all ABIs built (check build.gradle ndk.abiFilters)

## Quick Crash Log Script

Save as `mobile/get_crash_log.ps1`:

```powershell
param(
    [string]$AdbPath = "C:\android-sdk\platform-tools\adb.exe"
)

if (!(Test-Path $AdbPath)) {
    Write-Host "❌ ADB not found at: $AdbPath" -ForegroundColor Red
    Write-Host "Download from: https://developer.android.com/tools/releases/platform-tools" -ForegroundColor Yellow
    exit 1
}

Write-Host "📱 Checking connected devices..." -ForegroundColor Cyan
& $AdbPath devices

Write-Host "`n🔍 Clearing old logs..." -ForegroundColor Cyan
& $AdbPath logcat -c

Write-Host "`n▶️  Launch the app NOW and wait for crash..." -ForegroundColor Yellow
Write-Host "⏸️  Press Ctrl+C when done`n" -ForegroundColor Gray

$timestamp = Get-Date -Format "yyyy-MM-dd_HHmmss"
$logFile = "crash_log_$timestamp.txt"

& $AdbPath logcat | Tee-Object -FilePath $logFile | Select-String -Pattern "kundalii|saga|crash|fatal|exception|error" -Context 2

Write-Host "`n✅ Log saved to: $logFile" -ForegroundColor Green
```

## Analyzing Crash Logs

Look for these patterns:

```
FATAL EXCEPTION: main
Process: com.kundalii.saga
<--- This shows the crash details
```

```
java.lang.RuntimeException: Unable to start activity
<--- Activity startup issue
```

```
Caused by: java.lang.ClassNotFoundException
<--- Missing class/dependency
```

```
E/AndroidRuntime: FATAL EXCEPTION
<--- Fatal crash
```

## Send Crash Log to Me

Once you have the crash log:

1. Save the log file
2. Find the section with "FATAL EXCEPTION" or "crash"
3. Copy about 50 lines around the error
4. Share the error message

## Jai Sriram! 🙏

Let's fix this crash together!
