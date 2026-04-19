# How to Test v1.0.8 APK - Step by Step

## Your APK is Ready!
**Location**: `C:\AstroKnowledge\mobile\android\app\build\outputs\apk\release\app-release.apk`
**Size**: 122.23 MB
**Version**: 1.0.8 (includes multidex + auto JS bundle fixes)

---

## OPTION A: Quick Test (Manual Install - No USB Required)

### Step 1: Transfer APK to Your Phone
1. **Email Method**:
   - Email the APK file to yourself
   - Open email on your Android phone
   - Download the APK

2. **Google Drive Method**:
   - Upload APK to Google Drive from PC
   - Open Drive app on phone
   - Download the APK

3. **USB Transfer Method**:
   - Connect phone via USB
   - Copy APK to phone's Download folder
   - Safely eject phone

### Step 2: Install APK on Phone
1. Open **File Manager** or **Downloads** on your phone
2. Tap the **app-release.apk** file
3. Android will ask "Install unknown app?"
4. Tap **Settings** → Enable **Allow from this source**
5. Tap **Install**
6. Wait for installation to complete

### Step 3: Test the App
1. Tap **Open** after installation
2. Watch what happens:
   - ✅ **SUCCESS**: If app opens and shows login screen
   - ❌ **CRASH**: If app closes immediately or shows error

### Step 4: If App Crashes
The app will create a crash log. To get it:

1. **Open Play Console on your PC**
   - https://play.google.com/console
   - Go to your app
   - **Upload version 1.0.8 first** (it creates crash tracking)

2. **Or get crash log via logcat** (see Option B below)

---

## OPTION B: USB ADB Test (Get Detailed Crash Logs)

### Prerequisites
✅ ADB is already installed: `C:\Users\abhijit.pande\AppData\Local\Android\Sdk\platform-tools\adb.exe`

### Step 1: Enable USB Debugging

1. On your Android phone:
   - Go to **Settings**
   - Tap **About Phone**
   - Tap **Build Number** 7 times (enables Developer mode)
   - Message appears: "You are now a developer!"

2. Go back to **Settings**
   - Tap **Developer Options** (or **System** → **Developer Options**)
   - Enable **USB Debugging**

### Step 2: Connect Phone to PC
1. Connect phone to PC via USB cable
2. Phone shows popup: "Allow USB debugging?"
3. Check "Always allow from this computer"
4. Tap **OK**

### Step 3: Verify Connection
Run this command in PowerShell:
```powershell
& "C:\Users\abhijit.pande\AppData\Local\Android\Sdk\platform-tools\adb.exe" devices
```

Should show:
```
List of devices attached  
XXXXXXXX    device
```

### Step 4: Install and Test APK
Run this command:
```powershell
cd C:\AstroKnowledge\mobile

# Set ADB path
$adb = "C:\Users\abhijit.pande\AppData\Local\Android\Sdk\platform-tools\adb.exe"
$apk = "android\app\build\outputs\apk\release\app-release.apk"

# Uninstall old version
& $adb uninstall com.kundalii.saga

# Install new APK
& $adb install $apk

# Clear old logs
& $adb logcat -c

# Launch app
& $adb shell am start -n com.kundalii.saga/.MainActivity

# Watch for crashes (CTRL+C to stop)
& $adb logcat "*:E" "AndroidRuntime:E" "ReactNative:*"
```

### Step 5: Interpret Results

**If you see in logcat**:
- `FATAL EXCEPTION` → App crashed, copy the full error
- `Unable to load script` → JavaScript bundle issue
- `ClassNotFoundException` → Multidex/ProGuard issue
- Nothing after 10 seconds → App likely working!

**If app opens successfully**:
- Test login
- Test navigation
- Confirm no crashes
- Ready to upload v1.0.8 AAB to Play Store!

---

## Quick Commands Reference

```powershell
# Check device connection
& "C:\Users\abhijit.pande\AppData\Local\Android\Sdk\platform-tools\adb.exe" devices

# Install APK (replace old version)
$adb = "C:\Users\abhijit.pande\AppData\Local\Android\Sdk\platform-tools\adb.exe"
& $adb install -r "C:\AstroKnowledge\mobile\android\app\build\outputs\apk\release\app-release.apk"

# Launch app
& $adb shell am start -n com.kundalii.saga/.MainActivity

# Watch crashes
& $adb logcat "*:E"

# Save full crash log to file
& $adb logcat -d > C:\AstroKnowledge\mobile\crash_log.txt
```

---

## What To Do Next

### If App WORKS ✅
1. **Upload AAB to Play Store**
   - File: `mobile\android\app\build\outputs\bundle\release\app-release.aab`
   - Version: 1.0.8
   - This includes all fixes!

### If App CRASHES ❌
1. **Get the crash log**:
   ```powershell
   & "C:\Users\abhijit.pande\AppData\Local\Android\Sdk\platform-tools\adb.exe" logcat -d > crash_log.txt
   ```
2. **Share the crash log** with me
3. I'll identify the exact issue and fix it

---

## Why Test Before Upload?

- Old crashes in Play Console are from versions 1.0.0 and 1.0.1
- We need to verify v1.0.8 doesn't crash
- Better to find issues locally than after upload
- Saves time and app reputation
