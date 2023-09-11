#!/bin/bash

# Actualizar repositorios
apt-get update

# Instalar dependencias de sistema
apt-get install -y ffmpeg

# Instalar paquetes de Python
# Leer paquetes desde el archivo packages.txt
packageFile="packages.txt"
while IFS= read -r package || [[ -n "$package" ]]; do
    echo "Instalando paquete: $package"
    python/virtual/bin/pip install "$package"
done < "$packageFile"

echo "Instalación completada."

