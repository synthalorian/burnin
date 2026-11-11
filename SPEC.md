# burnin

Python 3 stdlib only. Tests must not invoke ffmpeg.

## Test command

`python -m unittest discover -s tests`

## Command

`burnin --input in.mp4 --subs in.srt --output out.mp4 --font "DejaVu Sans" --size 24 --margin-v 40 --print`

`--print` is the default. Print a single shell-quoted command to stdout:

`ffmpeg -y -i in.mp4 -vf subtitles=in.srt:force_style='FontName=DejaVu Sans,FontSize=24,MarginV=40' out.mp4`

Rules for the filter argument:

- The subtitles path is inserted after `subtitles=`.
- If the path contains `'`, reject it and exit 2. Do not try to escape it.
- FontName and FontSize and MarginV come from the flags.
- Default font is `DejaVu Sans`, default size is 24, default margin-v is 40.
- Shell-quote each ffmpeg argument so spaces survive. Print the quoted command as one line.

`--run` executes that command. Tests must not pass `--run`.

Missing `--input`, `--subs`, or `--output` exits 2.

## Tests

Assert the exact printed command for the example above, a path with a space, and a subtitle path containing a single quote.
