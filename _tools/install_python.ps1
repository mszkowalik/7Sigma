Add-Type -AssemblyName PresentationFramework

$p = [Enum]::ToObject([System.Net.SecurityProtocolType], 3072);
[System.Net.ServicePointManager]::SecurityProtocol = $p;
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }

$output = [System.IO.Path]::GetTempPath()

$url = "https://github.com/winpython/winpython/releases/download/1.11.20181031/Winpython32-3.7.1.0Zero.exe"

(New-Object Net.WebClient).DownloadFile($url, "$output\WinPython.exe") 

if (!(Test-Path "$output\WinPython.exe" -PathType Leaf)) {
    [System.Windows.MessageBox]::Show('Error downloading.', 'Error')
    exit
}

$scriptPath = split-path -parent $MyInvocation.MyCommand.Definition

$args = "/VERYSILENT /DIR=`"$scriptPath\python`""
(Start-Process -FilePath "$output\WinPython.exe" -ArgumentList $args -Pass).WaitForExit()
