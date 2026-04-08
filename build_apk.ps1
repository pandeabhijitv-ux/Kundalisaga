# KundaliSaga - EAS Build Setup

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  BUILDING KUNDALISAGA ANDROID AAB" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "This will create an AAB file for Google Play Store!" -ForegroundColor Green
Write-Host "The build happens in the cloud - no local dependencies!`n" -ForegroundColor Yellow

# Check if eas-cli is installed
Write-Host "Step 1: Checking EAS CLI..." -ForegroundColor Magenta
$easInstalled = Get-Command eas -ErrorAction SilentlyContinue

if (-not $easInstalled) {
    Write-Host "Installing EAS CLI globally..." -ForegroundColor Yellow
    npm install -g eas-cli
    Write-Host "✅ EAS CLI installed!`n" -ForegroundColor Green
} else {
    Write-Host "✅ EAS CLI already installed!`n" -ForegroundColor Green
}

# Login
Write-Host "Step 2: Login to Expo" -ForegroundColor Magenta
Write-Host "Account: pande.abhijit.v`n" -ForegroundColor Yellow
eas login

# Configure
Write-Host "`nStep 3: Configure build..." -ForegroundColor Magenta
cd C:\AstroKnowledge\mobile

# Build
Write-Host "`nStep 4: Starting build (this takes 10-15 minutes)..." -ForegroundColor Magenta
Write-Host "The build happens in the cloud, so you can close this and check later!`n" -ForegroundColor Yellow

$build = Read-Host "Ready to start build? (y/n)"

if ($build -eq "y") {
    Write-Host "`n🚀 Building your AAB for Play Store..." -ForegroundColor Green
    Write-Host "You'll get a download link when done!`n" -ForegroundColor Green
    
    # Build production AAB
    eas build -p android --profile production
    
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  BUILD COMPLETE!" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan
    Write-Host "Download the AAB from:" -ForegroundColor Green
    Write-Host "https://expo.dev/accounts/pande.abhijit.v/projects/kundalii-saga-mobile/builds`n" -ForegroundColor Cyan
} else {
    Write-Host "`nBuild cancelled. Run this script again when ready!" -ForegroundColor Yellow
}

Write-Host "`n"

