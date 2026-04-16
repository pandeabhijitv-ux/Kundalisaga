# 🔍 App Crash Debugging - Quick Start

Your app is crashing. Here's how to find out why:

## Option 1: Quick Test with Debug APK (Recommended)

Build a debug version that's easier to test:

```powershell
cd C:\AstroKnowledge\mobile

# Build debug APK with all logs
.\build_debug_apk.ps1

# Build and install on connected phone
.\build_debug_apk.ps1 -Install

# Build, install, and launch
.\build_debug_apk.ps1 -Install -Launch
```

The debug APK will:
- ✅ Include all debugging symbols
- ✅ Show detailed error messages
- ✅ Easier to install and test

## Option 2: Capture Crash Logs from Device

### Prerequisites:
1. **Install Android SDK Platform Tools**
   - Download: https://developer.android.com/tools/releases/platform-tools
   - Extract to: `C:\android-sdk\platform-tools`

2. **Enable USB Debugging on Phone**
   - Go to: Settings → About Phone
   - Tap "Build Number" 7 times (enables Developer Options)
   - Go to: Settings → Developer Options
   - Enable "USB Debugging"
   - Connect phone via USB
   - Accept "Allow USB Debugging" prompt

### Capture Logs:

```powershell
cd C:\AstroKnowledge\mobile

# Run the log capture script
.\get_crash_log.ps1

# Follow instructions:
# 1. Launch app on phone
# 2. Let it crash
# 3. Press Ctrl+C to stop logging
```

This creates `crash_log_YYYY-MM-DD_HHMMSS.txt` with the crash details.

## Option 3: Check Google Play Console

If you uploaded to Play Store (even as internal testing):

1. Go to: https://play.google.com/console
2. Navigate to: Your App → Quality → Android vitals → Crashes & ANRs
3. View automatic crash reports from users
4. See stack traces showing exact crash location

## Common Crash Causes

### 1. Missing React Native Bundle

**Symptom**: App crashes immediately  
**Fix**:
```powershell
cd C:\AstroKnowledge\mobile
npx react-native bundle --platform android --dev false --entry-file index.js --bundle-output android/app/src/main/assets/index.android.bundle
```

### 2. Missing Dependencies

**Symptom**: ClassNotFoundException in logs  
**Fix**:
```powershell
cd C:\AstroKnowledge\mobile
npm install
cd android
.\gradlew.bat clean
```

### 3. Python Initialization Error

**Symptom**: Crashes when starting  
**Check**: MainApplication.java has proper Python.start() call  
**Location**: `mobile/android/app/src/main/java/com/kundalii/saga/MainApplication.java`

### 4. Permissions Missing

**Symptom**: Crashes accessing features  
**Fix**: Check AndroidManifest.xml has required permissions

## What to Look For in Crash Logs

Search for these patterns:

```
FATAL EXCEPTION
└─ Shows the main crash

java.lang.RuntimeException
└─ Runtime error details

Caused by:
└─ Root cause of crash

Process: com.kundalii.saga
└─ Your app's crash
```

## Quick Win: Test on Different Device

Sometimes crashes are device-specific:
- Try on a different Android device
- Test on Android emulator
- Check Android version compatibility (need 7.0+)

## Files Created

1. **build_debug_apk.ps1** - Build testable APK
2. **get_crash_log.ps1** - Capture crash logs
3. **DEBUG_CRASH.md** - Detailed debugging guide

## Next Steps

1. **Run debug build**: `.\build_debug_apk.ps1 -Install -Launch`
2. **Capture logs**: `.\get_crash_log.ps1`
3. **Share crash details**: Send the error message/stack trace

## Need Help?

Share the crash log showing:
- FATAL EXCEPTION message
- Stack trace (10-20 lines after error)
- Device info (Android version, phone model)

## Jai Sriram! 🙏

Let's fix this crash!
