#!/usr/bin/env python3

import os
import unittest

from util import GitTestCase, touch


class GuidTest(GitTestCase):
    def test_the_guid_remaining_the_same_passes(self):
        assets_dir = os.path.join(self.dir, "Assets")
        os.mkdir(assets_dir)
        asset = os.path.join(assets_dir, "test.blah")
        with open(asset, "w"):
            pass
        metadata = os.path.join(assets_dir, "test.blah.meta")
        with open(metadata, "w") as file:
            file.write("guid: testing")
        self.repo.index.add([asset, metadata])
        self.repo.index.commit("test")
        with open(metadata, "w") as file:
            file.write("somethingelse: new\nguid: testing")
        self.repo.index.add([metadata])
        self.repo.index.commit("test")

    def test_the_guid_changing_in_a_change_fails(self):
        assets_dir = os.path.join(self.dir, "Assets")
        os.mkdir(assets_dir)
        asset = os.path.join(assets_dir, "test.blah")
        with open(asset, "w"):
            pass
        metadata = os.path.join(assets_dir, "test.blah.meta")
        with open(metadata, "w") as file:
            file.write("guid: testing")
        self.repo.index.add([asset, metadata])
        self.repo.index.commit("test")
        with open(metadata, "w") as file:
            file.write("guid: changed")
        self.repo.index.add([metadata])
        with self.hookFails():
            self.repo.index.commit("test")

    def test_the_guid_changing_in_a_rename_fails(self):
        assets_dir = os.path.join(self.dir, "Assets")
        os.mkdir(assets_dir)
        asset = os.path.join(assets_dir, "test.blah")
        with open(asset, "w") as file:
            file.write("This is the asset.")
        metadata = os.path.join(assets_dir, "test.blah.meta")
        with open(metadata, "w") as file:
            file.write("Lots of junk to make this look the same for a rename. asdhjklhjklasdfhjklasdfhkljasdfhjkfsdhjkldfshjkasdf\nguid: testing")
        self.repo.index.add([asset, metadata])
        self.repo.index.commit("test")
        self.repo.index.remove([asset, metadata])
        asset = os.path.join(assets_dir, "testrenamed.blah")
        with open(asset, "w") as file:
            file.write("This is the asset.")
        metadata = os.path.join(assets_dir, "testrenamed.blah.meta")
        with open(metadata, "w") as file:
            file.write("Lots of junk to make this look the same for a rename. asdhjklhjklasdfhjklasdfhkljasdfhjkfsdhjkldfshjkasdf\nguid: changed")
        self.repo.index.add([metadata, metadata])
        with self.hookFails():
            self.repo.index.commit("test")

if __name__ == "__main__":
    unittest.main()
