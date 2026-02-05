#!/usr/bin/env pwsh
# Android Studio Installation and Setup Script
# Automates Android Studio installation, SDK setup, and environment configuration

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Android Studio Setup for KundaliSaga" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Function to check if running as Administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Check admin privileges
if (-not (Test-Administrator)) {
    Write-Host "⚠️  This script requires Administrator privileges" -ForegroundColor Yellow
    Write-Host "Please right-click PowerShell and select 'Run as Administrator'`n" -ForegroundColor Yellow
    pause
    exit 1
}

# Step 1: Download Android Studio
Write-Host "Step 1: Downloading Android Studio..." -ForegroundColor Green
$androidStudioUrl = "https://redirector.gvt1.com/edgedl/android/studio/install/2023.3.1.18/android-studio-2023.3.1.18-windows.exe"
$installerPath = "$env:TEMP\android-studio-installer.exe"

if (Test-Path $installerPath) {
    Write-Host "✓ Installer already downloaded" -ForegroundColor Green
} else {
    Write-Host "Downloading Android Studio (1.1GB)..." -ForegroundColor Yellow
    try {
        $ProgressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri $androidStudioUrl -OutFile $installerPath -UseBasicParsing
        Write-Host "✓ Download complete" -ForegroundColor Green
    } catch {
        Write-Host "✗ Download failed: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "`nPlease download manually from: https://developer.android.com/studio" -ForegroundColor Yellow
        pause
        exit 1
    }
}

# Step 2: Install Android Studio
Write-Host "`nStep 2: Installing Android Studio..." -ForegroundColor Green
Write-Host "⚠️  Installation wizard will open - Please follow these settings:" -ForegroundColor Yellow
Write-Host "   1. Choose 'Standard' installation type" -ForegroundColor White
Write-Host "   2. Accept licenses when prompted" -ForegroundColor White
Write-Host "   3. Install Android SDK 35" -ForegroundColor White
Write-Host "   4. Wait for SDK components to download`n" -ForegroundColor White

try {
    Start-Process -FilePath $installerPath -Wait -NoNewWindow
    Write-Host "✓ Installation process completed" -ForegroundColor Green
} catch {
    Write-Host "✗ Installation failed: $($_.Exception.Message)" -ForegroundColor Red
    pause
    exit 1
}

# Step 3: Detect Android SDK location
Write-Host "`nStep 3: Detecting Android SDK..." -ForegroundColor Green

$possiblePaths = @(
    "$env:LOCALAPPDATA\Android\Sdk",
    "$env:PROGRAMFILES\Android\Android Studio\sdk",
    "$env:USERPROFILE\AppData\Local\Android\Sdk"
)

$sdkPath = $null
foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $sdkPath = $path
        Write-Host "✓ Found Android SDK at: $sdkPath" -ForegroundColor Green
        break
    }
}

if (-not $sdkPath) {
    Write-Host "✗ Android SDK not found automatically" -ForegroundColor Red
    Write-Host "Please enter SDK path manually (e.g., C:\Users\YourName\AppData\Local\Android\Sdk):" -ForegroundColor Yellow
    $sdkPath = Read-Host
    
    if (-not (Test-Path $sdkPath)) {
        Write-Host "✗ Invalid path: $sdkPath" -ForegroundColor Red
        pause
        exit 1
    }
}

# Step 4: Set Environment Variables
Write-Host "`nStep 4: Setting environment variables..." -ForegroundColor Green

try {
    # Set ANDROID_HOME
    [System.Environment]::SetEnvironmentVariable("ANDROID_HOME", $sdkPath, [System.EnvironmentVariableTarget]::User)
    Write-Host "✓ Set ANDROID_HOME=$sdkPath" -ForegroundColor Green
    
    # Add to PATH
    $currentPath = [System.Environment]::GetEnvironmentVariable("Path", [System.EnvironmentVariableTarget]::User)
    $pathsToAdd = @(
        "$sdkPath\platform-tools",
        "$sdkPath\tools",
        "$sdkPath\tools\bin",
        "$sdkPath\emulator"
    )
    
    foreach ($pathToAdd in $pathsToAdd) {
        if ($currentPath -notlike "*$pathToAdd*") {
            $currentPath = "$currentPath;$pathToAdd"
        }
    }
    
    [System.Environment]::SetEnvironmentVariable("Path", $currentPath, [System.EnvironmentVariableTarget]::User)
    Write-Host "✓ Updated PATH with SDK tools" -ForegroundColor Green
    
    # Update current session
    $env:ANDROID_HOME = $sdkPath
    $env:Path = "$env:Path;$sdkPath\platform-tools;$sdkPath\tools;$sdkPath\emulator"
    
} catch {
    Write-Host "✗ Failed to set environment variables: $($_.Exception.Message)" -ForegroundColor Red
    pause
    exit 1
}

