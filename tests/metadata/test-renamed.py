#!/usr/bin/env python3

import os
import unittest

from util import GitTestCase, newFile


class RenamedTest(GitTestCase):
    def test_both_being_renamed_passes(self):
        assets_dir = os.path.join(self.dir, "Assets")
        os.mkdir(assets_dir)
        files = [
            os.path.join(assets_dir, "test.blah"),
            os.path.join(assets_dir, "test.blah.meta"),
        ]
        newFile(files[0], "asset")
        newFile(files[1], "metadata")
        self.repo.index.add(files)
        self.repo.index.commit("test")
        self.repo.index.remove(files)
        files = [
            os.path.join(assets_dir, "testrenamed.blah"),
            os.path.join(assets_dir, "testrenamed.blah.meta"),
        ]
        newFile(files[0], "asset")
        newFile(files[1], "metadata")
        self.repo.index.add(files)
        self.repo.index.commit("test")

    def test_just_the_asset_being_renamed_fails(self):
        assets_dir = os.path.join(self.dir, "Assets")
        os.mkdir(assets_dir)
        files = [
            os.path.join(assets_dir, "test.blah"),
            os.path.join(assets_dir, "test.blah.meta"),
        ]
        newFile(files[0], "asset")
        newFile(files[1], "metadata")
        self.repo.index.add(files)
        self.repo.index.commit("test")
        self.repo.index.remove([files[0]])
        files = [
            os.path.join(assets_dir, "testrenamed.blah"),
        ]
        newFile(files[0], "asset")
        self.repo.index.add(files)
        with self.hookFails():
            self.repo.index.commit("test")

    def test_just_the_metadata_being_renamed_fails(self):
        assets_dir = os.path.join(self.dir, "Assets")
        os.mkdir(assets_dir)
        files = [
            os.path.join(assets_dir, "test.blah"),
            os.path.join(assets_dir, "test.blah.meta"),
        ]
        newFile(files[0], "asset")
        newFile(files[1], "metadata")
        self.repo.index.add(files)
        self.repo.index.commit("test")
        self.repo.index.remove([files[1]])
        files = [
            os.path.join(assets_dir, "testrenamed.blah.meta"),
        ]
        newFile(files[0], "metadata")
        self.repo.index.add(files)
        with self.hookFails():
            self.repo.index.commit("test")

if __name__ == "__main__":
    unittest.main()
