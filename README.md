# Homework #3

Homework #3 will test you on writing OpenMP code. 

Repository layout:

* `homework3/`:

  Python wrapper of C library. The functions defined here allow you to use your
  C code from within Python. The test suite calls these functions which, in
  turn, call your C functions. **DO NOT MODIFY**. Any modifications will be
  ignored / overwritten when the homework is submitted.
  
  Please read the docstrings in this file to see how to call the wrapper and
  what kind of information is expected to be returned. Compare with the
  signature of the underlying C function.

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

In this assignment we will implement several numerical integration in serial and
in parallel. Given a function, f, and some x-data points, form the arrays

```
    x = [x_0, x_1, ..., x_{N-1}]
fvals = [f(x_0), f(x_1), ..., f(x_{N-1})]
```

Using these data one can approximate the integral of f from `x_0` to `x_{N-1}`
using the following formulae

* [Trapezoidal Rule](http://mathworld.wolfram.com/TrapezoidalRule.html)

  ![trapezoidal](https://raw.githubusercontent.com/uwhpsc-2016/homework3_solution/master/report/trapezoidal.png)
  
* [Simpson's Rule](http://mathworld.wolfram.com/SimpsonsRule.html)

  ![simpson](https://raw.githubusercontent.com/uwhpsc-2016/homework3_solution/master/report/simpson.png)

Scipy has built-in functions
[`scipy.linalg.trapz`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.trapz.html#scipy.integrate.trapz)
and
[`scipy.linalg.simps`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.simps.html#scipy.integrate.simps)
which, given an x-data set and function evaluations, will use these rules to
estimate the integral. For example,

``` python
>>> from numpy import linspace, sin, pi
>>> from sicpy.integrate import trapz, simps
>>> x = linspace(-1,pi,8)  # eight, equally-spaced points between -1 and pi
>>> fvals = sin(x)
>>> integral_trapz = trapz(fvals, x)
>>> integral_simps = simps(fvals, x, even='first')  # see simps documentation
```

In this assignment we will write serial and parallel versions of these
algorithms. Additionally, we will perform some parameter tuning on our parallel
implementation of Simpson's rule. In particular, *you are to provide the
definitons of the below functions*. In each of these functions, `fvals` is a
length `N` array of function evaluations on the elements of `x`, a length `N`
array of domain points.

* `double trapz_serial(double* fvals, double* x, int N)`

  Approximate the value of the integral f using the trapezoidal rule.

* `double trapz_parallel(double* fvals, double* x, int N, int num_threads)`

  Approximate the value of the integral f using the trapezoidal rule in
  parallel. The number of threads to be used should be an argument to the
  function.

* `double simps_serial(double* fvals, double* x, int N)`

  Approximate the value of the integral f using Simpson's rule. Note that there
  are two cases to consider: the "nice" case when `N` is odd and the "not nice"
  case when `N` is even. Once you understand why there is an issue in the `N`
  even case resolve the issue by taking a single trapezoidal rule approximation
  at the end of the data array to capture the "missing" part of the integral.
  
  (Hint: read the
  [`scipy.linalg.simps`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.simps.html#scipy.integrate.simps)
  documentation.)

* `double simps_parallel(double* fvals, double* x, int N, int num_threads)`

  Approximate the value of the integral f using the trapezoidal rule in
  parallel. The number of threads to be used should be an argument to the
  function.

* `double simps_parallel_chunked(double* fvals, double* x, int N, int num_threads, int chunk_size)`

  Approximate the value of the integral f using the trapezoidal rule in
  parallel. The number of threads to be used should be an argument to the
  function. In this implemenation you should use a `#pragma omp for` construct
  so you can pass in a chunk size to the loop thread scheduler. (Or write one
  manually. See Lecture 11.) You do not need to use `#pragma omp for` in
  `simps_parallel` but you may if you want to.

### 1) Tests - 60% (INCOMPLETE)

Your implementations will be run through the following test suite:

* (pt) Check the definition of `trapz_serial` using data arrays of length two.
* (pt) Test if `trapz_serial` returns a sufficient approximation to a known
  integral for large `N`.
* (pt) Check the definition of `simps_serial` using data arrays of length three.
* (pt) Test if `simps_serial` returns a sufficient approximation to a known
  integral for large **odd** `N`. (This is the "nice" case.)
* (pt) Test if `simps_serial` returns a sufficient approximation to a known
  integral for large **even** `N`. (This is the "not nice" case where an extra
  trapezoidal rule approximation needs to be done at the *end* of the data.)

* (pt) Check the definition of `trapz_parallel` using data arrays of length two.
* (pt) Check the definition of `simps_parallel` using data arrays of length three.
* (pt) Do `simps_serial` and `simps_parallel` produce the correct result when
  there are an odd number of data poitns? (i.e. when `N` is odd?)
* (pt) Does `simps_parallel_chunked` behave well when the chunk size is less
  than or equal to zero. (What happens when this is the case?)
  
In this homework assignment we will manually verify that the `parallel` versions
of your algorithms correctly implement some sort of parallel structure. You will
recieve zero points on the `parallel` tests if you only implement the serial
version of the code.


### 2) Report - 20% (INCOMPLETE)

Produce a PDF document named `report.pdf` in the directory `report` of the
repository. Please write your name and UW NetID (e.g. "cswiercz", *not* your
student ID number) at the top of the document. The report should contain
responses to the following questions:

* (pt) Create a
  [`semilogx`](http://matplotlib.org/examples/pylab_examples/log_demo.html) plot
  of timings of `simps_parallel_chunked` with chunk size on horizontal axis and
  runtime on the vertical axis.
  
  ```
  x = numpy.linspace(-4,2, 1e7)
  y = sin(exp(x))
  chunk_sizes = [1e1, 1e2, ..., 1e6]
  ``` 
  
  * (pt) In black, timings with `num_threads = 1`.
  * (pt) In green, timings with `num_threads = 2`.
  * (pt) In blue, timings with `num_threads = 4`.
  * (pt) In red, timings `num_threads = 8`.
  * (pt) Axes are labeled.
  * (pt) Plot uses `semilogx`.

### 3) Documentation - 10%

Provide documentation for the function prototypes listed in all of the files in
`include` following the formatting described in the
[Grading document](https://github.com/uwhpsc-2016/syllabus/blob/master/Grading.md).

### 4) Performance - 10% (INCOMPLETE)


