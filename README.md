# Breathe

Cardiac Coherence breathing exercise from the comfort of your Unix terminal.

Feeling stressed out? Say no more!
Start `breathe.py` and follow along.

![](breathe.gif)

Breathe in calmly and evenly as the marker sweeps the terminal from the left
to the right, breathe out as the marker comes back to the left hand side.
Repeat. A five minute session will have a long relaxing calming effect.

## Usage

`breathe.py` provides 2 parameters to tweak inhalation and exhalation durations.
Both default to 5.5 seconds, but some may prefer slightly shorter or longer
durations for each phase. Popular timings are 5-5, 5-6 or even 6-6.

Another parameter limits the session time.

Halt the program with `Ctrl+C`.

```
usage: breathe.py [-h] [-i IN_DURATION] [-o OUT_DURATION] [-t SESSION_DURATION]

Cardiac Coherence breathing exercice from the confort of your Unix terminal.

options:
  -h, --help       show this help message and exit
  -i IN_DURATION   breathe in duration in seconds
  -o OUT_DURATION  breathe out duration in seconds
  -t SESSION_DURATION  session duration in minutes
```
