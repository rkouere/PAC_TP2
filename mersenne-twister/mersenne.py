import random
import base64

class MersenneTwister:
    """Based on the pseudocode in https://en.wikipedia.org/wiki/Mersenne_Twister.
       Generates uniformly distributed 32-bit integers in the range [0, 232 − 1] with the MT19937 algorithm.

       Written by Yaşar Arabacı <yasar11732 et gmail nokta com>
       Modified by C. Bouillaguet
    """

    bitmask_1 = (2 ** 32) - 1
    bitmask_2 = 2 ** 31
    bitmask_3 = (2 ** 31) - 1


    def __init__(self):
        """Class constructor"""
        self.MT = [ i+1 for i in range(624)]
        self.index = 0

    def rand(self):
        """Returns a 32-bit pseudo-random number. This should be equivalent
        to random.getrandbits(32). However, it does not return the
        same value because the seeding process is different.

        >>> mt = MersenneTwister()
        >>> mt.rand()
        4194449
        """
        # once each cell of the MT array has been used, we refresh the whole array
        if self.index == 624:
            self._generate_numbers()
        x = self.MT[self.index]
        self.index += 1
        # modify the content of the MT cell
        return self._f(x)


    def seed(self, seed):
        """Initialize the generator from a seed.

        This is ***not*** identical to random.seed(), because the
        latter is (a bit too) complicated (and it is written in C, as
        a built-in part of Python). See ``clone_python_state`` below.

        Examples:

        >>> mt = MersenneTwister()
        >>> mt.seed(0)
        >>> mt.rand()
        2479041101

        Compare with :
        >>> random.seed(0)
        >>> random.getrandbits(32)
        3626764237

        """
        self.MT[0] = seed
        for i in range(1,624):
            self.MT[i] = ((1812433253 * self.MT[i-1]) ^ ((self.MT[i-1] >> 30) + i)) & self.bitmask_1
        self.index = 624


    def set_state(self, MT):
        """initialize the internal state of the Mersenne Twister.

        The argument must be a list of 624 integers.
        """
        self.MT = MT
        self.index = 624


    def clone_python_state(self):
        """clone the internal state of the python built-in mersenne twister
           into this one. Once this is done, both PRNGs generate the **same**
           random sequence.

        >>> x = MersenneTwister()
        >>> x.clone_python_state()
        >>> for i in range(1000):
        ...     assert x.rand() == random.getrandbits(32)
        """
        s = random.getstate()
        self.index = s[1][-1]
        self.MT = list(s[1][:-1])


    ###### these functions are for internal use only ####

    def _generate_numbers(self):
        """update the MT array. For internal use only."""
        for i in range(624):
            y = (self.MT[i] & self.bitmask_2) + (self.MT[(i + 1 ) % 624] & self.bitmask_3)
            self.MT[i] = self.MT[(i + 397) % 624] ^ (y >> 1)
            if y % 2 != 0:
                self.MT[i] ^= 2567483615
        self.index = 0

    def _f(self, y):
        """function used to filter cells of the MT array."""
        print(y)
        y ^= y >> 11
        print(y)
        y ^= (y << 7) & 2636928640
        print(y)
        y ^= (y << 15) & 4022730752
        print(y)
        y ^= y >> 18
        print(y)
        return y

mt = MersenneTwister()
mt.seed(0)
test = []
for i in range(1):
   test.append(mt.rand())

def unshiftRight(val, shift):
    masq = val
    while masq != 0:
        masq = masq >> shift
        val = val ^ masq
    return val

def unshiftLeft(val, shift, mask):
    """ je pense qu'il faut faire un masque de taille du shift pour avoir la bonne valeur
    ex:
    a = 100101
    b = a << 4 = 1001010000
    b & 4xxxxx = 010000
    c = a xor b = 110101
  
"""
    masq = val
    while masq < 1000:
        masq = masq << shift
        val = (val ^ masq) & mask
    return val

print("unshift")
test = 123456789
shiftedValue = test ^ (test >> 1)
print(unshiftRight(shiftedValue, 1))
shiftedValue = test ^ (test << 15)
print(unshiftLeft(shiftedValue, 15, 4022730752))
#crackTest = (254 << 3) & 0xb
#print(unshiftLeft(crackTest, 3, 0xb))
#print(crackTest)
print("--------------")
#print(unshiftLeft(toShift, 15, 4022730752))
