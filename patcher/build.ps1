# Baut D1AL-ogue_DE_Patcher.exe (eigenständig, kein Python nötig) und das Release-ZIP.
# Aufruf (im Repo-Hauptordner):  powershell -ExecutionPolicy Bypass -File patcher\build.ps1
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

if (-not (Test-Path ".venv")) { python -m venv .venv }
& .venv\Scripts\python -m pip install -q -r patcher\requirements.txt

$version = (& .venv\Scripts\python -c "import json;print(json.load(open('translation/D1AL-ogue_DE.json',encoding='utf-8'))['version'])").Trim()

& .venv\Scripts\pyinstaller --noconfirm --clean --onefile --console `
    --name D1AL-ogue_DE_Patcher `
    --add-data "$root\translation\D1AL-ogue_DE.json;." `
    --collect-all UnityPy `
    --distpath "$root\dist" --workpath "$root\build" --specpath "$root\build" `
    "$root\patcher\d1al_de_patcher.py"
if ($LASTEXITCODE -ne 0) { throw "PyInstaller fehlgeschlagen" }

$pkg = "dist\D1AL-ogue_DE_v$version"
Remove-Item -Recurse -Force $pkg, "$pkg.zip" -ErrorAction SilentlyContinue
New-Item -ItemType Directory $pkg | Out-Null
Copy-Item dist\D1AL-ogue_DE_Patcher.exe, translation\D1AL-ogue_DE.json, patcher\LIESMICH.txt $pkg
Compress-Archive -Path "$pkg\*" -DestinationPath "$pkg.zip"
Write-Host "Fertig: $pkg.zip"
