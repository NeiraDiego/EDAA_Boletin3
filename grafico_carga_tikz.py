#!/usr/bin/env python3
import sys
import csv
import math
from collections import defaultdict

def leer_csv(path):
    datos = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        cols = {name: idx for idx, name in enumerate(header)}
        for row in reader:
            archivo = row[cols["archivo"]]
            tiempo_ms = float(row[cols["tiempo_ms"]])
            datos.append((archivo, tiempo_ms))
    return datos

def agrupar_promedios(datos):
    grupos = defaultdict(list)
    for archivo, tiempo in datos:
        grupos[archivo].append(tiempo)

    promedios = []
    for archivo, tiempos in grupos.items():
        n = len(tiempos)
        mean = sum(tiempos) / n
        var = sum((x - mean) ** 2 for x in tiempos) / (n - 1) if n > 1 else 0
        sd = math.sqrt(var)
        promedios.append((archivo, mean, sd))
    promedios.sort(key=lambda x: x[0])  # orden alfabético
    return promedios

def latex_escape(s):
    return s.replace('_', r'\_')

def generar_tikz(promedios, etiqueta):
    """
    Genera código LaTeX con pgfplots para graficar tiempos promedio por archivo.
    """
    lineas = []
    lineas.append(f"% ==== Gráfico de tiempos promedio ({etiqueta}) ====")
    lineas.append(r"\begin{figure}[h!]")
    lineas.append(r"\centering")
    lineas.append(r"\begin{tikzpicture}")
    lineas.append(r"\begin{axis}[")
    lineas.append(r"    ybar,")
    lineas.append(r"    bar width=12pt,")
    lineas.append(r"    ylabel={Tiempo promedio de carga (ms)},")
    lineas.append(r"    symbolic x coords={%s}," % (",".join(latex_escape(a) for a,_,_ in promedios)))
    lineas.append(r"    xtick=data,")
    lineas.append(r"    x tick label style={rotate=45, anchor=east},")
    lineas.append(r"    ymin=0,")
    lineas.append(r"    width=0.9\textwidth,")
    lineas.append(r"    height=0.45\textwidth,")
    lineas.append(r"    nodes near coords,")
    lineas.append(r"    every node near coord/.append style={font=\small, rotate=90, anchor=west},")
    lineas.append(r"    enlarge x limits=0.15,")
    lineas.append(r"]")

    # Datos
    lineas.append(r"\addplot coordinates {")
    for archivo, mean, _ in promedios:
        lineas.append(f"({latex_escape(archivo)}, {mean:.2f})")
    lineas.append(r"};")

    lineas.append(r"\end{axis}")
    lineas.append(r"\end{tikzpicture}")
    lineas.append(r"\caption{Tiempo promedio de carga/creación para %s.}" % etiqueta)
    lineas.append(r"\end{figure}")
    lineas.append("")
    return "\n".join(lineas)

def main():
    if len(sys.argv) != 3:
        print("Uso: python3 grafico_carga_tikz.py <csv> <etiqueta>")
        print("Ejemplo: python3 grafico_carga_tikz.py exp-FM-creacion.csv FM")
        sys.exit(1)

    csv_path = sys.argv[1]
    etiqueta = sys.argv[2]

    datos = leer_csv(csv_path)
    promedios = agrupar_promedios(datos)
    tikz = generar_tikz(promedios, etiqueta)

    out_file = f"grafico_carga_{etiqueta}.tex"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(tikz)

    print(f"✅ Gráfico TikZ generado: {out_file}")
    print("Inclúyelo en LaTeX con:")
    print(f"\\input{{{out_file}}}")

if __name__ == "__main__":
    main()
