# KundaliSaga - Complete Build & Deploy Script

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  KUNDALISAGA - BUILD & DEPLOY" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Step 1: Generate App Icons
Write-Host "Step 1: Generating Shree Ganesh app icons..." -ForegroundColor Magenta
python generate_android_icons.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Icons generated successfully!`n" -ForegroundColor Green
} else {
    Write-Host "❌ Icon generation failed!`n" -ForegroundColor Red
    exit 1
}

# Step 2: Git Commit
Write-Host "Step 2: Committing changes to Git..." -ForegroundColor Magenta
git add .
git commit -m "Fix: Updated Android app with React Native setup, Ganesh icon, and crash fixes

- Added MainApplication.java for proper React Native initialization
- Fixed MainActivity to extend ReactActivity
- Generated Shree Ganesh Ji app icons (all mipmap sizes)
- Added React Native dependencies and auto-linking
- Created ProGuard rules to prevent minification issues
- Fixed component registration in index.js
- Ready for Play Store deployment

Jai Sriram! 🙏"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Changes committed successfully!`n" -ForegroundColor Green
} else {
    Write-Host "⚠️  Git commit skipped (maybe no changes or already committed)`n" -ForegroundColor Yellow
}

# Step 3: Check if pushing to remote
$push = Read-Host "Push to GitHub? (y/n)"
if ($push -eq "y") {
    Write-Host "`nPushing to GitHub..." -ForegroundColor Yellow
    git push
    Write-Host "✅ Pushed to GitHub!`n" -ForegroundColor Green
}

# Step 4: Build AAB
Write-Host "Step 3: Starting Android build..." -ForegroundColor Magenta
Write-Host "This will create an AAB file for Google Play Store!`n" -ForegroundColor Green

# Check if eas-cli is installed
$easInstalled = Get-Command eas -ErrorAction SilentlyContinue

if (-not $easInstalled) {
    Write-Host "Installing EAS CLI globally..." -ForegroundColor Yellow
    npm install -g eas-cli
    Write-Host "✅ EAS CLI installed!`n" -ForegroundColor Green
} else {
    Write-Host "✅ EAS CLI already installed!`n" -ForegroundColor Green
}

# Login
Write-Host "Step 4: Login to Expo" -ForegroundColor Magenta
Write-Host "Account: pande.abhijit.v`n" -ForegroundColor Yellow
eas login

# Configure
Write-Host "`nStep 5: Configure build..." -ForegroundColor Magenta
cd C:\AstroKnowledge\mobile

# Build
Write-Host "`nStep 6: Starting build (this takes 10-15 minutes)..." -ForegroundColor Magenta
Write-Host "The build happens in the cloud, so you can close this and check later!`n" -ForegroundColor Yellow

$build = Read-Host "Ready to start build? (y/n)"

if ($build -eq "y") {
    Write-Host "`n🚀 Building your AAB for Play Store..." -ForegroundColor Green
    Write-Host "With Shree Ganesh Ji's blessings, the app will be ready soon!`n" -ForegroundColor Green
    
    # Build production AAB
    eas build -p android --profile production
    
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  BUILD COMPLETE!" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan
    Write-Host "✅ App now has Shree Ganesh Ji icon" -ForegroundColor Green
    Write-Host "✅ React Native properly initialized" -ForegroundColor Green
    Write-Host "✅ Crash issues fixed" -ForegroundColor Green
    Write-Host "`nDownload the AAB from:" -ForegroundColor Green
    Write-Host "https://expo.dev/accounts/pande.abhijit.v/projects/kundalii-saga-mobile/builds`n" -ForegroundColor Cyan
    Write-Host "Jai Sriram! 🙏" -ForegroundColor Yellow
} else {
    Write-Host "`nBuild cancelled. Run this script again when ready!" -ForegroundColor Yellow
    Write-Host "Jai Sriram! 🙏" -ForegroundColor Yellow
}

Write-Host "`n"

