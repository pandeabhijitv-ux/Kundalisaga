# Test v1.0.8 AAB Locally (Before Upload to Play Store)

## Requirements
- Android device with USB debugging enabled
- ADB (Android Debug Bridge) installed
- bundletool (Google's AAB testing tool)

## Step 1: Install bundletool

```powershell
# Download bundletool (if not already installed)
# Visit: https://github.com/google/bundletool/releases
# Download: bundletool-all-*.jar

# Or use this command to download latest:
Invoke-WebRequest -Uri "https://github.com/google/bundletool/releases/latest/download/bundletool-all-1.15.6.jar" -OutFile "C:\executables\bundletool.jar"
```

## Step 2: Convert AAB to APKs

```powershell
# Navigate to AAB location
cd C:\AstroKnowledge\mobile\android\app\build\outputs\bundle\release

# Generate APKs from AAB (connected device)
java -jar C:\executables\bundletool.jar build-apks `
  --bundle=app-release.aab `
  --output=app-release.apks `
  --mode=universal `
  --ks=C:\AstroKnowledge\mobile\android\app\upload-keystore.jks `
  --ks-pass=pass:kundalii123 `
  --ks-key-alias=upload `
  --key-pass=pass:kundalii123
```

## Step 3: Install on Device

```powershell
# Enable USB debugging on your Android device
# Connect device via USB

# Check device is connected
adb devices

# Install the APKs
java -jar C:\executables\bundletool.jar install-apks --apks=app-release.apks
```

## Step 4: Test the App

1. **Launch the app** on your device
2. **Check if it opens** without crashing
3. **Test key features**:
   - Login/Register
   - View birth chart
   - Ask a question
   - Navigate between screens

## What to Look For

✅ **Success Indicators**:
- App opens without crashing
- No "Unable to load script" error
- All screens navigate properly
- No ClassNotFoundException in logcat

❌ **Failure Indicators**:
- App crashes immediately on launch
- Red error screen with "Unable to load script"
- Logcat shows ClassNotFoundException

## Capture Logs While Testing

```powershell
# Open a separate PowerShell window and run:
adb logcat | Select-String -Pattern "kundalii|ReactNative|AndroidRuntime"
```

This will show real-time logs while you test.

## Alternative: Simpler APK Test

If bundletool is too complex, use the APK instead:

```powershell
# Build APK (simpler than AAB)
cd C:\AstroKnowledge\mobile\android
$env:JAVA_HOME = "C:\executables\jdk-21.0.9"
.\gradlew.bat assembleRelease

# Install APK
adb install app\build\outputs\apk\release\app-release.apk

# If already installed, use -r flag to replace
adb install -r app\build\outputs\apk\release\app-release.apk
```

## After Testing

**If it works**: Upload v1.0.8 AAB to Play Store (see UPLOAD_INSTRUCTIONS.md)

**If it still crashes**: 
1. Run `C:\AstroKnowledge\mobile\capture_crash.ps1`
2. Share the crash log
3. We'll investigate further
