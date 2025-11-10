# Makefile para compilar KMP y FM-index
# Uso:
#   make KMP          -> compila KMP.cpp -> ejecutable KMP
#   make FM           -> compila FM-index.cpp -> ejecutable FM
#   make all          -> compila ambos
#   make clean        -> elimina binarios
#   make runKMP FILE=archivo.txt -> ejecuta KMP
#   make runFM FILE=archivo.txt  -> ejecuta FM

# Compilador
CXX = g++

# Flags generales
CXXFLAGS = -Wall -Wextra

# =========================
#  PROGRAMA 1: KMP
# =========================
KMP_SRC = KMP.cpp
KMP_OUT = KMP
KMP_FLAGS = -std=c++17 -O2

# =========================
#  PROGRAMA 2: FM-INDEX
# =========================
FM_SRC = FM-index.cpp
FM_OUT = FM
FM_FLAGS = -std=c++11 -O3 -DNDEBUG -I ~/include -L ~/lib
FM_LIBS = -lsdsl -ldivsufsort -ldivsufsort64

# =========================
#  REGLAS
# =========================

all: KMP FM

# Compilar KMP
KMP: $(KMP_SRC)
	$(CXX) $(CXXFLAGS) $(KMP_FLAGS) $(KMP_SRC) -o $(KMP_OUT)

# Compilar FM-index
FM: $(FM_SRC)
	$(CXX) $(CXXFLAGS) $(FM_FLAGS) $(FM_SRC) -o $(FM_OUT) $(FM_LIBS)

# Ejecutar KMP con archivo
runKMP: KMP
	./$(KMP_OUT) $(FILE)

# Ejecutar FM con archivo
runFM: FM
	./$(FM_OUT) $(FILE)

# Limpiar
clean:
	rm -f $(KMP_OUT) $(FM_OUT)

