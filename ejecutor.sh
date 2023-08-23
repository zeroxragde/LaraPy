#!/bin/bash
# Ruta al script de Python que deseas ejecutar
ruta_script="main.py"

# Ruta al entorno virtual de Python
ruta_entorno_virtual="/home/ragde/python/virtual/bin/activate"

# Verificar si se proporcionó el argumento --reset o -r
if [[ $1 == "--reset" || $1 == "-r" ]]; then
    # Detener el proceso de Python si está en ejecución
    pkill -f "$ruta_script"

    # Esperar unos segundos para asegurar que el proceso se haya detenido
    sleep 2
fi

# Verificar si se proporcionó el argumento --stop o -s
if [[ $1 == "--stop" || $1 == "-s" ]]; then
    # Detener el proceso de Python si está en ejecución
    pkill -f "$ruta_script"
    echo "El script ha sido detenido."
    exit 0
fi

# Obtener la ruta absoluta del script
ruta_abs_script=$(realpath "$ruta_script")

# Obtener la carpeta del script
carpeta_script=$(dirname "$ruta_abs_script")

# Verificar si el script está en ejecución
if pgrep -f "$ruta_abs_script" >/dev/null; then
    echo "El script ya está en ejecución."
else
    echo "El script no está en ejecución. Iniciando..."
    source "$ruta_entorno_virtual"
    cd "$carpeta_script"
    nohup python3 "$ruta_abs_script" > api.log 2>&1 &
fi