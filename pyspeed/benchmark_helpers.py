import pathlib
from functools import lru_cache


@lru_cache()
def alphabet():
    include_ranges = [
        (0x0021, 0x0021, 1),
        (0x0023, 0x0026, 1),
        (0x0028, 0x007E, 100),
        (0x00A1, 0x00AC, 1),
        (0x00AE, 0x00FF, 1),
        (0x0100, 0x017F, 1),
        (0x0180, 0x024F, 1),
        (0x2C60, 0x2C7F, 1),
        (0x16A0, 0x16F0, 1),
        (0x0370, 0x0377, 1),
        (0x037A, 0x037E, 1),
        (0x0384, 0x038A, 1),
        (0x038C, 0x038C, 1),
    ]

    return "".join(
        chr(code_point) * weight
        for range_start, range_end, weight in include_ranges
        for code_point in range(range_start, range_end + 1)
    )


@lru_cache()
def load_txt(pathlib_obj):
    with pathlib_obj.open("r") as f:
        return f.read()


def iter_wikipedia_docs(max_docs=1000):
    data_path = pathlib.Path(__file__).parent.parent / "data" / "wikipediaArticles"
    for i, p in enumerate(data_path.glob("*.txt")):
        if i > max_docs:
            break
        yield load_txt(p)
