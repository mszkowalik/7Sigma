@echo off

set /p Build=<"%~dp0\_tools\_version.txt"

if exist "%~dp0\_tools\_version_now.txt" (
  set /p Now=<"%~dp0\_tools\_version_now.txt"
) else (
  set Now=0
)


if %Build% GTR %Now% (
  copy "%~dp0\_tools\_version.txt" "%~dp0\_tools\_version_now.txt"
  %~dp0\setup.bat
) else (
  copy _export\__template_7Sigma.MDB 7Sigma.MDB
  call "%~dp0\_tools\run_python.bat" ".\_tools\import_csv.py"
)