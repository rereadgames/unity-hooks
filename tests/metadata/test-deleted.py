#!/usr/bin/env python3

import os
import unittest

from util import GitTestCase, touch


class DeletedTest(GitTestCase):
    def test_both_being_deleted_passes(self):
        assets_dir = os.path.join(self.dir, "Assets")
        os.mkdir(assets_dir)
        files = [
            touch(assets_dir, "test.blah"),
            touch(assets_dir, "test.blah.meta"),
        ]
        self.repo.index.add(files)
        self.repo.index.commit("test")
        self.repo.index.remove(files)
        self.repo.index.commit("test")

    def test_just_the_metadata_being_deleted_fails(self):
        assets_dir = os.path.join(self.dir, "Assets")
        os.mkdir(assets_dir)
        files = [
            touch(assets_dir, "test.blah"),
            touch(assets_dir, "test.blah.meta"),
        ]
        self.repo.index.add(files)
        self.repo.index.commit("test")
        self.repo.index.remove(files[1:])
        with self.hookFails():
            self.repo.index.commit("test")

    def test_just_the_asset_being_deleted_fails(self):
        assets_dir = os.path.join(self.dir, "Assets")
        os.mkdir(assets_dir)
        files = [
            touch(assets_dir, "test.blah"),
            touch(assets_dir, "test.blah.meta"),
        ]
        self.repo.index.add(files)
        self.repo.index.commit("test")
        self.repo.index.remove(files[:1])
        with self.hookFails():
            self.repo.index.commit("test")

    def test_metadata_for_directory_can_be_deleted(self):
        assets_dir = os.path.join(self.dir, "Assets")
        os.mkdir(assets_dir)
        meta_name = os.path.join(assets_dir, "test.meta")
        with open(meta_name, "w") as file:
            file.write("folderAsset: yes")
        files = [meta_name]
        self.repo.index.add(files)
        self.repo.index.commit("test")
        self.repo.index.remove(files)
        self.repo.index.commit("test")


if __name__ == "__main__":
    unittest.main()
