# ============================================================
# SIH TEST DISK CREATOR
# Windows 10 Home - DiskPart
# Creates a 512 MiB NTFS virtual disk
# ============================================================

$DiskPath = "C:\test.vhd"
$DriveLetter = "T"
$VolumeLabel = "SIH_TEST"

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "       SIH TEST DISK CREATOR" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check administrator
$principal = New-Object Security.Principal.WindowsPrincipal(
    [Security.Principal.WindowsIdentity]::GetCurrent()
)

if (-not $principal.IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator
)) {
    Write-Host "[ERROR] Run PowerShell as Administrator." -ForegroundColor Red
    exit
}

Write-Host "[+] Administrator privileges confirmed." -ForegroundColor Green

# Check whether T: is already being used
if (Test-Path "T:\") {
    Write-Host "[ERROR] T: drive is already in use." -ForegroundColor Red
    exit
}

# Remove old VHD if it exists
if (Test-Path $DiskPath) {

    Write-Host "[INFO] Existing test.vhd found." -ForegroundColor Yellow

    $answer = Read-Host "Delete it and create a new one? (Y/N)"

    if ($answer -ne "Y" -and $answer -ne "y") {
        Write-Host "[INFO] Cancelled."
        exit
    }

    # Attempt to detach existing VHD
    $detach = @"
select vdisk file="$DiskPath"
detach vdisk
exit
"@

    $detachFile = "$env:TEMP\detach_sih.txt"

    $detach | Out-File `
        -FilePath $detachFile `
        -Encoding ASCII

    diskpart /s $detachFile

    Remove-Item $detachFile -Force -ErrorAction SilentlyContinue

    Start-Sleep -Seconds 2

    Remove-Item $DiskPath -Force -ErrorAction SilentlyContinue
}

# Create DiskPart instructions
Write-Host ""
Write-Host "[1] Creating 512 MiB VHD..." -ForegroundColor Cyan

$commands = @"
create vdisk file="$DiskPath" maximum=512 type=fixed
select vdisk file="$DiskPath"
attach vdisk
create partition primary
format fs=ntfs label="$VolumeLabel" quick
assign letter=$DriveLetter
exit
"@

$commandFile = "$env:TEMP\create_sih_disk.txt"

$commands | Out-File `
    -FilePath $commandFile `
    -Encoding ASCII

# Execute DiskPart
Write-Host "[2] Running DiskPart..." -ForegroundColor Cyan

diskpart /s $commandFile

Remove-Item $commandFile -Force -ErrorAction SilentlyContinue

# Give Windows time to mount it
Start-Sleep -Seconds 3

# Verify VHD
Write-Host ""
Write-Host "[3] Checking virtual disk..." -ForegroundColor Cyan

if (-not (Test-Path $DiskPath)) {
    Write-Host "[ERROR] test.vhd was not created." -ForegroundColor Red
    exit
}

Write-Host "[+] test.vhd created." -ForegroundColor Green

# Verify drive
Write-Host ""
Write-Host "[4] Checking T: drive..." -ForegroundColor Cyan

if (-not (Test-Path "T:\")) {
    Write-Host "[ERROR] T: drive was not mounted." -ForegroundColor Red
    exit
}

Write-Host "[+] T: drive is available." -ForegroundColor Green

# Check filesystem
$volume = Get-Volume -DriveLetter T

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "        TEST DISK CREATED SUCCESSFULLY" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

Write-Host "Image       : C:\test.vhd"
Write-Host "Size        : 512 MiB"
Write-Host "Filesystem  : $($volume.FileSystem)"
Write-Host "Label       : $($volume.FileSystemLabel)"
Write-Host "Drive       : T:\"
Write-Host ""

Write-Host "Open File Explorer and go to:" -ForegroundColor Cyan
Write-Host ""
Write-Host "    T:\" -ForegroundColor White
Write-Host ""

Write-Host "You can now copy your SIH test files into T:\." -ForegroundColor Green
Write-Host ""