from canon import _DataSet, _Int16, _String

MaxSongLength = 1024
ActionIds = range(-1, 53) + range(500, 508) + [100]


def load_data_set_into_object(data_set):
    song = {
        "SongName": data_set.entries[0].value,
        "Actions": [{
            "Time": data_set.entries[action].value,
            "Action": data_set.entries[action + 1].value
        } for action in xrange(1, len(data_set.entries) - 1, 2)]
    }

    return song


def load_data_set_from_object(data_object):
    data_set = _DataSet()

    data_set.append(_String(data_object["SongName"]))

    for action in data_object["Actions"]:
        data_set.append(_Int16(action["Time"]))
        data_set.append(_Int16(action["Action"]))
    return data_set
