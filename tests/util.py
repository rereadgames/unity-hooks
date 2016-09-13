#!/usr/bin/env python3

import os
import shutil
import tempfile
import unittest

import git


def touch(path, file):
    full_path = os.path.join(path, file)
    with open(full_path, "w"):
        pass
    return full_path


def newFile(path, contents):
    with open(path, "w") as file:
        file.write(contents)


def install_hooks(path):
    target_dir = os.path.join(path, ".git", "hooks")
    script_dir = os.path.dirname(os.path.realpath(__file__))
    hooks_dir = os.path.abspath(os.path.join(script_dir, "..", "hooks"))
    hooks = [file[:-2] for file in os.listdir(hooks_dir)
             if os.path.isdir(os.path.join(hooks_dir, file)) and
             file.endswith(".d")]
    delegate = os.path.join(hooks_dir, "delegate.py")
    for hook in hooks:
        os.symlink(delegate, os.path.join(target_dir, hook))


class GitTestCase(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.repo = git.Repo.init(self.dir)
        install_hooks(self.dir)

    def tearDown(self):
        shutil.rmtree(self.dir)

    def hookFails(self):
        return self.assertRaises(git.exc.HookExecutionError)
