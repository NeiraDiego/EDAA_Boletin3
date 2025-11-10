#!/usr/bin/env bash
#
# Script: experimentos_FM.sh
# Ejecuta automáticamente el programa FM (FM-index)
# sobre múltiples archivos y patrones, con repeticiones.
# Cada ejecución se lanza con nohup + nice en background.
#

# Ejecutable
FM_BIN=./FM

# Archivos a procesar
FILES=(
    "english.50MB"
    "english.200MB"
    "english.100MB"
    "english.1024MB_clean.txt"
)

# Patrones a buscar
PATTERNS=(
    "Moscow"
    "English"
    "XDdabsdrsaf"
    "Storm"
    "Government"
    "Salvation"
    "Revolution"
    "Power"
    "Congress"
)
# Número de repeticiones
REPEATS=5

# Nombre del archivo de salida de nohup
LOGFILE="nohup_FM_experimentos.out"

# Limpia logs previos (opcional)
rm -f exp-FM-creacion.csv exp-FM-busquedas.csv "$LOGFILE"

# Inicia ejecución
echo ">>> Iniciando experimentos en segundo plano..."
echo "Salida completa en: $LOGFILE"
echo "Inicio: $(date)" >> "$LOGFILE"

for file in "${FILES[@]}"; do
    for (( r=1; r<=REPEATS; r++ )); do
        echo "Lanzando experimento $r para archivo $file..." | tee -a "$LOGFILE"

        # Crea un input temporal para el programa
        INPUT_CMD=$(mktemp)
        {
            for pat in "${PATTERNS[@]}"; do
                echo "$pat"
            done
            echo "exit"
        } > "$INPUT_CMD"

        # Ejecuta el programa en background con prioridad reducida
        nohup "$FM_BIN" "$file" < "$INPUT_CMD" >> "$LOGFILE" 2>&1 &
        
        rm -f "$INPUT_CMD"  # limpiar archivo temporal
    done
done

echo ">>> Todos los experimentos se están ejecutando en background."
echo "Puedes monitorearlos con: tail -f $LOGFILE"
