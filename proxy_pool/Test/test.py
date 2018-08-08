class Meta(type):
    def __new__(cls, *args, **kwargs):
        print('meta __new__')
        return type.__new__(cls, *args, **kwargs)

    def __init__(cls, *args, **kwargs):
        print('meta __init__')

    def __call__(cls, *args, **kwargs):
        print('meta __call__')
        # obj = cls.__new__(cls, *args, **kwargs)
        # cls.__init__(obj, *args, **kwargs)  # Foo.__init__(obj)
        return super(Meta, cls).__call__(*args, **kwargs)


class Foo(object, metaclass=Meta):
    def __init__(self):
        print("Foo __init__")

    def __new__(cls, *args, **kwargs):
        print('Foo __new__')
        return object.__new__(cls)


Foo()


class A(object):
    def __init__(self):
        print('A')


class B(object):
    def __init__(self):
        print('B')


class C(A):
    def __init__(self):
        # super(C, self).__init__()
        print('C')


class D(C, B):
    def __init__(self):
        super(D, self).__init__()
        print('D')


D()
