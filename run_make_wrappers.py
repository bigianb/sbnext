import sys
from godot.core.extension.make_wrappers import run
from godot.core.extension.make_interface_dumper import run as run_dumper

# pass in binary dir and source dir

src_dir = sys.argv[1]
tgt_dir = sys.argv[2]

ext_wrappers_inc_file = tgt_dir + "/core/extension/ext_wrappers.gen.inc"

run([ext_wrappers_inc_file], "", "")
print(f"wrote {ext_wrappers_inc_file}")

gdextension_interface_dump = tgt_dir + "/core/extension/gdextension_interface_dump.gen.h"
gdextension_interface = src_dir + "/core/extension/gdextension_interface.h"
run_dumper([gdextension_interface_dump], [gdextension_interface], "")
print(f"wrote {gdextension_interface_dump}")
