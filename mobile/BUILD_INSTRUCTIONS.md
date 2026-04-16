# KundaliSaga Mobile Build Guide

## Quick Build (Recommended)

Build and auto-increment version in one command:

```powershell
# Patch update (1.0.1 -> 1.0.2) - Default for bug fixes
.\build_release.ps1

# Minor update (1.0.1 -> 1.1.0) - For new features
.\build_release.ps1 -VersionType minor

# Major update (1.0.1 -> 2.0.0) - For breaking changes
.\build_release.ps1 -VersionType major

# Build without incrementing version
.\build_release.ps1 -SkipVersionIncrement
```

## Manual Version Management

### Increment Version Only

```powershell
# Increment patch (1.0.1 -> 1.0.2)
.\increment_version.ps1

# Increment minor (1.0.1 -> 1.1.0)
.\increment_version.ps1 -Type minor

# Increment major (1.0.1 -> 2.0.0)
.\increment_version.ps1 -Type major
```

### Build Without Version Change

```powershell
cd android
.\gradlew.bat clean bundleRelease
```

## Current Version

Check [android/app/build.gradle](android/app/build.gradle) lines 38-39:
- `versionCode` - Integer, must increment for every Play Store upload
- `versionName` - String, shown to users (semantic versioning)

## Version History

| Version Code | Version Name | Date | Notes |
|--------------|--------------|------|-------|
| 1 | 1.0.0 | April 2026 | Initial Play Store release |
| 2 | 1.0.1 | April 16, 2026 | Full React Native + Python functionality |

## Output Location

After successful build:
```
android/app/build/outputs/bundle/release/app-release.aab
```

## Upload to Play Store

1. Go to [Google Play Console](https://play.google.com/console)
2. Select "KundaliSaga" app
3. Navigate to: Production → Create new release
4. Upload: `app-release.aab`
5. Review and roll out

## Important Notes

- Always increment version before uploading to Play Store
- Version code must be higher than previous release
- Keep SDK levels consistent (minSdk: 24, targetSdk: 35)
- All 4 ABIs must be included (arm64-v8a, armeabi-v7a, x86, x86_64)

## Jai Sriram! 🙏
