from typing import Callable, MutableMapping, TypeVar, Iterator
from datetime import timedelta, datetime

K = TypeVar('K')
T = TypeVar('T')

class PyObjectCache(MutableMapping[K, T]):
    def __init__(self, fetcher: Callable[[K], T], max_age: timedelta = timedelta(seconds=300), raise_on_error: bool = False) -> None:
        super().__init__()

        if max_age < timedelta(0):
            raise ValueError("max_age should be non-negative (0 for immediate expiration)")

        self.__fetcher = fetcher
        self.__cache = {}
        self.__expiries = {}
        self.__max_age = max_age
        self.__raise_on_error = raise_on_error

    def __is_expired(self, k: K) -> bool:
        return k not in self.__expiries or self.__expiries[k] < datetime.now()

    def __getitem__(self, k: K) -> T:
        try:
            if k not in self.__cache or self.__is_expired(k):
                self.__setitem__(k, self.__fetcher(k))

            return self.__cache[k]

        except:
            if self.__raise_on_error:
                raise

        return None

    def __setitem__(self, k: K, v: T) -> None:
        try:
            self.__cache.__setitem__(k, v)
            self.__expiries.__setitem__(k, datetime.now() + self.__max_age)

        except:
            if self.__raise_on_error: raise

    def __delitem__(self, v: K) -> None:
        try:
            if v in self.__cache:
                self.__cache.__delitem__(v)
                self.__expiries.__delitem__(v)

        except:
            if self.__raise_on_error: raise

    def __iter__(self) -> Iterator[K]:
        return self.__cache.__iter__()
    
    def __len__(self) -> int:
        return self.__cache.__len__()

def pyCache(max_age: timedelta = timedelta(300), raise_on_error: bool = False, **static_params):
    def pycache_decorator(target: Callable[[K,], T]):
        cache = PyObjectCache(lambda k: target(k, **static_params), max_age, raise_on_error)
        def pycache_shim(k: K):
            return cache[k]
        return pycache_shim
    return pycache_decorator