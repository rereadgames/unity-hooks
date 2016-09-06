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


def in_asset_dir(*paths):
    return all(path.startswith(ASSETS_DIR) for path in paths)


def is_metadata(*paths):
    return all(path.endswith(META_EXT) for path in paths)


def metadata_for(paths):
    return {metadata_name(path) for path in paths}


def assets_for(paths):
    return {asset_name(path) for path in paths}


def metadata_name(path):
    return path + META_EXT


def asset_name(path):
    return path[:-len(META_EXT)]


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
