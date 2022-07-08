import glob
import os
import subprocess
import fnmatch
from dotenv import load_dotenv  # todo: replace with builtin


# - Utils
def list_files(path, pattern=None, recursive=True):
    if not recursive:
        fns = os.listdir(path)
    else:
        # glob.glob('**/*') is slower 2.5 times than simple os.walk. It also returns directories
        fns = []
        for root, dirs, files in os.walk(path):
            fns += [os.path.join(root, fn) for fn in files]
    if pattern:
        fns = [fn for fn in fns if fnmatch.fnmatch(fn, pattern)]
    return fns


# - Function
def run_files_by_pattern(pattern, root=None, add_env=False):
    if not root:
        root = "."

    fns = list_files(root, pattern)

    current_dir = os.getcwd()

    for fn in fns:
        subprocess.call(f"chmod +x {fn}", shell=True)
        os.chdir(os.path.dirname(fn))

        if add_env and os.path.exists(".env"):
            load_dotenv()
        print("PLATFORM!!!!!!!!!!", os.environ.get("PLATFORM", "PLATFORM NOT SPECIFIED"))
        subprocess.call("./" + os.path.basename(fn), shell=True)
        os.chdir(current_dir)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("pattern")
    parser.add_argument("--root")

    args = parser.parse_args()
    run_files_by_pattern(args.pattern, args.root)
