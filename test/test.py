import datetime
from filecmp import cmp
from functools import wraps
import json


# obj = json.loads('{"name":"wg", "age":[23,24,25]}', encoding='utf-8')
# print(obj['age'])
#
#
# print(json.loads('[{"error":"hello"}]', encoding='utf-8'))
#
# print("1  2 3 4".split(" "))
#
# l=list()
# l.append({"id": 1})
# l.append({"id": 2})
# l.sort(key=lambda o:o['id'], reverse=True)
#
#
# print(datetime.datetime.now().timestamp()*1000000)
#
#
# def tell(msg):
#     print(msg)
#
# tell({'name': 'wg'})


def wrapper(*args, **kwargs):
    # print(self)
    print("参数列表: " + str(args))
    print("参数列表[0]: " + str(args[0]))
    print("不定参数: %s" % kwargs)


a={'name': 'hello', 'lalal': 'AAAA'}
wrapper({'n':'b'}, "1", a=1, b=2, **a)


class Person:
    __doc__ = 'hello world'
    _name=''
    def __init__(self):
        self.name = 'wg'

    def hello(self, world):
        print(world)

p = Person()

has = hasattr(p, 'name')
print(has)
has = hasattr(p, 'age')
print("是否含有hello方法: %s" % hasattr(p, 'hello'))
print(has)

print(dir(p))

print(p.__dict__)
print(p.__module__)
print("class:"+str(p.__class__))
print("name:"+p.__class__.__name__)

# print("hello %s", (greed))


def hello(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        print("--------------------------------- %s " % fn)
        return fn(self, args, kwargs)
    return wrapper


def auth(self, *args, **options):
    def decorator(f):
        endpoint = options.pop('endpoint', None)
        print("请求参数:%s"%args)
        return f
    return decorator


# @hello('wanggen')
def tell_age(self, *args):
    print("current scope is: %s" % self)
    print("类型: %s"%type(args))
    if args is not None:
        print("I am: " + str(args))
    return 24

print(type(tell_age))


p.age = tell_age

print("p's dict:%s"%p.__dict__)

print("hello's annotations: %s " % p.hello.__dict__)

print("my age is: %s" % p.age(p))

print("dicts: %s" % p.__dict__)

print("age type:%s"%type(p.age).__name__)

print("Person dict:%s"%Person.__dict__)

