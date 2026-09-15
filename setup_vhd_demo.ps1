# Create a Virtual Hard Disk for the Demo using Diskpart
# We will create it as a .vhd, and once you're done, the script will rename it to test.img for the backend.

$VhdPath = Join-Path -Path $PSScriptRoot -ChildPath "demo_drive.vhd"
$ImgPath = Join-Path -Path $PSScriptRoot -ChildPath "test.img"

# Make sure we run as Administrator
if (-not ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "Requesting Administrator privileges..."
    Start-Process powershell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

if (Test-Path $VhdPath) {
    Write-Host "Cleaning up existing VHD..."
    $detachScript = "select vdisk file=`"$VhdPath`"`ndetach vdisk"
    $detachScript | diskpart | Out-Null
    Remove-Item -Path $VhdPath -Force -ErrorAction SilentlyContinue
}

Write-Host "Creating demo_drive.vhd..."
$dpScript = @"
create vdisk file="$VhdPath" maximum=100 type=expandable
select vdisk file="$VhdPath"
attach vdisk
create partition primary
format fs=fat32 label="SIH_DEMO" quick
assign
"@

$dpScript | diskpart | Out-Null

Write-Host "Waiting for Windows to mount the drive..."
Start-Sleep -Seconds 3

# Find the drive letter by volume label
$Drive = Get-Volume | Where-Object FileSystemLabel -eq "SIH_DEMO"
if (-not $Drive) {
    Write-Host "Error: Could not find the mounted drive."
    pause
    exit
}

$DriveLetter = $Drive.DriveLetter + ":\"
Write-Host "Drive successfully mounted at $DriveLetter"

Write-Host "Copying test_data to the new drive..."
$TestDataPath = Join-Path -Path $PSScriptRoot -ChildPath "test_data\*"
Copy-Item -Path $TestDataPath -Destination $DriveLetter -Recurse -ErrorAction Stop

Write-Host ""
Write-Host "=========================================================="
Write-Host "DEMO DRIVE READY!"
Write-Host "1. Go to File Explorer and open $DriveLetter (SIH_DEMO)."
Write-Host "2. Show the judges the images, then DELETE them permanently (Shift+Delete)."
Write-Host "=========================================================="
Write-Host ""
Write-Host "PRESS ENTER HERE IN THIS WINDOW ONCE YOU HAVE DELETED THE FILES..."
$Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") | Out-Null

Write-Host "Unmounting the drive and preparing test.img for the recovery engine..."

$detachScript = "select vdisk file=`"$VhdPath`"`ndetach vdisk"
$detachScript | diskpart | Out-Null
Start-Sleep -Seconds 2

# Copy the VHD to test.img so the backend can read it
Copy-Item -Path $VhdPath -Destination $ImgPath -Force

Write-Host ""
Write-Host "=========================================================="
Write-Host "SUCCESS! The disk image has been finalized as test.img."
Write-Host "You can now go to the web dashboard and click 'START RAW CARVING' to recover!"
Write-Host "=========================================================="
Write-Host "Press any key to exit..."
$Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") | Out-Null
