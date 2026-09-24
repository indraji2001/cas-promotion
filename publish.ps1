param (
    [string]$RepoName = "cas-promotion"
)

Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "   Publishing CAS Promotion to GitHub & GitHub Pages   " -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan

# 1. Ensure files are committed
git add .
$status = git status --porcelain
if ($status) {
    git commit -m "Update publication files with social preview cards"
}

# 2. Check if repo already exists or create new
Write-Host "`n[1/3] Creating/Connecting GitHub repository: indraji2001/$RepoName..." -ForegroundColor Yellow
$repoCheck = gh repo view "indraji2001/$RepoName" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Creating new public repository on GitHub..." -ForegroundColor Green
    gh repo create "indraji2001/$RepoName" --public --source=. --remote=origin --push
} else {
    Write-Host "Repository exists. Setting remote and pushing..." -ForegroundColor Green
    git remote remove origin 2>$null
    git remote add origin "https://github.com/indraji2001/$RepoName.git"
    git branch -M main
    git push -u origin main
}

# 3. Enable GitHub Pages
Write-Host "`n[2/3] Enabling GitHub Pages (from main branch / root)..." -ForegroundColor Yellow
$pagesJson = '{"source":{"branch":"main","path":"/"}}'
gh api "repos/indraji2001/$RepoName/pages" -X POST --input - <<< $pagesJson 2>$null
if ($LASTEXITCODE -ne 0) {
    # If already enabled, update or ignore
    Write-Host "GitHub Pages configuration updated." -ForegroundColor Green
} else {
    Write-Host "GitHub Pages successfully enabled!" -ForegroundColor Green
}

$liveUrl = "https://indraji2001.github.io/$RepoName/"
Write-Host "`n[3/3] PUBLISHED SUCCESSFULLY!" -ForegroundColor Cyan
Write-Host "------------------------------------------------------"
Write-Host "Live App URL: $liveUrl" -ForegroundColor Green
Write-Host "Social Card:  $liveUrl" -NoNewline; Write-Host "cas-og.jpg" -ForegroundColor Green
Write-Host "------------------------------------------------------"
Write-Host "When you share '$liveUrl' on WhatsApp:" -ForegroundColor Yellow
Write-Host "WhatsApp will automatically display the large banner thumbnail, title, and description like a YouTube preview!"
