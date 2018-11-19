from canon import _DataSet, _Int16, _Boolean, _String

LevelCount = 36


def load_data_set_into_object(data_set, filtered=False):
    levels = {
        level: {
            "PuffleOs": data_set.entries[level].value,
            "BestTime": data_set.entries[level + LevelCount].value,
            "TurboDone": bool(data_set.entries[72 + level / 16].bit(level % 16))
        }
        for level in xrange(LevelCount) if not filtered or not (
            data_set.entries[level].value == 0 and data_set.entries[level + LevelCount].value == 600)}

    return levels


def load_data_set_from_object(data_object):
    data_set = _DataSet()

    for level in xrange(LevelCount):
        if level in data_object:
            data_set.append(_Int16(data_object[level]["PuffleOs"]))
        else:
            data_set.append(_Int16())

    for level in xrange(LevelCount):
        if level in data_object:
            data_set.append(_Int16(data_object[level]["BestTime"]))
        else:
            data_set.append(_Int16(600))

    for _ in xrange(3):
        data_set.append(_Boolean())

    for level in xrange(LevelCount):
        if level in data_object:
            data_set.entries[72 + level / 16].bit(level % 16, int(data_object[level]["TurboDone"]))

    for level_modifier in xrange(3):
        if data_set.entries[72 + level_modifier].value == 0:
            data_set.entries[72 + level_modifier] = _Int16(0)

    data_set.append(_String())

    return data_set
