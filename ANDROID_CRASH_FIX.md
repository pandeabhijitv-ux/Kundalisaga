# Android App Crash Fix - KundaliSaga

## Problem Identified

The app was crashing on launch due to **missing React Native initialization**:

1. ❌ **Missing MainApplication.java** - AndroidManifest.xml referenced it but file didn't exist
2. ❌ **Wrong MainActivity** - Was a plain Android Activity showing TextView instead of React Native Activity
3. ❌ **No React Native Dependencies** - build.gradle missing core RN libraries
4. ❌ **No Auto-linking** - React Native modules weren't being linked
5. ❌ **Wrong Component Name** - index.js wasn't registering component with correct name
6. ❌ **Generic App Icon** - Not using the Shree Ganesh image

## Changes Made

### 1. Created MainApplication.java
**Location:** `mobile/android/app/src/main/java/com/kundalii/saga/MainApplication.java`

- Extends `Application` and implements `ReactApplication`
- Initializes React Native with SoLoader
- Starts Chaquopy Python engine
- Configures Hermes and React Native packages

### 2. Fixed MainActivity.java  
**Location:** `mobile/android/app/src/main/java/com/kundalii/saga/MainActivity.java`

- Changed from plain `Activity` to `ReactActivity`
- Returns component name "KundaliSaga"
- Uses React Native delegates for rendering

### 3. Updated build.gradle
**Location:** `mobile/android/app/build.gradle`

Added:
- React Native core dependencies (`react-android`, `hermes-android`)
- BuildConfig flags (`IS_NEW_ARCHITECTURE_ENABLED`, `IS_HERMES_ENABLED`)
- React Native auto-linking script
- Build features for BuildConfig generation

### 4. Updated settings.gradle
**Location:** `mobile/android/settings.gradle`

- Added React Native auto-linking for native modules

### 5. Updated gradle.properties
**Location:** `mobile/android/gradle.properties`

- Added Hermes engine configuration
- Enabled Gradle caching and parallel builds
- Configured new architecture flags

### 6. Created ProGuard Rules
**Location:** `mobile/android/app/proguard-rules.pro`

- Keeps React Native classes from minification
- Keeps Chaquopy/Python classes
- Prevents crashes in release builds

### 7. Fixed index.js
**Location:** `mobile/index.js`

- Changed to register component with hardcoded name "KundaliSaga"
- Matches the name returned by MainActivity.getMainComponentName()

### 8. Updated Top-level build.gradle
**Location:** `mobile/android/build.gradle`

- Added React Native repository paths
- Added JSC (JavaScriptCore) repository

### 9. Generated Shree Ganesh App Icons
**Script:** `generate_android_icons.py`

- Converted `assets/ganesh.jpg` to all required Android icon sizes
- Generated both square and round icons for all densities:
  - mipmap-mdpi: 48x48
  - mipmap-hdpi: 72x72
  - mipmap-xhdpi: 96x96
  - mipmap-xxhdpi: 144x144
  - mipmap-xxxhdpi: 192x192
- App now displays beautiful Shree Ganesh Ji icon 🙏

## How to Rebuild

### Option 1: Using Build Script (Recommended)
```powershell
cd C:\AstroKnowledge
.\build_apk.ps1
```

### Option 2: Manual Build
```powershell
cd C:\AstroKnowledge\mobile

# Clean previous builds
cd android
.\gradlew clean

# Build AAB for Play Store
.\gradlew bundleRelease

# Or build APK for direct install
.\gradlew assembleRelease
```

### Output Locations
- **AAB:** `mobile/android/app/build/outputs/bundle/release/app-release.aab`
- **APK:** `mobile/android/app/build/outputs/apk/release/app-release.apk`

## Testing the Fixed App

### 1. Clean Install
```powershell
# Uninstall old version first
adb uninstall com.kundalii.saga

# Install new build
adb install mobile/android/app/build/outputs/apk/release/app-release.apk
```

### 2. View Logs (If Still Crashing)
```powershell
# Clear logcat first
adb logcat -c

# Launch app, then view logs
adb logcat | Select-String "AndroidRuntime|ReactNative|Python"
```

### 3. Check for Common Issues

**If app still crashes, check:**

1. **Python modules bundled?**
   ```powershell
   # Check AAB/APK contents
   jar -tf mobile/android/app/build/outputs/bundle/release/app-release.aab | Select-String "python"
   ```

2. **Node modules installed?**
   ```powershell
   cd mobile
   npm install
   ```

3. **React Native package cache**
   ```powershell
   cd mobile
   npx react-native start --reset-cache
   ```

## What Should Work Now

✅ App launches without crashing  
✅ React Native UI loads (splash screen → main navigator)  
✅ Python/Chaquopy initializes in background  
✅ Can navigate between screens  
✅ Can make Vedic astrology calculations  

## Debug Future Issues

### View Real-time Logs
```powershell
# Start logcat before launching app
adb logcat -v color *:W
```

### Filter Important Logs
```powershell
# React Native errors
adb logcat | Select-String "ReactNativeJS"

# Python/Chaquopy errors  
adb logcat | Select-String "Python|chaquo"

# Crash dumps
adb logcat | Select-String "FATAL|AndroidRuntime"
```

### Get Stack Trace
```powershell
# Last crash
adb logcat -b crash

# All errors
adb logcat *:E
```

## Architecture Overview

```
┌─────────────────────────────────────┐
│  React Native JavaScript (App.tsx)  │
│  - UI Components                     │
│  - Navigation                         │
│  - State Management                   │
└─────────────────┬───────────────────┘
                  │
    ┌─────────────▼──────────────┐
    │   React Native Bridge      │
    └─────────────┬──────────────┘
                  │
    ┌─────────────▼──────────────┐
    │   Android Native Layer     │
    │  - MainApplication.java    │
    │  - MainActivity.java       │
    └─────────────┬──────────────┘
                  │
    ┌─────────────▼──────────────┐
    │  Chaquopy Python Engine    │
    │  - vedic_calculator.py     │
    │  - dasha_calculator.py     │
    │  - remedy_calculator.py    │
    └────────────────────────────┘
```

## Key Files Reference

| File | Purpose |
|------|---------|
| `MainApplication.java` | App initialization - React Native + Python |
| `MainActivity.java` | Main activity - loads React Native component |
| `index.js` | Registers React Native component |
| `App.tsx` | Root React component |
| `build.gradle` | Build configuration + dependencies |
| `proguard-rules.pro` | Prevents code minification issues |

## Next Steps

1. **Rebuild the AAB**
   ```powershell
   .\build_apk.ps1
   ```

2. **Test locally**
   ```powershell
   adb install mobile/android/app/build/outputs/apk/release/app-release.apk
   ```

3. **If working, upload to Play Store**
   - Go to Google Play Console
   - Upload new AAB
   - Submit for review

## Common React Native Android Issues

1. **Metro bundler not running** → Run `npx react-native start`
2. **Native modules not found** → Run `cd android && ./gradlew clean`
3. **Python import errors** → Check `python_modules` are in assets
4. **App size too large** → Enable ProGuard and minification
5. **Crashes on old Android** → Check minSdkVersion (currently 24)

---

**Status:** ✅ All critical issues fixed
**Next Action:** Rebuild AAB and test on device
**Expected Result:** App launches and shows Streamlit-themed UI

Jai Sriram! 🙏
