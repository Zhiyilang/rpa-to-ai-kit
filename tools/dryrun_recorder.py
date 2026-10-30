#!/usr/bin/env python3
"""dryrun_recorder.py — record real RPA/automation calls, replay them as mocks.

Problem it solves
-----------------
You have an 影刀 / UiBot / Playwright flow that hits external systems
(click, type, call an API, read a cell). In CI or on a dev machine you
cannot run it for real. Wrap the risky calls with `record_or_replay`:

  * record mode  -> runs for real, saves each (name, args, result) to a JSON tape
  * replay mode  -> returns the saved result, so the *rest* of your pipeline
                    (transformations, assertions, downstream logic) still runs
                    and is fully testable offline.

Zero dependencies. Tapes are plain JSON.

Example
-------
    from dryrun_recorder import record_or_replay

    @record_or_replay("tape.json", mode="replay")
    def click_login(button):
        ...  # real automation here; never runs in replay mode
        return "ok"

MIT License.
"""
import json
import os
import functools


class Tape:
    def __init__(self, path):
        self.path = path
        self._calls = []
        if os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as f:
                    self._calls = json.load(f)
            except (ValueError, OSError):
                self._calls = []

    def _key(self, name, args, kwargs):
        return json.dumps({"name": name, "args": args, "kwargs": kwargs},
                          sort_keys=True, default=str)

    def record(self, name, args, kwargs, result):
        self._calls.append({
            "name": name, "args": list(args), "kwargs": kwargs,
            "result": result,
        })
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._calls, f, ensure_ascii=False, indent=2)

    def replay(self, name, args, kwargs):
        key = self._key(name, args, kwargs)
        for c in self._calls:
            if self._key(c["name"], c["args"], c["kwargs"]) == key:
                return c["result"]
        raise KeyError(f"no recorded call for {name}{tuple(args)}{kwargs}")


def record_or_replay(tape_path, mode="auto"):
    """Decorator. mode: 'record' | 'replay' | 'auto'.

    'auto' replays when the tape exists, otherwise records.
    """
    def decorate(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            tape = Tape(tape_path)
            effective = mode
            if effective == "auto":
                effective = "replay" if os.path.exists(tape_path) else "record"
            if effective == "replay":
                return tape.replay(fn.__name__, args, kwargs)
            result = fn(*args, **kwargs)
            tape.record(fn.__name__, args, kwargs, result)
            return result
        return wrapper
    return decorate


if __name__ == "__main__":
    # self-test
    import tempfile, shutil
    d = tempfile.mkdtemp()
    tape = os.path.join(d, "t.json")

    calls = {"n": 0}

    @record_or_replay(tape, mode="record")
    def fetch_user(uid):
        calls["n"] += 1
        return {"uid": uid, "name": "alice"}

    assert fetch_user(1) == {"uid": 1, "name": "alice"}
    assert calls["n"] == 1  # ran for real

    # now replay: real fn must NOT run, saved result returned
    @record_or_replay(tape, mode="replay")
    def fetch_user(uid):
        calls["n"] += 1  # would increment if it ran
        return {"uid": uid, "name": "alice"}

    assert fetch_user(1) == {"uid": 1, "name": "alice"}
    assert calls["n"] == 1  # still 1 -> real fn did NOT run
    print("dryrun_recorder self-test: OK")
    shutil.rmtree(d)
