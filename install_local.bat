@echo off

REM Instalar paquetes de Python

@echo off
pip install --upgrade pip
python.exe -m pip install --upgrade pip
REM Leer paquetes desde el archivo packages.txt
set "packageFile=packages.txt"
for /f "usebackq tokens=*" %%p in ("%packageFile%") do (
    echo Instalando paquete: %%p
     pip install %%p
)
pause