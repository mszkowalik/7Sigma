Add-Type -AssemblyName PresentationFramework

$p = [Enum]::ToObject([System.Net.SecurityProtocolType], 3072);
[System.Net.ServicePointManager]::SecurityProtocol = $p;
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = { $true }

$output = [System.IO.Path]::GetTempPath()

$url = "https://download.microsoft.com/download/2/4/3/24375141-E08D-4803-AB0E-10F2E3A07AAA/AccessDatabaseEngine_X64.exe"

(New-Object Net.WebClient).DownloadFile($url, "$output\AccessDBEngine.exe")

if (!(Test-Path "$output\AccessDBEngine.exe" -PathType Leaf)) {
    [System.Windows.MessageBox]::Show('Error downloading.', 'Error')
    exit
}

(Start-Process -FilePath "$output\AccessDBEngine.exe" -ArgumentList {"/quiet"} -Pass).WaitForExit()
