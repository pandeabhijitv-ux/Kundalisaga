# GitHub Setup & Deployment Guide for KundaliSaga

## Step 1: Create GitHub Repository

1. Go to https://github.com/pandeabhijitv-ux
2. Click the **"+"** icon in top-right → **"New repository"**
3. Fill in details:
   - **Repository name**: `kundalisaga`
   - **Description**: `Privacy-first Vedic Astrology app with AI - Web & Mobile (Android)`
   - **Visibility**: Public (recommended for open-source) or Private
   - **DO NOT** initialize with README (we already have one)
4. Click **"Create repository"**

## Step 2: Initialize Local Git Repository

Open PowerShell in the project directory (`C:\AstroKnowledge`) and run:

```powershell
# Initialize git repository
git init

# Add all files (respects .gitignore)
git add .

# Check what will be committed (verify no sensitive data)
git status

# Create first commit
git commit -m "Initial commit: KundaliSaga v1.0.0 - Web & Mobile app"

# Rename branch to main (if needed)
git branch -M main
```

## Step 3: Link to GitHub and Push

```powershell
# Add remote repository
git remote add origin https://github.com/pandeabhijitv-ux/kundalisaga.git

# Push to GitHub
git push -u origin main
```

**If prompted for credentials:**
- Username: `pandeabhijitv-ux`
- Password: Use a **Personal Access Token** (not your GitHub password)

