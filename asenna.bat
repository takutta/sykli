@echo off
setlocal
chcp 65001
if exist "%USERPROFILE%" (
    set docpath=%USERPROFILE%
) else (
    echo Kotihakemistoa ei löydy!
    exit /b
)

set docpath=%docpath%\Merikarhu
rd /s /q %docpath%
xcopy /E /I "%CD%\Merikarhu" %docpath%
IF ERRORLEVEL 1 (
    echo Tiedostojen kopioimisessa tapahtui virhe: %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)

cls
echo. 
echo. 
echo. 
echo                                             88  88                                 88                        
echo                                             ""  88                                 88                        
echo                                                 88                                 88                        
echo 88,dPYba,,adPYba,    ,adPPYba,  8b,dPPYba,  88  88   ,d8   ,adPPYYba,  8b,dPPYba,  88,dPPYba,   88       88  
echo 88P'   "88"    "8a  a8P_____88  88P'   "Y8  88  88 ,a8"    ""     `Y8  88P'   "Y8  88P'    "8a  88       88  
echo 88      88      88  8PP"""""""  88          88  8888[      ,adPPPPP88  88          88       88  88       88  
echo 88      88      88  "8b,   ,aa  88          88  88`"Yba,   88,    ,88  88          88       88  "8a,   ,a88  
echo 88      88      88   `"Ybbd8"'  88          88  88   `Y8a  `"8bbdP"Y8  88          88       88   `"YbbdP'Y8  
echo.
echo.

set /p userinput=Kuinka monta Titania-listaa päiväkodissanne käytetään: 
echo Kiitos!
echo.
echo Lataa...
echo.
REM Määritä Python-suoritettavan tiedoston polku
for /f "tokens=*" %%i in ('python -c "import sys; print(sys.executable)"') do set "python_exe=%%i"
IF ERRORLEVEL 1 (
    echo Python-version tarkistamisessa tapahtui virhe: %ERRORLEVEL%
    echo Olethan asentanut Pythonin?
    exit /b %ERRORLEVEL%
)
REM Määritä pikakuvakkeen tiedostopolku ja kohdekansio
set "shortcut_file=%userprofile%\Desktop\Merikarhu.lnk"

REM Luo pikakuvake
powershell.exe -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%shortcut_file%'); $s.TargetPath='%python_exe%'; $s.Arguments='\"%docpath%\\Merikarhu.py\" %userinput%'; $s.IconLocation='%docpath%\\merikarhu.ico'; $s.WorkingDirectory='%docpath%'; $s.Save()"
IF ERRORLEVEL 1 (
    echo Linkin luomisessa tapahtui virhe: %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)

cmd /c "cd /d %docpath% && python -m pip install --user --upgrade pip && pip install --user --no-warn-script-location -r requirements.txt"
IF ERRORLEVEL 1 (
    echo Pythonin pakettien asennuksessa tapahtui virhe: %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)

echo.
echo Merikarhu on asennettu.
echo Voit nyt käynnistää sen työpöydän kuvakkeesta
echo.
pause
endlocal
