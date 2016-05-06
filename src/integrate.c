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
  double dx;

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
  double end, start = omp_get_wtime();
  trapz_parallel(fvals, x, N, num_threads);
  end = omp_get_wtime();
  return (end - start);
}


double simps_serial(double* fvals, double* x, int N)
{
  double integral = 0;
  double dx;

  for (int i=0; i<N-2; i+=2)
    {
      dx = x[i+2] - x[i];
      integral += dx * (fvals[i+2] + 4.0*fvals[i+1] + fvals[i]);
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

  #pragma omp parallel for                        \
    shared(x,fvals)                               \
    private(dx)                                   \
    reduction(+:integral)                         \
    num_threads(num_threads)
  for (int i=0; i<N-2; i+=2)
    {
      dx = x[i+2] - x[i];
      integral += dx * (fvals[i+2] + 4.0*fvals[i+1] + fvals[i]);
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


double time_simps_parallel(double* fvals, double* x, int N, int num_threads,
                           int repeat)
{
  double end, start = omp_get_wtime();
  for (int i=0; i<repeat; ++i)
    simps_parallel(fvals, x, N, num_threads);
  end = omp_get_wtime();
  return (end - start) / (double)repeat;
}


double simps_parallel_chunked(double* fvals, double* x, int N,
                              int num_threads, int chunk_size)
{
  double integral = 0;
  double dx;

  // set chunk_size > 0
  chunk_size = (chunk_size <= 0 ? 1 : chunk_size);

  #pragma omp parallel for                        \
    shared(x,fvals)                               \
    private(dx)                                   \
    reduction(+:integral)                         \
    schedule(static,chunk_size)                   \
    num_threads(num_threads)
  for (int i=0; i<N-2; i+=2)
    {
      dx = x[i+2] - x[i];
      integral += dx * (fvals[i+2] + 4.0*fvals[i+1] + fvals[i]);
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


double time_simps_parallel_chunked(double* fvals, double* x, int N,
                                   int num_threads, int chunk_size,
                                   int repeat)
{
  double end, start = omp_get_wtime();
  for (int i=0; i<repeat; ++i)
    simps_parallel_chunked(fvals, x, N, num_threads, chunk_size);
  end = omp_get_wtime();
  return (end - start) / (double)repeat;
}
