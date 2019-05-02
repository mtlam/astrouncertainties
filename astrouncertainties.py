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
        return str(self.unc)+" %s"%str(self.unit)

    def __getitem__(self,key):
        if isinstance(self.unc,uncertainties.core.Variable):
            raise TypeError("Internal value is not iterable")
        return ufloat(split(self.unc)[0][key],split(self.unc)[1][key])

    def __len__(self):
        if isinstance(self.unc,uncertainties.core.Variable):
            raise TypeError("Internal value is not iterable")
        return len(self.unc)
        
        
    def __add__(self,other):
        return self.binop(other,operator.add,convert=True)
    __iadd__ = __add__
    __radd__ = __add__

        
    def __sub__(self,other):
        return self.binop(other,operator.sub,convert=True)
    __isub__ = __sub__
    def __rsub__(self,other):
        return self.binop(other,(lambda x,y: y-x))

    
    def __mul__(self,other):
        return self.binop(other,operator.mul)
    __imul__ = __mul__
    __rmul__ = __mul__

    
    def __div__(self,other):
        return self.binop(other,operator.div)
    __idiv__ = __div__
    def __rdiv__(self,other):
        return self.binop(other,(lambda x,y: y/x))#,unitfunc=lambda x: 1./x)

    def __pow__(self,other): #works oddly if other has units
        return self.binop(other,operator.pow)


    def __eq__(self,other):
        other = other.to(self.unit,save=False)
        v,s = split(self.unc)
        ov,os = split(other.unc)
        if reduce(lambda x,y: x and y,v == ov) and reduce(lambda x,y: x and y,s == os):
            return True
        return False

    
    def to(self,unit,save=False):
        """
        Converts the arrays to the new unit
        """
        if type(unit) == str:
            unit = units.Unit(unit)

        v,s = split(self.unc)        
        conv_v = (v*self.unit).to(unit)
        conv_s = (s*self.unit).to(unit)

        if save:
            self.unit = unit
            if isinstance(self.unc,uncertainties.core.Variable):
                self.unc = ufloat(conv_v.value,conv_s.value)
            else:
                self.unc = unumpy.uarray(conv_v.value,conv_s.value)
            return self
        else:
            return AUVariable(conv_v.value,conv_s.value,unit)

    def si(self,save=False):
        """
        Converts the arrays to SI units
        """
        v,s = split(self.unc)
        conv_v = (v*self.unit).si
        conv_s = (s*self.unit).si
        if save:
            self.unit = conv_v.unit
            if isinstance(self.unc,uncertainties.core.Variable):
                self.unc = ufloat(conv_v.value,conv_s.value)
            else:
                self.unc = unumpy.uarray(conv_v.value,conv_s.value)
            return self
        else:
            return AUVariable(conv_v.value,conv_s.value,conv_v.unit)
        

    
    def binop(self,other,op,convert=False):
        """
        Primary function for mathematical binary operators
        """

        if isinstance(other,AUVariable):
            if convert:
                other = other.to(self.unit,save=False)
            # Calculate new uncertainties array
            new_unc = op(self.unc,other.unc)
            # Calculate new units
            new_unit = op(self.get_values()[0],other.get_values()[0]).unit
        elif isinstance(other,units.quantity.Quantity):
            if convert:
                other = other.to(self.unit)
            new_unc = op(self.unc,other.value)
            new_unit = op(self.get_values()[0],other).unit
        else: 
            new_unc = op(self.unc,other)
            new_unit = op(self.get_values(),other).unit
        v,s = split(new_unc)
        
        return AUVariable(v,s,new_unit)


    def compop(self,other,op):
        pass
    
    def get_value(self):
        """ Returns the number/array of values, with units """
        return split(self.unc)[0]*self.unit
    get_values = get_value

    def get_std_dev(self):
        """ Returns the number/array of errors, with units """
        return split(self.unc)[1]*self.unit
    get_std_devs = get_std_dev

    
