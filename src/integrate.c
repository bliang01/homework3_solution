#include <omp.h>

double trapz_serial(double* fvals, double* x, int N)
{
  double integral = 0;
  double dx;
  for (int i=0; i<N-1; ++i)
    {
      dx = x[i+1] - x[i];
      integral += dx * (fvals[i+1] + fvals[i]);
    }

  integral *= 0.5;
  return integral;
}


double trapz_parallel(double* fvals, double* x, int N, int num_threads)
{
  double integral = 0;
  double dx, val;

  // parallel loop with reduction
  #pragma omp parallel for                        \
    shared(x,fvals)                               \
    private(dx)                                   \
    reduction(+:integral)                         \
    num_threads(num_threads)
  for (int i=0; i<N-1; ++i)
    {
      dx = x[i+1] - x[i];
      integral += dx * (fvals[i+1] + fvals[i]);
    }

  integral *= 0.5;
  return integral;
}


double time_trapz_parallel(double* fvals, double* x, int N, int num_threads)
{
  double start = omp_get_wtime();
  trapz_parallel(fvals, x, N, num_threads);
  double end = omp_get_wtime();

  return (end - start);
}


double simps_serial(double* fvals, double* x, int N)
{
  double integral = 0;
  double dx;

  for (int i=1; i<N-1; i+=2)
    {
      dx = x[i+1] - x[i-1];
      integral += dx * (fvals[i+1] + 4.0*fvals[i] + fvals[i-1]);
    }
  integral *= 0.166666666666666666;

  // if there are an even number of elements then add the last integral via
  // trapezoidal rule. this need not be parallel since it only happens once
  if (N % 2 == 0)
    {
      dx = x[N-1] - x[N-2];
      integral += 0.5 * dx * (fvals[N-1] + fvals[N-2]);
    }

  return integral;
}


double simps_parallel(double* fvals, double* x, int N, int num_threads)
{
  double integral = 0;
  double dx;

  // set number of threads
  omp_set_num_threads(num_threads);

  #pragma omp parallel for                        \
    shared(x,fvals)                               \
    private(dx)                                   \
    reduction(+:integral)
  for (int i=1; i<N-1; i+=2)
    {
      dx = x[i+1] - x[i-1];
      integral += dx * (fvals[i+1] + 4.0*fvals[i] + fvals[i-1]);
    }
  integral *= 0.166666666666666666;

  // if there are an even number of elements then add the last integral via
  // trapezoidal rule. this need not be parallel since it only happens once
  if (N % 2 == 0)
    {
      dx = x[N-1] - x[N-2];
      integral += 0.5 * dx * (fvals[N-1] + fvals[N-2]);
    }

  return integral;
}


double time_simps_parallel(double* fvals, double* x, int N, int num_threads)
{
  double start = omp_get_wtime();
  simps_parallel(fvals, x, N, num_threads);
  double end = omp_get_wtime();

  return (end - start);
}


double simps_parallel_chunked(double* fvals, double* x, int N, int num_threads, int chunk_size)
{
  double integral = 0;
  double dx;

  // set number of threads and chunk size
  omp_set_num_threads(num_threads);
  if (chunk_size <= 0)
    chunk_size = 1;

  #pragma omp parallel for                        \
    shared(x,fvals)                               \
    private(dx)                                   \
    shared(static,chunk_size)                     \
    reduction(+:integral)
  for (int i=1; i<N-1; i+=2)
    {
      dx = x[i+1] - x[i-1];
      integral += dx * (fvals[i+1] + 4.0*fvals[i] + fvals[i-1]);
    }
  integral *= 0.166666666666666666;

  // if there are an even number of elements then add the last integral via
  // trapezoidal rule. this need not be parallel since it only happens once
  if (N % 2 == 0)
    {
      dx = x[N-1] - x[N-2];
      integral += 0.5 * dx * (fvals[N-1] + fvals[N-2]);
    }

  return integral;
}


double time_simps_parallel_chunked(double* fvals, double* x, int N, int num_threads, int chunk_size)
{
  double start = omp_get_wtime();
  simps_parallel_chunked(fvals, x, N, num_threads, chunk_size);
  double end = omp_get_wtime();
  
  return (end - start);
}
