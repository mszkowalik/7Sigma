@rem %TEMP%\altiumdb_log.txt
@rem %TEMP%\altiumdb_log1.txt
@rem %TEMP%\altiumdb_log2.txt

xcopy ".\_tools\hooks" ".\.git\hooks"

powershell.exe -noprofile -executionpolicy bypass ".\_tools\setup.ps1 2>&1 | tee %TEMP%\altiumdb_log1.txt"

copy %TEMP%\altiumdb_log1.txt+%TEMP%\altiumdb_log2.txt %TEMP%\altiumdb_log.txt