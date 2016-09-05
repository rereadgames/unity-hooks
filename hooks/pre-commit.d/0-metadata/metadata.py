#!/usr/bin/env python3

import git

META_EXT = ".meta"
ASSETS_DIR = "Assets"


def staged_paths(*, change_type):
    repo = git.Repo(search_parent_directories=True)
    return paths(repo.head.commit.diff(), change_type=change_type)


def paths(diffs, *, change_type):
    for diff in diffs.iter_change_type(change_type):
        yield (diff.a_path, diff.b_path)
