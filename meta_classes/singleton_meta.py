class SingletonMeta(type):
    """metaclass for Pattern Singleton"""
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance:
            return cls._instance
        cls._instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance


# pylint: disable=R0903
class Singleton(metaclass=SingletonMeta):
    """parent class for Pattern Singleton"""
