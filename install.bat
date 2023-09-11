@echo off

REM Instalar paquetes de Python 2

@echo off
echo Actualizar pip
"C:\Users\Ragde\PycharmProjects\DebugLarapy\venv\Scripts\pip.exe" install --upgrade pip
REM Leer paquetes desde el archivo packages.txt
set "packageFile=packages.txt"
for /f "usebackq tokens=*" %%p in ("%packageFile%") do (
    echo Instalando paquete: %%p
     "C:\Users\Ragde\PycharmProjects\DebugLarapy\venv\Scripts\pip.exe" install %%p
)
pause