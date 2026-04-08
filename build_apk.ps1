# Simple Android Build Script for KundaliSaga

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Building KundaliSaga Android App" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Setup environment
Write-Host "Setting up environment..." -ForegroundColor Green
$env:ANDROID_HOME = "C:\Users\Abhijit.Pande\AppData\Local\Android\Sdk"
$env:JAVA_HOME = "C:\executables\AndroidStudio\jbr"

if (-not (Test-Path $env:JAVA_HOME)) {
    Write-Host "WARNING: JDK not found at $env:JAVA_HOME" -ForegroundColor Yellow
    Write-Host "Searching for Java..." -ForegroundColor Yellow
    $javaPath = (Get-Command java -ErrorAction SilentlyContinue).Source
    if ($javaPath) {
        $env:JAVA_HOME = (Get-Item $javaPath).Directory.Parent.FullName
        Write-Host "Found Java at: $env:JAVA_HOME" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Java not found. Please install JDK" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Java found: $env:JAVA_HOME" -ForegroundColor Green
}

# Step 2: Check Gradle wrapper
Write-Host ""
Write-Host "Checking Gradle wrapper..." -ForegroundColor Green
$gradleWrapperJar = "C:\AstroKnowledge\mobile\android\gradle\wrapper\gradle-wrapper.jar"

if (-not (Test-Path $gradleWrapperJar)) {
    Write-Host "Downloading Gradle wrapper..." -ForegroundColor Yellow
    $url = "https://services.gradle.org/distributions/gradle-8.3-bin.zip"
    $zip = "$env:TEMP\gradle.zip"
    try {
        Invoke-WebRequest -Uri $url -OutFile $zip
        Expand-Archive -Path $zip -DestinationPath "$env:TEMP\gradle" -Force
        Copy-Item "$env:TEMP\gradle\gradle-8.3\lib\plugins\gradle-wrapper-8.3.jar" -Destination $gradleWrapperJar -Force
        Write-Host "Gradle wrapper installed" -ForegroundColor Green
    } catch {
        Write-Host "Could not download Gradle: $_" -ForegroundColor Red
    }
} else {
    Write-Host "Gradle wrapper exists" -ForegroundColor Green
}

# Step 3: Build APK
Write-Host ""
Write-Host "Building APK (5-10 minutes)..." -ForegroundColor Green
cd C:\AstroKnowledge\mobile\android

if (Test-Path "gradlew.bat") {
    cmd /c "gradlew.bat assembleRelease"
    
    $apkPath = "app\build\outputs\apk\release\app-release.apk"
    if (Test-Path $apkPath) {
        $apkSize = [math]::Round((Get-Item $apkPath).Length / 1MB, 2)
        Write-Host ""
        Write-Host "SUCCESS: APK built!" -ForegroundColor Green
        Write-Host "Location: $apkPath" -ForegroundColor White
        Write-Host "Size: $apkSize MB" -ForegroundColor White
    }
}

# Step 4: Build AAB
Write-Host ""
Write-Host "Building AAB for Play Store..." -ForegroundColor Green
cmd /c "gradlew.bat bundleRelease"

$aabPath = "app\build\outputs\bundle\release\app-release.aab"
if (Test-Path $aabPath) {
    $aabSize = [math]::Round((Get-Item $aabPath).Length / 1MB, 2)
    Write-Host ""
    Write-Host "SUCCESS: AAB built!" -ForegroundColor Green
    Write-Host "Location: $aabPath" -ForegroundColor White
    Write-Host "Size: $aabSize MB" -ForegroundColor White
}

Write-Host ""
Write-Host "========================================"  -ForegroundColor Cyan
Write-Host "Build Complete!" -ForegroundColor Green
Write-Host "========================================"  -ForegroundColor Cyan
Write-Host ""

