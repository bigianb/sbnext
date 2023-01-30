import sys
from godot.core.object.make_virtuals import run

run(sys.argv[1:], "", "")
print(f"wrote {sys.argv[1]}")

