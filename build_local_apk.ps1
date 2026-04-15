# KundaliSaga - Local Gradle Build (Alternative)
# Use this if EAS build has SSL issues

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  KUNDALISAGA - LOCAL GRADLE BUILD" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Building AAB/APK locally using Gradle...`n" -ForegroundColor Green

# Navigate to mobile android folder
cd C:\AstroKnowledge\mobile\android

# Clean previous builds
Write-Host "Step 1: Cleaning previous builds..." -ForegroundColor Magenta
.\gradlew clean
Write-Host "✅ Clean complete!`n" -ForegroundColor Green

# Choose build type
Write-Host "What do you want to build?" -ForegroundColor Yellow
Write-Host "1. AAB for Play Store (recommended)" -ForegroundColor Cyan
Write-Host "2. APK for direct install" -ForegroundColor Cyan
$choice = Read-Host "`nEnter choice (1 or 2)"

if ($choice -eq "1") {
    Write-Host "`nStep 2: Building AAB (Android App Bundle)..." -ForegroundColor Magenta
    Write-Host "This may take 5-10 minutes...`n" -ForegroundColor Yellow
    
    .\gradlew bundleRelease
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n========================================" -ForegroundColor Cyan
        Write-Host "  BUILD SUCCESSFUL!" -ForegroundColor Green
        Write-Host "========================================`n" -ForegroundColor Cyan
        
        $aabPath = "C:\AstroKnowledge\mobile\android\app\build\outputs\bundle\release\app-release.aab"
        Write-Host "✅ AAB file created at:" -ForegroundColor Green
        Write-Host "$aabPath`n" -ForegroundColor Cyan
        
        # Show file info
        $fileInfo = Get-Item $aabPath
        Write-Host "File size: $([math]::Round($fileInfo.Length/1MB, 2)) MB" -ForegroundColor Yellow
        Write-Host "`nUpload this AAB to Google Play Console!" -ForegroundColor Green
    } else {
        Write-Host "`n❌ Build failed! Check errors above.`n" -ForegroundColor Red
    }
    
} elseif ($choice -eq "2") {
    Write-Host "`nStep 2: Building APK..." -ForegroundColor Magenta
    Write-Host "This may take 5-10 minutes...`n" -ForegroundColor Yellow
    
    .\gradlew assembleRelease
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n========================================" -ForegroundColor Cyan
        Write-Host "  BUILD SUCCESSFUL!" -ForegroundColor Green
        Write-Host "========================================`n" -ForegroundColor Cyan
        
        $apkPath = "C:\AstroKnowledge\mobile\android\app\build\outputs\apk\release\app-release.apk"
        Write-Host "✅ APK file created at:" -ForegroundColor Green
        Write-Host "$apkPath`n" -ForegroundColor Cyan
        
        # Show file info
        $fileInfo = Get-Item $apkPath
        Write-Host "File size: $([math]::Round($fileInfo.Length/1MB, 2)) MB" -ForegroundColor Yellow
        
        # Ask to install
        Write-Host "`n" -ForegroundColor Yellow
        $install = Read-Host "Install on connected device? (y/n)"
        
        if ($install -eq "y") {
            Write-Host "`nInstalling APK..." -ForegroundColor Yellow
            adb install -r $apkPath
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ App installed successfully!" -ForegroundColor Green
                Write-Host "Launch 'KundaliSaga' from your device!`n" -ForegroundColor Green
            } else {
                Write-Host "❌ Installation failed. Make sure:" -ForegroundColor Red
                Write-Host "  - Device is connected via USB" -ForegroundColor Yellow
                Write-Host "  - USB debugging is enabled" -ForegroundColor Yellow
                Write-Host "  - Run 'adb devices' to check connection`n" -ForegroundColor Yellow
            }
        }
    } else {
        Write-Host "`n❌ Build failed! Check errors above.`n" -ForegroundColor Red
    }
} else {
    Write-Host "`n❌ Invalid choice!`n" -ForegroundColor Red
}

Write-Host "`n🙏 Jai Sriram!`n" -ForegroundColor Yellow
cd C:\AstroKnowledge
