/*
  integrate.h
  -----------

  Defines routines for numerically integrating (x_i,fval_i) data. That is, given
  a function f, some points along a domain x = [x_0, x_1, ..., x_{N-1}] and
  function values

  fvals = [f(x_0), f(x_1), ..., f(x_{N-1})]

  numerically approximate the integral of f using these function evaluations.
  These are meant to replecate the work done by `scipy.integrate.trapz` and
  `scipy.integrate.simps`, but written in C and using OpenMP.
*/


// remember to document these
double trapz_serial(double* fvals, double* x, int N);


double trapz_parallel(double* fvals, double* x, int N, int num_threads);


double time_trapz_parallel(double* fvals, double* x, int N, int num_threads);


double simps_serial(double* fvals, double* x, int N);


double simps_parallel(double* fvals, double* x, int N, int num_threads);


double time_simps_parallel(double* fvals, double* x, int N, int num_threads);


double simps_parallel_chunked(double* fvals, double* x, int N, int num_threads, int chunk_size);


double time_simps_parallel_chunked(double* fvals, double* x, int N, int num_threads, int chunk_size);
