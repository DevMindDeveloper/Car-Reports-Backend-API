## custom function for dict retrieving
def find_dict(dicts, key, value):
    for d in dicts:
        if d.get(key) == value:
            return d
