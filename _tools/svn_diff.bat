@echo off
call "%~dp0\python\scripts\env_for_icons.bat"
"%~dp0\python\python-3.7.1\python" "%~dp0\altium_parser\diff_svn.py" %* > diff
notepad.exe diff
del diff