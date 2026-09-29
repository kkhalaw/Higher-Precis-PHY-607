from decimal import Decimal, getcontext
from functools import total_ordering

# value = mantissa * base^exponent 

Base = 10 
Bound = 30 

def normalize(mantissa, exponent=0 ): # the =0 sets the default exponent to 0 
    if mantissa == 0:
        return 0, 0                #if the mantissa is 0 the whole function will return 0 due to multiplication rules 

    if mantissa > 0:
        sign = 1
    else:
        sign = -1    #a way to represent positive and negative numbers in the mantissa zone
    
    mantissa = abs(mantissa)            # the absolute value allows us to not have to worry about the negative sign messing with comparisons

    digits = len(str(mantissa))    # our number of precise digits is correlated to the length of our mantissa term
    shift = digits - Bound          # keep the mantissa inside a set bound to limit the shrinking/growing effects repeated operations can cause 

    if shift > 0:
        mantissa = mantissa // (Base ** shift)   # over 30 digits, round the mantissa and bump up the exponent (// for rounded division)
        exponent += shift 
    elif shift < 0:
        mantissa = mantissa * (Base ** (- shift)) # under 30 digits, push the mantissa up and reduce the exponent 
        exponent += shift
    return sign * mantissa, exponent   # reintroduces the sign we removed earlier back to the mantissa , and returns both terms 

def float_to_mantissa_exp(x): #convert an input float into our desired representation
    if x == 0.0:
        return 0, 0

    d = Decimal(x)                    # exact binary value of x, as a Decimal
    sign, digits, exponent = d.as_tuple() # breaks the decimal into 3 pieces -- sign, digit, and exponent 

    mantissa = int(''.join(map(str, digits))) #join the tupled digits into a string 
    if sign:                                   # deal with the sign 
        mantissa = -mantissa

    return mantissa, exponent

@total_ordering
class KRHiPer(object): 

    # Constructor -- the first argument needs to be self 
        
    def __init__ (self, mantissa, exponent=0):
        self.mantissa = mantissa
        self.exponent = exponent

        if isinstance(mantissa, float):                             # check if the input was given in integers or as a float
            mantissa , exponent = float_to_mantissa_exp(mantissa)   # if given as a float, convert into the correct form

        self.mantissa, self.exponent = normalize(mantissa, exponent) # store the mantissa and the exponent, use normalize to make sure the mantissa has the right number of digits 

    # Outputs -- either in scientific notation or descimal form 

    def __repr__(self): # seperated terms output (scientific notation w/ 30 digits)
        return f"KRHiPer({self.mantissa}, {self.exponent})"

    def __str__(self):  #  combined terms output (actual answer)
        value = self.mantissa * Base**self.exponent
        return str(value) 

    # Operations -- add, subtract, multiply, divide 

    def __mul__(self, other): #seems weird to start with multilpcation instead of division, but multiplying exponents are easier since you don't need to worry about having a common exponent term
        if not isinstance(other, KRHiPer):
            other = KRHiPer(other)

        m = self.mantissa * other.mantissa  # multiply the mantissa terms
        e = self.exponent + other.exponent  # add the exponents 
        m, e = normalize(m, e)              # runs the answer though the normalize function to make sure the mantissa stays as 30 digits 
        return KRHiPer(m ,e)

    def __add__(self, other):
        if not isinstance(other, KRHiPer):
            other = KRHiPer(other)

        if self.exponent >= other.exponent:
            shift = self.exponent - other.exponent
            tm = self.mantissa * Base**shift + other.mantissa
            e = other.exponent
        else:
            shift = other.exponent - self.exponent
            tm = self.mantissa + other.mantissa * Base**shift
            e = self.exponent
        tm, e = normalize(tm, e)
        return KRHiPer(tm, e)

    def __sub__(self, other):
        if not isinstance(other, KRHiPer):
            other = KRHiPer(other)

        if self.exponent >= other.exponent:
            shift = self.exponent - other.exponent
            tm = self.mantissa * Base**shift - other.mantissa
            e = other.exponent
        else:
            shift = other.exponent - self.exponent
            tm = self.mantissa - other.mantissa * Base**shift
            e = self.exponent
        tm, e = normalize(tm, e)
        return KRHiPer(tm, e)

    def __truediv__ (self, other): #most difficult due to how python divides integers (rounds to the nearest full number) to combat we can artifically inflate our numerator to ensure we get a non decimal number 
        if not isinstance(other, KRHiPer):
            other = KRHiPer(other)

        m = (self.mantissa * Base**Bound) // other.mantissa # add 30 more digits to the numerator as a buffer 
        e = self.exponent - other.exponent - Bound # sub the two exponents, then undo our buffer 
        m, e = normalize(m, e) # make sure we are back to 30 digits 
        return KRHiPer(m, e)


    # Comparisons equal to, less than, greater than, less than or equal, and greater than or equal 

    def __eq__(self, other):
        return self.mantissa == other.mantissa and self.exponent == other.exponent

    def __lt__(self, other):
        diff = self - other
        return diff.mantissa < 0

    # total_ordering should be able to derive 
        # le as self < other or self == other
        # gt as not (le)
        # ge as not self < other
        

def KRHiPer_cos(x, terms=20):
        """Compute cos(x) using a Taylor series, entirely in KRHiPer arithmetic."""
        result = KRHiPer(1, 0)      # start with the '1' term
        term = KRHiPer(1, 0)        # current term in the series, starts at 1
        x2 = x * x                  # x^2, reused every iteration

        for n in range(1, terms):
            # each new term = previous term * (-x^2) / ((2n-1)(2n))
            factor_num = KRHiPer(-1, 0) * x2
            factor_den = KRHiPer((2*n - 1) * (2*n), 0)
            term = (term * factor_num) / factor_den
            result = result + term

        return result


#Set decimal precision higher as to avoid being rounded down
getcontext().prec = 60

def decimal_cos(x, terms=20):   #Very similar to the KRHiPer_cos
    result = Decimal('1')
    term = Decimal('1')

    x2 = x * x

    for n in range(1,terms):
        term = (-term * x2) / ((2*n - 1) * (2*n))
        result += term 

    return result





import math

for k in range(1, 12):
    x_float = 10.0 ** -k
    x_hp = KRHiPer(x_float, exponent=any)          # convert into your type
    x_decimal = Decimal('10') ** -k

    # plain float version (what you're comparing against)
    float_result = (1 - math.cos(x_float)) / x_float**2
    # your type's version, all arithmetic done in KRHiPer
    one = KRHiPer(1, 0)
    KRHiPer_result = (one - KRHiPer_cos(x_hp)) / (x_hp * x_hp)
    #decimal version we are also comparing against (hopefully the KRHPer_result agrees more with)
    decimal_result = (1 - decimal_cos(x_decimal)) / (x_decimal**2)




    print(k, float_result, KRHiPer_result, decimal_result)