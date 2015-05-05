import functools

__author__ = 'wanggen'


def auth(**kwargs):
    def decorator(fn):
        print("注解参数: %s"%kwargs)
        def wrapper(*args, **kwargs):
            print("方法参数1:"+str(*args))
            print("方法参数2:"+str(kwargs))
            return fn(*args, **kwargs)
        return wrapper
    return decorator


def need_login(method):
    @functools.wraps
    def wrapper(self, *args, **kwargs):
        if kwargs['name']:
            raise Exception('user not login')
        return method(self, args, **kwargs)
    return wrapper


@auth(name='wg')
def view_score(name, **kwargs):
    print("实际执行的方法>> [%s]'s score: %s" % (name, '100'))


view_score('王根', age=24)