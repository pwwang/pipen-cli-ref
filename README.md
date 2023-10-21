# pipen-cli-ref
Make reference documentation for [pipen][1] pipeline/processes

## Installation

```bash
pip install pipen-cli-ref
```

## Usage

```bash
pipen ref --help
```

```
Usage: pipen ref [-h] -p PIPELINE -d DESTDIR [-s] [-r REPLACE_TITLES]
                 [-i HIDE_SECTIONS]

Make API reference documentation for pipen pipeline/processes.

Required Arguments:
  -p PIPELINE, --pipeline PIPELINE
                        Specify the pipeline to generate the docs for, in the
                        format of `part1:part2` where `part1` could be either:
                        1. a package name that can be imported by
                        `importlib.import_module`, or
                        2. a submodule of a package, for example,
                        `package.module`; or
                        3. a path to a python file, for example,
                        `path/to/file.py`.
                        and `part2` is the name of the pipeline class.
                        When the module is loaded, the pipeline class will be
                        searched in the module.
  -d DESTDIR, --destdir DESTDIR
                        The destination directory to save the docs.

Options:
  -h, --help            show help message and exit
  -s, --show-hidden-items
                        Do not include hidden items.
  -r REPLACE_TITLES, --replace-titles REPLACE_TITLES
                        Replace the title of a section, in the format of
                        `old=new`. Multiple replacements can be specified.
  -i HIDE_SECTIONS, --hide-sections HIDE_SECTIONS
                        Hiden some sections in docstring
```

[1]: https://github.com/pwwang/pipen
