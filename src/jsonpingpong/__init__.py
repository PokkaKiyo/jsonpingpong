from time import perf_counter

import msgspec
from msgspec import Struct
from polyfactory.factories.msgspec_factory import MsgspecFactory


class Datum(Struct):
    id: int
    days: list[str]


class DatumFactory(MsgspecFactory[Datum]):
    __model__ = Datum


def time_it(func):
    def _(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        end = perf_counter()
        print(f"{func.__name__} took {end - start:.6f}s")
        return result

    return _


@time_it
def test_decode_everything(encoded: bytes):
    decoded = _decode_into_datum(encoded)
    for i in range(100):
        decoded.pop(i)
    reencoded = msgspec.json.encode(decoded)
    return reencoded


@time_it
def _decode_into_datum(encoded: bytes):
    decoded = msgspec.json.decode(encoded, type=dict[int, Datum])
    return decoded


@time_it
def test_partial_decode(encoded: bytes):
    decoded = _decode_into_partial_raw(encoded)

    for i in range(100):
        decoded.pop(i)
    reencoded = msgspec.json.encode(decoded)
    return reencoded


@time_it
def _decode_into_partial_raw(encoded: bytes):
    decoded = msgspec.json.decode(encoded, type=dict[int, msgspec.Raw])
    return decoded


@time_it
def build_data():
    data: dict[int, Datum] = {}
    for i in range(100_000):
        data[i] = DatumFactory.build()

    encoded = msgspec.json.encode(data)
    return encoded


def main():
    encoded = build_data()
    encoded_1 = test_decode_everything(encoded)
    encoded_2 = test_partial_decode(encoded)
    assert encoded_1 == encoded_2


if __name__ == "__main__":
    main()
