# KundaliSaga Mobile App - Build Setup Script
# This script prepares and builds the Android mobile app

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  KundaliSaga Mobile App Build Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Navigate to mobile directory
Write-Host "[1/7] Navigating to mobile directory..." -ForegroundColor Yellow
Set-Location -Path "mobile"

# Step 2: Check Node.js
Write-Host "[2/7] Checking Node.js installation..." -ForegroundColor Yellow
$nodeVersion = node --version 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Node.js not found! Please install Node.js 18+" -ForegroundColor Red
    Write-Host "  Download from: https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Step 3: Install NPM dependencies
Write-Host "[3/7] Installing NPM dependencies..." -ForegroundColor Yellow
Write-Host "  This may take 5-10 minutes..." -ForegroundColor Gray
npm install
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ NPM dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✗ NPM install failed" -ForegroundColor Red
    exit 1
}

# Step 4: Link Python backend
Write-Host "[4/7] Linking Python backend to mobile app..." -ForegroundColor Yellow
if (Test-Path "python_modules\src") {
    Write-Host "✓ Python backend already linked" -ForegroundColor Green
} else {
    # Copy src folder to python_modules
    Write-Host "  Copying Python backend files..." -ForegroundColor Gray
    $copyResult = xcopy /E /I ..\src python_modules\src 2>&1
    Write-Host "✓ Python backend linked successfully" -ForegroundColor Green
}

# Step 5: Check Android SDK
Write-Host "[5/7] Checking Android SDK..." -ForegroundColor Yellow
$androidHome = $env:ANDROID_HOME
if ($androidHome -and (Test-Path $androidHome)) {
    Write-Host "✓ Android SDK found at: $androidHome" -ForegroundColor Green
} else {
    Write-Host "⚠ ANDROID_HOME not set or SDK not found" -ForegroundColor Yellow
    Write-Host "  Please install Android Studio and set ANDROID_HOME" -ForegroundColor Yellow
    Write-Host "  See QUICKSTART.md for instructions" -ForegroundColor Yellow
}

# Step 6: Create local.properties for Android
Write-Host "[6/7] Creating Android local.properties..." -ForegroundColor Yellow
if ($androidHome) {
    $androidHomePath = $androidHome -replace '\\', '\\'
    "sdk.dir=$androidHomePath" | Out-File -FilePath "android\local.properties" -Encoding ASCII
    Write-Host "✓ local.properties created" -ForegroundColor Green
} else {
    Write-Host "⚠ Skipped (ANDROID_HOME not set)" -ForegroundColor Yellow
}

# Step 7: Summary and next steps
Write-Host ""
Write-Host "[7/7] Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Next Steps:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Connect Android device or start emulator:" -ForegroundColor White
Write-Host "   - Open Android Studio" -ForegroundColor Gray
Write-Host "   - Tools > AVD Manager > Create/Start Virtual Device" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Check device connection:" -ForegroundColor White
Write-Host "   adb devices" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Run the app:" -ForegroundColor White
Write-Host "   npm run android" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Or build release APK:" -ForegroundColor White
Write-Host "   cd android" -ForegroundColor Gray
Write-Host "   .\gradlew assembleRelease" -ForegroundColor Gray
Write-Host "   # APK will be in: android\app\build\outputs\apk\release\" -ForegroundColor Gray
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "For detailed instructions, see:" -ForegroundColor Yellow
Write-Host "  - QUICKSTART.md" -ForegroundColor Gray
Write-Host "  - README_MOBILE.md" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Return to root
Set-Location -Path ".."
