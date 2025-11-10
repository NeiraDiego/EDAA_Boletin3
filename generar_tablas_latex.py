#!/usr/bin/env python3
import sys
import csv
import math
from collections import defaultdict

def leer_csv(path):
    """Lee el CSV (archivo, tiempo_ms, tamano_mb)"""
    datos = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        cols = {name: idx for idx, name in enumerate(header)}
        for row in reader:
            archivo = row[cols["archivo"]]
            tiempo_ms = float(row[cols["tiempo_ms"]])
            tam_mb = float(row[cols["tamano_mb"]])
            datos.append((archivo, tiempo_ms, tam_mb))
    return datos

def agrupar_por_archivo(datos):
    grupos = defaultdict(lambda: {"tiempos": [], "tamanos": []})
    for archivo, t_ms, tam_mb in datos:
        grupos[archivo]["tiempos"].append(t_ms)
        grupos[archivo]["tamanos"].append(tam_mb)
    return grupos

def stats(valores):
    n = len(valores)
    if n == 0:
        return 0, 0.0, 0.0
    mean = sum(valores) / n
    if n > 1:
        var = sum((x - mean)**2 for x in valores) / (n - 1)
        sd = math.sqrt(var)
    else:
        sd = 0.0
    return n, mean, sd

def latex_escape(s):
    """Evita errores con guiones bajos"""
    return s.replace('_', r'\_')

def generar_tablas_latex(grupos, etiqueta):
    archivos = sorted(grupos.keys())

    lineas = []
    lineas.append(f"% ==== Tablas LaTeX para {etiqueta} ====")

    # Tabla 1: archivo vs tamaño
    lineas.append(r"\subsection{Tamaño de los archivos (%s)}" % etiqueta)
    lineas.append(r"\begin{tabular}{lr}")
    lineas.append(r"\hline")
    lineas.append(r"Archivo & Tamaño (MB) \\")
    lineas.append(r"\hline")
    for archivo in archivos:
        tamanos = grupos[archivo]["tamanos"]
        tam_prom = sum(tamanos) / len(tamanos)
        lineas.append(f"{latex_escape(archivo)} & {tam_prom:.3f} \\\\")
    lineas.append(r"\hline")
    lineas.append(r"\end{tabular}")
    lineas.append("")

    # Tabla 2: archivo vs promedio tiempo + std
    lineas.append(r"\subsection{Tiempo promedio de carga (%s)}" % etiqueta)
    lineas.append(r"\begin{tabular}{lrrr}")
    lineas.append(r"\hline")
    lineas.append(r"Archivo & Reps & $\overline{t}$ (ms) & $\sigma$ (ms) \\")
    lineas.append(r"\hline")
    for archivo in archivos:
        tiempos = grupos[archivo]["tiempos"]
        n, mean, sd = stats(tiempos)
        lineas.append(f"{latex_escape(archivo)} & {n} & {mean:.2f} & {sd:.2f} \\\\")
    lineas.append(r"\hline")
    lineas.append(r"\end{tabular}")
    lineas.append("")

    return "\n".join(lineas)

def main():
    if len(sys.argv) != 3:
        print("Uso: python3 analisis_carga_tablas.py <csv> <etiqueta>")
        print("Ejemplo: python3 analisis_carga_tablas.py exp-FM-creacion.csv FM")
        sys.exit(1)

    csv_path = sys.argv[1]
    etiqueta = sys.argv[2]

    datos = leer_csv(csv_path)
    grupos = agrupar_por_archivo(datos)

    tablas_latex = generar_tablas_latex(grupos, etiqueta)
    tex_filename = f"tablas_carga_{etiqueta}.tex"

    with open(tex_filename, "w", encoding="utf-8") as f:
        f.write(tablas_latex)

    print(f"✅ Tablas LaTeX generadas en: {tex_filename}")

if __name__ == "__main__":
    main()

