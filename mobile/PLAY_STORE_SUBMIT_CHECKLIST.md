# Play Store Submit Checklist (EAS)

Use this once your AAB build succeeds.

## A) Play Console prerequisites

- App exists in Google Play Console with package name: `com.kundalii.saga`
- At least one release track is available (`internal` recommended first)
- Required store listing fields are filled enough for internal testing

## B) Service account setup

1. In Google Cloud Console (same project linked to Play):
   - Create a service account for CI/CD submit
   - Create and download JSON key file
2. In Google Play Console:
   - Go to API access and link the same Google Cloud project
   - Grant this service account access to your app (Release manager or equivalent)

## C) Local credential handling (safe)

- Save key as: `mobile/credentials/google-play-service-account.json`
- This path is git-ignored (do not commit credentials)

## D) First submit using EAS

```powershell
cd mobile
npm run eas:build:production
npm run eas:submit:production
```

During first `eas submit`, provide/select:
- Service account JSON path (`mobile/credentials/google-play-service-account.json`)
- App package (`com.kundalii.saga`)
- Track (`internal`)

## E) Verify after submit

- Check Play Console > Testing > Internal testing
- Confirm new artifact appears and processing completes
- Add tester emails/groups and roll out

## Troubleshooting

- `The caller does not have permission`: service account is not granted app access in Play Console API access.
- `Package name mismatch`: ensure Play app package is exactly `com.kundalii.saga`.
- `Version code already used`: increase Android `versionCode` before next production build.
