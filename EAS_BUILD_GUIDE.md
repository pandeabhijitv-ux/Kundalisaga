# EAS Build Guide for KundaliSaga

## Quick Start - Create AAB Build on EAS

Your EAS project is already configured:
- **Project ID**: 61002ebc-fa68-4e6a-a137-2bfdfa58c561
- **Owner**: pande.abhijit.v
- **Project URL**: https://expo.dev/accounts/pande.abhijit.v/projects/kundalii-saga-mobile

## Step 1: Install EAS CLI (If not already installed)

```powershell
# Install EAS CLI globally
npm install -g eas-cli

# Verify installation
eas --version
```

## Step 2: Login to Expo

```powershell
# Navigate to mobile directory
cd C:\AstroKnowledge\mobile

# Login to your Expo account
eas login

# Enter your credentials:
# Email: pande.abhijit.v@gmail.com (or your Expo email)
# Password: Your Expo password
```

## Step 3: Verify Configuration

Your `eas.json` is already configured for production builds:
```json
{
  "build": {
    "production": {
      "android": {
        "buildType": "app-bundle"
      }
    }
  }
}
```

## Step 4: Create Production AAB Build

```powershell
# Create production build (AAB for Play Store)
eas build --platform android --profile production

# Or use the npm script:
npm run eas:build:production
```

### What happens during build:
1. ✅ Code is uploaded to Expo servers
2. ✅ Android project is configured
3. ✅ Dependencies are installed
4. ✅ AAB is compiled on Expo's build servers
5. ✅ Build completes in ~10-20 minutes

## Step 5: Monitor Build Progress

After starting the build:

1. **Console Output**: Watch progress in terminal
2. **Expo Dashboard**: Visit https://expo.dev/accounts/pande.abhijit.v/projects/kundalii-saga-mobile/builds
3. **Email Notification**: You'll receive email when build completes

## Step 6: Download AAB

Once build completes:

### Option A: From Dashboard
1. Go to https://expo.dev/accounts/pande.abhijit.v/projects/kundalii-saga-mobile/builds
2. Find your latest build
3. Click "Download" to get the AAB file

### Option B: From CLI
```powershell
# The CLI will provide a download link when build completes
# Download URL format:
# https://expo.dev/artifacts/eas/[build-id]/download
```

## Step 7: Submit to Play Store (Optional)

EAS can submit directly to Play Store:

```powershell
# Submit the build (requires Play Store setup)
eas submit --platform android --profile production

# Or use npm script:
npm run eas:submit:production
```

**Note**: This requires:
- Google Play Console account
- Service account JSON key
- App created on Play Console

## Troubleshooting

### Build Fails with "No Chaquopy License"
EAS doesn't support Chaquopy (Python-Java bridge) by default. You have two options:

#### Option 1: Use Local Gradle Build (Recommended)
```powershell
# Build locally with Gradle (includes Chaquopy)
.\build_apk.ps1
```
Output: `mobile\android\app\build\outputs\bundle\release\app-release.aab`

#### Option 2: Configure EAS for Custom Build
Create `eas-build-pre-install.sh` in mobile folder:
```bash
#!/bin/bash
# Add Chaquopy configuration
echo "Configuring Chaquopy..."
```

### Authentication Issues
```powershell
# Logout and login again
eas logout
eas login
```

### Build Status Check
```powershell
# Check latest build status
eas build:list --platform android --limit 5
```

## Build Configuration Details

### Current Configuration (eas.json)

**Development Profile**:
- Distribution: Internal
- Build Type: APK
- Use: For testing on devices

**Preview Profile**:
- Distribution: Internal
- Build Type: APK
- Use: For internal testing

**Production Profile**:
- Build Type: AAB (App Bundle)
- Use: For Google Play Store submission

### App Configuration (app.json)

- **App Name**: KundaliSaga
- **Package**: com.kundalii.saga
- **Version**: 1.0.0
- **Version Code**: 1

## Important Notes

### ⚠️ Chaquopy Limitation
EAS builds may not support Chaquopy (Python integration) out of the box. For full Python support, use local Gradle build:

```powershell
.\build_apk.ps1
```

### ✅ What Works on EAS
- React Native code
- Native modules (except Chaquopy)
- Standard Android libraries
- APK/AAB generation

### ❌ What May Not Work on EAS
- Chaquopy Python bridge
- Custom Python modules
- pyswisseph calculations (requires local build)

## Recommended Approach

### For Full Python Features (Vedic Calculations):
**Use Local Build**: `.\build_apk.ps1`

### For React Native-Only Features:
**Use EAS Build**: `eas build --platform android --profile production`

## Quick Commands Reference

```powershell
# Install EAS CLI
npm install -g eas-cli

# Login
eas login

# Build production AAB
cd mobile
eas build --platform android --profile production

# Check build status
eas build:list --platform android

# Download build
# Use the link provided in dashboard or email

# Submit to Play Store (if configured)
eas submit --platform android --profile production
```

## Support & Documentation

- **EAS Build Docs**: https://docs.expo.dev/build/introduction/
- **EAS Submit Docs**: https://docs.expo.dev/submit/introduction/
- **Expo Dashboard**: https://expo.dev/accounts/pande.abhijit.v/projects/kundalii-saga-mobile
- **EAS CLI Reference**: https://docs.expo.dev/eas/cli/

## Next Steps After Build

1. ✅ Download AAB from Expo dashboard
2. ✅ Test AAB using Play Console's internal testing
3. ✅ Fill out Play Store listing
4. ✅ Submit for review
5. ✅ Monitor for approval

---

**Good luck with your build!** 🚀

For questions, check Expo Discord or documentation.
