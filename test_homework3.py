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
)


class TestIntegrate(unittest.TestCase):

    def test_trapz_serial(self):
        x = linspace(-2*pi,pi,2)
        y = sin(exp(x))
        i1 = trapz(y,x)
        i2 = trapz_serial(y,x)
        self.assertLess(abs(i1 - i2), 1e-8)

        x = linspace(-2*pi,pi,3)
        y = sin(exp(x))
        i1 = trapz(y,x)
        i2 = trapz_serial(y,x)
        self.assertLess(abs(i1 - i2), 1e-8)

        x = linspace(-2*pi,pi,1024)
        y = sin(exp(x))
        i1 = trapz(y,x)
        i2 = trapz_serial(y,x)
        self.assertLess(abs(i1 - i2), 1e-8)

    def test_trapz_parallel(self):
        x = linspace(-2*pi,pi,2)
        y = sin(exp(x))
        i1 = trapz(y,x)
        i2 = trapz_parallel(y,x)
        self.assertLess(abs(i1 - i2), 1e-8)

        x = linspace(-2*pi,pi,3)
        y = sin(exp(x))
        i1 = trapz(y,x)
        i2 = trapz_parallel(y,x)
        self.assertLess(abs(i1 - i2), 1e-8)

        x = linspace(-2*pi,pi,1e4)
        y = sin(exp(x))
        i1 = trapz(y,x)
        i2 = trapz_parallel(y,x)
        self.assertLess(abs(i1 - i2), 1e-8)

    def test_simps_serial_single_interval(self):
        x = linspace(-2*pi,pi,3)
        y = sin(exp(x))
        i1 = simps(y,x)
        i2 = simps_serial(y,x)
        self.assertLess(abs(i1 - i2), 1e-8)

    def test_simps_serial_odd(self):
        x = linspace(-2*pi,pi,7)
        y = sin(exp(x))
        i1 = simps(y,x)
        i2 = simps_serial(y,x)
        self.assertLess(abs(i1 - i2), 1e-8)

    def test_simps_serial_even(self):
        x = linspace(-2*pi,pi,8)
        y = sin(exp(x))
        i1 = simps(y,x,even='first')
        i2 = simps_serial(y,x)
        self.assertLess(abs(i1 - i2), 1e-8)

    def test_simps_parallel_odd(self):
        x = linspace(-2*pi,pi,7)
        y = sin(exp(x))
        i1 = simps(y,x)
        i2 = simps_serial(y,x)
        self.assertLess(abs(i1 - i2), 1e-8)

        x = linspace(-2*pi,pi,1e4-1)
        y = sin(exp(x))
        i1 = simps(y,x)
        i2 = simps_serial(y,x)
        self.assertLess(abs(i1 - i2), 1e-8)

    def test_simps_parallel_even(self):
        x = linspace(-2*pi,pi,8)
        y = sin(exp(x))
        i1 = simps(y,x,even='first')
        i2 = simps_serial(y,x)
        self.assertLess(abs(i1 - i2), 1e-8)

        x = linspace(-2*pi,pi,1e4)
        y = sin(exp(x))
        i1 = simps(y,x,even='first')
        i2 = simps_serial(y,x)
        self.assertLess(abs(i1 - i2), 1e-8)

if __name__ == '__main__':
    print '\n===== Running Timings ====='
    x = linspace(-2*pi, pi, 1e7)
    y = sin(exp(x))

    t1 = time_trapz_parallel(y, x, num_threads=1)
    print 'threads = %d, time = %f'%(1, t1)

    t2 = time_trapz_parallel(y, x, num_threads=2)
    print 'threads = %d, time = %f'%(2, t2)

    t4 = time_trapz_parallel(y, x, num_threads=4)
    print 'threads = %d, time = %f'%(4, t4)

    print '\n===== Running Tests ====='
    unittest.main(verbosity=2)

