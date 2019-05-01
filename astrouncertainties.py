import astropy.units as units
import uncertainties
from uncertainties import ufloat,unumpy
import operator


def split(x):
    if isinstance(x,uncertainties.core.Variable):
        return x.n,x.s
    else:
        return unumpy.nominal_values(x),unumpy.std_devs(x)
    

class AUVariable:
    def __init__(self,value,std_dev,unit):
        """
        Primary class for handling values and their associated errors, with units attached

        Parameters:
        value: either a float or a list/numpy array
        std_dev: either a float or a list/numpy array, must match the former
        unit: an astropy units or a string that will be read into an astropy unit
        """
        if hasattr(value, "__iter__"):
            self.unc = unumpy.uarray(value,std_dev)
        else:
            self.unc = ufloat(value,std_dev)
        if type(unit) == str:
            self.unit = units.Unit(unit)
        else:
            self.unit = unit

    def __repr__(self):
        v,s = split(self.unc)
        return "AUArray(%s,%s,%s)"%(repr(v),repr(s),repr(self.unit))

    def __str__(self):
        return str(self.unc)+"*%s"%str(self.unit)
        
    def __add__(self,other):
        return self.binop(other,operator.add,convert=True)
        
    def __sub__(self,other):
        return self.binop(other,operator.sub,convert=True)

    def __mul__(self,other):
        return self.binop(other,operator.mul)

    def __div__(self,other):
        return self.binop(other,operator.div)

    def __pow__(self,other): #works oddly if other has units
        return self.binop(other,operator.pow)

    
    def to(self,unit):
        """
        Converts the arrays to the new unit
        """
        if type(unit) == str:
            unit = units.Unit(unit)

        v,s = split(self.unc)        
        conv_v = (v*self.unit).to(unit)
        conv_s = (s*self.unit).to(unit)
        self.unit = conv_v.unit

        if isinstance(self.unc,uncertainties.core.Variable):
            self.unc = ufloat(conv_v.value,conv_s.value)
        else:
            self.unc = unumpy.uarray(conv_v.value,conv_s.value)
        return self

    def si(self):
        """
        Converts the arrays to SI units
        """
        v,s = split(self.unc)
        conv_v = (v*self.unit).si
        conv_s = (s*self.unit).si
        if isinstance(self.unc,uncertainties.core.Variable):
            self.unc = ufloat(conv_v.value,conv_s.value)
        else:
            self.unc = unumpy.uarray(conv_v.value,conv_s.value)
        return self
        

    
    def binop(self,other,op,convert=False):
        """
        Primary function for mathematical binary operators
        """
        if isinstance(other,AUVariable):
            if convert:
                other.to(self.unit)
            new_unc = op(self.unc,other.unc)
        elif isinstance(other,units.quantity.Quantity):
            new_unc = op(self.unc,other.to(self.unit).value)
        else: #Assume same units, which is against what astropy does
            new_unc = op(self.unc,other)
        v,s = split(new_unc)
        return AUVariable(v,s,self.unit)


    def compop(self,other,op):
        pass
    
    def get_value(self):
        """ Returns the number/array of values """
        return split(self.unc)[0]
    get_values = get_value

    def get_std_dev(self):
        """ Returns the number/array of errors """
        return split(self.unc)[1]
    get_std_devs = get_std_dev

    
