import typing
import abc


class BenchmarkSolver:
    @abc.abstractclassmethod
    def description(cls) -> str:
        pass

    @abc.abstractclassmethod
    def direct_dependencies(cls) -> typing.List[str]:
        pass

    @abc.abstractmethod
    def mergesort(cls, input):
        pass
