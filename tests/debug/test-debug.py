#!/usr/bin/env python3

import os
import unittest

from util import GitTestCase, newFile


class AddedTest(GitTestCase):
    def test_file_containing_debug_log_fails(self):
        assets_dir = os.path.join(self.dir, "Assets")
        os.mkdir(assets_dir)
        source_file = os.path.join(assets_dir, "test.cs")
        newFile(source_file, "Debug.Log(\"test\");")
        self.repo.index.add([source_file])
        with self.hookFails():
            self.repo.index.commit("test")


if __name__ == "__main__":
    unittest.main()
