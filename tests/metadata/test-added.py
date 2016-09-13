#!/usr/bin/env python3

import os
import unittest

from util import GitTestCase, touch


class AddedTest(GitTestCase):
    def test_both_added_passes(self):
        assets_dir = os.path.join(self.dir, "Assets")
        os.mkdir(assets_dir)
        self.repo.index.add([
            touch(assets_dir, "test.blah"),
            touch(assets_dir, "test.blah.meta"),
        ])
        self.repo.index.commit("test")

    def test_just_the_asset_added_fails(self):
        assets_dir = os.path.join(self.dir, "Assets")
        os.mkdir(assets_dir)
        self.repo.index.add([
            touch(assets_dir, "test.blah"),
        ])
        with self.hookFails():
            self.repo.index.commit("test")

    def test_just_the_metadata_added_fails(self):
        assets_dir = os.path.join(self.dir, "Assets")
        os.mkdir(assets_dir)
        self.repo.index.add([
            touch(assets_dir, "test.blah.meta"),
        ])
        with self.hookFails():
            self.repo.index.commit("test")

    def test_adding_metadata_for_folders_passes(self):
        assets_dir = os.path.join(self.dir, "Assets")
        os.mkdir(assets_dir)
        meta_name = os.path.join(assets_dir, "test.meta")
        with open(meta_name, "w") as file:
            file.write("folderAsset: yes")
        files = [meta_name]
        self.repo.index.add(files)
        self.repo.index.commit("test")


if __name__ == "__main__":
    unittest.main()
