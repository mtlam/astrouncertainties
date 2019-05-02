import unittest
import numpy as np
from astrouncertainties import *




class TestAUVariable(unittest.TestCase):        
    def test_get_value(self):
        assert np.all(x.get_value() == np.array([1.,2.,3.])*units.m)
        self.assertEqual(u.get_value(),4*units.m)

    def test_get_std_devs(self):
        assert np.all(x.get_std_devs() == np.array([1.,1.,1.])*units.m)
        self.assertEqual(u.get_std_devs(),1*units.m)
        self.assertNotEqual(u.get_std_devs(),1*units.km)
        self.assertEqual(u.get_std_devs(),0.001*units.km)

    def test_eq(self):
        z = y.to("m",save=False)
        self.assertEqual(y,z)

    def test_add(self):
        self.assertEqual(str(x+y).replace("\n",""),"[6.0+/-1.4142135623730951 7.0+/-1.4142135623730951 10.0+/-1.4142135623730951]*m")
        self.assertEqual(str(x+3),"[4.0+/-1.0 5.0+/-1.0 6.0+/-1.0]*m")
        
    def test_to(self):
        z = y.to("m",save=False)
        self.assertEqual(str(z),"[5.0+/-1.0 5.0+/-1.0 7.0+/-1.0]*m")

    def test_si(self):
        z = y.si(save=False)
        self.assertEqual(str(z),"[5.0+/-1.0 5.0+/-1.0 7.0+/-1.0]*m")

        


if __name__ == '__main__':
    a = 3*units.m
    b = 0.004*units.km
    c = unumpy.uarray([1,2,3],[1,1,1])
    d = unumpy.uarray([3,3,3],[1,1,1])
    e = ufloat(2,0.1)

    u = AUVariable(4,1,"m")
    v = AUVariable(0.005,0.002,"km")
    
    x = AUVariable([1,2,3],[1,1,1],"m")
    y = AUVariable([0.005,0.005,0.007],[0.001,0.001,0.001],units.km)
    unittest.main()
