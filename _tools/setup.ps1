Add-Type -AssemblyName PresentationFramework

function Test-RegistryValue($path, $name)
{
    $key = Get-Item -LiteralPath $path -ErrorAction SilentlyContinue
    $key -and $null -ne $key.GetValue($name, $null)
}

function Get-RegistryValue($path, $name)
{
    $key = Get-Item -LiteralPath $path -ErrorAction SilentlyContinue
    if ($key) {
        $key.GetValue($name, $null)
    }
}

function Check_Program_Installed($programName)
{
    $wmi_check = (Get-WmiObject -Class Win32_Product | sort-object Name | select Name | where { $_.Name -match "$programName”})
    return [boolean]$wmi_check
}


$scriptPath = split-path -parent $MyInvocation.MyCommand.Definition
$repoPath = split-path -parent $scriptPath
$trustedLocationPath = $repoPath

$tempPath = [System.IO.Path]::GetTempPath()

Write-Output ""
Write-Output ""
Write-Output "-------------------------------------------------------"
Write-Output "-------------------------------------------------------"
Write-Output "-------- Installing InMotion Altium libraries ---------"
Write-Output "-------------------------------------------------------"
Write-Output "-------- Allow couple of minutes to complete ----------"
Write-Output "-------------------------------------------------------"
Write-Output "-------------------------------------------------------"
Write-Output ""
Write-Output ""


if (($repoPath -match "[^\u0000-\u007F]") -or
    ($repoPath -match "\s")) {
    [System.Windows.MessageBox]::Show('Repository path ' + $repoPath + ' contains non-ascii or whitespace characters. This is not allowed!', 'Error')
    exit
}

# ----------------------- Check if altium is opened ----------------------------

$processes = Get-Process X2,DXP -ErrorAction SilentlyContinue

While($processes -ne $null) {
    [System.Windows.MessageBox]::Show('Please close Altium!', 'Warning')

    $processes = Get-Process X2,DXP -ErrorAction SilentlyContinue
}

# --------------------------- Python interpreter -------------------------------

$python_installed = Test-Path "$repoPath\_tools\python"
if (!$python_installed) {
    & "$scriptPath\install_python.ps1"
}

# --------------------- Install required python packages -----------------------

cmd.exe "/c `"`"$scriptPath\install_python_requirements.bat`" 2>&1`""

# --------------------------- Remove Access file -------------------------------

Remove-Item "$repoPath\7Sigma.mdb" -ErrorAction SilentlyContinue

# ----------------- find MS Access and setup trusted location ------------------

$access_versions = @(16, 14, 12, 10)
$found=0

for ($i=0; $i -lt $access_versions.length; $i++) {
    $now = $access_versions[$i]
    $path = 'HKCU:\Software\Microsoft\Office\' + "$now" + '.0\Access\Security\Trusted Locations'

    If (Test-Path "$path") {
        $found=1
        break
    }
}

if ($found -eq 0) {
    [System.Windows.MessageBox]::Show('Do you have MS Access installed?', 'Error')
    exit
}

Write-Output 'Found access:' $path

# ---------------------- Install Access Database Engine ------------------------

$database_engine_installed = Check_Program_Installed("Microsoft Access database engine")
if (!$database_engine_installed) {
    & "$scriptPath\install_database_engine.ps1"
}

$found = 0
$already_done = 0

for ($i=1; $i -lt 1000; $i++) {
    $path2 = $path + "\Location" + "$i"

    If (Test-Path "$path2") {
        $val = Get-ItemProperty -Path $path2 -Name "Path"

        if ($val.Path -eq $trustedLocationPath) {
            $already_done = 1
            break
        }
    } Elseif ($found -eq 0) {
        $found = 1
        $path = $path2
    }
}

if (($already_done -eq 0) -and ($found -eq 0)) {
    [System.Windows.MessageBox]::Show('Something is really (really) wrong. Run around screaming and seek for help.')
    [System.Windows.MessageBox]::Show('For real: ask GGajoch for help. Check ' + "$path" + " for trash")
    exit
}

if ($already_done -eq 0) {
    New-Item -Path $path
    New-ItemProperty -Path $path -Name "Path" -Value "$trustedLocationPath" -PropertyType String
    New-ItemProperty -Path $path -Name "AllowSubfolders" -Value 00000001 -PropertyType DWORD
} else {
    Write-Output "Trusted location already applied"
}

# -------------------- Done -----------------------------

if (!(Test-Path "HKCU:\Software\Altium")) {
    [System.Windows.MessageBox]::Show('Do you have Altium installed?', 'Error')
    exit
}

$table = Get-ChildItem "HKCU:\Software\Altium"

$db_lib_path = $repoPath + "\7Sigma.DBLib"



foreach ($row in $table) {
    $found = $row.Name.IndexOf("Altium Designer {")
    if ($found -eq -1) {
        # not altium subfolder
        continue
    }

    $reg_path = "HKCU:\Software\Altium\" + $row.PSChildName

    #found altium register path

    #try to find libraries
    $reg_path += "\DesignExplorer\Preferences\IntegratedLibrary\Loaded Libraries"

    $place = -1
    $first_free = -1
        
    if (!(Test-Path "$reg_path")) {
        New-Item -Path $reg_path
    }
        
    for ($i=0; $i -lt 100; $i++) {
            
        $val = Get-RegistryValue $reg_path "Library$i"

        if ($val -eq $db_lib_path) {
            Write-Output "File already loaded!"
            $place = $i
        } 
            
        if ($val -eq $none -and $first_free -eq -1) {
            $first_free = $i
        }
    }

    Write-Output "Adding altium $reg_path : $place,$first_free"

    if ($place -eq -1) {
        $place = $first_free
    } else {
        Remove-ItemProperty -Path $reg_path -Name "Library$place"
        Remove-ItemProperty -Path $reg_path -Name "LibraryActivated$place"
        Remove-ItemProperty -Path $reg_path -Name "LibraryRelativePath$place"
        Remove-ItemProperty -Path $reg_path -Name "LibraryViewSettings$place"
    }

    if ($place -eq -1) {
        [System.Windows.MessageBox]::Show('Something is really (really) wrong. Run around screaming and seek for help. Do you have 100 libraries installed?')
        [System.Windows.MessageBox]::Show('For real: ask GGajoch for help. Check ' + "$reg_path")
        exit
    }

    New-ItemProperty -Path $reg_path -Name "Library$place" -Value "$db_lib_path" -PropertyType String
    New-ItemProperty -Path $reg_path -Name "LibraryActivated$place" -Value "1" -PropertyType String
    New-ItemProperty -Path $reg_path -Name "LibraryRelativePath$place" -Value "$db_lib_path" -PropertyType String
    New-ItemProperty -Path $reg_path -Name "LibraryViewSettings$place" -Value "" -PropertyType String
}

# ----------------------------------- Check python ----------------------------------------

cmd.exe "/c `"`"$repoPath\check.bat`" 2>&1`""

# --------------------------------------- Done --------------------------------------------

# [System.Windows.MessageBox]::Show('Completed successfully!.')

Write-Output ""
Write-Output ""
Write-Output "-------------------------------------------------------"
Write-Output "-------------------------------------------------------"
Write-Output "---------------- Finished successfully ----------------"
Write-Output "-------------------------------------------------------"
Write-Output "-------------------------------------------------------"
Write-Output ""
Write-Output ""
