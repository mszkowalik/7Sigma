@echo off
call "%~dp0\_tools\python\scripts\env_for_icons.bat"
"%~dp0\_tools\python\python-3.7.1\python" "%~dp0\_tools\altium_parser\open_suppliers.py"