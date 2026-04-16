# Build Debug APK for Testing
# Easier to test than AAB, includes debug info

param(
    [switch]$Install,
    [switch]$Launch
)

Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   KundaliSaga - Debug APK Build" -ForegroundColor White
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Set Java Home
$env:JAVA_HOME = "C:\executables\jdk-21.0.9"
Write-Host "✓ Java Home: $env:JAVA_HOME" -ForegroundColor Green

Push-Location $PSScriptRoot

try {
    # Step 1: Bundle JavaScript
    Write-Host "`n📦 Step 1: Bundling JavaScript..." -ForegroundColor Yellow
    
    $assetsDir = "android\app\src\main\assets"
    if (!(Test-Path $assetsDir)) {
        New-Item -ItemType Directory -Path $assetsDir -Force | Out-Null
    }
    
    npx react-native bundle `
        --platform android `
        --dev false `
        --entry-file index.js `
        --bundle-output "$assetsDir\index.android.bundle" `
        --assets-dest android\app\src\main\res
    
    if ($LASTEXITCODE -ne 0) {
        throw "JavaScript bundling failed"
    }
    
    Write-Host "✓ JavaScript bundled" -ForegroundColor Green
    
    # Step 2: Build Debug APK
    Write-Host "`n🔨 Step 2: Building Debug APK..." -ForegroundColor Yellow
    
    Push-Location android
    
    .\gradlew.bat assembleDebug
    
    if ($LASTEXITCODE -ne 0) {
        Pop-Location
        throw "Gradle build failed"
    }
    
    Pop-Location
    
    $apkPath = "android\app\build\outputs\apk\debug\app-debug.apk"
    
    if (!(Test-Path $apkPath)) {
        throw "APK not found at: $apkPath"
    }
    
    $apkFile = Get-Item $apkPath
    $sizeMB = [math]::Round($apkFile.Length / 1MB, 2)
    
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host "   ✅ DEBUG APK BUILT" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host ""
    Write-Host "File:    $($apkFile.Name)" -ForegroundColor Cyan
    Write-Host "Size:    $sizeMB MB" -ForegroundColor Cyan
    Write-Host "Path:    $($apkFile.FullName)" -ForegroundColor Gray
    Write-Host "Created: $($apkFile.LastWriteTime)" -ForegroundColor Gray
    Write-Host ""
    
    # Step 3: Install if requested
    if ($Install) {
        Write-Host "📱 Step 3: Installing on device..." -ForegroundColor Yellow
        
        # Find ADB
        $adbPath = ""
        $possiblePaths = @(
            "C:\android-sdk\platform-tools\adb.exe",
            "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe",
            "$env:USERPROFILE\AppData\Local\Android\Sdk\platform-tools\adb.exe"
        )
        
        foreach ($path in $possiblePaths) {
            if (Test-Path $path) {
                $adbPath = $path
                break
            }
        }
        
        if ($adbPath -eq "") {
            Write-Host "⚠️  ADB not found - cannot install" -ForegroundColor Yellow
            Write-Host "   Manually copy APK to device: $($apkFile.FullName)" -ForegroundColor Gray
        } else {
            Write-Host "✓ ADB found: $adbPath" -ForegroundColor Green
            
            & $adbPath install -r $apkPath
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ APK installed" -ForegroundColor Green
                
                if ($Launch) {
                    Write-Host "`n🚀 Launching app..." -ForegroundColor Yellow
                    & $adbPath shell am start -n com.kundalii.saga/.MainActivity
                    
                    Write-Host ""
                    Write-Host "📋 To view logs in real-time:" -ForegroundColor Cyan
                    Write-Host "   .\get_crash_log.ps1" -ForegroundColor Gray
                }
            } else {
                Write-Host "❌ Installation failed" -ForegroundColor Red
            }
        }
    } else {
        Write-Host "To install on device:" -ForegroundColor Cyan
        Write-Host "  .\build_debug_apk.ps1 -Install" -ForegroundColor Gray
        Write-Host ""
        Write-Host "To install and launch:" -ForegroundColor Cyan
        Write-Host "  .\build_debug_apk.ps1 -Install -Launch" -ForegroundColor Gray
    }
    
} catch {
    Write-Host ""
    Write-Host "❌ Build failed: $_" -ForegroundColor Red
    exit 1
} finally {
    Pop-Location
}

Write-Host ""
Write-Host "Jai Sriram! 🙏" -ForegroundColor Magenta
