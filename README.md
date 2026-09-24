# Group Exercise: A Higher Precision Number Type

Started Thursday, September 24, in groups. Continues next week.

* Agree on the representation and the interface first, and record it in the repo
    * two floats: a big part plus a correction term holding the lost bits
    * integer mantissa + integer exponent (python ints are arbitrary precision)
    * a list of digits in a base you choose
    * or any other idea you might think of
* Implement the class
    * `__init__`, `__repr__`, construction from a normal python number
    * `__add__`, `__sub__`, `__mul__`, `__div__`
    * `__eq__`, `__lt__`  (and other comparison operations),  enough to sort a list of them
* Pick an algorithm where double precision is the limiting factor and show the
  difference against plain `float`
    * `(1 - cos x) / x^2` for small x — see [../9-22/cancel.py](../9-22/cancel.py)
    * summing many small values into a large one — [../9-22/iter.py](../9-22/iter.py)
    * the quadratic formula when `b^2 >> 4ac`
    * `(1 + 1/n)^n` converging to e
    * iterating the logistic map
* Validate against something you did not write
    * `decimal` and `fractions` are in the standard library
    * use them to check your type, not to implement it

## Questions to answer

* How many correct digits do you get, and how do you know?
* What does it cost? Time an operation against the equivalent on floats.
* Where does your representation break down?

## Next week

Sorting algorithms that work with this class, and how the sort time scales with
list length. Get `__lt__` and the constructor clean now.
