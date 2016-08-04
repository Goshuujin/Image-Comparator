# Author: David Allen
#
# Renames all hidden image files by removing the preceding '.'

import sys
import os
import test

def main(argv):
    path = "."
    if len(argv) == 1:
        path = argv[0]

    for root, dirs, files in os.walk(path):
        files = [f for f in files if test.is_image(os.path.join(path, f))]
        for f in files:
            if f[0] == ".":
                print("renaming file {}".format(f))
                full_path = os.path.join(path, f)
                full_rename = os.path.join(path, f[1:])
                os.rename(full_path, full_rename)
                print("file renamed to {}".format(f[1:]))


if __name__ == "__main__":
    main(sys.argv[1:])