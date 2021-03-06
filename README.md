astrouncertainties
===========

A wrapper to combine the uncertainties package with astropy units.

BEWARE: there is still a problem with correlations, i.e., x - x**2 returns different errors than x * (1-x)

**Requires**:<br>
astropy <br>
uncertainties <br>

AUVariable
--------------

A class for handling either a value and error pair or an array pair

Usage:

    >>> from astrouncertainties import *
    >>> x = AUVariable([1,2,3],[1,1,1],"m")
    >>> y = AUVariable([0.005,0.005,0.007],[0.001,0.001,0.001],units.km)
    >>> z = x+y
    >>> print z
    [6.0+/-1.4142135623730951 7.0+/-1.4142135623730951 10.0+/-1.4142135623730951]*m