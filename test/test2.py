__author__ = 'wanggen'

def _say(self, *args):
    print("hello: %s" % args)


class Person:

    def __init__(self):
        pass

    def add(self):
        self.__a += 1
        self._b += 1
        self.c += 1

    def print(self):
        print("a=%s, b=%s, c=%s" % (self.__a, self._b, self.c))

    __a=1
    _b=1
    c=1

p = Person()

p.add()
p.print()

p._b += 1
print("_b after +1: %s" % p._b)

print("c after +=1: %s "%p.c)
p.c=0


p2 = Person()
print(p2._b)
print(p2.c)


p.say = _say


# print("p's dict: %s" % p.__dict__)
# print("Person's dict: %s" % p.__class__.__dict__)
# for k, v in p.__class__.__dict__.items():
#     print("%-20s%s" % (k, v))