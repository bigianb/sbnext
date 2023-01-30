import sys
from godot.core.core_builders import make_authors_header, make_donors_header, make_license_header

# pass in binary dir and source dir

src_dir = sys.argv[1]
tgt_dir = sys.argv[2]

print("make_core_headers.py")
print(f"Source Dir = {src_dir}, binary dir = {tgt_dir}")

authors_md = src_dir + "/AUTHORS.md"
authors_gen = tgt_dir + "/core/authors.gen.h"
make_authors_header([authors_gen], [authors_md], "")
print(f"wrote {authors_gen}")

# Donors
donors_md = src_dir + "/DONORS.md"
donors_gen = tgt_dir + "/core/donors.gen.h"
make_donors_header([donors_gen], [donors_md], "")
print(f"wrote {donors_gen}")

# License
license_gen = tgt_dir + "/core/license.gen.h"
input_files = [src_dir + "/COPYRIGHT.txt", src_dir + "/LICENSE.txt"]
make_license_header([license_gen], input_files, "")
print(f"wrote {license_gen}")

