#include <math.h>
#include <stdio.h>
#include <stdlib.h>

#include "integrate.h"


int main(int argc, char** argv)
{
  // get the problem size from the command line
  int N = 32;
  if (argc > 1)
    N = atoi(argv[1]);

  printf("\n===== Timings.c =====");
  printf("\n(for N = %d)\n\n", N);

  double* x = (double*) malloc(N * sizeof(double));
  double* y = (double*) malloc(N * sizeof(double));

  // populate x and y with sample data: y = sin(exp(x)) for x between -2*pi and pi
  double pi = 3.14159
  double dx = ()/ (N + 1.0);
  for (int i=0; i<N; ++i)
    {
      x[i] = i*dx;
      y[i] = sin(exp(x[i]));
    }

}
