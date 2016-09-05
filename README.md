# Unity Git Hooks

Git hooks for Unity project.

Unity projects use `.meta` files to manage assets, but these can become inconsistent with the actual assets, especially
when mixed with version control. This can lead to conflicts.

Unity also seems to use multiple versions

## Features

- Stop committing if meta files are inconsistent - if a file is added, check it has a `.meta` file, if removed, check
  there isn't one, and do the same in reverse for meta files without base files.
- Delete empty asset directories after checkout and merge. Unity generates `.meta` files for empty asset directories,
  but git ignores them. This causes hanging `.meta` files.

## Usage

Run `install-hooks.sh` from within the repository you wish to add the hooks to. You may need to delete an exisitng
`.git/hooks` folder first.

If you have other hooks you want to run as well, instead make those hooks call these scripts.
