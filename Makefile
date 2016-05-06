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
CTESTSSOURCES=ctests/*.c
CTESTPROGRAMS=$(CTESTSOURCES:.c:.out)

.PHONY: all lib clean

default: all

all: lib

lib: $(LIBTARGET)

test: lib
	python test_homework3.py

#
#     $ make example.out
#
# copy format if you want to write more ctest files
#
example.out: ctests/example.c
	$(CC) -Wl,-rpath,./lib -I$(INCLUDE) -Llib -lhomework3 -lm -fopenmp $< -o $@

$(LIBTARGET): $(LIBOBJECTS)
	$(CC) $(LDFLAGS) $(LIBOBJECTS) -o $(LIB)/$(LIBTARGET)

%.o : %.c
	$(CC) -I$(INCLUDE) $(CFLAGS) $< -o $@

clean:
	@rm -fr $(SRC)/*.o

clobber: clean
	@rm -fd $(LIB)/*.so
