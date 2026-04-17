from collections.abc import Callable
from typing import TypeVar
from weakref import WeakValueDictionary

D = TypeVar("D")


class Names[T]:
    class Existed(Exception):
        pass

    def __init__(self):
        self.origs: WeakValueDictionary[str, T] | dict[str, T] = WeakValueDictionary()

    def name(self, item: T, *names: str):
        for name in names:
            if name in self.origs:
                raise self.Existed(f"{item.__qualname__} -×- {name} <-> {self.origs[name].__qualname__}")
        for name in names:
            try:
                self.origs[name] = item
            except TypeError:
                self.origs = dict(self.origs)
                self.origs[name] = item

    def named(self, *names: str) -> Callable[[T], T]:
        def wrapper(item: T) -> T:
            self.name(item, *names)
            return item

        return wrapper

    @property
    def names(self) -> set[str]:
        return set(self.origs.keys())

    def __getitem__(self, name: str) -> T:
        if name not in self.origs:
            raise NameError(name)
        return self.origs[name]

    def get(self, name: str, default: D = None) -> T | D:
        return self.origs.get(name, default)

    def fuzzy(self, name: str, default: D = None, threshold: int = 70) -> T | D:
        from fuzzywuzzy import process

        name = name.lower()
        best = process.extractOne(name, self.names, scorer=process.fuzz.ratio)
        if best and best[1] >= threshold:
            return self[best[0]]
        return default
