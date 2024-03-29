import abc
import typing


class BenchmarkSolver:
    @classmethod
    @abc.abstractmethod
    def description(cls) -> str:
        raise NotImplementedError("Method not implemented")

    @abc.abstractmethod
    def mergesort(cls, input):
        raise NotImplementedError("Method not implemented")

    @abc.abstractmethod
    def groupby_sum(self, data_dict) -> typing.Dict[str, typing.Any]:
        raise NotImplementedError("Method not implemented")

    @abc.abstractmethod
    def string_slice(self, test_data: typing.Dict) -> typing.List[str]:
        raise NotImplementedError("Method not implemented")

    @abc.abstractmethod
    def ngram_count(self, test_data):
        raise NotImplementedError("Method not implemented")

    @abc.abstractmethod
    def ngram_count_parallel(self, test_data):
        raise NotImplementedError("Method not implemented")

    @abc.abstractmethod
    def minhash(self, test_data):
        raise NotImplementedError("Method not implemented")
