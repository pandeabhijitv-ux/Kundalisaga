# EAS Build Setup (Expo.dev)

This project is configured for EAS Android cloud builds.

## 1) Login and link project

```powershell
cd mobile
eas login
```

Login with your Expo account: `pande.abhijit.v`.

Then initialize/link project:

```powershell
eas init
```

- If prompted, create a new Expo project (or link existing if you prefer).
- Copy the generated `projectId` and replace `REPLACE_WITH_EAS_PROJECT_ID` in `app.json`.

## 2) Android credentials (keystore)

Run:

```powershell
eas credentials
```

For Android, let Expo manage the keystore (recommended) unless you already have a production keystore.

## 3) Build APK for testing

```powershell
npm run eas:build:preview
```

## 4) Build AAB for Google Play

```powershell
npm run eas:build:production
```

## 5) Submit to Play Console (optional automation)

```powershell
npm run eas:submit:production
```

You need a Google Play service account JSON configured in Expo/EAS submit credentials.

Recommended local path for key file:

```text
mobile/credentials/google-play-service-account.json
```

This folder is git-ignored.

For full Play setup and troubleshooting, use `PLAY_STORE_SUBMIT_CHECKLIST.md`.

## 6) Version code for each new Play upload

Google Play requires each upload to have a new Android `versionCode`.

- Update `android.versionCode` in `app.json` before a new production build.
- Keep `version` (`versionName`) in sync for release clarity.

## Important notes for this project

- Android release signing now supports EAS injected signing properties.
- Chaquopy Python build now uses env var `PYTHON_EXECUTABLE` if provided, so there is no Windows-only hardcoded path.
- Local release build still works with debug signing fallback when no release keystore is configured.
