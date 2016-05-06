import numpy
import scipy
import matplotlib.pyplot as plt

from numpy import linspace, sin, exp, pi

from homework3 import (
    time_simps_parallel_chunked,
)


def main():
    # set up problem
    exponent = 20
    N = 2**exponent
    chunk_sizes = [2**n for n in range(0,exponent+1,2)]
    x = linspace(-1,3,N)
    y = sin(exp(x))

    # compute timings for each number of threads
    repeat = 10
    times1 = [
        time_simps_parallel_chunked(y,x,num_threads=1,chunk_size=c,repeat=10)
        for c in chunk_sizes
    ]

    times2 = [
        time_simps_parallel_chunked(y,x,num_threads=2,chunk_size=c,repeat=10)
        for c in chunk_sizes
    ]

    times4 = [
        time_simps_parallel_chunked(y,x,num_threads=4,chunk_size=c,repeat=10)
        for c in chunk_sizes
    ]

    times8 = [
        time_simps_parallel_chunked(y,x,num_threads=8,chunk_size=c,repeat=10)
        for c in chunk_sizes
    ]

    # plot the timings
    plt.hold(True)
    fig = plt.semilogx(chunk_sizes, times1, 'ko-', label='1 thread')
    fig = plt.semilogx(chunk_sizes, times2, 'go-', label='2 threads')
    fig = plt.semilogx(chunk_sizes, times4, 'bo-', label='4 threads')
    fig = plt.semilogx(chunk_sizes, times8, 'ro-', label='8 threads')

    # add figure elements
    plt.legend()
    plt.xlabel('Chunk Size')
    plt.ylabel('Time (sec)')
    plt.title("Paralell Simpson's Rule Timings")
    plt.savefig('/Users/cswiercz/Desktop/bar.png')






if __name__ == '__main__':
    main()
