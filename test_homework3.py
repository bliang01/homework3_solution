import unittest
import numpy

from numpy import array, linspace, pi, sin, exp
from scipy.integrate import trapz, simps

from homework3 import (
    trapz_serial,
    trapz_parallel,
    time_trapz_parallel,
    simps_serial,
    simps_parallel,
    time_simps_parallel,
    simps_parallel_chunked,
    time_simps_parallel_chunked,
)


class TestIntegrateTrapz(unittest.TestCase):

    # serial
    def test_trapz_single_interval(self):
        x = linspace(-1,3,2)
        y = sin(exp(x))
        i1 = trapz(y,x)
        i2 = trapz_serial(y,x)
        self.assertLess(abs(i1 - i2), 1e-14)

    def test_trapz_serial(self):
        x = linspace(-1,3,3)
        y = sin(exp(x))
        i1 = trapz(y,x)
        i2 = trapz_serial(y,x)
        self.assertLess(abs(i1 - i2), 1e-14)

        x = numpy.append(linspace(-1,0,500,endpoint=False),
                         linspace(0,3,500))
        y = sin(exp(x))
        i1 = trapz(y,x)
        i2 = trapz_serial(y,x)
        self.assertLess(abs(i1 - i2), 1e-14)

    # parallel
    def test_trapz_parallel_single_interval(self):
        x = linspace(-1,3,2)
        y = sin(exp(x))
        i1 = trapz(y,x)
        i2 = trapz_parallel(y,x)
        self.assertLess(abs(i1 - i2), 1e-14)

    def test_trapz_parallel(self):
        x = linspace(-1,3,3)
        y = sin(exp(x))
        i1 = trapz(y,x)
        i2 = trapz_parallel(y,x)
        self.assertLess(abs(i1 - i2), 1e-14)

        x = numpy.append(linspace(-1,0,500,endpoint=False),
                         linspace(0,3,500))
        y = sin(exp(x))
        i1 = trapz(y,x)
        i2 = trapz_parallel(y,x)
        self.assertLess(abs(i1 - i2), 1e-14)

class TestIntegrateSimps(unittest.TestCase):

    # serial
    def test_simps_serial_single_interval(self):
        x = linspace(-1,3,3)
        y = sin(exp(x))
        i1 = simps(y,x)
        i2 = simps_serial(y,x)
        self.assertLess(abs(i1 - i2), 1e-14)

    def test_simps_serial_odd(self):
        x = linspace(-1,3,7)
        y = sin(exp(x))
        i1 = simps(y,x)
        i2 = simps_serial(y,x)
        self.assertLess(abs(i1 - i2), 1e-14)

        x = numpy.append(linspace(-1,0,500,endpoint=False),
                         linspace(0,3,501))
        y = sin(exp(x))
        i1 = simps(y,x)
        i2 = simps_serial(y,x)
        self.assertLess(abs(i1 - i2), 1e-14)

    def test_simps_serial_even(self):
        x = linspace(-1,3,8)
        y = sin(exp(x))
        i1 = simps(y,x,even='first')
        i2 = simps_serial(y,x)
        self.assertLess(abs(i1 - i2), 1e-14)

        x = numpy.append(linspace(-1,0,500,endpoint=False),
                         linspace(0,3,500))
        y = sin(exp(x))
        i1 = simps(y,x,even='first')
        i2 = simps_serial(y,x)
        self.assertLess(abs(i1 - i2), 1e-14)

    # parallel
    def test_simps_parallel_single_interval(self):
        x = linspace(-1,3,3)
        y = sin(exp(x))
        i1 = simps(y,x)
        i2 = simps_parallel(y,x)
        self.assertLess(abs(i1 - i2), 1e-14)

    def test_simps_parallel_odd(self):
        x = linspace(-1,3,7)
        y = sin(exp(x))
        i1 = simps(y,x)
        i2 = simps_parallel(y,x)
        self.assertLess(abs(i1 - i2), 1e-14)

        x = numpy.append(linspace(-1,0,500,endpoint=False),
                         linspace(0,3,501))
        y = sin(exp(x))
        i1 = simps(y,x)
        i2 = simps_parallel(y,x)
        self.assertLess(abs(i1 - i2), 1e-14)

    def test_simps_parallel_even(self):
        x = linspace(-1,3,8)
        y = sin(exp(x))
        i1 = simps(y,x,even='first')
        i2 = simps_parallel(y,x)
        self.assertLess(abs(i1 - i2), 1e-14)

        x = numpy.append(linspace(-1,0,500,endpoint=False),
                         linspace(0,3,501))
        y = sin(exp(x))
        i1 = simps(y,x,even='first')
        i2 = simps_parallel(y,x)
        self.assertLess(abs(i1 - i2), 1e-14)

class TestIntegrateSimpsChunked(unittest.TestCase):

    def test_simps_parallel_chunked_single_interval(self):
        x = linspace(-1,3,3)
        y = sin(exp(x))
        i1 = simps(y,x)
        i2 = simps_parallel_chunked(y,x,chunk_size=2)
        self.assertLess(abs(i1 - i2), 1e-14)

    def test_simps_chunked_parallel_odd(self):
        x = linspace(-1,3,7)
        y = sin(exp(x))
        i1 = simps(y,x)
        i2 = simps_parallel_chunked(y,x, chunk_size=2)
        self.assertLess(abs(i1 - i2), 1e-12)

        x = numpy.append(linspace(-1,0,500,endpoint=False),
                         linspace(0,3,501))
        y = sin(exp(x))
        i1 = simps(y,x)
        i2 = simps_parallel_chunked(y,x, chunk_size=100)
        self.assertLess(abs(i1 - i2), 1e-12)

    def test_simps_chunked_parallel_even(self):
        x = linspace(-1,3,8)
        y = sin(exp(x))
        i1 = simps(y,x,even='first')
        i2 = simps_parallel_chunked(y,x, chunk_size=2)
        self.assertLess(abs(i1 - i2), 1e-12)

        x = numpy.append(linspace(-1,0,500,endpoint=False),
                         linspace(0,3,501))
        y = sin(exp(x))
        i1 = simps(y,x,even='first')
        i2 = simps_parallel_chunked(y,x,chunk_size=100)
        self.assertLess(abs(i1 - i2), 1e-12)


if __name__ == '__main__':
    print '\n===== Running Timings ====='
    x = linspace(-1, 3, 1e7)
    y = sin(exp(x))

    t1 = time_trapz_parallel(y, x, num_threads=1)
    print 'threads = %d, time = %f'%(1, t1)

    t2 = time_trapz_parallel(y, x, num_threads=2)
    print 'threads = %d, time = %f'%(2, t2)

    t4 = time_trapz_parallel(y, x, num_threads=4)
    print 'threads = %d, time = %f'%(4, t4)

    print '\n===== Running Tests ====='
    unittest.main(verbosity=2)

