#!/usr/bin/env python3

import sys
import os
from contextlib import suppress

from natsort import natsorted
import envoy
try:
    import colorama
except ImportError:
    colorama = None

# Possible git hooks. (from http://githooks.com/)
GIT_HOOKS = """\
applypatch-msg
pre-applypatch
post-applypatch
pre-commit
prepare-commit-msg
commit-msg
post-commit
pre-rebase
post-checkout
post-merge
pre-receive
update
post-receive
post-update
pre-auto-gc
post-rewrite
pre-push""".split("\n")

BULLET_POINTS = "*-+=#~"

PASS = " ✓ PASS"
WARN = " ! WARN"
FAIL = " ✗ FAIL"


def bullet(depth):
    return BULLET_POINTS[depth % len(BULLET_POINTS)]


def title(name):
    return " ".join(name.split("-")[1:]).capitalize() + "."


def print_item(prefix, depth, name, state, suffix):
    point = bullet(depth)
    spaces = " " * (depth * 4)
    print("{}{} {} {:<60} {}{}".format(
        prefix, spaces, point, title(name), state, suffix))


def indent(text, depth):
    padding = " " * (depth * 4)
    return padding + "\n{0}".format(padding).join(text.split("\n")).rstrip()


if __name__ == "__main__":
    if colorama:
        colorama.init()

    script_path = os.path.dirname(os.path.realpath(__file__))

    hook = os.path.basename(sys.argv[0])
    if hook not in GIT_HOOKS:
        print("This script must be run as a hook.", file=sys.stderr)
        sys.exit(2)

    fail = False

    print(" {0} {1} hooks".format(bullet(0), hook.capitalize()))

    fail_prefix = ""
    warn_prefix = ""
    pass_prefix = ""
    suffix = ""
    if colorama:
        fail_prefix = colorama.Fore.RED
        warn_prefix = colorama.Fore.YELLOW
        pass_prefix = colorama.Fore.GREEN
        suffix = colorama.Style.RESET_ALL

    scripts_path = os.path.join(script_path, hook + ".d")
    for subdir, dirs, files in natsorted(os.walk(scripts_path)):
        groups = [group for group in os.path.relpath(subdir, scripts_path).split(os.path.sep) if group != "."]
        if any(not (group[0] == "." or group[0].isdigit()) for group in groups):
            continue
        depth = len(groups)
        if files and depth > 0:
            print_item("", depth, groups[-1], "", "")
        for filename in natsorted(files):
            if not filename[0].isdigit():
                continue
            path = os.path.join(subdir, filename)
            file_depth = depth + 1
            result = envoy.run(path, timeout=2)
            out_depth = file_depth + 1
            out = indent(result.std_out, out_depth) if result.std_out else None
            err = indent(result.std_err, out_depth) if result.std_err else None
            if result.status_code:
                fail = True
                print_item(fail_prefix, file_depth, filename, FAIL, suffix)
                if err:
                    print(fail_prefix + err + suffix)
                if out:
                    print(fail_prefix + out + suffix)
            else:
                if not err:
                    print_item(pass_prefix, file_depth, filename, PASS, suffix)
                else:
                    print_item(warn_prefix, file_depth, filename, WARN, suffix)
                if err:
                    print(warn_prefix + err + suffix)
                if out:
                    if not err:
                        print(out)
                    else:
                        print(warn_prefix + out + suffix)

    if fail:
        sys.exit(1)
    else:
        sys.exit(0)
