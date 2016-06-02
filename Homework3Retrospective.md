# Common Mistakes

## Array/Loop Bounds

By far the most severe common issue was trying to use `x[N]`/`fvals[N]`. These
are invalid array accesses in C, because for a size `N` array, the indices run
from `0` to `N-1`. As an example, the following loop is incorrect:

```c
for (int i=0; i<N; ++i) {
    dx = x[i+1] - x[i];
    integral += dx * (fvals[i+1] + fvals[i]);
}
```

If you think about it, the very last value of `i` will be `N-1`. If you plug in
that value in the loop, you find that the last loop iteration is equivalent to
this invalid code:

```c
dx = x[N] - x[N-1];
integral += dx * (fvals[N] + fvals[N-1]);
```

There were also some cases where the loop bounds might have been too *small*. As
a rule of thumb, if you're not sure where a loop should start or end, you should
try to actually plug in the first and last values of `i`, and see if each line
is actually doing what you expect it do be doing to the first/last values in the
arrays.

## Not Accounting For Non-Uniform Grids

This may have been more of an issue with understanding the assignment
requirements. Many people did something like this:

```c
dx = (x[N-1] - x[0]) / (N-1);
```

This is the correct *average* distance between neighboring grid points, but it
doesn't work to use this value if the grid points are unevenly spaced.

## Using A Chunk Size Of Zero

In `simps_parallel_chunked`, the chunk size parameter is an input. Several
people also specified a chunk size for the other parallel functions
(`trapz_parallel` and `simps_parallel`). Normally, this would be fine, but
several people estimated a chunk size that ended up being zero for small numbers
of points (like a single interval, for instance). A chunk size of zero is
invalid.

# Performance Tips

## The Good

Most people were able to achieve similar levels of performance in their code
(within a factor of 2 on the test I used). A couple of things that helped a
little bit were:

- Doing division outside of loops (e.g. for Simpson's rule, dividing by 6
  outside the loop instead of inside). It's a small difference in this case, but
  not quite zero.

- Using the `reduction` clause to avoid too much thread synchronization. This
  was faster than most of the solutions using `atomic` or `critical` constructs
  (though some of the `atomic` versions were equally fast).

## The Bad

A few things that particularly slowed down the code:

- Using an array of partial sums (one for each thread). This is a little bit of
  a subtle point, but in most cases, it's as good or better to use a private
  variable, rather than creating a shared array of variables with one entry for
  each thread. This is due to a phenomenon known as
  [false sharing](https://en.wikipedia.org/wiki/False_sharing), which causes a
  cache miss (or something similar) to occur whenever a thread running on one
  core modifies memory that's within a few bytes of data used by a thread on a
  different core.

- Worse than this is if the threads are using a single variable to accumulate
  values at every time step. This can make the code much slower than even the
  serial version!

- Using `schedule(dynamic)` caused a serious slowdown. The reason for this is
  that (a) the dynamic scheduling in this case was probably unnecessary since
  every loop iteration has a similar number of threads, and (b) the default
  chunk size for the dynamic scheduler is always 1, which is much worse than the
  default for the static scheduler in this case. So specifying dynamic
  scheduling with a chunk size of 1 forces every iteration of the loop to incur
  some degree of scheduling overhead.

## The "Meh"

There are some things that a few people tried, but which don't really make a
difference.

- Tweaking the order of variables in a single line (e.g. writing
  `fvals[i] + fvals[i+1]` versus `fvals[i+1] + fvals[i]`). Unless you have some
  definitive testing that shows a difference, or you are familiar with how the
  compiler code generation works, it's hard to know if these two versions even
  produce *different* code at all, let alone whether one or the other is better.

- Multiplying by `1./6.` instead of dividing by `6`. The former is faster, but
  as long as the division is done outside of the loop, it doesn't really matter.

- Multiplying by `0.166666666666666666` instead of `1./6.` doesn't do anything
  because the compiler usually evaluates math involving constants at compile
  time. (This optimization is almost always done, and in fact many compilers
  don't even let you turn it off.)

- Using bitwise operators instead of `%` or `/`. For instance, using `N&1` can
  tell you whether `N` is even or not, just by looking at the last digit of the
  binary representation. In general, this is faster than using `N%2`, which in
  theory requires a division. However, in practice, this is such a common
  optimization that the compiler will do this for you. That is to say, if `N` is
  an integer type, `N%2` and `N&1` generate the exact same code.

# Report Questions

Rather than describe common errors, I will simply make a very brief series of
points about the four questions on the report.

1. Regardless of chunk size, the `nthreads=8` case should have had similar or
   worse performance compared to `nthreads=4`, because there are only 4 cores
   available (except for a few people who used a different number of cores).
   When the chunk size is small, performance will be particularly bad when there
   are more threads, due to a higher rate of cache misses when data is spread
   out. E.g. if the chunk size is 1, each thread in the `nthreads=2` case will
   have to look points spaced a distance of 2 apart. For the `nthreads=8` case,
   each thread has to look at every 8th point, so there is much less work done
   for each cache miss.

2. When the chunk size is equal to the problem size (or greater), one thread
   gets all the work, so we are effectively solving the problem serially.
   Therefore, using more than one thread requires more overhead for no gain
   (e.g. running threads that have nothing to do and immediately have to yield
   to the next scheduled task).

3. Looking at the
   [Lecture 12 code](https://github.com/uwhpsc-2016/lectures/blob/master/lecture12/pi_inclass.c),
   you can see that there are no input arrays being accessed at all, since the
   values of x and f(x) are being generated "on the fly" in the loop. This is
   the biggest reason why there's little-to-no effect to changing the chunk size
   in this case; with no arrays being accessed, there are no cache issues to
   worry about.

4. There were a lot of defensible answers to this question. Generally speaking,
   some middle-of-the-road value of the chunk size probably worked best, but
   many people saw very little difference between a chunk size of 2^8 and 2^16
   (the curve was pretty flat in the middle of the graph). You could justifiably
   say that it's too hard to conjecture an ideal size, since it depends on
   attributes of a particular machine, as well as number of cores and number of
   threads. However, there are some guesses that are likely to give reasonable
   results. For instance, since we use ~`N/2 - 1` iterations in Simpson's rule,
   a chunk size close to `N/(2*nthreads)` might be expected to work well, since
   every thread will get work, but the data access uses contiguous chunks.
   Smaller sizes might work better for `schedule(dynamic, chunk_size)` (or a
   different scheduling strategy).
