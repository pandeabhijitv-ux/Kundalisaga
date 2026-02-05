# Quick Start Guide - KundaliSaga Mobile

## 🚀 For Windows (Your Environment)

### Step-by-Step Setup

#### 1️⃣ Install Prerequisites

**Node.js & npm:**
```powershell
# Download and install from: https://nodejs.org/
# Version 18+ required
node --version  # Check installation
```

**Android Studio:**
```powershell
# Download from: https://developer.android.com/studio
# During installation, select:
# - Android SDK
# - Android SDK Platform
# - Android Virtual Device
```

**JDK 17:**
```powershell
# Download from: https://adoptium.net/
# Install and set JAVA_HOME
```

#### 2️⃣ Setup Environment Variables

```powershell
# Run PowerShell as Administrator

# Set ANDROID_HOME
[System.Environment]::SetEnvironmentVariable('ANDROID_HOME', 'C:\Users\YourUsername\AppData\Local\Android\Sdk', 'User')

# Add to PATH
$oldPath = [System.Environment]::GetEnvironmentVariable('Path', 'User')
$newPath = $oldPath + ';%ANDROID_HOME%\platform-tools;%ANDROID_HOME%\tools;%ANDROID_HOME%\tools\bin'
[System.Environment]::SetEnvironmentVariable('Path', $newPath, 'User')

# Restart PowerShell after this
```

#### 3️⃣ Install Dependencies

```powershell
cd C:\AstroKnowledge\mobile
npm install
```

#### 4️⃣ Link Python Backend

```powershell
# Option 1: Symbolic link (requires Admin)
cd C:\AstroKnowledge\mobile\python_modules
cmd /c mklink /D src "..\..\src"

# Option 2: Copy (simpler)
xcopy /E /I C:\AstroKnowledge\src C:\AstroKnowledge\mobile\python_modules\src
```

#### 5️⃣ Test Python Modules

```powershell
cd C:\AstroKnowledge\mobile\python_modules
python vedic_calculator.py
# Should print sample chart data
```

#### 6️⃣ Start Android Emulator

```powershell
# Open Android Studio
# Tools -> AVD Manager -> Create Virtual Device
# Choose Pixel 6
# Choose API 34 (Android 14)
# Start emulator
```

#### 7️⃣ Run the App

```powershell
cd C:\AstroKnowledge\mobile

# Start Metro bundler
npm start

# In another terminal, run:
npm run android
```

## 📱 Expected Result

1. App builds successfully
2. Installs on emulator/device
3. Shows KundaliSaga splash screen
4. Opens to Login/Register screen
5. Can continue as guest
6. See Home screen with quick access cards

## 🐛 Common Issues & Fixes

### Issue: "SDK location not found"
```powershell
# Create local.properties in android/ folder:
echo "sdk.dir=C:\\Users\\YourUsername\\AppData\\Local\\Android\\Sdk" > android\local.properties
```

### Issue: "Python module not found"
```powershell
# Make sure python_modules/src exists
dir mobile\python_modules\src
# Should show astrology_engine, user_manager, etc.
```

### Issue: "Could not find build tools"
```powershell
# Open Android Studio
# SDK Manager -> SDK Tools
# Install:
# - Android SDK Build-Tools 34
# - Android SDK Platform-Tools
```

### Issue: "Chaquopy build failed"
```powershell
# Clean and rebuild
cd mobile\android
.\gradlew clean
cd ..
npm run android
```

## ✅ Verification Checklist

- [ ] Node.js 18+ installed
- [ ] Android Studio installed
- [ ] ANDROID_HOME set
- [ ] Emulator running
- [ ] npm install completed
- [ ] Python backend linked
- [ ] App runs on emulator
- [ ] Can navigate between screens

## 🎯 Next Steps After Setup

1. **Test Python Integration**:
   - Uncomment Python calls in HomeScreen.tsx
   - Test chart calculation

2. **Implement Horoscope Screen**:
   - Add form for birth details
   - Call calculateChart function
   - Display results

3. **Add More Features**:
   - Complete all screens
   - Add data persistence
   - Implement remedies display

## 📞 Need Help?

Check logs:
```powershell
# React Native logs
npx react-native log-android

# Android logs
adb logcat

# Metro bundler (already shows logs)
```

## 🎉 Success!

If you see the app running with:
- Login/Register screens
- Home screen after login
- Bottom navigation tabs
- Saffron/peach theme

**You're ready to start building features!** 🚀
