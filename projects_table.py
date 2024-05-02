"""
Generate a table of maintained projects

With thanks to https://github.com/gaborbernat/gaborbernat/

To print to console:

Put your projects in DETAILS
python3 -m pip install "prettytable >= 1"
python3 projects_table.py

To update README.md:

Place these markers in README.md where you want the table:

[start_generated]: # (start_generated)
[end_generated]: # (end_generated)

python3 projects_table.py --update
"""

from __future__ import annotations

import argparse

from prettytable import MARKDOWN, PrettyTable

DETAILS: dict[str, dict[str, str]] = {
    # "project": {
    #     "pypi": "python-example",  # only needed if different from "project"
    #     "slug": "org/example",  # only needed if different from "{project}/{project}"
    # },
    "Pillow": {
        "slug": "python-pillow/Pillow",
    },
    "pylast": {},
    "pypistats": {
        "slug": "hugovk/pypistats",
    },
    "pypinfo": {
        "slug": "ofek/pypinfo",
    },
    "norwegianblue": {
        "slug": "hugovk/norwegianblue",
    },
    "pepotron": {
        "slug": "hugovk/pepotron",
    },
    "termcolor": {
        "slug": "termcolor/termcolor",
    },
    "humanize": {
        "slug": "python-humanize/humanize",
    },
    "PrettyTable": {
        "slug": "jazzband/prettytable",
    },
    "Tablib": {
        "slug": "jazzband/tablib",
    },
    "UltraJSON": {
        "pypi": "ujson",
        "slug": "ultrajson/ultrajson",
    },
    "OSMViz": {
        "slug": "hugovk/osmviz",
    },
    "tinytext": {
        "slug": "hugovk/tinytext",
    },
    "em-keyboard": {
        "slug": "hugovk/em-keyboard",
    },
    "stravavis": {
        "slug": "marcusvolz/strava_py",
    },
    "flake8-implicit-str-concat": {
        "slug": "flake8-implicit-str-concat/flake8-implicit-str-concat",
    },
}


def update_readme(output: str) -> None:
    with open("README.md") as f:
        contents = f.read()

    before, delim1, _ = contents.partition("[start_generated]: # (start_generated)\n")
    _, delim2, after = contents.partition("[end_generated]: # (end_generated)\n")

    new_contents = before + delim1 + "\n" + output + "\n\n" + delim2 + after

    if contents == new_contents:
        print("No changes to README.md")
    else:
        with open("README.md", "w") as f:
            f.write(new_contents)
        print("README.md updated")


def badger(project: str) -> list[str]:
    pypi = DETAILS[project].get("pypi", project)
    slug = DETAILS[project].get("slug", f"{project}/{project}")
    url = f"https://github.com/{slug}"

    return [
        f"[{project}]({url})",
        f"[![PyPI version](https://img.shields.io/pypi/v/{pypi}?style=flat-square)](https://pypi.org/project/{pypi})",  # noqa: E501
        f"[![Supported Python versions](https://img.shields.io/pypi/pyversions/{pypi}.svg?style=flat-square)](https://pypi.org/project/{pypi}/)",  # noqa: E501
        f"[![GitHub last commit](https://img.shields.io/github/last-commit/{slug}?style=flat-square)]({url}/commits)",  # noqa: E501
        f"[![PyPI downloads](https://img.shields.io/pypi/dm/{pypi}?style=flat-square)](https://pypistats.org/packages/{pypi})",  # noqa: E501
    ]


def projects_table() -> PrettyTable:
    table = PrettyTable()
    table.field_names = [
        "Project",
        "Release",
        "Python versions",
        "Activity",
        "Downloads",
    ]
    table.align = "l"
    table.set_style(MARKDOWN)

    for project in DETAILS:
        table.add_row(badger(project))

    return table


class CustomFormatter(
    argparse.ArgumentDefaultsHelpFormatter,
    argparse.RawDescriptionHelpFormatter,
):
    pass


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=CustomFormatter
    )
    parser.add_argument(
        "-u", "--update", action="store_true", help="Update README.md with table"
    )
    args = parser.parse_args()

    table = projects_table()

    if args.update:
        update_readme(table.get_string())
    else:
        print(table)


if __name__ == "__main__":
    main()
