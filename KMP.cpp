#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <algorithm>
#include <chrono>

using namespace std;
using namespace std::chrono;

// Construye el arreglo LPS para el patrón
void constructLps(const string &pat, vector<int> &lps) {
    int m = pat.length();
    lps.assign(m, 0);  // asegurar tamaño correcto

    int len = 0;       // longitud del prefijo-sufijo más largo
    int i = 1;

    while (i < m) {
        if (pat[i] == pat[len]) {
            len++;
            lps[i] = len;
            i++;
        } else {
            if (len != 0) {
                len = lps[len - 1];
            } else {
                lps[i] = 0;
                i++;
            }
        }
    }
}

// Devuelve las posiciones donde aparece el patrón en el texto
vector<int> search(const string &pat, const string &txt) {
    int n = txt.length();
    int m = pat.length();

    vector<int> res;
    if (m == 0 || n == 0) return res;

    vector<int> lps(m);
    constructLps(pat, lps);

    int i = 0; // índice en txt
    int j = 0; // índice en pat

    while (i < n) {
        if (txt[i] == pat[j]) {
            i++;
            j++;

            if (j == m) {
                // patrón encontrado comenzando en i - j
                res.push_back(i - j);
                j = lps[j - 1];
            }
        } else {
            if (j != 0) {
                j = lps[j - 1];
            } else {
                i++;
            }
        }
    }
    return res;
}

// Carga todo el archivo de texto en un string grande
string cargar_archivo(const string &nombre_archivo) {
    ifstream in(nombre_archivo);
    if (!in) {
        throw runtime_error("No se pudo abrir el archivo: " + nombre_archivo);
    }
    return string((istreambuf_iterator<char>(in)),
                  istreambuf_iterator<char>());
}

int main(int argc, char** argv) {
    if (argc != 2) {
        cout << "Uso: " << argv[0] << " <archivo entrada>" << endl;
        return 1;
    }

    string archivo_entrada = argv[1];

    try {
        cout << "Cargando el texto en memoria..." << endl;
        auto inicio = high_resolution_clock::now();

        string txt = cargar_archivo(archivo_entrada);

        auto fin = high_resolution_clock::now();
        auto t_carga = duration_cast<milliseconds>(fin - inicio).count();

        double tamano_mb = static_cast<double>(txt.size()) / (1024.0 * 1024.0);

        cout << "Texto cargado. Longitud: " << txt.size() << " caracteres\n";
        cout << "Tiempo empleado en la carga: " << t_carga << " ms\n";
        cout << "Tamaño del texto: " << tamano_mb << " MB\n";

        // ============================
        // Log de carga: exp-KMP-carga.csv
        // columnas: archivo,tiempo_ms,tamano_mb
        // ============================
        {
            ofstream out("exp-KMP-carga.csv", ios::app);
            if (!out) {
                cerr << "Advertencia: no se pudo abrir exp-KMP-carga.csv para escribir." << endl;
            } else {
                if (out.tellp() == 0) {
                    out << "archivo,tiempo_ms,tamano_mb\n";
                }
                out << archivo_entrada << ","
                    << t_carga << ","
                    << tamano_mb << "\n";
            }
        }

        // ============================
        // Búsquedas repetidas hasta 'exit'
        // ============================

        // Abrimos una vez el archivo de búsquedas
        // columnas: archivo,patron,tiempo_ms
        ofstream out_busq("exp-KMP-busquedas.csv", ios::app);
        if (!out_busq) {
            cerr << "Advertencia: no se pudo abrir exp-KMP-busquedas.csv para escribir." << endl;
        } else {
            if (out_busq.tellp() == 0) {
                out_busq << "archivo,patron,tiempo_ms\n";
            }
        }

        while (true) {
            string patron;
            cout << "Ingrese un patrón a buscar (o 'exit' para terminar): ";
            if (!(cin >> patron)) {
                // EOF o error de entrada
                break;
            }
            if (patron == "exit") {
                cout << "Terminando búsquedas." << endl;
                break;
            }

            cout << "Buscando patrón en el texto..." << endl;
            inicio = high_resolution_clock::now();
            vector<int> res = search(patron, txt);
            fin = high_resolution_clock::now();
            auto t_busqueda = duration_cast<milliseconds>(fin - inicio).count();

            auto occs = res.size();
            cout << "# de ocurrencias: " << occs << endl;

            if (!res.empty()) {
                sort(res.begin(), res.end());
                cout << "Las ocurrencias comienzan en las siguientes posiciones:\n";
                for (size_t i = 0; i + 1 < res.size(); i++)
                    cout << res[i] << ",";
                cout << res.back() << "\n";
            }

            cout << "Tiempo de búsqueda: " << t_busqueda << " ms\n";

            // Log en CSV de búsquedas
            if (out_busq) {
                out_busq << archivo_entrada << ","
                         << patron << ","
                         << t_busqueda << "\n";
            }
        }

    } catch (const exception &e) {
        cerr << "Error: " << e.what() << endl;
        return 1;
    }

    return 0;
}
