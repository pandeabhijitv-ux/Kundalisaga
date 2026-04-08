# Quick GitHub Push Script for KundaliSaga
# Run this after creating the repository on GitHub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "KundaliSaga - GitHub Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if git is installed
Write-Host "Checking Git installation..." -ForegroundColor Green
$gitInstalled = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitInstalled) {
    Write-Host "ERROR: Git not found. Please install Git first:" -ForegroundColor Red
    Write-Host "https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}
Write-Host "✓ Git found: $(git --version)" -ForegroundColor Green
Write-Host ""

# Step 2: Initialize repository if needed
if (-not (Test-Path ".git")) {
    Write-Host "Initializing Git repository..." -ForegroundColor Green
    git init
    Write-Host "✓ Repository initialized" -ForegroundColor Green
} else {
    Write-Host "✓ Git repository already exists" -ForegroundColor Green
}
Write-Host ""

# Step 3: Check for sensitive files
Write-Host "Checking for sensitive files..." -ForegroundColor Green
$sensitiveFiles = @(
    "mobile\android\app\release\*.keystore",
    "mobile\android\app\release\*.jks",
    "data\users\users.json",
    "data\payments\*.json"
)

$foundSensitive = $false
foreach ($pattern in $sensitiveFiles) {
    $files = Get-ChildItem -Path . -Filter $pattern -Recurse -ErrorAction SilentlyContinue
    if ($files) {
        Write-Host "⚠️  Found sensitive file: $($files.FullName)" -ForegroundColor Yellow
        $foundSensitive = $true
    }
}

if (-not $foundSensitive) {
    Write-Host "✓ No sensitive files detected in tracked area" -ForegroundColor Green
}
Write-Host ""

# Step 4: Stage all files
Write-Host "Staging files for commit..." -ForegroundColor Green
git add .
Write-Host ""

# Step 5: Show status
Write-Host "Files to be committed:" -ForegroundColor Green
git status --short
Write-Host ""

# Step 6: Confirm before commit
Write-Host "Review the files above. Proceed with commit? (Y/N)" -ForegroundColor Yellow
$confirm = Read-Host
if ($confirm -ne "Y" -and $confirm -ne "y") {
    Write-Host "Aborted by user" -ForegroundColor Red
    exit 0
}

# Step 7: Commit
Write-Host ""
Write-Host "Creating commit..." -ForegroundColor Green
git commit -m "Initial commit: KundaliSaga v1.0.0 - Privacy-first Vedic Astrology (Web + Mobile)"
Write-Host "✓ Commit created" -ForegroundColor Green
Write-Host ""

# Step 8: Rename branch to main
Write-Host "Setting branch to 'main'..." -ForegroundColor Green
git branch -M main
Write-Host "✓ Branch set to main" -ForegroundColor Green
Write-Host ""

# Step 9: Check if remote exists
$remoteExists = git remote get-url origin 2>$null
if (-not $remoteExists) {
    Write-Host "Adding GitHub remote..." -ForegroundColor Green
    Write-Host "Enter your GitHub repository URL:" -ForegroundColor Yellow
    Write-Host "Example: https://github.com/pandeabhijitv-ux/kundalisaga.git" -ForegroundColor Cyan
    $repoUrl = Read-Host
    
    if ($repoUrl) {
        git remote add origin $repoUrl
        Write-Host "✓ Remote added: $repoUrl" -ForegroundColor Green
    } else {
        Write-Host "ERROR: No URL provided" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "✓ Remote already configured: $remoteExists" -ForegroundColor Green
}
Write-Host ""

# Step 10: Push to GitHub
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Ready to push to GitHub!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANT: You'll need your GitHub credentials:" -ForegroundColor Yellow
Write-Host "- Username: pandeabhijitv-ux" -ForegroundColor White
Write-Host "- Password: Use a Personal Access Token (PAT)" -ForegroundColor White
Write-Host "  Generate PAT at: https://github.com/settings/tokens" -ForegroundColor Cyan
Write-Host ""
Write-Host "Proceed with push? (Y/N)" -ForegroundColor Yellow
$confirmPush = Read-Host

if ($confirmPush -eq "Y" -or $confirmPush -eq "y") {
    Write-Host ""
    Write-Host "Pushing to GitHub..." -ForegroundColor Green
    git push -u origin main
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host "SUCCESS! 🎉" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Your code is now on GitHub!" -ForegroundColor Green
        Write-Host "View it at: https://github.com/pandeabhijitv-ux/kundalisaga" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "1. Add repository description and topics on GitHub" -ForegroundColor White
        Write-Host "2. Create a release (v1.0.0)" -ForegroundColor White
        Write-Host "3. Build AAB for Play Store: .\build_apk.ps1" -ForegroundColor White
        Write-Host "4. Submit to Google Play Console" -ForegroundColor White
        Write-Host ""
        Write-Host "See GITHUB_SETUP.md for detailed instructions" -ForegroundColor Cyan
    } else {
        Write-Host ""
        Write-Host "ERROR: Push failed" -ForegroundColor Red
        Write-Host "Check your credentials and try again" -ForegroundColor Yellow
        Write-Host "Manual push: git push -u origin main" -ForegroundColor White
    }
} else {
    Write-Host ""
    Write-Host "Push cancelled. You can manually push later with:" -ForegroundColor Yellow
    Write-Host "git push -u origin main" -ForegroundColor White
}

Write-Host ""
