# 🔍 How to Get ACTUAL Crash Logs

**We've been working blind - let's see the REAL error!**

## Option 1: Play Console (Easiest - Automatic)

1. Go to: https://play.google.com/console
2. Select **KundaliSaga** app
3. Go to **Quality** → **Crashes & ANRs** (left menu)
4. Look for crash reports from the last versions uploaded
5. **Copy the entire stacktrace** and share with me

## Option 2: Your Phone via ADB (Best for immediate testing)

### Step 1: Enable USB Debugging on Your Phone
1. Go to **Settings** → **About Phone**
2. Tap **Build Number** 7 times (enable Developer Options)
3. Go back to **Settings** → **Developer Options**
4. Enable **USB Debugging**

### Step 2: Connect Phone to Laptop
1. Connect your phone via USB cable
2. On phone, tap **Allow** when asked to authorize USB debugging

### Step 3: Get Crash Log
Open PowerShell on your laptop and run:

```powershell
# Check if phone is connected
adb devices

# Clear old logs
adb logcat -c

# Start recording logs
adb logcat > crash.txt

# Now open the KundaliSaga app on your phone (it will crash)
# Press Ctrl+C in PowerShell to stop recording
# Open crash.txt file to see the error
```

**OR use this automated script:**

```powershell
# Save this as capture_crash.ps1
$logFile = "kundalii_crash_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"
Write-Host "📱 Waiting for phone connection..." -ForegroundColor Cyan
adb wait-for-device
Write-Host "✅ Phone connected!" -ForegroundColor Green
Write-Host "🧹 Clearing old logs..." -ForegroundColor Yellow
adb logcat -c
Write-Host "`n🎬 Recording crash logs..." -ForegroundColor Cyan
Write-Host "👉 Now OPEN THE APP on your phone" -ForegroundColor Yellow
Write-Host "   Press Ctrl+C when it crashes`n" -ForegroundColor Yellow
adb logcat *:E | Tee-Object -FilePath $logFile
Write-Host "`n✅ Crash log saved to: $logFile" -ForegroundColor Green
```

### Step 4: Filter for Our App's Crash
```powershell
# Search for crash in the log file
Select-String -Path crash.txt -Pattern "kundalii|saga|FATAL|AndroidRuntime" -Context 5,20
```

## Option 3: Build Debug APK (For Testing on Emulator/Device)

Run this command:
```powershell
cd C:\AstroKnowledge\mobile\android
.\gradlew assembleDebug

# The debug APK will be at:
# android/app/build/outputs/apk/debug/app-debug.apk

# Install and see crash immediately:
adb install app/build/outputs/apk/debug/app-debug.apk
adb logcat -c
adb logcat
# Open app, watch crash in real-time
```

## What We're Looking For

The crash log will show something like:

```
FATAL EXCEPTION: main
Process: com.kundalii.saga, PID: 12345
java.lang.RuntimeException: Unable to start activity ...
    at android.app.ActivityThread.performLaunchActivity(...)
    at android.app.ActivityThread.handleLaunchActivity(...)
Caused by: com.facebook.react.common.JavascriptException:
    TypeError: Cannot read property 'XXX' of undefined
    at HomeScreen.tsx:27:10
```

**This will tell us the EXACT LINE causing the crash!**

## 🚨 Most Likely Culprits (Based on Code)

1. **PythonBridge.getCurrentDasha()** in HomeScreen.tsx line ~27
2. **AsyncStorage** initialization in AuthContext
3. **Navigation** trying to render a screen before auth loads
4. **Vector Icons** font loading failure

Once we see the actual error, we can fix it in 2 minutes instead of guessing!