### Creating Personal Access Token (PAT)

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name: "KundaliSaga Development"
4. Select scopes: `repo` (full control of private repositories)
5. Click "Generate token"
6. **COPY THE TOKEN** (you won't see it again!)
7. Use this token as your password when pushing

## Step 4: Verify Upload

1. Go to https://github.com/pandeabhijitv-ux/kundalisaga
2. Verify files are uploaded
3. Check that sensitive data is NOT uploaded:
   - ✅ No `data/users/` folder should be visible
   - ✅ No `data/payments/` folder
   - ✅ No `.apk` or `.aab` files
   - ✅ No `*.keystore` or `*.jks` files
   - ✅ No `local.properties`

## Step 5: Set Up Repository Settings

### Add Topics/Tags
Go to repository → About section (gear icon) → Add topics:
- `vedic-astrology`
- `astrology`
- `android-app`
- `privacy-first`
- `local-ai`
- `ollama`
- `streamlit`
- `react-native`
- `python`
- `typescript`

### Enable GitHub Pages (Optional)
For hosting documentation:
1. Settings → Pages
2. Source: Deploy from a branch
3. Branch: `main` / `docs` folder
4. Save

### Add Description
**Description**: Privacy-first Vedic Astrology app with AI - Web (Streamlit) & Mobile (Android/React Native) - 100% local data

**Website**: (Leave blank for now, or add your domain if you have one)

## Step 6: Create Releases

Once your repository is set up:

```powershell
# Create a tag for v1.0.0
git tag -a v1.0.0 -m "KundaliSaga v1.0.0 - Initial Release"

# Push tag to GitHub
git push origin v1.0.0
```

Then create a release on GitHub:
1. Go to Releases → Create new release
2. Choose tag: `v1.0.0`
3. Release title: `KundaliSaga v1.0.0 - Initial Release`
4. Description: List major features
5. Attach APK file (optional): Upload `app-release.apk` for users

## Step 7: Google Play Store Preparation

### 1. Build Signed AAB

```powershell
# Run the build script
.\build_apk.ps1

# The AAB file will be at:
# mobile\android\app\build\outputs\bundle\release\app-release.aab
```

### 2. Create Assets for Play Store

You'll need:
- **App Icon**: 512x512 PNG (high-resolution)
- **Feature Graphic**: 1024x500 PNG
- **Screenshots**: At least 2 phone screenshots (16:9 or 9:16 ratio)
- **Privacy Policy URL**: https://github.com/pandeabhijitv-ux/kundalisaga/blob/main/PRIVACY_POLICY.md

### 3. Play Store Listing Information

**App Name**: KundaliSaga - Vedic Astrology

**Short Description** (80 chars max):
Privacy-first Vedic Astrology with AI - Birth Charts, Dasha, Remedies & More

**Full Description** (4000 chars max):
```
🔮 KundaliSaga - Your Personal Vedic Astrology Companion

PRIVACY-FIRST ASTROLOGY
✅ 100% Local Data - No cloud servers
✅ No Tracking - Your data stays on YOUR device
✅ Offline AI - All processing happens locally
✅ Open Source - Verify our privacy claims

COMPLETE VEDIC ASTROLOGY
📊 Birth Charts - Accurate Vedic horoscope calculations
🌙 Dasha Analysis - Vimshottari, Yogini, Ashtottari periods
🌍 Transit Predictions - Current planetary effects
💑 Compatibility - Relationship analysis
🔢 Numerology - Life path, destiny numbers

AI-POWERED INSIGHTS
💬 Ask Questions - Get personalized answers about your chart
🏥 Smart Remedies - Mantras, gemstones, rituals
📖 Knowledge Base - Ancient astrology wisdom
🧠 Context-Aware - All answers based on YOUR birth chart

FAMILY FRIENDLY
👨‍👩‍👧‍👦 Multiple Profiles - Manage family member charts
📜 History - Track all your queries
💳 Simple Pricing - One-time credits, no subscriptions
🌐 Multi-Language - English, Hindi, Marathi

TECHNICAL EXCELLENCE
- Swiss Ephemeris for high-precision calculations
- Lahiri Ayanamsa (Chitrapaksha)
- Local AI (Ollama LLM)
- File-based storage (easy backup)

PERFECT FOR
- Astrology enthusiasts
- Privacy-conscious users
- Families wanting to explore Vedic astrology
- Anyone seeking personalized astrological guidance

Download now and discover the wisdom of Vedic astrology with complete privacy!

GitHub: https://github.com/pandeabhijitv-ux/kundalisaga
```

**Category**: Lifestyle

**Tags**: 
- Astrology
- Lifestyle
- Entertainment
- Education

**Content Rating**: ESRB Everyone, PEGI 3

**Privacy Policy**: https://github.com/pandeabhijitv-ux/kundalisaga/blob/main/PRIVACY_POLICY.md

### 4. Play Store Submission Checklist

- [ ] AAB file signed and built
- [ ] App icon (512x512)
- [ ] Feature graphic (1024x500)
- [ ] Screenshots (min 2)
- [ ] Privacy policy URL
- [ ] App description
- [ ] Content rating questionnaire completed
- [ ] Pricing set (Free with in-app purchases)
- [ ] Countries/regions selected (start with India)
- [ ] Test the app thoroughly on multiple devices

## Step 8: Future Updates

When making updates:

```powershell
# Make your changes, then:
git add .
git commit -m "Describe your changes here"
git push

# For new releases:
git tag -a v1.1.0 -m "Version 1.1.0 - New features"
git push origin v1.1.0
```

## Important Reminders

### NEVER Commit These Files:
- ❌ `data/users/` - User accounts
- ❌ `data/payments/` - Payment data
- ❌ `*.keystore` or `*.jks` - Signing keys
- ❌ `local.properties` - Local Android SDK paths
- ❌ `.env` files - Environment variables
- ❌ API keys or secrets

### DO Commit:
- ✅ Source code (Python, TypeScript)
- ✅ Configuration templates
- ✅ Documentation
- ✅ README, LICENSE
- ✅ Requirements.txt
- ✅ Build scripts
- ✅ `.gitkeep` files for directory structure

## Need Help?

- GitHub Docs: https://docs.github.com
- Play Store Console: https://play.google.com/console
- React Native Android Guide: https://reactnative.dev/docs/signed-apk-android

---

**Ready to push to GitHub?** Follow Step 2 & 3 above! 🚀
