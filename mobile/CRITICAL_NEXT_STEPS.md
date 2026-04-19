# ⚠️ CRITICAL: Get ACTUAL Crash Logs

##  What Changed in v1.0.6
- Built with Java 21 (configured properly)
- Kotlin JVM target set to 17
- All previous fixes included (JavaScript bundle, gesture handler, vector fonts, PythonBridge)

## 🔴 STOP GUESSING - Get Real Crash Data!

We've made 6 versions (v1.0.1-v1.0.6) based on educated guesses, but **all still crash**. 

**WE NEED ACTUAL CRASH LOGS TO FIX THE REAL PROBLEM!**

---

## Option 1: Play Console Crash Reports (Easiest - 2 minutes)

1. Go to https://play.google.com/console
2. Select **KundaliSaga**
3. Click **Quality** → **Crashes & ANRs** (left sidebar)
4. Find crashes from v1.0.1-v1.0.5
5. **Copy the entire stacktrace** and send to me

**This is automatic - Google already has all the crash data!**

---

## Option 2: Your Phone + ADB (Best - 5 minutes)

### Quick Setup:
1. **Enable USB Debugging** on your phone:
   - Settings → About Phone → Tap "Build Number" 7 times
   - Settings → Developer Options → Enable "USB Debugging"

2. **Connect phone to laptop** via USB cable
   - Accept "Allow USB Debugging" popup on phone

3. **Run the automated script:**
   ```powershell
   cd C:\AstroKnowledge\mobile
   .\capture_crash.ps1
   ```

4. **Open the app** when prompted (it will crash)
5. **Press Ctrl+C** in PowerShell
6. **Send the log file** created (kundalii_crash_TIMESTAMP.txt)

**The script does everything automatically!**

---

## Option 3: Manual ADB (If script doesn't work)

```powershell
# Install platform-tools if needed
# Download: https://developer.android.com/tools/releases/platform-tools

# Check connection
adb devices

# Clear old logs
adb logcat -c

# Start recording
adb logcat > crash.txt

# NOW OPEN THE APP (let it crash)
# Then press Ctrl+C and send crash.txt
```

---

## What to Look For in Crash Log

The crash will show something like:

```
FATAL EXCEPTION: main
Process: com.kundalii.saga, PID: 12345
java.lang.RuntimeException: Unable to start activity ...
Caused by: com.facebook.react.common.JavascriptException:
    TypeError: Cannot read property 'XXX' of undefined
    at HomeScreen.tsx:27:10
```

**This tells us the EXACT line and error!**

---

## 🎯 Most Likely Crash Causes (My Guesses)

Based on code review, the crash is probably:

1. **AsyncStorage not initialized** (line ~38 in AuthContext.tsx)
   - App tries to read AsyncStorage before it's ready
   - Fix: Add try-catch or loading state

2. **PythonBridge module missing** (line ~27 in HomeScreen.tsx)
   - getCurrentDasha() returns null or throws error
   - Fix: Already added safety checks, but might need more

3. **Navigation before auth loads** (App.tsx)
   - Navigator tries to render screens before auth state loads
   - Fix: Should be handled by isLoading check, but might have timing issue

4. **Vector Icons font loading** (various screens)
   - Icon fonts might not load on some devices
   - Fix: Fallback icons or different icon library

**BUT I'M GUESSING! The crash log will tell us for sure!**

---

## 📦 v1.0.6 AAB Ready

File: `mobile/android/app/build/outputs/bundle/release/app-release.aab`

**BUT PLEASE - Get crash logs BEFORE uploading another version!**

Let's fix the ACTUAL problem instead of guessing!

---

## Need Help with ADB?

1. **Download ADB Platform Tools**: https://developer.android.com/tools/releases/platform-tools
2. **Extract** to a folder (e.g., C:\platform-tools)
3. **Add to PATH** or cd into the folder
4. **Run**: `adb devices` to check connection

**Or just use Play Console - it's easier!**
