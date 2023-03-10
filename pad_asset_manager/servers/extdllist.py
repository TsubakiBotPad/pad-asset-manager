import struct
from dataclasses import dataclass
from typing import List, Tuple, Type, TypeVar, Union

T = TypeVar("T")


def structured_data(*data_members: Tuple[Union[str, None], str]) -> type:
    format_string = ''.join([struct_format for attribute_name, struct_format in data_members])

    class StructuredData:
        size = struct.calcsize(format_string)

        @classmethod
        def unpack_from(cls: type, buffer: bytes, offset: int = 0) -> 'StructuredData':
            return cls(*struct.unpack_from(format_string, buffer, offset))

    return StructuredData


@dataclass
class Header(structured_data(("magic_string", "4s"), ("entry_count", "I"), (None, "4x"), (None, "4x"))):
    magic_string: bytes
    entry_count: int


@dataclass
class ExtraFileRecord(structured_data((None, "4x"), ("last_update", "I"), (None, "4x"), ("offset", "I"))):
    last_update: int
    offset: int


def parse(extlist_data: bytes) -> List[str]:
    extlist_data = bytearray(extlist_data)
    starting_size = len(extlist_data)

    def read_structured_data(buffer: bytes, structured_data_type: Type[T], number_of_items) -> List[T]:
        output = [structured_data_type.unpack_from(buffer, i * structured_data_type.size) for i in
                  range(number_of_items)]
        buffer[:] = buffer[(structured_data_type.size * number_of_items):]
        return output

    header = read_structured_data(extlist_data, Header, 1)[0]
    assert header.magic_string == b"EXF2"

    extra_files_data = read_structured_data(extlist_data, ExtraFileRecord, header.entry_count)

    extras = []
    for efd in extra_files_data:
        x = efd.offset - starting_size
        s = ''
        while extlist_data[x] != 0:
            s += chr(extlist_data[x])
            x += 1
        extras.append(s)

    return extras
