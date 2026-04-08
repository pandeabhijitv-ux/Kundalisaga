# Privacy Policy for KundaliSaga

**Effective Date:** April 8, 2026  
**Last Updated:** April 8, 2026

## Introduction

KundaliSaga ("we", "our", or "us") is committed to protecting your privacy. This Privacy Policy explains how we handle your information when you use our Vedic astrology application.

## Our Privacy-First Approach

**KundaliSaga is designed with privacy at its core.** Unlike most apps, we do NOT:
- Send your data to cloud servers
- Use third-party analytics services
- Track your activity across devices
- Share your information with advertisers
- Store your data on external databases

## Information We Collect

### Information You Provide
When you create a birth chart or profile, you may provide:
- **Personal Information:** Name, date of birth, time of birth, place of birth
- **Contact Information:** Email address (for account authentication only)
- **Questions & Queries:** Astrology-related questions you ask the AI

### Automatically Collected Information
- **Usage Data:** Stored locally on your device for app functionality
- **Session Data:** Temporary data to maintain your login state

## How We Use Your Information

All data processing happens **locally on your device**:

1. **Birth Chart Calculations:** Using Swiss Ephemeris library (offline)
2. **AI Interpretations:** Using local LLM (Ollama) running on your device
3. **Profile Storage:** Saved in local files on your device
4. **Payment Records:** Stored locally for credit management

## Data Storage

- **Location:** All data is stored in local files on your device
- **Format:** JSON files in the application data directory
- **Access:** Only you have access to your data through the app
- **Backup:** You are responsible for backing up your device

### Data File Locations
- Birth charts: `data/user_data/charts/`
- User profiles: `data/user_data/profiles/`
- Query history: `data/user_data/history/`
- User accounts: `data/users/`

## Data Security

We implement security measures including:
- **Password Encryption:** Using bcrypt hashing algorithm
- **Session Management:** Secure session tokens
- **Local Storage:** No transmission over the internet
- **OTP Verification:** Email-based one-time passwords for account security

## Third-Party Services

### Local Services Only
- **Swiss Ephemeris:** Astronomical calculation library (offline)
- **Ollama:** Local AI/LLM service running on your device
- **ChromaDB:** Local vector database for knowledge search

### Email Service (Optional)
If configured, we may use SMTP servers to send:
- One-time password (OTP) codes
- Account verification emails

**Note:** Email functionality is optional and disabled by default.

## Payment Information

- **Payment Method:** UPI/Bank Transfer (India)
- **Storage:** Transaction records stored locally
- **No Card Data:** We do not collect or store credit/debit card information
- **Credits System:** All credit balances maintained in local files

## Your Rights

You have the right to:
- **Access:** View all your stored data through the app
- **Delete:** Remove your account and all associated data
- **Export:** Back up your data by copying the data directory
- **Modify:** Edit or update your profile information anytime

## Data Deletion

To delete your data:
1. Go to Settings → Delete Account (in-app), OR
2. Manually delete the application data folder, OR
3. Uninstall the application

**Note:** Deletion is permanent and cannot be reversed.

## Children's Privacy

KundaliSaga is intended for users aged 13 and above. We do not knowingly collect information from children under 13. If you believe a child has provided us with information, please contact us.

## Mobile App Permissions

### Android Permissions
The KundaliSaga mobile app may request:
- **Internet:** To download ephemeris data and LLM models (one-time)
- **Storage:** To save birth charts and user data locally
- **Email (via Chaquopy):** For OTP verification (optional)

All permissions are used solely for offline functionality.

## Changes to This Privacy Policy

We may update this Privacy Policy from time to time. We will notify you of changes by:
- Updating the "Last Updated" date
- Displaying a notice in the app
- Sending an email (if configured)

## Open Source

KundaliSaga is open-source software. You can review the source code to verify our privacy practices at:
**GitHub:** https://github.com/pandeabhijitv-ux/kundalisaga

## Data Portability

Your data is stored in standard JSON format, making it easy to:
- Export and backup
- Transfer to another device
- Import into other applications

## Limitations of Liability

KundaliSaga provides astrological information for entertainment and personal insight purposes only. We are not responsible for decisions made based on astrological interpretations.

## Contact Us

If you have questions about this Privacy Policy or your data, please contact:

**Email:** support@kundalisaga.com  
**GitHub Issues:** https://github.com/pandeabhijitv-ux/kundalisaga/issues

## Consent

By using KundaliSaga, you consent to this Privacy Policy and our handling of your information as described.

---

## Technical Details (For Transparency)

### Data Processing Flow
1. User inputs birth details → stored locally
2. Swiss Ephemeris calculates positions → results stored locally
3. Local LLM generates interpretations → saved to local history
4. No external API calls for sensitive data

### Data Retention
- **User Accounts:** Until account deletion
- **Birth Charts:** Until manually deleted
- **Query History:** Retained locally, can be cleared anytime
- **Session Data:** Cleared on logout

### Encryption
- Passwords: bcrypt with salt
- Session tokens: Secure random generation
- Data files: Standard file system permissions

## Compliance

KundaliSaga is designed to comply with:
- **GDPR** (General Data Protection Regulation) - EU
- **IT Act 2000** - India
- **Data Protection Principles** - Local-first, user-controlled data

**Note:** Since all data is processed locally on your device, traditional cloud-based data protection concerns do not apply.

---

**Last Reviewed:** April 8, 2026  
**Version:** 1.0.0
