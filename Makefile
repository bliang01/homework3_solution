# compiler settings
CC=gcc-5
CFLAGS=-c -Wall -fPIC -fopenmp -lm
LDFLAGS=--shared -fopenmp

# target
LIBTARGET=libhomework3.so

# directories
SRC=src

LIB=lib
INCLUDE=include

# sources
LIBSOURCES=$(SRC)/integrate.c
LIBOBJECTS=$(LIBSOURCES:.c=.o)

.PHONY: all lib clean

default: all

all: lib

lib: $(LIBTARGET)

test: lib
	python test_homework3.py

$(LIBTARGET): $(LIBOBJECTS)
	$(CC) $(LDFLAGS) $(LIBOBJECTS) -o $(LIB)/$(LIBTARGET)

%.o : %.c
	$(CC) -I$(INCLUDE) $(CFLAGS) $< -o $@

clean:
	@rm -fr $(SRC)/*.o

clobber: clean
	@rm -fd $(LIB)/*.so
