from decimal import Decimal
from functools import total_ordering

# value = mantissa * base^exponent 

Base = 10 
Bound = 30 

def normalize(mantissa, exponent):
    if mantissa == 0:
        return 0, 0                #if the mantissa is 0 the whole function will return 0 due to multiplication rules 

    sign = 1 if mantissa > 0 else -1    #a way to represent positive and negative numbers in the mantissa zone
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

def float_to_mantissa_exp(x):
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
        
    def __init__ (self, mantissa, exponent):
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
        m = self.mantissa * other.mantissa  # multiply the mantissa terms
        e = self.exponent + other.exponent  # add the exponents 
        m, e = normalize(m, e)              # runs the answer though the normalize function to make sure the mantissa stays as 30 digits 
        return KRHiPer(m ,e)

    def __add__(self, other):
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

    # total_orderign shoudl be able to derive 
        # le as self < other or self == other
        # gt as not (le)
        # ge as not self < other
        

        