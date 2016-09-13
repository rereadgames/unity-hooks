#!/usr/bin/env python3

import os

import git


MULTIPLE_STAGED_ERROR = "Multiple files staged for '{}'."


EMPTY_COMMIT = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def repo():
    if not repo.repo:
        repo.repo = git.Repo(search_parent_directories=True)
    return repo.repo
repo.repo = None


def staged_paths(*, change_type):
    r = repo()
    if r.active_branch.is_valid():
        diff = r.head.commit.diff()
    else:
        diff = r.tree(EMPTY_COMMIT).diff(staged=True)
    return paths(diff, change_type=change_type)


def working_dir_paths():
    r = repo()
    if r.active_branch.is_valid():
        for diff in r.head.commit.diff(None):
            yield (diff.a_path, diff.b_path, diff.change_type)
    else:
        return


def paths(diffs, *, change_type):
    for diff in diffs.iter_change_type(change_type):
        yield (diff.a_path, diff.b_path)


def get_working_dir_content_for(path):
    with open(os.path.join(repo().working_dir, path)) as f:
        return f.read()


def get_staged_content_for(path):
    content = None
    for (stage, blob) in repo().index.iter_blobs(lambda e: e[1].path == path):
        if content is not None:
            raise Exception(MULTIPLE_STAGED_ERROR.format(path))
        content = blob.data_stream.read().decode("utf-8")
    return content


def get_head_content_for(path):
    return repo().head.commit.tree[path].data_stream.read().decode("utf-8")
