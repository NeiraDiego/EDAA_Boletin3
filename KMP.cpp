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

    try {
        cout << "Cargando el texto en memoria..." << endl;
        auto inicio = high_resolution_clock::now();

        string txt = cargar_archivo(argv[1]);

        auto fin = high_resolution_clock::now();
        auto t_total = duration_cast<milliseconds>(fin - inicio).count();

        cout << "Texto cargado. Longitud: " << txt.size() << " caracteres\n";
        cout << "Tiempo empleado: " << t_total << " ms\n";

        string patron;
        cout << "Ingrese un patrón a buscar: ";
        cin >> patron;

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
            for (size_t i = 0; i < res.size(); i++)
                cout << res[i] << " ";
            cout << "\n";
        }

        cout << "Tiempo de búsqueda: " << t_busqueda << " ms\n";

    } catch (const exception &e) {
        cerr << "Error: " << e.what() << endl;
        return 1;
    }

    return 0;
}

