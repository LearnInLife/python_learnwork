

## 注意点

1. 在多继承的时候，调用super(type, obj_or_type) 会按照 MRO 的顺序去委托 type 的 父类 或 兄弟类 的方法来调用
     比如：

     * ProxyCheck类在初始化时，如果调用`super(ProxyCheck,self).__init()__`,初始化调用的是MRO顺序中的ProxyCheck类下一个类,如果父类不调用`__init()__`，则不会继续调用后面的`__init()__`

     * 所以如果要初始化父类Thread，必须手动调用`Thread.__init(self)__`

     * super 指的是 MRO 中的下一个类！

       

2. inspect.getmembers(object[, predicate])

   * 返回一个包含对象的所有成员的(name, value)列表。返回的内容比对象的`__dict__`包含的内容多，源码是通过dir()实现的。

   * predicate是一个可选的函数参数，被此函数判断为True的成员才被返回。

   * 比如：

     > inspect.getmembers(GetFreeProxy, predicate=inspect.isfunction)返回的是GetFreeProxy中的所有方法
     >
     > name是方法名，value是方法的对象



3. response.text 和 response.content

   * response.text返回的类型是str，解码类型：根据HTTP头部对响应的编码做出有根据的推测，推测的文本编码
   * response.content返回的类型是bytes，可以通过decode()方法将bytes类型转为str类型

   

4. xpath查询

   > .//tr[position()>1]  第一个以后的所有tr标签
   >
   > /tr/@data-ip tr标签中的data-ip的属性的值

   

5.  any 和 all

   * any(x)判断x对象是否为空对象，如果都为空、0、false，则返回false，如果不都为空、0、false，则返回true
   * all(x)如果all(x)参数x对象的所有元素不为0、''、False或者x为空对象，则返回True，否则返回False

   

6. `__getattr__` 、`__getattribute__`、`__get__`

   * ``object.__getattr__(self, name)`当一般位置找不到attribute的时候，会调用getattr，返回一个值或AttributeError异常。

   * `object.__getattribute__(self, name)`无条件被调用，通过实例访问属性。如果class中定义了`__getattr__` ()，则`__getattr__` ()不会被调用（除非显示调用或引发AttributeError异常）

   * `object.__get__(self, instance, owner)`

     * 如果class定义了它，则这个class就可以称为descriptor。
     * owner是所有者的类，instance是访问descriptor的实例，如果不是通过实例访问，而是通过类访问的话，instance则为None。
     * 可以理解为当对象a作为对象b的某个属性时，b.a调用时，就会调用a的`__get__`方法

     

   * 每次通过实例访问属性，都会经过`__getattribute__`函数。

   * 而当属性不存在时，仍然需要访问`__getattribute__`，不过接着要访问`__getattr__` 。这就好像是一个异常处理函数。

   * 每次访问descriptor（即实现了`__get__`的类），都会先经过`__get__`函数。

   

7. 如何理解类装饰器LazyProperty

class A(object):
    @LazyProperty
    def fuc():
        pass

相当于，类A中的 方法func变为了 LazyProperty(fuc)，类LazyProperty作为了A中的一个属性值
如果调用 A.fuc 则会相应调用LazyProperty的`__get__`方法，得到其返回值



8. `__call__`

   元类中有一个特殊的方法`__call__`，这个方法会截断类的`__new__`和`__init__`方法,阻止其执行`__call__`应该返回实例，和类的`__new__`方法返回的一样。

6.1 如果元类中定义了`__call__`，此方法必须返回一个对象，
否则类的实例化就不会起作用。（实例化得到的结果为`__call__`的返回值）
6.2 如果元类的`__call__`中返回type.`__call__`(cls, *args, **kwargs),
type创建的对象,里面会调用定义类的`__new__`方法,和`__init__`方法

```
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
```
```
meta __new__
meta __init__
meta __call__
Foo __new__
Foo __init__
```
Foo类中，如果`__new__`方法不返回实体，则`__init__`方法不会被调用
