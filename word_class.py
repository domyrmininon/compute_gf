import time

DEPTH_LIMIT = 1000
CHECK_LOOP_DEPTH_LIMIT = 1000

def inv(l):
    return [-i for i in l[::-1]]

class SignedWord:
    """
    A class representing a signed word, by a list of integer values, negative values are inverse letters 
    """
    def __init__(self, l : list, rc = None):
        self.l = l
        self.rc = rc #The right complement of the word, a function that takes two words and returns the right two complements
        if self.is_positive():
            self.repr = set([str(self)]) #We keep track of the different representations of the word
        
    def inv(self):
        """
        return the inverse of the word, by negating all the letters and reversing the order
        """
        return SignedWord(inv(self.l), self.rc)

    def is_positive(self):
        """
        return True if the word is positive, False otherwise
        """
        return all(i > 0 for i in self.l)

    def __str__(self):
        """
        return a string representation ([1, -2, 3]) -> "ab^{-1}c" latex compatible
        """
        if self.l == []:
            return "1"
        s = ""
        for i in self.l:
            if i > 0:
                s += chr(i + 96)
            else:
                s += chr(-i + 96) + "^{-1}"
        return s
    

    def __eq__(self, other):
        if self.l == other.l:
            return True
        if self.is_positive() and other.is_positive():
            if len(self.l) != len(other.l):
                return False
            #check if a common representation appear in their list of representations
            if self.repr.intersection(other.repr):
                #fusion the two lists of representations
                self.repr = self.repr.union(other.repr)
                return True
            
            try :
                x,y = (self.inv()+other).right_reverse_check_loop().extract_positive_negative()
                assert self.is_positive() 

                if x == SignedWord([], self.rc) and y == SignedWord([], self.rc):
                    #fusion the two lists of representations
                    self.repr = self.repr.union(other.repr)
                    return True
                else:
                    return False
            except ValueError:
                return False
        else:
            return False

    def from_string(s, rc = None):
        """
        create a SignedWord from a string, "ab^{-1}c" -> [1, -2, 3]
        """
        if s == "1":
            return SignedWord([], rc)
        l = []
        i = 0
        while i < len(s):
            if s[i].isalpha():
                l.append(ord(s[i]) - 96)
                i += 1
            elif s[i] == "^" and s[i+1] == "{":
                l.append(-ord(s[i-1]) + 96)
                i += 4
            else:
                raise ValueError(f"Invalid character {s[i]} in string {s}")
        return SignedWord(l, rc)

    def __add__(self, other):
        """
        concatenate two words
        """
        return SignedWord(self.l + other.l, self.rc)

    def __repr__(self):
        return self.__str__()
    
    def right_reverse_break(self):
        """
        Find the first position where we can apply a right reverse step to a pair st and return the four words u, x,y, v where x,y are the two right complement of s and t, and w = u^{-1} s^{-1} t v
        """
        if self.rc is None:
            raise ValueError("Right complement function is not defined")
        
        if len(self.l) < 2:
            return None
        i = 0
        while i < len(self.l) - 1:
            a, b = self.l[i], self.l[i+1]
            if a < 0 and b > 0:
                # We have a negative followed by a positive, we can apply the right complement
                try:
                    c, d = self.rc(-a, b) # we have the right complement ac = bd
                except ValueError:
                    raise ValueError(f"Right complement is not defined for {-a} and {b}")
                u = SignedWord(self.l[:i], self.rc).inv()
                v = SignedWord(self.l[i+2:], self.rc)
                c = SignedWord(c, self.rc)
                d = SignedWord(d, self.rc)
                return u, c, d, v
            i += 1
        raise Exception("The word is irreducible")

    def right_reverse_step(self):
        """
        Perform a right reverse step on the word
        """
        u,c,d,v = self.right_reverse_break()
        self.l = (u.inv() + c + d.inv() + v).l

    def right_reverse(self):
        """
        Perform right reverse steps until the word is irreducible
        """
        for i in range(DEPTH_LIMIT): # we put a limit to avoid infinite loops
            try:
                self.right_reverse_step()
            except ValueError as e:
                raise ValueError("right reverse step failed: " + str(e))
            except Exception:
                return self
        raise Exception(f"Depth limit {DEPTH_LIMIT} reached in right reverse, use right_reverse_check_loop to check for loops")
    
    def right_reverse_check_loop(self, seen = None, depth = 0, rr_table = None):
        """
        Perform right reverse steps until the word is irreducible, but check for loops. rr_table is a cache for already computed right reverse
        """
        if rr_table is None:
            rr_table = {}
        if str(self) in rr_table:
            if rr_table[str(self)] is None:
                raise ValueError(f"Loop detected in right reverse, word {self} is cyclic")
            else:
                self.l = rr_table[str(self)].l
                return self
        if seen is None:
            seen = []
        if self.__str__() in seen:
            raise ValueError(f"Loop detected in right reverse, word {self} is cyclic")
        if depth > CHECK_LOOP_DEPTH_LIMIT:
            raise ValueError(f"Depth limit {CHECK_LOOP_DEPTH_LIMIT} reached in right reverse")
        seen.append(self.__str__())
        try :
            u,c,d,v = self.right_reverse_break()
        except Exception:
            # The word is irreducible, we can stop
            return self
        try :
            cp, up = (u.inv()+c).right_reverse_check_loop(seen.copy(), depth = depth + 1, rr_table=rr_table).extract_positive_negative()
            vp, dp = (d.inv()+v).right_reverse_check_loop(seen.copy(), depth = depth + 1, rr_table=rr_table).extract_positive_negative()
            vpp, upp = (up.inv()+vp).right_reverse_check_loop(seen.copy(), depth = depth + 1, rr_table=rr_table).extract_positive_negative()
        except ValueError as e:
            rr_table[str(self)] = None #means loop
            raise ValueError(e)
        old_str = str(self)        
        self.l = (cp + vpp + upp.inv() + dp.inv()).l
        rr_table[old_str] = self
        
        return self

            
        
            


    #when right reversing ends, the word is a positive-negative word
    def extract_positive_negative(self):
        """
        return the positive and negative part of the word, as two separate words
        """
        positive = []
        negative = []
        for i in self.l:
            if i > 0:
                positive.append(i)
            else:
                negative.append(-i)
        negative = negative[::-1] # we reverse the negative part to have the correct order
        return SignedWord(positive, self.rc), SignedWord(negative, self.rc)
    


