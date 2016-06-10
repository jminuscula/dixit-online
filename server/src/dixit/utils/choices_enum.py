

class ChoicesEnumMeta(type):
    """
    Metaclass that copies non underscored class attributes into _choices
    """
    def __new__(mcls, name, bases, namespace):
        mcls._choices = dict(filter(lambda i: not i[0].startswith('__'), namespace.items()))
        return super().__new__(mcls, name, bases, namespace)


class ChoicesEnum(metaclass=ChoicesEnumMeta):
    """
    Enum like class that provices django-compatible choices()

    Usage:

        class MyChoices(ChoicesEnum):
            FOO = 'foo_value'
            BAR = 'bar_Value'

        >>> MyChoices.choices()
        (('foo_value', 'FOO'), ('bar_value', 'BAR'))
    """

    @classmethod
    def choices(cls):
        return tuple((value, name) for (name, value) in cls._choices.items())
