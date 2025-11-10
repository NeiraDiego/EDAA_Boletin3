#!/usr/bin/env python3
import csv
import os
import math
from collections import defaultdict

# ============ UTILIDADES ============

def leer_csv(path):
    if not os.path.exists(path):
        print(f"% Archivo no encontrado: {path}")
        return []
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def stats(valores):
    n = len(valores)
    if n == 0:
        return 0, 0.0, 0.0, 0.0, 0.0
    mean = sum(valores) / n
    if n > 1:
        var = sum((x - mean) ** 2 for x in valores) / (n - 1)
        sd = math.sqrt(var)
    else:
        sd = 0.0
    return n, mean, sd, min(valores), max(valores)

def num(x, d=2): return f"{x:.{d}f}"
def esc(s): return s.replace('_', r'\_')

# ============ GENERADORES DE TABLAS ============

def tabla_fm_creacion():
    rows = leer_csv("exp-FM-creacion.csv")
    if not rows: return ""

    grupos = defaultdict(list)
    for r in rows:
        grupos[r["archivo"]].append((float(r["tiempo_ms"]), float(r["tamano_mb"])))

    out = []
    out.append(r"\subsection{Construcción del FM-index}")
    out.append(r"\begin{tabular}{lrrrrr}")
    out.append(r"\hline")
    out.append(r"Archivo & Reps & $\overline{t}$ (ms) & $\sigma$ & $t_{\min}$ & $t_{\max}$ \\")
    out.append(r"\hline")

    for archivo, datos in grupos.items():
        tiempos = [t for t, _ in datos]
        tamanos = [mb for _, mb in datos]
        n, mean, sd, tmin, tmax = stats(tiempos)
        tam = sum(tamanos)/len(tamanos)
        out.append(f"{esc(archivo)} & {n} & {num(mean)} & {num(sd)} & {num(tmin)} & {num(tmax)} \\\\ % {num(tam,3)} MB")

    out.append(r"\hline")
    out.append(r"\end{tabular}")
    return "\n".join(out) + "\n\n"

def tabla_fm_busquedas():
    rows = leer_csv("exp-FM-busquedas.csv")
    if not rows: return ""
    grupos = defaultdict(list)
    for r in rows:
        grupos[(r["archivo"], r["patron"])].append((float(r["tiempo_ms"]), float(r["ocurrencias"])))

    out = []
    out.append(r"\subsection{Búsquedas con FM-index}")
    out.append(r"\begin{tabular}{llrrrrr}")
    out.append(r"\hline")
    out.append(r"Archivo & Patrón & Reps & $\overline{t}$ (ms) & $\sigma$ & $t_{\min}$ & Ocurrencias \\")
    out.append(r"\hline")

    for (archivo, patron), datos in grupos.items():
        tiempos = [t for t, _ in datos]
        occs = [o for _, o in datos]
        n, mean, sd, tmin, tmax = stats(tiempos)
        occ_prom = sum(occs)/len(occs)
        out.append(f"{esc(archivo)} & {esc(patron)} & {n} & {num(mean,3)} & {num(sd,3)} & {num(tmin,3)} & {num(occ_prom,0)} \\\\")

    out.append(r"\hline")
    out.append(r"\end{tabular}")
    return "\n".join(out) + "\n\n"

def tabla_kmp_carga():
    rows = leer_csv("exp-KMP-carga.csv")
    if not rows: return ""
    grupos = defaultdict(list)
    for r in rows:
        grupos[r["archivo"]].append((float(r["tiempo_ms"]), float(r["tamano_mb"])))

    out = []
    out.append(r"\subsection{Carga del texto para KMP}")
    out.append(r"\begin{tabular}{lrrrrr}")
    out.append(r"\hline")
    out.append(r"Archivo & Reps & $\overline{t}$ (ms) & $\sigma$ & $t_{\min}$ & $t_{\max}$ \\")
    out.append(r"\hline")

    for archivo, datos in grupos.items():
        tiempos = [t for t, _ in datos]
        tamanos = [mb for _, mb in datos]
        n, mean, sd, tmin, tmax = stats(tiempos)
        tam = sum(tamanos)/len(tamanos)
        out.append(f"{esc(archivo)} & {n} & {num(mean)} & {num(sd)} & {num(tmin)} & {num(tmax)} \\\\ % {num(tam,3)} MB")

    out.append(r"\hline")
    out.append(r"\end{tabular}")
    return "\n".join(out) + "\n\n"

def tabla_kmp_busquedas():
    rows = leer_csv("exp-KMP-busquedas.csv")
    if not rows: return ""
    grupos = defaultdict(list)
    for r in rows:
        grupos[(r["archivo"], r["patron"])].append(float(r["tiempo_ms"]))

    out = []
    out.append(r"\subsection{Búsquedas con KMP}")
    out.append(r"\begin{tabular}{llrrrr}")
    out.append(r"\hline")
    out.append(r"Archivo & Patrón & Reps & $\overline{t}$ (ms) & $\sigma$ & $t_{\min}$ \\")
    out.append(r"\hline")

    for (archivo, patron), tiempos in grupos.items():
        n, mean, sd, tmin, tmax = stats(tiempos)
        out.append(f"{esc(archivo)} & {esc(patron)} & {n} & {num(mean,3)} & {num(sd,3)} & {num(tmin,3)} \\\\")

    out.append(r"\hline")
    out.append(r"\end{tabular}")
    return "\n".join(out) + "\n\n"

# ============ MAIN ============

if __name__ == "__main__":
    contenido = []
    contenido.append(r"\section{Resultados del FM-index}")
    contenido.append(tabla_fm_creacion())
    contenido.append(tabla_fm_busquedas())
    contenido.append(r"\section{Resultados del KMP}")
    contenido.append(tabla_kmp_carga())
    contenido.append(tabla_kmp_busquedas())

    tex = "\n".join(c for c in contenido if c.strip())

    with open("resultados_experimentos.tex", "w", encoding="utf-8") as f:
        f.write(tex)

    print("✅ Archivo generado: resultados_experimentos.tex")

