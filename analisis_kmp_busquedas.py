#!/usr/bin/env python3
import csv
import math
from collections import defaultdict

INPUT_CSV = "exp-KMP-busquedas.csv"
TABLA_TEX = "tabla_kmp_busquedas.tex"
GRAFICO_TEX = "grafico_kmp_busquedas.tex"

def leer_csv(path):
    datos = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # archivo,patron,tiempo_ms
        cols = {name: idx for idx, name in enumerate(header)}
        for row in reader:
            archivo = row[cols["archivo"]]
            tiempo_ms = float(row[cols["tiempo_ms"]])
            datos.append((archivo, tiempo_ms))
    return datos

def agrupar_por_archivo(datos):
    grupos = defaultdict(list)
    for archivo, t in datos:
        grupos[archivo].append(t)
    return grupos

def stats(valores):
    n = len(valores)
    if n == 0:
        return 0, 0.0, 0.0
    media = sum(valores) / n
    if n > 1:
        var = sum((x - media) ** 2 for x in valores) / (n - 1)
        sd = math.sqrt(var)
    else:
        sd = 0.0
    return n, media, sd

def latex_escape(s):
    return s.replace("_", r"\_")

def generar_tabla_latex(grupos):
    archivos = sorted(grupos.keys())

    lineas = []
    lineas.append(r"% ==== Tabla KMP: tiempos de búsqueda por archivo ====")
    lineas.append(r"\begin{table}[h!]")
    lineas.append(r"\centering")
    lineas.append(r"\begin{tabular}{lrrr}")
    lineas.append(r"\hline")
    lineas.append(r"Archivo & Reps & $\overline{t}$ (ms) & $\sigma$ (ms) \\")
    lineas.append(r"\hline")

    for archivo in archivos:
        tiempos = grupos[archivo]
        n, media, sd = stats(tiempos)
        lineas.append(
            f"{latex_escape(archivo)} & {n} & {media:.3f} & {sd:.3f} \\\\"
        )

    lineas.append(r"\hline")
    lineas.append(r"\end{tabular}")
    lineas.append(r"\caption{Tiempo promedio y desviación estándar de las búsquedas con KMP por archivo.}")
    lineas.append(r"\end{table}")
    lineas.append("")
    return "\n".join(lineas)

def generar_grafico_tikz(grupos):
    archivos = sorted(grupos.keys())
    promedios = []
    for archivo in archivos:
        tiempos = grupos[archivo]
        _, media, _ = stats(tiempos)
        promedios.append((archivo, media))

    lineas = []
    lineas.append(r"% ==== Gráfico KMP: tiempos promedio de búsqueda por archivo ====")
    lineas.append(r"\begin{figure}[h!]")
    lineas.append(r"\centering")
    lineas.append(r"\begin{tikzpicture}")
    lineas.append(r"\begin{axis}[")
    lineas.append(r"    ybar,")
    lineas.append(r"    bar width=12pt,")
    lineas.append(r"    ylabel={Tiempo promedio de búsqueda (ms)},")
    lineas.append(
        r"    symbolic x coords={%s}," %
        ",".join(latex_escape(a) for a, _ in promedios)
    )
    lineas.append(r"    xtick=data,")
    lineas.append(r"    x tick label style={rotate=45, anchor=east},")
    lineas.append(r"    ymin=0,")
    lineas.append(r"    width=0.9\textwidth,")
    lineas.append(r"    height=0.45\textwidth,")
    lineas.append(r"    nodes near coords,")
    lineas.append(r"    every node near coord/.append style={font=\small, rotate=90, anchor=west},")
    lineas.append(r"    enlarge x limits=0.15,")
    lineas.append(r"]")

    lineas.append(r"\addplot coordinates {")
    for archivo, media in promedios:
        lineas.append(f"({latex_escape(archivo)}, {media:.3f})")
    lineas.append(r"};")

    lineas.append(r"\end{axis}")
    lineas.append(r"\end{tikzpicture}")
    lineas.append(r"\caption{Tiempo promedio de búsqueda con KMP por archivo.}")
    lineas.append(r"\end{figure}")
    lineas.append("")
    return "\n".join(lineas)

def main():
    datos = leer_csv(INPUT_CSV)
    grupos = agrupar_por_archivo(datos)

    tabla_tex = generar_tabla_latex(grupos)
    with open(TABLA_TEX, "w", encoding="utf-8") as f:
        f.write(tabla_tex)
    print(f"✅ Tabla LaTeX guardada en: {TABLA_TEX}")

    grafico_tex = generar_grafico_tikz(grupos)
    with open(GRAFICO_TEX, "w", encoding="utf-8") as f:
        f.write(grafico_tex)
    print(f"✅ Gráfico TikZ guardado en: {GRAFICO_TEX}")
    print(r"Incluye en tu .tex con: \input{tabla_kmp_busquedas} y \input{grafico_kmp_busquedas}")

if __name__ == "__main__":
    main()
