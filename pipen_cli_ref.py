"""Make API reference documentation for pipen pipeline/processes.

If some processes are conditional, you can use `pipen.utils.is_loading_pipeline()` to
include them conditionally. For example:

```diff
- if some_condition:
+ if some_condition or is_loading_pipeline():
    class Process(Proc):
        ...
"""
from __future__ import annotations
from typing import TYPE_CHECKING, Type

import sys
import asyncio
import textwrap

import argx
from pipen.utils import load_pipeline
from pipen.cli import CLIPlugin
from pipen_annotate import annotate

if TYPE_CHECKING:
    from pipen import Proc
    from pipen_annotate.sections import Mixin

__version__ = "0.3.0"

args = argx.ArgumentParser(
    description=("Make API reference documentation for pipen pipeline/processes.")
)


def format_section(
    section: Mixin,
    title_prefix: str | bool = "## ",
    title: str = None,
    show_hidden: bool = False,
) -> str:
    """Format a section.

    Args:
        section: The section object.

    Returns:
        The formatted section.
    """
    formatted = textwrap.dedent(section.to_markdown(show_hidden))
    if title_prefix is False:
        return formatted

    title = title or section._get_meta("name")
    return f"{title_prefix}{title}\n\n{formatted}"


def generate_doc(proc: Type[Proc], args: argx.Namespace, i: int, total: int) -> None:
    """Generate the API reference documentation for a process.

    Args:
        proc: The process class.
        args: The parsed arguments.
        i: The index of the process (1-based).
        total: The total number of processes.
    """
    print(f"- [{i}/{total}] Generating doc for {proc.name} ...")
    anno = annotate(proc)
    summary = format_section(
        anno.Summary,
        title_prefix=False,
        show_hidden=args.show_hidden_items,
    )
    doc = f"# {proc.name}\n\n{summary}\n\n"
    title_replaces = {}
    for oldnew in args.replace_titles or []:
        if "=" not in oldnew:
            print(
                f"Invalid replacement: {oldnew}. Should be in the format of `old=new`.",
                file=sys.stderr,
            )
            sys.exit(1)
        old, new = oldnew.split("=", 1)
        title_replaces[old] = new

    for key, val in anno.items():
        if key == "Summary" or key in (args.hide_sections or ()):
            continue

        key = title_replaces.get(key, key)
        val = format_section(val, title=key, show_hidden=args.show_hidden_items)
        if val.rstrip("\n").lstrip("#").strip() == key:
            continue

        doc += f"{val}\n\n"

    for rep in args.replace or []:
        if "=" not in rep:
            print(
                f"Invalid replacement: {rep}. Should be in the format of `old=new`.",
                file=sys.stderr,
            )
            sys.exit(1)
        old, new = rep.split("=", 1)
        doc = doc.replace(old, new)

    destfile = f"{args.destdir}/{proc.name}.md"
    with open(destfile, "w", encoding="utf8") as fout:
        fout.write(doc)


async def main(args: argx.Namespace) -> None:
    """Generate the API reference documentation for all processes.

    Args:
        args: The parsed arguments.
    """
    pipeline = await load_pipeline(args.pipeline)

    total = len(pipeline.procs)
    for i, proc in enumerate(pipeline.procs):
        generate_doc(proc, args, i + 1, total)


class PipenCliRefPlugin(CLIPlugin):
    """Make API reference documentation for pipen pipeline/processes."""

    version = __version__
    name = "ref"

    def __init__(
        self,
        parser: argx.ArgumentParser,
        subparser: argx.ArgumentParser,
    ) -> None:
        super().__init__(parser, subparser)
        subparser.add_argument(
            "-p",
            "--pipeline",
            required=True,
            help="\n".join((
                "Specify the pipeline to generate the docs for, in the format of "
                "`part1:part2` where `part1` could be either: ",
                "1. a package name that can be imported by `importlib.import_module`, "
                "or ",
                "2. a submodule of a package, for example, `package.module`; or ",
                "3. a path to a python file, for example, `path/to/file.py`.",
                "and `part2` is the name of the pipeline class.",
                "When the module is loaded, the pipeline class will be searched in "
                "the module."
            )),
        )
        subparser.add_argument(
            "-d",
            "--destdir",
            required=True,
            help="The destination directory to save the docs."
        )
        subparser.add_argument(
            "-s",
            "--show-hidden-items",
            action="store_true",
            help="Do not include hidden items.",
        )
        subparser.add_argument(
            "-r",
            "--replace-titles",
            action="append",
            help=(
                "Replace the title of a section, in the format of `old=new`. Multiple "
                "replacements can be specified."
            )
        )
        subparser.add_argument(
            "-i",
            "--hide-sections",
            action="append",
            help="Hiden some sections in docstring"
        )
        subparser.add_argument(
            "--replace",
            action="append",
            help="Replace placeholders in the docstring in the format of `old=new`."
        )

    def exec_command(self, args: argx.Namespace) -> None:
        """Execute the command"""
        asyncio.run(main(args))
