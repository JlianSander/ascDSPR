# Thanks to Job Vranish (https://spin.atomicobject.com/2016/08/26/makefile-c-projects/)
# and to chaselambda (https://makefiletutorial.com/)

.DELETE_ON_ERROR:

#--------------------------------------------------------------------------#
# The target name should be the name of this app, which actually should be
# the same as the name of this directory, e.g., 'parallelSolver'.
#--------------------------------------------------------------------------#

TARGET=$(shell basename "`pwd`")

#--------------------------------------------------------------------------#
# When called from the 'mkone.sh' script the 'IPASIRSOLVER' variable will be
# overwritten.  For testing purposes, we simply set it to the default CaDiCaL
# front-end.
#--------------------------------------------------------------------------#

#The number of the algorithmic shortcut to use. Read from parameter at call e.g. "make ASC=3".
ASC	?= 1

# Name of IPASIR solver (library), e.g., cadical
IPASIRSOLVER	?= cadical

# Path to the IPASIR library (e.g., points to where libcadical.a is)
IPASIRLIBDIR	?=	sat/$(IPASIRSOLVER)/build/ 

# Directory to store object files, libraries, executables, and dependencies:
BUILD_DIR := ./build

# Paths to the .cpp files
SRC				=	./src/
SRC_LOGIC		=	./src/logic/
SRC_UTIL		=	./src/util/

#Paths to the .h files
INCLUDE			=	./include/
INCLUDE_LOGIC	=	./include/logic/
INCLUDE_UTIL	=	./include/util/

#--------------------------------------------------------------------------#
# There is usually no need to change something here unless you want to force
# a specific compiler or specific compile flags.
#--------------------------------------------------------------------------#

CC	=	gcc
CFLAGS	?=	-Wall -std=c11
CXX = g++
CXXFLAGS ?= -Wall -std=c++11 -D ASC_${ASC}
LDFLAGS ?= -L$(IPASIRLIBDIR)
LDLIBS ?= -l$(IPASIRSOLVER)

# Find all the C and C++ files we want to compile
# Note the single quotes around the * expressions. The shell will incorrectly expand these otherwise, but we want to send the * directly to the find command.
SRCS := $(shell find $(SRC) -name '*.cpp' -or -name '*.c' -or -name '*.s')

# Prepends BUILD_DIR and appends .o to every src file
# As an example, ./your_dir/hello.cpp turns into ./build/./your_dir/hello.cpp.o
OBJS := $(SRCS:%=$(BUILD_DIR)/%.o)

# String substitution (suffix version without %).
# As an example, ./build/hello.cpp.o turns into ./build/hello.cpp.d
DEPS := $(OBJS:.o=.d)

# Every folder in ./include will need to be passed to GCC so that it can find header files
INC_DIRS := $(shell find $(INCLUDE) -type d)
# Add a prefix to INC_DIRS. So moduleA would become -ImoduleA. GCC understands this -I flag
INC_FLAGS := $(addprefix -I,$(INC_DIRS))
# The -MMD and -MP flags together generate Makefiles for us!
# These files will have .d instead of .o as the output.
CPPFLAGS := $(INC_FLAGS) -MMD -MP

#--------------------------------------------------------------------------#
# Here comes the real makefile part which needs to be adapted and provide
# both an 'all' and a 'clean' target. In essence, you need to provide
# linking options, which link your app to a generic 'IPASIRSOLVER'.
#--------------------------------------------------------------------------#

.PHONY:	all
all: CXXFLAGS += -DNDEBUG -O3 
all: CCFLAGS += -DNDEBUG -O3 
all: $(BUILD_DIR)/$(TARGET)

.PHONY: clean
clean: 
	rm -r $(BUILD_DIR)

.PHONY: debug
debug: CXXFLAGS += -DDEBUG -g -O0
debug: CCFLAGS += -DDEBUG -g -O0
debug: $(BUILD_DIR)/$(TARGET)

#--------------------------------------------------------------------------#
# The executable target (your program).
#--------------------------------------------------------------------------#

$(BUILD_DIR)/$(TARGET): $(OBJS)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $(OBJS) -o $@ $(LDFLAGS) $(LDLIBS)

#--------------------------------------------------------------------------#
# Local app specific rules.
#--------------------------------------------------------------------------#

# Rule to build the object file for your C++ program

# Build step for C source
$(BUILD_DIR)/%.c.o: %.c
	mkdir -p $(dir $@)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

# Build step for C++ source
$(BUILD_DIR)/%.cpp.o: %.cpp
	mkdir -p $(dir $@)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $< -o $@

# Include the .d makefiles. The - at the front suppresses the errors of missing
# Makefiles. Initially, all the .d files will be missing, and we don't want those
# errors to show up.
-include $(DEPS)