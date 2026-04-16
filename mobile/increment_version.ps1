# KundaliSaga Version Increment Script
# Usage: .\increment_version.ps1 -Type [patch|minor|major]
# Default: patch (1.0.1 -> 1.0.2)

param(
    [ValidateSet('patch', 'minor', 'major')]
    [string]$Type = 'patch'
)

$buildGradlePath = "$PSScriptRoot\android\app\build.gradle"

# Read current build.gradle
$content = Get-Content $buildGradlePath -Raw

# Extract current versionCode and versionName
if ($content -match 'versionCode (\d+)') {
    $currentVersionCode = [int]$matches[1]
    Write-Host "Current versionCode: $currentVersionCode" -ForegroundColor Cyan
} else {
    Write-Error "Could not find versionCode in build.gradle"
    exit 1
}

if ($content -match 'versionName "([^"]+)"') {
    $currentVersionName = $matches[1]
    Write-Host "Current versionName: $currentVersionName" -ForegroundColor Cyan
} else {
    Write-Error "Could not find versionName in build.gradle"
    exit 1
}

# Parse version name (e.g., "1.0.1" -> major=1, minor=0, patch=1)
if ($currentVersionName -match '(\d+)\.(\d+)\.(\d+)') {
    $major = [int]$matches[1]
    $minor = [int]$matches[2]
    $patch = [int]$matches[3]
} else {
    Write-Error "Invalid version name format: $currentVersionName"
    exit 1
}

# Increment version based on type
$newVersionCode = $currentVersionCode + 1

switch ($Type) {
    'patch' {
        $patch++
    }
    'minor' {
        $minor++
        $patch = 0
    }
    'major' {
        $major++
        $minor = 0
        $patch = 0
    }
}

$newVersionName = "$major.$minor.$patch"

Write-Host "`nUpdating versions:" -ForegroundColor Green
Write-Host "  versionCode: $currentVersionCode -> $newVersionCode" -ForegroundColor Yellow
Write-Host "  versionName: $currentVersionName -> $newVersionName" -ForegroundColor Yellow

# Update build.gradle
$content = $content -replace "versionCode $currentVersionCode", "versionCode $newVersionCode"
$content = $content -replace "versionName `"$currentVersionName`"", "versionName `"$newVersionName`""

# Write back to file
Set-Content -Path $buildGradlePath -Value $content -NoNewline

Write-Host "`n✅ Version updated successfully!" -ForegroundColor Green
Write-Host "Next build will be: v$newVersionName (code: $newVersionCode)" -ForegroundColor Cyan
Write-Host "`nTo build the AAB, run:" -ForegroundColor White
Write-Host "  cd android" -ForegroundColor Gray
Write-Host "  .\gradlew.bat clean bundleRelease" -ForegroundColor Gray
