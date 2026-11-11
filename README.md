# burnin

Build an ffmpeg command that burns subtitles into a video. It prints the command. It does not run ffmpeg unless asked.

Author: synthalorian

## Build

No build step. burnin uses the Python 3 standard library only.

```
python -m burnin --help
```

## Test

```
python -m unittest discover -s tests
```

Tests do not invoke ffmpeg.

## Usage

Print the ffmpeg command. `--print` is the default and may be omitted.

```
python -m burnin --input in.mp4 --subs in.srt --output out.mp4 --font "DejaVu Sans" --size 24 --margin-v 40 --print
```

That prints:

```
ffmpeg -y -i in.mp4 -vf subtitles=in.srt:force_style='FontName=DejaVu Sans,FontSize=24,MarginV=40' out.mp4
```

Defaults are `--font "DejaVu Sans"`, `--size 24`, and `--margin-v 40`. `--input`, `--subs`, and `--output` are required. A subtitle path that contains a single quote is rejected and the process exits 2.

Run the printed command:

```
python -m burnin --input in.mp4 --subs in.srt --output out.mp4 --run
```
