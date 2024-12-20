CC = gcc
CFLAGS= -Wall -fPIC -O2
LIBS = -lm

SRC_DIR = Predator_Prey
BIN_DIR = bin
OUTPUTS_DIR = Outputs

# Targets
SHARED_LIB = $(BIN_DIR)/clib.so
EXECUTABLE = $(BIN_DIR)/calcvalcstes
PYTHON_SCRIPT = $(SRC_DIR)/main.py

# Object files and dependencies
OBJ = $(BIN_DIR)/functions.o


# Default target: build clib.so and .exe
all: $(BIN_DIR) $(OUTPUTS_DIR) $(SHARED_LIB) $(EXECUTABLE)

# Ensure bin and outputs directories exist
$(BIN_DIR):
	@mkdir -p $(BIN_DIR)
	@echo "Created $(BIN_DIR) directory."

$(OUTPUTS_DIR):
	@mkdir -p $(OUTPUTS_DIR)
	@echo "Created $(OUTPUTS_DIR) directory."




# Compile functions.c into clib.so
$(BIN_DIR)/functions.o: $(SRC_DIR)/functions.c $(DEPS)
	$(CC) $(CFLAGS) -o $@ -c $<
	@echo "Compiled: $< -> $@"

$(SHARED_LIB): $(OBJ)
	$(CC) -shared -o $@ $^
	@echo "Built shared library: $@"

# Compile Calcvalcstes.c into a .exe
$(EXECUTABLE): $(SRC_DIR)/Calcvalcstes.c
	$(CC) $(CFLAGS) -o $@ $< $(LIBS)
	@echo "Built executable: $@"

# Clean
clean:
	@rm -f $(BIN_DIR)/*.o $(BIN_DIR)/*.so $(BIN_DIR)/*calcvalcstes
	@rm -rf $(OUTPUTS_DIR)/*
	@echo "Cleaned build artifacts and outputs"



# Run Both Codes 
run: all
	@echo "Running Calcvalcstes..."
	./$(EXECUTABLE)
	@echo "Running main.py..."
	python3 $(PYTHON_SCRIPT)
