import re
import os
import subprocess
import sys

# - Utils


def bisect_left(a, x, lo=0, hi=None, *, key=None):
    """Return the index where to insert item x in list a, assuming a is sorted.
    The return value i is such that all e in a[:i] have e < x, and all e in
    a[i:] have e >= x.  So if x already appears in the list, a.insert(i, x) will
    insert just before the leftmost x already there.
    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """

    if lo < 0:
        raise ValueError("lo must be non-negative")
    if hi is None:
        hi = len(a)
    # Note, the comparison uses "<" to match the
    # __lt__() logic in list.sort() and in heapq.
    if key is None:
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] < x:
                lo = mid + 1
            else:
                hi = mid
    else:
        while lo < hi:
            mid = (lo + hi) // 2
            if key(a[mid]) < x:
                lo = mid + 1
            else:
                hi = mid
    return lo


def _execute_command(cmd):
    if isinstance(cmd, list):
        cmd = " ".join(cmd)
    return subprocess.check_output(cmd.split()).decode().strip()


# - Git Functions
def get_branch_name():
    return _execute_command("git rev-parse --abbrev-ref HEAD")


def get_sanitized_branch_name():
    return get_branch_name().replace("/", "-")


def get_commit_short_sha():
    return _execute_command("git rev-parse --short HEAD")


def _parse_branches_log(branches_log):
    branches = re.findall(r"\S+", branches_log)
    branches = [branch for branch in branches if branch != "*"]
    return branches


def list_branches():
    """feature/add_linting
      feature/dev
    * master"""
    branches_log = _execute_command("git branch")
    return _parse_branches_log(branches_log)


def get_master_branch_name():
    branches = list_branches()
    for variant in ["main", "master"]:
        if variant in branches:
            return variant

    raise Exception("Couldn't find master branch")


def get_path():
    master_branch = get_master_branch_name()
    if get_branch_name() == master_branch:

        inner_desc = _execute_command('git describe --tags --match "release*" --candidates 100 --always')
        if "release" not in inner_desc:
            # no release found

            # find number of commits
            git_log = _execute_command("git log")
            commits = re.findall(r"commit (\S+)", git_log)
            n_commits = len(commits)

            return f"release-0.0.0-{n_commits}-{get_commit_short_sha()}"

        latest_release = _execute_command("git describe --abbrev=0")
        if inner_desc == latest_release:
            # release-0.2.33
            return inner_desc
        else:
            # 'release-0.2.33-7-g07b7bc1'
            split = inner_desc.rsplit("-", 2)  # ['release-0.2.33', '7', 'g07b7bc1']
            split = [split[0], split[1], split[2][1:]]  # ['release-0.2.33', '7', '07b7bc1']
            return "-".join(split)
    else:
        # custom branch

        # - Find how much commits past master/main branch
        git_log = _execute_command("git log")
        commits = re.findall(r"commit (\S+)", git_log)

        # find number of commits after branching from master branch
        def _is_master_branch_commit(commit):
            return master_branch in _parse_branches_log(_execute_command(f"git branch --contains {commit}"))

        n_commits = bisect_left(commits, 1, key=lambda commit: int(_is_master_branch_commit(commit)))
        return "-".join([get_sanitized_branch_name(), str(n_commits), get_commit_short_sha()])


def get_commit_id(suffix=None):
    if not suffix:
        return get_path()
    return "--".join([get_path(), suffix])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--suffix")
    args = parser.parse_args()
    print(get_commit_id(suffix=args.suffix or "local"))
