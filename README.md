# Canon

**This library is new and relatively untested, please be cautious when choosing to use this for your project.**

Canon is a tool for emulating the compression found in two of the Club Penguin mini-games.

- [Sound Studio](https://icer.ink/media1.clubpenguin.com/play/v2/games/mixmaster)
- [Puffle Launch](https://icer.ink/media1.clubpenguin.com/play/v2/games/canon)

Canon was written for the Club Penguin server emulator, [Houdini](https://github.com/solero/houdini), however it may be used for other emulators or perhaps generating your own game saves.

The compression algorithm was taken from the Club Penguin client (`com.clubpenguin.lib.data.compression.Compressor`).

The library currently only has utility functions for converting Puffle Launch game saves into objects, however it can convert any compressed string into a `Canon._DataSet`.

## Installation

Canon is now available on the PyPI, hurray!

`pip install Canon`

~~Canon is not available on PyPI. You have to clone the repository and import it manually.~~

` $ git clone https://github.com/ketnipz/canon`

## Usage

### Decompressing a game save
This is the most common usage, and it how the library is used inside Houdini.

```py
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Canon import Compressor
from Canon.Data.Launch import load_data_set_into_object

if __name__ == "__main__":
	decompressed = Compressor.decompress(u"Ȑ Ȑ ȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȐ㺀ȐȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȠȑȑŀ")
	new_data = load_data_set_into_object(decompressed, filtered=True)
	print(new_data)

	# Result: {0: {'PuffleOs': 32, 'BestTime': 16000, 'TurboDone': True}, 1: {'PuffleOs': 32, 'BestTime': 17, 'TurboDone': True}}
```

### Generating a save game
Whilst canon can be used to convert a unicode save game into an object, it can also be used to do the reverse!

```py
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Canon import Compressor
from Canon.Data.Launch import load_data_set_from_object

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

    new_data_set = load_data_set_from_object(data)
    compressed = Compressor.compress(new_data_set)
    print(compressed)
    
    # Result: u"Ȑ Ȑ ȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȑȐ㺀ȐȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȐɘȠȑȑŀ"
```

### Filter flag

`load_data_set_into_object` has a parameter `filtered`. This can be used to filter level results which have not been completed yet. Since Puffle Launch game saves contain the data for every level, you may just want the ones which have been completed, if this is the case, pass `filter= True` into the function.

```py
new_data = Compressor.load_data_set_into_object(decompressed)
print(new_data)
# Result: {0: {'PuffleOs': 32, 'BestTime': 16000, 'TurboDone': True}, 1: {'PuffleOs': 32, 'BestTime': 17, 'TurboDone': True}, 2: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 3: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 4: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 5: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 6: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 7: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 8: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 9: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 10: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 11: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 12: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 13: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 14: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 15: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 16: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 17: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 18: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 19: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 20: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 21: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 22: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 23: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 24: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 25: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 26: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 27: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 28: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 29: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 30: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 31: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 32: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 33: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 34: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}, 35: {'PuffleOs': 0, 'BestTime': 600, 'TurboDone': False}}

```


```py
new_data = Compressor.load_data_set_into_object(decompressed, filtered=True)
print(new_data)
# Result: {0: {'PuffleOs': 32, 'BestTime': 16000, 'TurboDone': True}, 1: {'PuffleOs': 32, 'BestTime': 17, 'TurboDone': True}}
```


