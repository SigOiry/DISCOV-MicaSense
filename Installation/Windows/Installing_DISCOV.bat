@echo off
setlocal enabledelayedexpansion

REM Check if Conda is already installed
where conda >nul 2>&1
if %ERRORLEVEL%==0 (
    echo Conda is already installed. Skipping installation.
    pause
    
) else (
REM Detect architecture
	if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
		set DOWNLOAD=https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
	) else (
		set DOWNLOAD=https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86.exe
	)

	REM Download Miniconda installer
	echo Downloading Miniconda installer...
	powershell -Command "Invoke-WebRequest -Uri !DOWNLOAD! -OutFile MinicondaInstaller.exe"

	REM Run Miniconda installer
	echo Running Miniconda installer...
	start /wait MinicondaInstaller.exe /S /D=%USERPROFILE%\Miniconda3

	REM Final message
	echo Miniconda installed! Please restart your terminal.
	pause
)


@echo off
echo Creating Conda environment from DISCOV_env.yml...

REM Ensure Conda is initialized
call "%USERPROFILE%\Miniconda3\condabin\conda.bat" init

REM Create the environment from the YAML file
call "%USERPROFILE%\Miniconda3\condabin\conda.bat" env create --file DISCOV_env.yml

echo Environment created successfully from DISCOV_env.yml!
pause
