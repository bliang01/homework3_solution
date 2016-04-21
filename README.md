# Homework #3

Homework #3 will test you on writing OpenMP code. 

Repository layout:

* `homework3/`:

  Python wrapper of C library. The functions defined here allow you to use your
  C code from within Python. The test suite calls these functions which, in
  turn, call your C functions. **DO NOT MODIFY**. Any modifications will be
  ignored / overwritten when the homework is submitted.
  
  Please read the docstrings in this file to see how to call the wrapper and
  what kind of information is expected to be returned.

* `include/`:

  The library headers containing (1) the C function prototypes and (2) the C
  function documentation. Document your C functions here.
  
* `lib/`:

  The compiled C code will be placed here as a shared object library named
  `libhomework3.so`.
  
* `report/`:

  Place your `report.pdf` here. See the *"Report"* section below.

* `src/`:

  C library source files. This is where you will provide the bodies of the
  corresponding functions requested below. *Do not change the way in which these
  functions are called.* Doing so will break the Python wrappers located in
  `homework3/wrappers.py`. Aside from writing your own tests and performing
  computations for your report, everything you need to write for this homework
  will be put in the files here.
  
* `ctests/`:

  Directory in which to place any optional C code used to debug and test your
  library as well as practice compiling and linking C code. See the file
  `ctests/example.c` for more information and on how to compile.
    
* `Makefile`: See *"Compiling and Testing"* below.

* `test_homework3.py`: A sample test suite for your own testing purposes.

## Compiling and Testing

The makefile for this homework assignment has been provided for you. It will
compile the source code located in `src/` and create a shared object library
`lib/libhomework3.so`.

Run,

```
$ make lib
```

to create `lib/libhomework3.so`. This library must exist in order for the Python
wrappers to work. As a shortcut, running

```
$ make test
```

will perform

```
$ make lib
$ python test_homework3.py
```

## Assignment

(TBD)

### 1) Tests - 60%

Your implementations will be run through the following test suite:

(TBD)

### 2) Report - 20%

Produce a PDF document named `report.pdf` in the directory `report` of the
repository. Please write your name and UW NetID (e.g. "cswiercz", *not* your
student ID number) at the top of the document. The report should contain
responses to the following questions:

(TBD)

### 3) Documentation - 10%

Provide documentation for the function prototypes listed in all of the files in
`include` following the formatting described in the
[Grading document](https://github.com/uwhpsc-2016/syllabus/blob/master/Grading.md).

### 4) Performance - 10%

(TBD)
