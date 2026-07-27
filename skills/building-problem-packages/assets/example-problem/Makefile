CXX = g++
CXX_OPTIONS = -std=c++23 -O2
SRC_DIR = src
BUILD_DIR ?= build
DATA_DIR = $(BUILD_DIR)/data

STD = $(BUILD_DIR)/std
GEN = $(BUILD_DIR)/gen
VAL = $(BUILD_DIR)/val
DOCS = $(patsubst %,$(BUILD_DIR)/%,std.cpp gen.cpp val.cpp statement.md solution.md)
TEST_POINTS := 

# Add problem-specific test points with BUILD_SINGLE_POINT or BUILD_SUBTASK.
# $(1): test-point prefix
# $(2): generator arguments
define BUILD_SINGLE_POINT
TEST_POINTS += $(DATA_DIR)/$(1).in $(DATA_DIR)/$(1).ans

$(DATA_DIR)/$(1).in: $(GEN) $(VAL) | $(DATA_DIR)
	$(GEN) $(shell echo $(1) | md5sum | cut -d ' ' -f 1) $(2) > $$@
	$(VAL) < $$@

$(DATA_DIR)/$(1).ans: $(DATA_DIR)/$(1).in $(STD) | $(DATA_DIR)
	$(STD) < $$< > $$@
endef

# $(1): test-point prefix
# $(2): number of test cases
# $(3): generator arguments
define BUILD_SUBTASK
$(foreach i,$(shell seq 1 $(2)),$(eval $(call BUILD_SINGLE_POINT,$(1)-$(i),$(3))))
endef

.DEFAULT_GOAL := all

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(DATA_DIR):
	mkdir -p $(DATA_DIR)

$(DOCS): $(BUILD_DIR)/%: $(SRC_DIR)/% | $(BUILD_DIR)
	cp $< $@

$(GEN) $(STD) $(VAL): $(BUILD_DIR)/%: $(SRC_DIR)/%.cpp | $(BUILD_DIR)
	$(CXX) $(CXX_OPTIONS) $< -o $@

all: $(TEST_POINTS) $(DOCS) $(GEN) $(STD) $(VAL)
clean:
	rm -rf $(BUILD_DIR)/*

.PHONY: all clean
.DELETE_ON_ERROR: $(TEST_POINTS)