def right_complement(u_str : str, v_str : str, rc): #This function computes the right complement of two positive words u and v, by applying right reversing. Infinte loops can happen and raise an Exception if the depth is too high
    u = SignedWord.from_string(u_str, rc)
    v = SignedWord.from_string(v_str, rc)
    w = u.inv() + v
    w.right_reverse()
    return w.extract_positive_negative()

def right_complement_check_loop(u_str : str, v_str : str, rc, rr_table): #This function does the same but checks for loops in the right reverse process
    try :
        u = SignedWord.from_string(u_str, rc)
        v = SignedWord.from_string(v_str, rc)
        w = u.inv() + v
        w.right_reverse_check_loop(rr_table=rr_table)
        vp, up = w.extract_positive_negative()
        return vp, up

    except ValueError as e:
        raise ValueError(f"Right complement is not defined for {u_str} and {v_str} because {e}")
    



def compute_garside_family(rc, n):
    '''
    Start with the set of atoms and compute the closure under right-lcm and right-divisor
    '''
    atoms = [SignedWord.from_string(chr(i+97), rc) for i in range(n)]
    family = [SignedWord([], rc)]
    to_insert = atoms.copy()
    already_inserted = set()
    total_time = time.time()
    rr_table = {}
    while to_insert:
        x = to_insert.pop()
        if x not in family:
            family.append(x)
            for y in family:
                try:
                    yp, xp = right_complement_check_loop(str(x), str(y), rc, rr_table)
                    lcm = x + yp
                    #assert lcm == y + xp, f"Error: {lcm} != {y + xp}"
                    for w in [yp, xp, lcm]:
                        if not str(w) in already_inserted:
                            already_inserted.add(str(w))
                            to_insert.append(w)
                except ValueError as e:
                    pass
            print(f"Total time so far: {time.time() - total_time:.2f} seconds, family has size {len(family)}", end="\r")
    return family  

