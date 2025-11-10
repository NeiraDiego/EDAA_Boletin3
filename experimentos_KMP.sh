#!/usr/bin/env bash
#
# Script: experimentos_KMP.sh
# Ejecuta el programa KMP sobre varios archivos y varios patrones,
# repitiendo cada experimento completo 5 veces.

KMP_BIN=./KMP   # ejecutable compilado desde KMP.cpp

# Archivos de texto a usar (ajusta estos nombres)
FILES=(
    "english.50MB"
    "english.200MB"
    "english.100MB"
    "english.1024MB_clean.txt"
)

# Patrones a buscar (ajusta según tu experimento)
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
    "aksld;fjaslbk" 
    "asklbkashhvcsd"
)

# Número de repeticiones de cada experimento completo
REPEATS=5

# Opcional: limpiar CSVs anteriores al empezar
rm -f exp-KMP-carga.csv exp-KMP-busquedas.csv
touch exp-KMP-carga.csv
touch exp-KMP-busquedas.csv

for file in "${FILES[@]}"; do
    echo ">>> Archivo: $file"
    for (( r=1; r<=REPEATS; r++ )); do
        echo "  - Ejecución $r / $REPEATS para $file"

        # Creamos un input temporal con todos los patrones + 'exit'
        INPUT_CMD=$(mktemp)
        {
            for pat in "${PATTERNS[@]}"; do
                echo "$pat"
            done
            echo "exit"
        } > "$INPUT_CMD"

         # Ejecutamos KMP de forma secuencial (esperamos a que termine) 
         "$KMP_BIN" "$file" < "$INPUT_CMD"

        rm -f "$INPUT_CMD"
    done
done

echo "Experimentos de KMP terminados."
echo "Revisa exp-KMP-carga.csv y exp-KMP-busquedas.csv"

