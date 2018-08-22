#!/usr/bin/env python
# -*- coding: utf-8 -*-

from canon import Compressor

if __name__ == "__main__":
    data = {
        0: {
            "PuffleOs": 32,
            "BestTime": 16000,
            "TurboDone": True
        },
        1: {
            "PuffleOs": 32,
            "BestTime": 17,
            "TurboDone": True
        }
    }

    new_data_set = Compressor.load_data_set_from_object(data)
    compressed = Compressor.compress(new_data_set)
    print(compressed)

    decompressed = Compressor.decompress(compressed)

    new_data = Compressor.load_data_set_into_object(decompressed)
    print(new_data)