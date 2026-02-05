# KundaliSaga Mobile App

## 🎯 Overview

This is the **React Native mobile application** for KundaliSaga, integrating your existing Python backend for Vedic astrology calculations directly into the mobile app using **Chaquopy**.

## 📁 Project Structure

```
mobile/
├── android/                    # Android native code
│   ├── app/
│   │   ├── build.gradle       # Chaquopy configuration
│   │   └── src/main/java/com/kundalii/saga/
│   │       ├── MainActivity.java
│   │       ├── MainApplication.java
│   │       ├── PythonBridgeModule.java    # Java-Python bridge
│   │       └── PythonBridgePackage.java
│   └── build.gradle           # Top-level build config
│
├── src/
│   ├── contexts/              # React Context providers
│   │   └── AuthContext.tsx   # Authentication state
│   ├── navigation/            # Navigation setup
│   │   └── AppNavigator.tsx  # Stack & Tab navigation
│   ├── screens/               # All app screens
│   │   ├── auth/             # Login, Register
│   │   ├── home/             # Home dashboard
│   │   ├── profiles/         # User profiles
│   │   ├── horoscope/        # Birth chart
│   │   ├── remedies/         # Remedies
│   │   └── ask/              # Q&A
│   ├── services/
│   │   └── PythonBridge.ts   # TypeScript interface to Python
│   └── components/            # Reusable UI components (to be added)
│
├── python_modules/            # Python backend wrappers
│   ├── vedic_calculator.py   # Chart calculations
│   ├── remedy_calculator.py  # Remedies
│   ├── numerology_calculator.py
│   ├── dasha_calculator.py
│   └── knowledge_search.py
│
├── App.tsx                    # Main app entry
├── package.json              # Node dependencies
└── README_MOBILE.md          # This file
```

## 🚀 Setup Instructions

### Prerequisites

1. **Node.js 18+** and npm
2. **Android Studio** with SDK 34
3. **JDK 17**
4. **Python 3.9** (for testing Python modules)

### Step 1: Install Dependencies

```bash
cd mobile
npm install
```

### Step 2: Setup Android Environment

```bash
# Set ANDROID_HOME environment variable
# Windows:
setx ANDROID_HOME "C:\Users\YourUsername\AppData\Local\Android\Sdk"

# Add to PATH:
# %ANDROID_HOME%\platform-tools
# %ANDROID_HOME%\tools
# %ANDROID_HOME%\tools\bin
```

### Step 3: Copy Python Backend

The Python modules in `python_modules/` wrap your existing backend. They need access to your `src/` folder:

```bash
# Create symbolic link (run as Administrator on Windows)
mklink /D "mobile\python_modules\src" "..\src"

# Or copy the entire src folder:
xcopy /E /I ..\src mobile\python_modules\src
```

### Step 4: Test Python Modules

```bash
cd python_modules
python vedic_calculator.py
python remedy_calculator.py
python numerology_calculator.py
```

### Step 5: Build Android App

```bash
# Connect Android device or start emulator
# Check device connection:
adb devices

# Run the app
npm run android
```

## 🔧 How It Works

### Architecture Flow

```
React Native UI (JavaScript/TypeScript)
         ↓
PythonBridge.ts (TypeScript Interface)
         ↓
PythonBridgeModule.java (Native Module)
         ↓
Chaquopy (Python Runtime)
         ↓
Python Backend (vedic_calculator.py, etc.)
         ↓
Your Existing Modules (src/astrology_engine/, etc.)
```

### Example Usage

**In React Native:**
```typescript
import {calculateChart} from './services/PythonBridge';

const birthDetails = {
  name: 'John Doe',
  date: '1990-01-01',
  time: '12:00',
  location: 'Mumbai',
  latitude: 19.0760,
  longitude: 72.8777,
  timezone: 'Asia/Kolkata'
};

const chart = await calculateChart(birthDetails);
console.log(chart.planets);
```

