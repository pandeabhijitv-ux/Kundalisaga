# KundaliSaga - Quick Build Script
# Automatically increments version and builds AAB

param(
    [ValidateSet('patch', 'minor', 'major')]
    [string]$VersionType = 'patch',
    
    [switch]$SkipVersionIncrement
)

Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   KundaliSaga Android Build" -ForegroundColor White
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Set Java Home
$env:JAVA_HOME = "C:\executables\jdk-21.0.9"
Write-Host "✓ Java Home: $env:JAVA_HOME" -ForegroundColor Green

# Change to mobile directory
Push-Location $PSScriptRoot

try {
    # Increment version (unless skipped)
    if (-not $SkipVersionIncrement) {
        Write-Host "`n📝 Incrementing version ($VersionType)..." -ForegroundColor Yellow
        & .\increment_version.ps1 -Type $VersionType
        if ($LASTEXITCODE -ne 0) {
            throw "Version increment failed"
        }
    } else {
        Write-Host "`n⏭️  Skipping version increment" -ForegroundColor Gray
    }

    # Build AAB
    Write-Host "`n🔨 Building Android App Bundle..." -ForegroundColor Yellow
    Push-Location android
    
    .\gradlew.bat clean bundleRelease
    
    if ($LASTEXITCODE -eq 0) {
        Pop-Location
        
        Write-Host "`n═══════════════════════════════════════════════════" -ForegroundColor Green
        Write-Host "   ✅ BUILD SUCCESSFUL!" -ForegroundColor Green
        Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Green
        
        $aabPath = "android\app\build\outputs\bundle\release\app-release.aab"
        if (Test-Path $aabPath) {
            $aabFile = Get-Item $aabPath
            $sizeMB = [math]::Round($aabFile.Length / 1MB, 2)
            
            Write-Host "`n📦 Output:" -ForegroundColor Cyan
            Write-Host "   File: $($aabFile.Name)" -ForegroundColor White
            Write-Host "   Size: $sizeMB MB" -ForegroundColor White
            Write-Host "   Path: $($aabFile.FullName)" -ForegroundColor Gray
            Write-Host "   Time: $($aabFile.LastWriteTime)" -ForegroundColor Gray
            
            Write-Host "`n🚀 Ready to upload to Google Play Store!" -ForegroundColor Green
            Write-Host "   https://play.google.com/console" -ForegroundColor Blue
        }
    } else {
        Pop-Location
        throw "Gradle build failed"
    }
    
} catch {
    Write-Host "`n❌ Build failed: $_" -ForegroundColor Red
    exit 1
} finally {
    Pop-Location
}

Write-Host "`nJai Sriram! 🙏" -ForegroundColor Magenta
