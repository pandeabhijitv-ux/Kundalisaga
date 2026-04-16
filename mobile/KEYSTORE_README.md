# ⚠️ CRITICAL - Keystore Credentials

## Release Keystore Information

### Files (NEVER commit to Git!)
- `android/app/release.keystore` - Release signing certificate
- `android/keystore.properties` - Keystore credentials

### Credentials
- **Store Password**: `KundaliSaga@2026#Secure`
- **Key Alias**: `kundalii-saga-key`
- **Key Password**: `KundaliSaga@2026#Secure`

### Certificate Details
```
CN=KundaliSaga
OU=AstroKnowledge
O=KundaliSaga
L=India
ST=India
C=IN
```

### Validity
- Created: April 16, 2026
- Expires: ~2053 (10,000 days)

## 🔐 Security Checklist

- [x] Files added to `.gitignore`
- [ ] **TODO: Backup keystore to secure cloud storage (Google Drive/OneDrive)**
- [ ] **TODO: Save credentials in password manager**
- [ ] **TODO: Upload keystore to Google Play Console (opt-in to Play App Signing)**

## ⚠️ IMPORTANT WARNINGS

### If You Lose This Keystore:
- ❌ **You CANNOT update your app on Google Play**
- ❌ All future updates must use the SAME keystore
- ❌ Losing it means starting over with a new app listing

### What To Do NOW:
1. **Backup the keystore file** to at least 2 secure locations:
   - Google Drive (encrypted folder)
   - External hard drive
   - Password manager with file attachments
   
2. **Save these passwords** in a secure password manager

3. **Optional but recommended**: Upload to Google Play Console
   - Go to: Release → Setup → App Integrity → Choose signing key
   - Upload `release.keystore`
   - Google will manage it for you (safest option)

## How to Use This Keystore

The build scripts automatically use this keystore when it exists.

### Manual Verification
```powershell
# Verify AAB signature
$env:JAVA_HOME = "C:\executables\jdk-21.0.9"
& "$env:JAVA_HOME\bin\jarsigner.exe" -verify -verbose -certs "android\app\build\outputs\bundle\release\app-release.aab"
```

### If You Need to Recreate (Emergency Only)
⚠️ **DO NOT DO THIS unless absolutely necessary** - it will break app updates!

If you must:
```powershell
cd android/app
& "$env:JAVA_HOME\bin\keytool.exe" -genkeypair -v -keystore release.keystore `
  -alias kundalii-saga-key -keyalg RSA -keysize 2048 -validity 10000 `
  -storepass "KundaliSaga@2026#Secure" -keypass "KundaliSaga@2026#Secure" `
  -dname "CN=KundaliSaga, OU=AstroKnowledge, O=KundaliSaga, L=India, ST=India, C=IN"
```

## Jai Sriram! 🙏

**Remember**: This keystore is the KEY to your app's future. Protect it like your bank password!
