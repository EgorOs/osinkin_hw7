#!/usr/bin/env python3


class BePositive:
    class Descriptor:
        def __init__(self, name):
            self.name = name
        def __get__(self, instance, owner):
            # self экземпляр класса дескриптора
            # instance - экземпляр класса BePositive
            # owner - класс BePositive
            # getattr возвращает значение атрибута с именем name экземпляра BePositive
            return getattr(instance, self.name, self)

        def __set__(self, instance, value):
            try:
                value = float(value)
                if value >= 0:
                    # К экземпляру класса BePositive крепится атрибут с именем self.name
                    # и значением value
                    setattr(instance, self.name, value)
                else:
                    raise ValueError('Value must be positive')
            except Exception as error:
                raise error

    some_value = Descriptor('__some')
    another_value = Descriptor('__another')


instance = BePositive()
instance.some_value = 1
instance.another_value = -1

'''
  1) уровень на котором задаётся дескриптор в самом классе:
Может быть определён вне класса, в классе или внутри класса, вложенного в класс, так как классы
- это пространства имён.

  2) что если задать дескриптор внутри метода, или вне класса?
Дескриптор можно определить вне класса, но тогда возможен конфликт имён с другими классами или дескрипторами.
Если инстанциировать дескриптор для переменной внутри метода или вне класса, то при попытке изменения
значения переменной дескриптор перезапишется новым значением.

  3) проверку инстанции в самом дескрипторе,
  что если мы создадим несколько объектов этого класса?

  4) может ли дескриптор принимать какие-то аргументы?
Да, если определить для него метод __init__(self, arg)

  5) как в этом случае мы можем модифицировать получение значений из дескриптора?
def __get__(self, instance, owner): return self.arg
'''