#!/usr/bin/env python3

import enum

from helpers import repository

META_EXT = ".meta"
ASSETS_DIR = "Assets"
FOLDER_METADATA_INDICATOR = "folderAsset: yes"


class File:
    def __init__(self, path, renamed_from_path=None):
        self.path = path
        self.renamed_from_path = renamed_from_path

    @property
    def is_metadata(self):
        return self.is_in_asset_dir and self.path.endswith(META_EXT)

    @property
    def is_asset(self):
        return self.is_in_asset_dir and not self.is_metadata

    @property
    def asset(self):
        if self.is_asset:
            return self
        else:
            return File(self.path[:-len(META_EXT)])

    @property
    def metadata(self):
        if self.is_metadata:
            return self
        else:
            return File(self.path + META_EXT)

    @property
    def is_in_asset_dir(self):
        return self.path.startswith(ASSETS_DIR)

    @property
    def working_dir(self):
        return WorkingDirFile(self)

    @property
    def staged(self):
        return StagedFile(self)

    @property
    def head(self):
        return HeadFile(self)

    @property
    def renamed_from(self):
        return File(self.renamed_from_path)

    def __eq__(self, other):
        return self.path == other.path

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash(self.path)

    def __repr__(self):
        return "File(\"{}\")".format(self.path)


class SourcedFile:
    def __init__(self, file):
        self.file = file

    @property
    def is_directory_metadata(self):
        return (self.file.is_metadata and
                FOLDER_METADATA_INDICATOR in self.content)

    @property
    def guid(self):
        for line in self.content.split("\n"):
            if line.startswith("guid:"):
                return line.split(" ")[1].strip()


class WorkingDirFile(SourcedFile):
    @property
    def content(self):
        return repository.get_working_dir_content_for(self.file.path)


class StagedFile(SourcedFile):
    @property
    def content(self):
        return repository.get_staged_content_for(self.file.path)

    @property
    def exists(self):
        return self.content is not None


class HeadFile(SourcedFile):
    @property
    def content(self):
        return repository.get_head_content_for(self.file.path)


class Files:
    @property
    def added(self):
        return {File(p) for _, p in repository.staged_paths(change_type="A")}

    @property
    def deleted(self):
        return {File(p) for _, p in repository.staged_paths(change_type="D")}

    @property
    def modified(self):
        return {File(p) for _, p in repository.staged_paths(change_type="M")}

    @property
    def renamed(self):
        return {File(p, rf) for rf, p in
                repository.staged_paths(change_type="R")}

    @property
    def likely_missed_deleted_metadata(self):
        return {file.renamed_from for file in Files.renamed}

    @property
    def likely_missed_added_metadata(self):
        return {File(file.path) for file in Files.renamed}

    @property
    def renames_likely_to_be_different_files(self):
        metadata_for_deleted_assets = \
            {file.metadata for file in Files.deleted if file.is_asset}

        metadata_for_added_assets = \
            {file.metadata for file in Files.added if file.is_asset}

        return {file for file in Files.renamed if file.is_metadata and
                file in metadata_for_deleted_assets and
                file in metadata_for_added_assets}

    @property
    def working_directory(self):
        return {File(p, rf) if ct == "R" else File(p)
                for rf, p, ct in repository.working_dir_paths()}

Files = Files()
