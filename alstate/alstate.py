import json
import os

_file = "_state.json"


class _StateVal:
    def __init__(self, name, default_val):
        self.name = name
        if name not in _state:
            _state[name] = default_val
            _store()

    def get(self):
        return get(self.name)

    def set(self, val):
        set(self.name, val)

    def __str__(self):
        return str(self.get())

    def __repr__(self):
        return self.get().__repr__()


state_val = _StateVal.__init__


def _exist():
    return _file in os.listdir("/")


def _load():
    if _exist():
        with open(_file) as f:
            return json.load(f)
    else:
        return {}


def _store():
    with open(_file, "w") as f:
        json.dump(_state, f)


def _reload():
    if not _exist() or not _load():
        _store()
    else:
        _state.update(_load())


def get(key):
    return _state.get(key)


def set(key, val):
    _state[key] = val
    _store()


_state = _load()
if not _state and not _exist():
    _store()