# Step 5: Install SDK Platform 35
Write-Host "`nStep 5: Installing Android SDK 35..." -ForegroundColor Green

$sdkmanagerPath = "$sdkPath\cmdline-tools\latest\bin\sdkmanager.bat"
if (-not (Test-Path $sdkmanagerPath)) {
    $sdkmanagerPath = "$sdkPath\tools\bin\sdkmanager.bat"
}

if (Test-Path $sdkmanagerPath) {
    Write-Host "Installing SDK packages..." -ForegroundColor Yellow
    
    $packages = @(
        "platforms;android-35",
        "build-tools;35.0.0",
        "platform-tools",
        "emulator",
        "system-images;android-35;google_apis;x86_64"
    )
    
    foreach ($package in $packages) {
        Write-Host "  Installing $package..." -ForegroundColor White
        & $sdkmanagerPath --install $package 2>$null | Out-Null
    }
    
    # Accept licenses
    Write-Host "Accepting SDK licenses..." -ForegroundColor Yellow
    & $sdkmanagerPath --licenses 2>$null | Out-Null
    
    Write-Host "✓ SDK packages installed" -ForegroundColor Green
} else {
    Write-Host "⚠️  SDK Manager not found - Install SDK 35 manually through Android Studio" -ForegroundColor Yellow
}

# Step 6: Create local.properties
Write-Host "`nStep 6: Creating local.properties..." -ForegroundColor Green

$localPropsPath = "C:\AstroKnowledge\mobile\android\local.properties"
$localPropsContent = "sdk.dir=$($sdkPath -replace '\\', '\\')"

try {
    Set-Content -Path $localPropsPath -Value $localPropsContent -Force
    Write-Host "✓ Created $localPropsPath" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to create local.properties: $($_.Exception.Message)" -ForegroundColor Red
}

# Step 7: Create AVD (Android Virtual Device)
Write-Host "`nStep 7: Creating Android Emulator..." -ForegroundColor Green

$avdmanagerPath = "$sdkPath\cmdline-tools\latest\bin\avdmanager.bat"
if (-not (Test-Path $avdmanagerPath)) {
    $avdmanagerPath = "$sdkPath\tools\bin\avdmanager.bat"
}

if (Test-Path $avdmanagerPath) {
    $avdName = "Pixel_6_API_35"
    Write-Host "Creating AVD: $avdName..." -ForegroundColor Yellow
    
    $avdCommand = "echo no | `"$avdmanagerPath`" create avd -n $avdName -k `"system-images;android-35;google_apis;x86_64`" -d `"pixel_6`" --force"
    Invoke-Expression $avdCommand 2>$null | Out-Null
    
    Write-Host "✓ Emulator created: $avdName" -ForegroundColor Green
} else {
    Write-Host "⚠️  AVD Manager not found - Create emulator manually through Android Studio" -ForegroundColor Yellow
}

# Final Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✓ Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nEnvironment Variables Set:" -ForegroundColor White
Write-Host "  ANDROID_HOME = $sdkPath" -ForegroundColor Gray
Write-Host "`nNext Steps:" -ForegroundColor White
Write-Host "  1. RESTART PowerShell/Terminal (for env vars to take effect)" -ForegroundColor Yellow
Write-Host "  2. cd C:\AstroKnowledge\mobile" -ForegroundColor Gray
Write-Host "  3. npx react-native run-android" -ForegroundColor Gray
Write-Host "`nOr to build APK/AAB:" -ForegroundColor White
Write-Host "  cd C:\AstroKnowledge\mobile\android" -ForegroundColor Gray
Write-Host "  .\gradlew assembleRelease      # For APK" -ForegroundColor Gray
Write-Host "  .\gradlew bundleRelease        # For AAB (Play Store)" -ForegroundColor Gray
Write-Host "`nOutput locations:" -ForegroundColor White
Write-Host "  APK: mobile\android\app\build\outputs\apk\release\app-release.apk" -ForegroundColor Gray
Write-Host "  AAB: mobile\android\app\build\outputs\bundle\release\app-release.aab" -ForegroundColor Gray
Write-Host "`n⚠️  IMPORTANT: Open a NEW terminal after this script completes!" -ForegroundColor Yellow
Write-Host ""

pause
