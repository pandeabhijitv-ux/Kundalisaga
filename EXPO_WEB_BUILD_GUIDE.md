# Build KundaliSaga AAB via Expo.dev Website

## 🌐 Build from Expo Dashboard (No Local Dependencies!)

Follow these simple steps to create your AAB build directly from the Expo website.

---

## Step 1: Open Your Project Dashboard

Go to: **https://expo.dev/accounts/pande.abhijit.v/projects/kundalii-saga-mobile**

Or:
1. Visit https://expo.dev
2. Sign in with your account (pande.abhijit.v)
3. Click on **kundalii-saga-mobile** project

---

## Step 2: Navigate to Builds Section

On the project page:
1. Click on **"Builds"** in the left sidebar
2. You'll see your build history (if any)

---

## Step 3: Create New Build

Click the **"Create a build"** button (or "+ New Build" button)

### Configure Build Options:

**Platform**: 
- ✅ Select **Android**

**Build Profile**:
- ✅ Select **production** (this creates AAB for Play Store)

**Git Branch**:
- Select **main** (your default branch)
- Or select specific commit/branch

---

## Step 4: Start the Build

1. Review your configuration
2. Click **"Build"** button
3. Build will start automatically on Expo's servers

**Build Time**: ~10-20 minutes

---

## Step 5: Monitor Build Progress

You can monitor the build in real-time:

### On Dashboard:
- Watch the build status (Queued → In Progress → Finished)
- See live logs as the build progresses

### Build Stages:
1. ⏳ Queued - Waiting for build server
2. 🔧 Installing dependencies
3. 📦 Configuring Android project
4. 🏗️ Building AAB
5. ✅ Complete!

### Email Notification:
You'll receive an email when:
- Build starts
- Build completes (success or failure)

---

## Step 6: Download Your AAB

Once build completes successfully:

1. On the builds page, click on your completed build
2. Click **"Download"** button
3. Save the AAB file (e.g., `build-xxxxx.aab`)

**Or**: The email will include a direct download link

---

## Step 7: Verify AAB Details

Build Information Shown:
- **Size**: ~25-40 MB (typical for React Native app)
- **Build ID**: Unique identifier
- **Version**: 1.0.0 (from app.json)
- **Version Code**: 1
- **Created**: Timestamp

---

## Alternative: Use Expo CLI (If Preferred)

If you prefer command line later:

```powershell
# Once EAS CLI installation completes:
cd C:\AstroKnowledge\mobile

# Login (one-time)
eas login

# Start build
eas build --platform android --profile production

# The build happens on Expo servers, not locally!
```

---

## Your Project Configuration

Already set up in your files:

**app.json**:
```json
{
  "name": "KundaliSaga",
  "slug": "kundalii-saga-mobile",
  "owner": "pande.abhijit.v",
  "version": "1.0.0",
  "android": {
    "package": "com.kundalii.saga",
    "versionCode": 1
  }
}
```

**eas.json** (production profile):
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

---

## What Gets Built

The AAB includes:
- ✅ React Native app code
- ✅ JavaScript bundle
- ✅ Native Android code
- ✅ App resources (icons, images)
- ✅ All dependencies from package.json

### ⚠️ Note about Python/Chaquopy:
If your app uses Chaquopy (Python bridge), you may need to:
1. Add custom build configuration (eas-build-pre-install.sh)
2. Or use local Gradle build for Python features

For pure React Native features, Expo build works perfectly!

---

## Troubleshooting

### Build Fails?

**Check build logs** on the dashboard:
1. Click on failed build
2. View "Build logs" tab
3. Look for error messages

**Common Issues**:
- Missing dependencies → Check package.json
- Configuration error → Verify eas.json
- Native module issue → May need local build

### Need to Update Configuration?

1. Edit `app.json` or `eas.json` locally
2. Commit and push changes to GitHub:
   ```powershell
   git add .
   git commit -m "Update build configuration"
   git push
   ```
3. Create new build from updated code

---

## After Download: Next Steps

Once you have the AAB:

1. ✅ **Test**: Upload to Play Console Internal Testing
2. ✅ **Store Listing**: Complete Play Store information
3. ✅ **Submit**: Send for review
4. ✅ **Publish**: Release to users!

See **PLAY_STORE_CHECKLIST.md** for detailed submission guide.

---

## Quick Links

- **Your Project**: https://expo.dev/accounts/pande.abhijit.v/projects/kundalii-saga-mobile
- **Builds**: https://expo.dev/accounts/pande.abhijit.v/projects/kundalii-saga-mobile/builds
- **Expo Docs**: https://docs.expo.dev/build/introduction/
- **Build Troubleshooting**: https://docs.expo.dev/build-reference/troubleshooting/

---

## Summary: Zero Local Dependencies! ✨

**What you need**:
- ✅ Expo account (you have: pande.abhijit.v)
- ✅ Project set up (done: kundalii-saga-mobile)
- ✅ Code pushed to GitHub (done!)
- ✅ Web browser

**What you DON'T need locally**:
- ❌ Android Studio
- ❌ Gradle
- ❌ JDK/Java
- ❌ Large downloads
- ❌ Complex setup

**Just click "Build" on the website and wait!** ⏰

---

**Ready to build?** Go to:
👉 https://expo.dev/accounts/pande.abhijit.v/projects/kundalii-saga-mobile/builds

Click **"Create a build"** → Select **Android** → Select **production** → Click **Build**! 🚀
