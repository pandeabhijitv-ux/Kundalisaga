# Background APK Build Script for KundaliSaga
# This script runs the build without interactive prompts

$ErrorActionPreference = "Continue"

# Setup environment variables
$env:ANDROID_HOME = "C:\Users\Abhijit.Pande\AppData\Local\Android\Sdk"
$env:JAVA_HOME = "C:\executables\AndroidStudio\jbr"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Building KundaliSaga Android APK" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to android directory
Set-Location "C:\AstroKnowledge\mobile\android"

Write-Host "Current directory: $(Get-Location)" -ForegroundColor Gray
Write-Host "JAVA_HOME: $env:JAVA_HOME" -ForegroundColor Gray
Write-Host "ANDROID_HOME: $env:ANDROID_HOME" -ForegroundColor Gray
Write-Host ""

# Start build
Write-Host "Starting Gradle build (this takes 5-10 minutes)..." -ForegroundColor Yellow
Write-Host "Please be patient - no interaction required" -ForegroundColor Yellow
Write-Host ""

# Run gradle build with full output
$gradleOutput = & .\gradlew.bat assembleRelease 2>&1 | ForEach-Object { 
    Write-Host $_ -ForegroundColor Gray
    $_
}

$buildExitCode = $LASTEXITCODE

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($buildExitCode -eq 0) {
    Write-Host "BUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    
    # Check for APK
    $apkPath = "app\build\outputs\apk\release\app-release.apk"
    if (Test-Path $apkPath) {
        $apkSize = [math]::Round((Get-Item $apkPath).Length / 1MB, 2)
        Write-Host ""
        Write-Host "APK Location: $apkPath" -ForegroundColor White
        Write-Host "APK Size: $apkSize MB" -ForegroundColor White
        Write-Host ""
        Write-Host "You can install this APK on your Android device!" -ForegroundColor Green
    }
} else {
    Write-Host "BUILD FAILED (Exit code: $buildExitCode)" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Check the output above for errors" -ForegroundColor Yellow
}

Write-Host ""