**Python Backend (Automatic):**
```python
# vedic_calculator.py handles the calculation
def calculate_chart(name, date_str, time_str, ...):
    engine = VedicAstrologyEngine()
    chart = engine.calculate_chart(birth_details)
    return json.dumps(result)
```

## 📱 Features Implemented

### ✅ Core Structure
- [x] React Native setup
- [x] Navigation (Stack + Bottom Tabs)
- [x] Authentication flow (Login/Register/Guest)
- [x] Chaquopy integration
- [x] Python bridge module
- [x] Theme matching your Streamlit app

### 🚧 To Be Implemented
- [ ] Birth chart calculation screen
- [ ] Chart visualization
- [ ] Profiles management
- [ ] Remedies display
- [ ] Q&A with knowledge base
- [ ] Numerology screen
- [ ] Dasha timeline
- [ ] Settings screen
- [ ] Push notifications
- [ ] Offline storage

## 🎨 Theme

The app uses the same color scheme as your Streamlit app:
- Background: `#FFF5E6` (Light Saffron/Peach)
- Primary: `#FF6B35` (Orange)
- Secondary: `#F9C74F` (Yellow)
- Card: `#FFFFF0` (Ivory)

## 🔐 Data Storage

All data is stored locally on the device:
- **AsyncStorage**: User sessions, settings
- **File System**: Charts, profiles (JSON files)
- **No Cloud**: Everything stays on device

## 📦 Dependencies

### React Native Core
- `react-native`: 0.73.0
- `react-navigation`: Navigation system
- `react-native-vector-icons`: Icons

### Python Integration
- Chaquopy: 14.0.2 (configured in build.gradle)
- Python packages (auto-installed by Chaquopy):
  - pyswisseph
  - pytz
  - geopy
  - timezonefinder
  - pandas
  - numpy

## 🧪 Testing

### Test Python Modules
```bash
cd python_modules
python -m pytest  # if you add tests
```

### Test React Native
```bash
npm test
```

### Run on Device
```bash
npm run android
# or
npm run ios  # (requires Mac + Xcode)
```

## 📋 Build Release APK

```bash
cd android
./gradlew assembleRelease

# APK will be at:
# android/app/build/outputs/apk/release/app-release.apk
```

## 🚀 Deploy to Play Store

1. **Create signed APK**:
   - Generate keystore
   - Update `android/app/build.gradle` with signing config
   - Build: `./gradlew bundleRelease`

2. **Upload to Play Console**:
   - Create app on Google Play Console
   - Upload AAB file
   - Fill out store listing
   - Submit for review

## 🔧 Troubleshooting

### Python Import Errors
```bash
# Make sure src/ is accessible to Python modules
# Check sys.path in vedic_calculator.py
```

### Build Errors
```bash
# Clean build
cd android
./gradlew clean
cd ..
npm run android
```

### Chaquopy Issues
```bash
# Check Chaquopy is properly installed
# See android/app/build.gradle
```

## 📚 Next Steps

1. **Complete Remaining Screens**:
   - Implement HoroscopeScreen with chart input
   - Add chart visualization
   - Build ProfilesScreen
   - Implement RemediesScreen

2. **Enhance Python Integration**:
   - Complete all calculator functions
   - Add error handling
   - Optimize performance

3. **Add Features**:
   - Push notifications for daily horoscope
   - Offline mode
   - Chart sharing
   - PDF export

4. **Polish**:
   - Add animations
   - Improve loading states
   - Add onboarding flow
   - Localization (Hindi/Marathi)

## 📞 Support

For issues or questions:
- Check Python module logs
- Check React Native logs: `npx react-native log-android`
- Check Java bridge logs in Android Studio Logcat

## 🎉 Summary

Your mobile app is now set up with:
- ✅ Complete project structure
- ✅ Python backend integration via Chaquopy
- ✅ Navigation system
- ✅ Authentication flow
- ✅ Theme matching your Streamlit app
- ✅ Ready for feature implementation

**Next**: Start implementing the horoscope calculation screen! 🚀
