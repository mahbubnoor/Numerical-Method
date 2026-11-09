# Numerical Methods (CSE-3107)

Interactive course materials for **CSE-3107 Numerical Methods**, B.Sc. 3rd Year 1st Semester,
Department of CSE, University of Barishal. Md Mahbub E Noor.

Open `index.html` in any browser. Everything works **offline**: fonts, formulas (KaTeX), and the
in-browser Python and C runners are all inside this folder.

## What is inside

| Folder | Contents |
|---|---|
| `index.html` | Course home: 25-lecture roadmap in 7 modules |
| `lectures/` | HTML slide decks (1920×1080, scaled to any screen) |
| `labs/` | One lab per lecture: explorer, solver for your own problem, coding tasks, practice questions with answers |
| `notes/` | Speaker notes and homework answers (**instructor edition only**: delete this folder for the student edition; the Notes button hides itself) |
| `assets/` | Viewer, widgets, MiniPy and MiniC interpreters, fonts, KaTeX |

## Using the slides

| Key | Action |
|---|---|
| <kbd>→</kbd> <kbd>Space</kbd> / <kbd>←</kbd> | next step / back (worked solutions build line by line) |
| <kbd>A</kbd> | reveal the whole slide |
| number + <kbd>Enter</kbd> | jump to a slide |
| <kbd>S</kbd> | slide list · <kbd>F</kbd> full screen · <kbd>N</kbd> notes |
| <kbd>[</kbd> <kbd>]</kbd> | previous / next lecture · <kbd>L</kbd> open the lab |
| <kbd>Ctrl</kbd>+<kbd>Enter</kbd> | run the code in a live code box |

## Live code

Code boxes run **Python** (MiniPy) and **C** (MiniC), small interpreters written for this course.
They cover what numerical methods need: loops, functions, lists/arrays (1-D and 2-D), `math`/`math.h`,
f-strings and `printf`, `input()`/`scanf()`, `float` vs `double`. NumPy is not available in the
browser; use ⤓ to download any program and run it in Jupyter or with `gcc file.c -lm` on the lab PC.

Every program in the course is run by `build.py --check` in real Python 3 and gcc, and in MiniPy/MiniC;
the outputs must match exactly, character for character.

## Building (for the instructor)

```
npm install katex@0.16.11     # once
python3 build.py --check      # builds site/ and verifies every program
```
Lecture content lives in `content/Lxx.py` (slides, speaker notes, code, lab), so editing a lecture
means editing one Python file.

## Licences

Course content: CC BY-NC-SA 4.0 (`LICENSE.md`). Code: MIT (`LICENSE-CODE.txt`).
Third-party: IBM Plex fonts (SIL OFL 1.1), KaTeX (MIT). See `THIRD-PARTY-NOTICES.md`.
