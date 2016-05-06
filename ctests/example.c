#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#include "integrate.h"

int main(int argc, char** argv)
{
  // get the problem size from the command line
  int N = 10000;
  if (argc > 1)
    N = atoi(argv[1]);

  printf("\n===== example.c =====");
  printf("\n(for N = %d)\n\n", N);

  double* x = (double*) malloc(N * sizeof(double));
  double* y = (double*) malloc(N * sizeof(double));

  // populate x and y with sample data: y = sin(exp(x)) for x between -1 and 3
  // (in this example, the points in x are uniformly spaced)
  double pi_actual = 3.14159265359;
  double pi_approx;
  double dx = 1.0 / (N + 1.0);
  for (int i=0; i<N; ++i)
    {
      x[i] = i*dx;
      y[i] = 4.0 / (1 + x[i]*x[i]);
    }

  double end, start = omp_get_wtime();
  pi_approx = trapz_serial(y,x,N);
  end = omp_get_wtime();

  printf("pi_actual: %.15f\n", pi_actual);
  printf("pi_approx: %.15f\n", pi_approx);
  printf("error:     %e\n", fabs(pi_actual - pi_approx));
  printf("time:      %f\n", end - start);

  free(x);
  free(y);
}
