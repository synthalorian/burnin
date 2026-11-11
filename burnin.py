#!/usr/bin/env python3
"""Print or run an ffmpeg command that burns subtitles into a video."""

import argparse
import shlex
import subprocess
import sys

DEFAULT_FONT = "DejaVu Sans"
DEFAULT_SIZE = 24
DEFAULT_MARGIN_V = 40


def build_parser():
    parser = argparse.ArgumentParser(
        prog="burnin",
        description="Print or run an ffmpeg command that burns subtitles into a video.",
    )
    parser.add_argument("--input", required=True, help="input video path")
    parser.add_argument("--subs", required=True, help="subtitle file path")
    parser.add_argument("--output", required=True, help="output video path")
    parser.add_argument("--font", default=DEFAULT_FONT, help="subtitle font name")
    parser.add_argument("--size", type=int, default=DEFAULT_SIZE, help="subtitle font size")
    parser.add_argument(
        "--margin-v",
        type=int,
        default=DEFAULT_MARGIN_V,
        help="vertical subtitle margin",
    )
    parser.add_argument(
        "--print",
        action="store_true",
        help="print the ffmpeg command (default)",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="execute the ffmpeg command",
    )
    return parser


def format_command(input_path, subs, output, font, size, margin_v):
    """Return one shell-quoted ffmpeg command line.

    The force_style value is wrapped in single quotes so a font name with
    spaces survives the shell. Path arguments are quoted the same way.
    A subtitle path containing a single quote is rejected before this runs.
    """
    vf = (
        f"subtitles={shlex.quote(subs)}:force_style="
        f"'FontName={font},FontSize={size},MarginV={margin_v}'"
    )
    parts = [
        "ffmpeg",
        "-y",
        "-i",
        shlex.quote(input_path),
        "-vf",
        vf,
        shlex.quote(output),
    ]
    return " ".join(parts)


def ffmpeg_argv(input_path, subs, output, font, size, margin_v):
    """Argv equivalent of format_command(), without shell quoting."""
    vf = f"subtitles={subs}:force_style=FontName={font},FontSize={size},MarginV={margin_v}"
    return ["ffmpeg", "-y", "-i", input_path, "-vf", vf, output]


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if "'" in args.subs:
        print("error: subtitle path must not contain a single quote", file=sys.stderr)
        return 2
    if args.run:
        completed = subprocess.run(
            ffmpeg_argv(args.input, args.subs, args.output, args.font, args.size, args.margin_v)
        )
        return completed.returncode
    print(
        format_command(args.input, args.subs, args.output, args.font, args.size, args.margin_v)
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
