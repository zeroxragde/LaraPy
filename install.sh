@echo off

REM Cambiar al directorio del script
cd %~dp0

REM Buscar la carpeta venv en el directorio actual
for /d %%d in (*) do (
    if "%%d"=="venv" (
        echo Carpeta venv encontrada en el directorio actual.
        set "venvPath=%%~dpdvenv\"
    )
)

REM Verificar si se encontró la carpeta venv
if defined venvPath (
    echo Usando la carpeta venv encontrada en: %venvPath%
    echo.

    REM Instalar paquetes de Python 2
    echo Actualizar pip
    "%venvPath%\Scripts\python.exe" -m pip install --upgrade pip

    REM Leer paquetes desde el archivo packages.txt
    set "packageFile=packages.txt"
    for /f "usebackq tokens=*" %%p in ("%packageFile%") do (
        echo Instalando paquete: %%p
        %venvPath%Scripts\pip.exe install %%p
    )
) else (
    echo Carpeta venv no encontrada en el directorio actual.
)

pause
