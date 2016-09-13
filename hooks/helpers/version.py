#!/usr/bin/env python3

import os


VERSION_FILE = os.path.join("ProjectSettings", "ProjectVersion.txt")


def normalize(version):
    return version.replace("Linux", "").replace("x", "")


def extract_version(config):
    return config.split(" ")[1].strip()
