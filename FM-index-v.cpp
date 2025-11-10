// Construcción del FM index de un texto
//
// Prerrequisitos: Tener la biblioteca SDSL instalada
//
// Compilación: g++ -O3 -o fmi FM-index.cpp -lsdsl -ldivsufsort -ldivsufsort64

#include <sdsl/suffix_arrays.hpp>
#include <string>
#include <iostream>
#include <algorithm>
#include <chrono>

using namespace sdsl;
using namespace std;
using namespace std::chrono;


int main(int argc, char** argv) {
  if (argc !=  2) {
    cout << "Uso: " << argv[0] << " <archivo entrada>" << endl;
    return 1;
  }

  // Una versión compacta del suffix array, implementada en la biblioteca
  // SDSL. En este caso, utiliza un wavelet tree tipo wt_int<> como
  // building-block
  // Otros posibles building blocks son: wt_huff<>, wt_int<rrr_vector<> >, entre
  // otras combinaciones
  cout << "Construyendo el FM-index ..." << endl;
  csa_wt<wt_int<>> fm_index;
  auto inicio = high_resolution_clock::now();
  construct(fm_index, argv[1], 1);
  
  auto fin = high_resolution_clock::now();
  auto t_construccion = duration_cast<milliseconds>(fin - inicio).count();
    
  cout << "Tamaño del FM-index " << size_in_mega_bytes(fm_index) << " MB." << endl;
  cout << "Tiempo empleado: " << t_construccion << " ms" << endl;

    string patron;
    cout << "Ingrese un patrón a buscar: ";
    cin >> patron;

   // tamano del patron
    // size_t m = patron.size();

    // Buscando las ocurrencias del patrón
  inicio = high_resolution_clock::now();
  
  size_t occs = sdsl::count(fm_index, patron.begin(), patron.end());
  fin = high_resolution_clock::now();
  auto t_busqueda = duration_cast<milliseconds>(fin - inicio).count();

  cout << "Tiempo de busqueda: " << t_busqueda << " ms" << endl;
    cout << "# de ocurrencias: " << occs << endl;
    if (occs > 0) {
      cout << "Las ocurrencias comienzan en las siguientes posiciones: " << endl;
      auto posiciones = sdsl::locate(fm_index, patron.begin(), patron.end());
      sort(posiciones.begin(), posiciones.end());
      
      for (size_t i = 0; i < occs - 1; ++i) {
      	cout << posiciones[i] << ",";
      }
      cout << posiciones[occs-1] << endl;
    }
    return 0;
}
