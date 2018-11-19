#!/usr/bin/env python
# -*- coding: utf-8 -*-

from canon import Compressor
from canon.data.studio import load_data_set_from_object, load_data_set_into_object

if __name__ == "__main__":
    sample_song = {
        "SongName": "Hello world",
        "Actions": [
            {"Time": 10, "Action": 1}
        ]
    }

    new_data_set = load_data_set_from_object(sample_song)
    compressed = Compressor.compress(new_data_set)

    decompressed = Compressor.decompress(compressed)

    new_data = load_data_set_into_object(decompressed)
    print(new_data)
