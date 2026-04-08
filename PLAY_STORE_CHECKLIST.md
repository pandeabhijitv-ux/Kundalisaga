# Google Play Store Submission Checklist for KundaliSaga

## Pre-Submission Requirements

### ✅ 1. Google Play Console Account
- [ ] Create account at https://play.google.com/console
- [ ] Pay one-time registration fee ($25 USD)
- [ ] Verify identity (may take 1-2 days)
- [ ] Accept Developer Distribution Agreement

### ✅ 2. Build Signed AAB (Android App Bundle)

#### Create Keystore (First Time Only)
```powershell
# Navigate to android folder
cd mobile\android\app

# Generate keystore (save this file securely!)
keytool -genkeypair -v -storetype PKCS12 -keystore kundalisaga-release.keystore -alias kundalisaga -keyalg RSA -keysize 2048 -validity 10000

# You'll be asked for:
# - Keystore password (remember this!)
# - Key password (remember this!)
# - Name, Organization, City, State, Country
```

#### Configure Gradle for Signing
Create `mobile/android/keystore.properties`:
```properties
storePassword=YOUR_KEYSTORE_PASSWORD
keyPassword=YOUR_KEY_PASSWORD
keyAlias=kundalisaga
storeFile=app/kundalisaga-release.keystore
```

⚠️ **NEVER commit keystore.properties or .keystore files to GitHub!**

#### Build AAB
```powershell
.\build_apk.ps1
```

AAB location: `mobile\android\app\build\outputs\bundle\release\app-release.aab`

### ✅ 3. App Assets

#### Icon (Required)
- [ ] 512x512 PNG, 32-bit, high-resolution
- [ ] No transparency
- [ ] File size < 1MB
- [ ] Design: KundaliSaga logo/branding

#### Feature Graphic (Required)
- [ ] 1024x500 PNG or JPG
- [ ] Showcases app's main features
- [ ] No borders or additional padding

#### Screenshots (Required - Minimum 2)
- [ ] Phone: 16:9 or 9:16 aspect ratio
- [ ] At least 320px on shortest side
- [ ] At most 3840px on longest side
- [ ] Recommended: 1080x1920 (portrait) or 1920x1080 (landscape)
- [ ] Suggested screenshots:
  1. Home screen / Birth chart
  2. Dasha analysis
  3. AI Q&A interface
  4. Remedies page
  5. Profile management

#### Screenshots for 7-inch Tablet (Optional)
- [ ] Same requirements as phone

#### Screenshots for 10-inch Tablet (Optional)
- [ ] Same requirements as phone

#### Promotional Video (Optional)
- [ ] YouTube URL
- [ ] 30 seconds to 2 minutes
- [ ] Shows app functionality

## App Information

### ✅ 4. Store Listing Details

#### App Name
```
KundaliSaga - Vedic Astrology
```
(Max 50 characters)

#### Short Description
```
Privacy-first Vedic Astrology with AI - Birth Charts, Dasha, Remedies & More
```
(Max 80 characters)

#### Full Description
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

