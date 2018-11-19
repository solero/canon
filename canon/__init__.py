import manifest_masks
import type_masks

from exceptions import CompressionError, DecompressionError, NotUnicodeError


_SpecialTypes = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "=", "+", "|"]


class _ManifestEntry(object):

    def __init__(self, character=None):
        self.null_chars = [True, True, True, True]

        self.type = 1
        self.size = 2

        if character:
            self.deserialize(character)

    def serialize(self):
        char_code = 0
        for index, null_char in enumerate(self.null_chars):
            char_code = char_code | 0 if not null_char else 1 << index
        char_code = char_code | self.type << 4
        char_code = char_code | self.size << 8
        return unichr(char_code)

    def deserialize(self, character):
        char_code = ord(character)
        for index, null_char in enumerate(self.null_chars):
            self.null_chars[index] = False if not char_code >> index & manifest_masks.NullMask == 1 else True

        self.type = char_code >> 4 & manifest_masks.TypeMask
        self.size = char_code >> 8 & manifest_masks.SizeMask


class _DataSet(object):
    def __init__(self):
        self.entries = []
        self.size = 0

    def append(self, data, index=None):
        self.size += data.manifest.size

        if index is None:
            self.entries.append(data)
            return

        if len(self.entries) > index and self.entries[index] is not None:
            self.size -= self.entries[index].manifest.size

        self.entries[index] = data

    def remove(self, index):
        data = self.entries[index]
        self.entries[index] = None
        return data


class _DataType(object):
    def __init__(self, value, manifest):
        self.value = value
        self.manifest = manifest

    def compress(self):
        raise NotImplementedError()

    def decompress(self, data):
        raise NotImplementedError()


class _Int16(_DataType):
    TypeID = 1

    def __init__(self, value=0, manifest=None):
        if manifest is None:
            manifest = _ManifestEntry()
            manifest.null_chars[1] = False
            manifest.null_chars[2] = False
            manifest.null_chars[3] = False

        super(_Int16, self).__init__(value, manifest)

    def compress(self):
        if not self.value:
            self.manifest.null_chars[0] = True
            character = unichr(1)
        else:
            self.manifest.null_chars[0] = False
            character = unichr(self.value & type_masks.Int16)

            for index, special_type in enumerate(_SpecialTypes):
                if character == special_type:
                    character = unichr(index + 1) + unichr(index + 1)
                    self.manifest.size = 3
                    break

                self.manifest.size = 2

        return self.manifest.serialize() + character

    def decompress(self, data):
        if self.manifest.size == 3:
            data = _SpecialTypes[ord(data[0]) - 1]

        if self.manifest.null_chars[0]:
            self.value = 0
        else:
            self.value = ord(data[0])

            if self.value >> 15 == 1:
                self.value = self.value | type_masks.UpperInt32

    def bit(self, _):
        return self.value


class _Boolean(_Int16):
    TypeID = 2

    def __init__(self, value=0, manifest = None):
        super(_Boolean, self).__init__(value, manifest)
        self.manifest.type = _Boolean.TypeID

    def decompress(self, data):
        if self.manifest.size == 3:
            data = _SpecialTypes[ord(data[0]) - 1]

        if self.manifest.null_chars[0]:
            self.value = 0
        else:
            self.value = ord(data[0])

    def bit(self, bit, value=None):
        if value is None:
            return False if not self.value >> bit & True else True
        self.value = self.value | 1 << bit if value else self.value & (type_masks.Int16 ^ 1 << bit)


class _Float(_DataType):
    TypeID = 3

    def __init__(self, value=0, manifest=None):
        if manifest is None:
            manifest = _ManifestEntry()
            manifest.type = _Float.TypeID
            manifest.size = 3
            manifest.null_chars[2] = False
            manifest.null_chars[3] = False

        super(_Float, self).__init__(value, manifest)

    def compress(self):
        first_value_mask = self.value >> 15 & type_masks.Int16
        second_value_mask = self.value & type_masks.Int16

        if first_value_mask == 0:
            self.manifest.null_chars[0] = True
            first_value_mask = 1
        else:
            self.manifest.null_chars[0] = False

        if second_value_mask == 0:
            self.manifest.null_chars[1] = True
            second_value_mask = 1
        else:
            self.manifest.null_chars[1] = False

        first_char_code = unichr(first_value_mask)
        second_char_code = unichr(second_value_mask)
        return self.manifest.serialize() + first_char_code + second_char_code

    def decompress(self, data):
        first_char_code = ord(data[0])
        second_char_code = ord(data[1])

        if self.manifest.null_chars[0]:
            first_char_code = 0
        if self.manifest.null_chars[1]:
            second_char_code = 0

        self.value = second_char_code | first_char_code << 15


class _String(_DataType):
    TypeID = 4

    def __init__(self, value="", manifest=None):
        if not value:
            value = ""

        if manifest is None:
            manifest = _ManifestEntry()
            manifest.type = _String.TypeID
            manifest.size = len(value)
            manifest.null_chars = [False] * len(manifest.null_chars)

        super(_String, self).__init__(value, manifest)

    def compress(self):
        value = self.value
        for index, special_type in enumerate(_SpecialTypes):
            if special_type in self.value:
                characters = unichr(index + 1) + unichr(index + 1)
                value = characters.join(value.split(special_type))

        self.manifest.size = len(value) + 1
        return self.manifest.serialize() + value

    def decompress(self, data):
        for index, special_type in enumerate(_SpecialTypes):
            characters = unichr(index + 1) + unichr(index + 1)
            if characters in data:
                data = special_type.join(data.split(characters))

        self.value = data
        self.manifest.size = len(self.value) + 1


class Compressor(object):

    @staticmethod
    def compress(data_set):
        try:
            result = ""
            for entry in data_set.entries:
                result += entry.compress()

            return result
        except (IndexError, KeyError, AttributeError):
            raise CompressionError("There was an error during compression")

    @staticmethod
    def decompress(data):
        try:
            if not isinstance(data, unicode):
                raise NotUnicodeError()

            length_limit = len(data) + 2
            data_set = _DataSet()
            while len(data) > 0 and len(data) != length_limit:
                manifest_entry = _ManifestEntry(data[0])
                compressed_data = data[1:manifest_entry.size]

                types = [_Int16, _Boolean, _Float, _String]
                type_instance = types[manifest_entry.type - 1](0, manifest_entry)

                type_instance.decompress(compressed_data)
                data_set.append(type_instance)
                length_limit = len(data)

                data = data[manifest_entry.size:len(data) + manifest_entry.size]

            return data_set
        except (IndexError, KeyError, AttributeError):
            raise DecompressionError("There was an error during decompression")
