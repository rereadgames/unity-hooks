#!/usr/bin/env python3

import os
import unittest

from util import GitTestCase, newFile


class VersionTest(GitTestCase):
    def test_version_changes_to_platform_neutral_one_passes(self):
        ps_dir = os.path.join(self.dir, "ProjectSettings")
        os.mkdir(ps_dir)
        version = os.path.join(ps_dir, "ProjectVersion.txt")
        newFile(version, "m_EditorVersion: 5.5.0b1")
        self.repo.index.add([version])
        self.repo.index.commit("test")
        newFile(version, "m_EditorVersion: 5.5.1b1")
        self.repo.index.add([version])
        self.repo.index.commit("test")

    def test_version_changes_to_an_equivalent_platform_specific_one_fails(self):
        ps_dir = os.path.join(self.dir, "ProjectSettings")
        os.mkdir(ps_dir)
        version = os.path.join(ps_dir, "ProjectVersion.txt")
        newFile(version, "m_EditorVersion: 5.5.0b1")
        self.repo.index.add([version])
        self.repo.index.commit("test")
        newFile(version, "m_EditorVersion: 5.5.0xb1Linux")
        self.repo.index.add([version])
        with self.hookFails():
            self.repo.index.commit("test")

    def test_version_changes_to_a_different_platform_specific_one_passes(self):
        ps_dir = os.path.join(self.dir, "ProjectSettings")
        os.mkdir(ps_dir)
        version = os.path.join(ps_dir, "ProjectVersion.txt")
        newFile(version, "m_EditorVersion: 5.5.0b1")
        self.repo.index.add([version])
        self.repo.index.commit("test")
        newFile(version, "m_EditorVersion: 5.5.1xb1Linux")
        self.repo.index.add([version])
        self.repo.index.commit("test")

    def test_version_does_not_change_when_the_working_one_does_fails(self):
        ps_dir = os.path.join(self.dir, "ProjectSettings")
        os.mkdir(ps_dir)
        version = os.path.join(ps_dir, "ProjectVersion.txt")
        newFile(version, "m_EditorVersion: 5.5.0b1")
        self.repo.index.add([version])
        self.repo.index.commit("test")
        newFile(version, "m_EditorVersion: 5.5.1xb1Linux")
        derp =  os.path.join(ps_dir, "derp")
        newFile(derp, "herp")
        self.repo.index.add([derp])
        with self.hookFails():
            self.repo.index.commit("test")


if __name__ == "__main__":
    unittest.main()
