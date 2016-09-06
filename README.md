# Unity Git Hooks

Git hooks for Unity project.

Unity projects use `.meta` files to manage assets, but these can become inconsistent with the actual assets, especially
when mixed with version control. This can lead to conflicts.

Unity also seems to use platform-specific versioning, that can result in ping-pong commits of the project version.

## Features

- Stop committing if meta files are inconsistent - if a file is added, check it has a `.meta` file, if removed, check
  there isn't one, if moved, check it was also moved, and do the same in reverse for meta files without base files.
  The GUID is also checked for consistency, stopping the case that Unity generated a new one after accidental deletion.
- Delete empty asset directories after checkout and merge. Unity generates `.meta` files for empty asset directories,
  but git ignores them. This causes hanging `.meta` files.
- Check for version problems due to platform-specific versioning.

## Usage

Requires Python 3.5. Do a `pip install -r requirements.txt` to get the dependencies.

For Windows/Gitbash users the default python3 installation will not add a "python3" executable to the path. To add one
yourself simply ensure that the python3 installation directory is on the path and add a symbolic link from "python.exe"
to "python3.exe" as such:

cd [python installation dir]
mklink "python3.exe" "python.exe"

The result should be a link file called "python3.exe" in the python installation directory pointing at "python.exe".

Run `install-hooks.sh`/`install-hooks.bat` from within the repository you wish to add the hooks to.
