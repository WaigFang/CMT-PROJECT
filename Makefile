CC = gcc
CFLAGS= -Wall -fPIC -O2
LIBS = -lm

SRC_DIR = Predator_Prey
BIN_DIR = bin

# Targets
SHARED_LIB = $(BIN_DIR)/clib.so
EXECUTABLE = $(BIN_DIR)/calcvalcstes
PYTHON_SCRIPT = $(SRC_DIR)/main.py

# Object files and dependencies
OBJ = $(BIN_DIR)/functions.o
DEPS = $(SRC_DIR)/functions.h

# Default target: build clib.so and .exe
all: $(SHARED_LIB) $(EXECUTABLE)

# Compile functions.c into clib.so
$(BIN_DIR)/functions.o: $(SRC_DIR)/functions.c $(DEPS)
	$(CC) $(CFLAGS) -o $@ -c $<

$(SHARED_LIB): $(OBJ)
	$(CC) -shared -o $@ $^

# Compile Calcvalcstes.c into a .exe
$(EXECUTABLE): $(SRC_DIR)/Calcvalcstes.c
	$(CC) $(CFLAGS) -o $@ $< $(LIBS)

# Clean
clean:
	rm -f $(BIN_DIR)/*.o $(BIN_DIR)/*.so $(BIN_DIR)/*calcvalcstes
	rmdir $(BIN_DIR)

# Create bin directory if it doesn't exist 
$(shell mkdir -p $(BIN_DIR))

# Run Both Codes 
run: all
	@echo "Running Calcvalcstes..."
	./$(EXECUTABLE)
	@echo "Running main.py..."
	python3 $(PYTHON_SCRIPT)
