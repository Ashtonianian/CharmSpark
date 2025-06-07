# Set paths
$UE_PATH = "C:\Program Files\Epic Games\UE_5.5\Engine\Binaries\Win64\UnrealEditor.exe"
$UPROJECT = "C:\Users\mikwa\OneDrive\Documents\Unreal Projects\CharmSpark\CharmSpark.uproject"
$BUILD_SCRIPT = "C:\Program Files\Epic Games\UE_5.5\Engine\Build\BatchFiles\Build.bat"

Get-Process UE4Editor -ErrorAction SilentlyContinue | Stop-Process -Force
Start-Sleep -Seconds 2


# Step 1: Build
& "$BUILD_SCRIPT" CharmSparkEditor Win64 Development "$UPROJECT"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed." -ForegroundColor Red
    exit 1
}

# Step 2: Launch UE editor
Start-Process "`"$UE_PATH`"" "`"$UPROJECT`""