Privacy Policy: https://github.com/pandeabhijitv-ux/kundalisaga/blob/main/PRIVACY_POLICY.md
Source Code: https://github.com/pandeabhijitv-ux/kundalisaga
```
(Max 4000 characters)

### ✅ 5. Categorization

- [ ] **App Category**: Lifestyle
- [ ] **Tags**: Astrology, Vedic, Horoscope, Privacy, AI
- [ ] **Content Rating**: Complete questionnaire (likely Everyone/PEGI 3)

### ✅ 6. Contact Details

- [ ] **Email**: support@kundalisaga.com (or your email)
- [ ] **Website**: https://github.com/pandeabhijitv-ux/kundalisaga
- [ ] **Phone** (optional): Your phone number
- [ ] **Privacy Policy URL**: https://github.com/pandeabhijitv-ux/kundalisaga/blob/main/PRIVACY_POLICY.md

### ✅ 7. Pricing & Distribution

- [ ] **Free or Paid**: Free
- [ ] **In-app Purchases**: Yes (Credits: 10 INR, 50 INR, 100 INR, etc.)
- [ ] **Contains Ads**: No
- [ ] **Countries**: Start with India, expand later
- [ ] **Content Rating Questionnaire**: Complete honestly

## Technical Requirements

### ✅ 8. App Details

#### Package Name
```
com.kundalii.saga
```

#### Version Code & Name
```
Version Code: 1
Version Name: 1.0.0
```

#### Minimum SDK
```
API Level 24 (Android 7.0 Nougat)
```

#### Target SDK
```
API Level 35 (Android 15)
```

### ✅ 9. App Access

- [ ] **Restricted Access**: No (app is publicly accessible)
- [ ] **Test Account** (if any restricted features): Provide credentials

### ✅ 10. Privacy & Security

#### Data Safety Section
You must declare how the app collects and handles data:

**Data Collection**:
- [ ] Does your app collect or share user data? **YES**
  - User account info (email, name)
  - Birth details (date, time, location)
  - Query history

**Data Usage**:
- [ ] All data stored locally on device ✅
- [ ] Data not shared with third parties ✅
- [ ] Data not used for tracking ✅
- [ ] Users can request data deletion ✅

**Security Practices**:
- [ ] Data is encrypted in transit: NO (local only)
- [ ] Data is encrypted at rest: Partial (passwords with bcrypt)
- [ ] Users can request data deletion: YES

#### Permissions Justification
Explain why you need each permission:
- **INTERNET**: Download ephemeris data, Ollama models (one-time)
- **ACCESS_FINE_LOCATION**: For accurate chart calculations (optional)
- **WRITE_EXTERNAL_STORAGE**: Save charts locally

### ✅ 11. Content Rating

Complete the questionnaire honestly:
- [ ] No violence
- [ ] No sexual content
- [ ] No profanity
- [ ] No drugs/alcohol
- [ ] May contain spiritual/religious content (astrology)

**Expected Rating**: Everyone / PEGI 3 / ESRB Everyone

### ✅ 12. App Content

- [ ] **Target Audience**: Adults primarily, suitable for all ages
- [ ] **News App**: No
- [ ] **COVID-19 contact tracing/status app**: No
- [ ] **Data Safety Form**: Complete all sections
- [ ] **Government App**: No

## Testing

### ✅ 13. Internal Testing (Recommended First)

- [ ] Upload AAB to Internal Testing track
- [ ] Add test users (up to 100 email addresses)
- [ ] Distribute to testers
- [ ] Fix any bugs reported
- [ ] Get feedback

### ✅ 14. Production Release

- [ ] All assets uploaded
- [ ] Store listing complete
- [ ] Content rating approved
- [ ] Data safety form submitted
- [ ] Privacy policy URL working
- [ ] AAB uploaded to Production track
- [ ] Pricing & distribution set
- [ ] Submit for review

## Post-Submission

### ✅ 15. Review Process

- [ ] **Review Time**: Typically 3-7 days
- [ ] **Status**: Check Play Console for updates
- [ ] **Respond to Google**: If they request changes, respond within 7 days

### ✅ 16. After Approval

- [ ] **Celebrate!** 🎉
- [ ] Monitor reviews
- [ ] Respond to user feedback
- [ ] Plan updates
- [ ] Promote the app

## Common Rejection Reasons (Avoid!)

❌ Missing privacy policy  
❌ Inappropriate content  
❌ Misleading app description  
❌ Icon does not match guidelines  
❌ App crashes on startup  
❌ Incomplete data safety form  
❌ Permissions not justified  

## Resources

- **Play Console**: https://play.google.com/console
- **Developer Policy**: https://play.google.com/about/developer-content-policy/
- **Design Specifications**: https://developer.android.com/distribute/google-play/resources/icon-design-specifications
- **Launch Checklist**: https://developer.android.com/distribute/best-practices/launch/launch-checklist

---

## Quick Command Reference

```powershell
# Build AAB
.\build_apk.ps1

# Check AAB location
ls mobile\android\app\build\outputs\bundle\release

# Generate keystore (first time only)
keytool -genkeypair -v -storetype PKCS12 -keystore kundalisaga-release.keystore -alias kundalisaga -keyalg RSA -keysize 2048 -validity 10000
```

---

**Need Help?** Check Play Console Help or contact Google Play Developer Support.

**Good luck with your submission!** 🚀
