#!/usr/bin/env python3

import os

import git

META_EXT = ".meta"
ASSETS_DIR = "Assets"

MULTIPLE_STAGED_ERROR = "Multiple files staged for '{}'."


def repo():
    if not repo.repo:
        repo.repo = git.Repo(search_parent_directories=True)
    return repo.repo
repo.repo = None


def staged_paths(*, change_type):
    return paths(repo().head.commit.diff(), change_type=change_type)


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


def is_directory_metadata(metadata):
    return "folderAsset: yes" in metadata


def get_head_content_for(path):
    return repo().head.commit.tree[path].data_stream.read().decode("utf-8")


def in_asset_dir(*paths):
    return all(path.startswith(ASSETS_DIR) for path in paths)


def is_metadata(*paths):
    return all(path.endswith(META_EXT) for path in paths)


def metadata_for(paths):
    return {metadata_name(path) for path in paths}


def assets_for(paths):
    return {asset_name(path) for path in paths}


def metadata_name(path):
    if isinstance(path, str):
        return path + META_EXT
    else:
        return metadata_name(path[0]), metadata_name(path[1])


def asset_name(path):
    if isinstance(path, str):
        return path[:-len(META_EXT)]
    else:
        return asset_name(path[0]), asset_name(path[1])


def added():
    return {p for p, _ in staged_paths(change_type="A") if in_asset_dir(p)}


def added_assets():
    return {p for p in added() if not is_metadata(p)}


def added_metadata():
    return {p for p in added() if is_metadata(p)}


def deleted():
    return {p for p, _ in staged_paths(change_type="D") if in_asset_dir(p)}


def deleted_assets():
    return {p for p in deleted() if not is_metadata(p)}


def deleted_metadata():
    return {p for p in deleted() if is_metadata(p)}


def modified():
    return {p for p, _ in staged_paths(change_type="M") if in_asset_dir(p)}


def modified_assets():
    return {p for p in modified() if not is_metadata(p)}


def modified_metadata():
    return {p for p in modified() if is_metadata(p)}


def renamed():
    return {r for r in staged_paths(change_type="R") if in_asset_dir(*r)}


def renamed_assets():
    return {r for r in renamed() if not is_metadata(*r)}


def renamed_metadata():
    return {r for r in renamed() if is_metadata(*r)}


def deleted_metadata_mistaken_as_rename():
    return {d for d, _ in likely_mistaken_renames()}


def added_metadata_mistaken_as_rename():
    return {a for _, a in likely_mistaken_renames()}


def likely_mistaken_renames():
    metadata_for_deleted_assets = metadata_for(deleted_assets())
    metadata_for_added_assets = metadata_for(added_assets())
    for old_name, new_name in renamed_metadata():
        if (old_name in metadata_for_deleted_assets and
                new_name in metadata_for_added_assets):
            yield old_name, new_name
