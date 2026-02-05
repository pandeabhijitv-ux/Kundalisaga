# 🚀 KundaliSaga Mobile - Quick Reference

## ⚡ Essential Commands

### Setup (One-Time)
```powershell
# Run automated setup
.\build_mobile.ps1

# Or manual setup:
cd mobile
npm install
xcopy /E /I ..\src python_modules\src
```

### Development
```powershell
# Start Metro bundler
cd mobile
npm start

# Run on Android (in another terminal)
npm run android

# View logs
npx react-native log-android
```

### Building
```powershell
# Debug APK
cd mobile\android
.\gradlew assembleDebug

# Release APK
.\gradlew assembleRelease
# Output: android\app\build\outputs\apk\release\app-release.apk
```

### Troubleshooting
```powershell
# Clean build
cd mobile\android
.\gradlew clean

# Clear Metro cache
cd ..
npx react-native start --reset-cache

# Reinstall packages
rm -r node_modules
npm install
```

## 📱 Testing Checklist

- [ ] Run `npm run android`
- [ ] App launches successfully
- [ ] Login screen displays
- [ ] Can create account
- [ ] Guest mode works
- [ ] Navigation between tabs
- [ ] Theme displays correctly
- [ ] No crash on navigation

## 🔗 Quick Links

- [Full Documentation](mobile/README_MOBILE.md)
- [Setup Guide](mobile/QUICKSTART.md)
- [Build Status](BUILD_STATUS.md)
- [Project Overview](MOBILE_TRANSFORMATION.md)

## 📞 ADB Commands

```powershell
# List devices
adb devices

# Install APK manually
adb install app-release.apk

# Uninstall app
adb uninstall com.kundalii.saga

# View logs
adb logcat | Select-String "ReactNative"

# Clear app data
adb shell pm clear com.kundalii.saga
```

## 🎯 Next Steps

1. ✅ **Setup Complete** - All dependencies installed
2. ⏳ **Setup Android SDK** - Install Android Studio
3. ⏳ **Run First Build** - `npm run android`
4. ⏳ **Test Features** - Navigate, login, etc.
5. ⏳ **Develop Features** - Implement screens
6. ⏳ **Build Release** - Create signed APK
7. ⏳ **Deploy** - Upload to Play Store

---

**Status**: ✅ Ready for Testing  
**Last Updated**: Feb 5, 2026
