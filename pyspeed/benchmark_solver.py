import typing
import abc


class BenchmarkSolver:
    @abc.abstractclassmethod
    def description(cls) -> str:
        pass

    @abc.abstractmethod
    def mergesort(cls, input):
        pass
