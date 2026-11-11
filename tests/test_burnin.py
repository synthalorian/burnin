"""CLI tests for burnin. These tests must not invoke ffmpeg."""

import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXAMPLE = (
    "ffmpeg -y -i in.mp4 -vf "
    "subtitles=in.srt:force_style='FontName=DejaVu Sans,FontSize=24,MarginV=40' "
    "out.mp4"
)


def run_burnin(*args):
    return subprocess.run(
        [sys.executable, "-m", "burnin", *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


class BurninTests(unittest.TestCase):
    def test_example_command(self):
        result = run_burnin(
            "--input",
            "in.mp4",
            "--subs",
            "in.srt",
            "--output",
            "out.mp4",
            "--font",
            "DejaVu Sans",
            "--size",
            "24",
            "--margin-v",
            "40",
            "--print",
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, EXAMPLE + "\n")
        self.assertNotIn("ffmpeg", result.stderr)

    def test_print_is_the_default(self):
        result = run_burnin(
            "--input",
            "in.mp4",
            "--subs",
            "in.srt",
            "--output",
            "out.mp4",
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, EXAMPLE + "\n")

    def test_path_with_a_space(self):
        expected = (
            "ffmpeg -y -i 'my video.mp4' -vf "
            "subtitles='my file.srt':force_style='FontName=DejaVu Sans,FontSize=24,MarginV=40' "
            "'out file.mp4'"
        )
        result = run_burnin(
            "--input",
            "my video.mp4",
            "--subs",
            "my file.srt",
            "--output",
            "out file.mp4",
            "--print",
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, expected + "\n")

    def test_subtitle_path_containing_a_single_quote(self):
        result = run_burnin(
            "--input",
            "in.mp4",
            "--subs",
            "in'.srt",
            "--output",
            "out.mp4",
            "--print",
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertNotIn("ffmpeg", result.stdout)
        self.assertNotIn("'\"'\"'", result.stdout)
        self.assertNotIn("'\"'\"'", result.stderr)

    def test_style_flags_are_inserted(self):
        expected = (
            "ffmpeg -y -i in.mp4 -vf "
            "subtitles=in.srt:force_style='FontName=Noto Sans,FontSize=18,MarginV=12' "
            "out.mp4"
        )
        result = run_burnin(
            "--input",
            "in.mp4",
            "--subs",
            "in.srt",
            "--output",
            "out.mp4",
            "--font",
            "Noto Sans",
            "--size",
            "18",
            "--margin-v",
            "12",
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, expected + "\n")

    def test_missing_input_exits_2(self):
        result = run_burnin("--subs", "in.srt", "--output", "out.mp4")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("ffmpeg -y", result.stdout)

    def test_missing_subs_exits_2(self):
        result = run_burnin("--input", "in.mp4", "--output", "out.mp4")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("ffmpeg -y", result.stdout)

    def test_missing_output_exits_2(self):
        result = run_burnin("--input", "in.mp4", "--subs", "in.srt")
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("ffmpeg -y", result.stdout)


if __name__ == "__main__":
    unittest.main()
