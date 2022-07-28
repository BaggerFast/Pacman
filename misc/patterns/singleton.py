class SingletonMeta(type):
    """Metaclass for Pattern Singleton"""

    instance = None

    def __call__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls.instance


# pylint: disable=R0903
class Singleton(metaclass=SingletonMeta):
    """Easy use SingletonMeta"""

    instance = None
