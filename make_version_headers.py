import sys
import os
import godot.methods
# pass in binary dir and source dir

src_dir = sys.argv[1]
tgt_dir = sys.argv[2]

print("make_version_headers.py")
print(f"Source Dir = {src_dir}, binary dir = {tgt_dir}")

savedPath = os.getcwd()
os.chdir(tgt_dir)

sys.path.append(src_dir)
godot.methods.generate_version_header();

os.chdir(savedPath)
