import struct
from dataclasses import dataclass
from typing import List, NamedTuple, Tuple, Type, TypeVar, Union

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
class Header(structured_data(("mons_count", "I"), ("cards_count", "I"), ("magic_string", "4s"), (None, "4x"))):
    mons_count: int
    cards_count: int
    magic_string: bytes


@dataclass
class UncompressedAssetRecord(structured_data(("id_number", "H"), (None, "4x"), (None, "4x"), (None, "4x"),
                                                (None, "2x"), ("uncompressed_size", "I"), (None, "4x"))):
    id_number: int
    uncompressed_size: int


@dataclass
class CompressedAssetRecord(structured_data(("compressed_size", "I"), (None, "4x"))):
    compressed_size: int


class UnifiedAssetRecord(NamedTuple):
    id_number: int
    uncompressed_size: int
    compressed_size: int

    @staticmethod
    def from_assetrecords(uncompressed: UncompressedAssetRecord, compressed: CompressedAssetRecord):
        return UnifiedAssetRecord(uncompressed.id_number, uncompressed.uncompressed_size, compressed.compressed_size)


def parse(extlist_data: bytes) -> Tuple[List[UnifiedAssetRecord], List[UnifiedAssetRecord]]:
    extlist_data = bytearray(extlist_data)

    def read_structured_data(buffer: bytes, structured_data_type: Type[T], number_of_items: int) -> List[T]:
        output = [structured_data_type.unpack_from(buffer, i * structured_data_type.size) for i in
                  range(number_of_items)]
        buffer[:] = buffer[(structured_data_type.size * number_of_items):]
        return output

    header = read_structured_data(extlist_data, Header, 1)[0]
    assert header.magic_string == b"EXT2"

    uncompressed_mons_data = read_structured_data(extlist_data, UncompressedAssetRecord, header.mons_count)
    uncompressed_cards_data = read_structured_data(extlist_data, UncompressedAssetRecord, header.cards_count)
    compressed_mons_data = read_structured_data(extlist_data, CompressedAssetRecord, header.mons_count)
    compressed_cards_data = read_structured_data(extlist_data, CompressedAssetRecord, header.cards_count)

    # Unify the compressed and uncompressed data:
    mons_data = [UnifiedAssetRecord.from_assetrecords(uncompressed, compressed)
                 for uncompressed, compressed in
                 zip(uncompressed_mons_data, compressed_mons_data)
                 if uncompressed.id_number != 0]
    cards_data = [UnifiedAssetRecord.from_assetrecords(uncompressed, compressed)
                  for uncompressed, compressed in
                  zip(uncompressed_cards_data, compressed_cards_data)
                  if uncompressed.id_number != 0]
    return mons_data, cards_data
