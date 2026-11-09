# Numerical Methods (CSE-3107)

Interactive course materials for **CSE-3107 Numerical Methods**, B.Sc. 3rd Year 1st Semester,
Department of CSE, University of Barishal. Md Mahbub E Noor.

**Live site:** [Here](https://mahbubnoor.github.io/Numerical-Method/)
25 lectures in 7 modules: floating point and errors, roots of equations, linear systems,
interpolation, numerical differentiation and integration, ODEs, and data fitting and optimisation
for machine learning. Every lecture has an HTML slide deck with live widgets and runnable Python and C
code, and a lab page with a solver for your own problems, coding tasks and practice questions.

Everything is static and self-contained (fonts, KaTeX and the in-browser Python/C interpreters are in
`assets/`), so the same folder also works offline: download it and open `index.html`.
## Contents

| Path | Contents |
|---|---|
| `index.html` | Course home: roadmap of all 25 lectures |
| `lectures/` | Slide decks (1920×1080, scaled to any screen) |
| `labs/` | One lab per lecture |
| `assets/` | Viewer, widgets, MiniPy and MiniC interpreters, fonts, KaTeX |
| `notes/` | Speaker notes and homework answers |
| `_source/` | Build script, lecture content (`content/Lxx.py`), tests |

This is the **instructor edition**. It also contains `notes/` (speaker notes and homework answers,
shown with the Notes button or the <kbd>N</kbd> key) and `_source/` (the build files: `build.py`,
lecture content, tests). In a public repository both are visible to anyone, students included.
To rebuild the site after editing a lecture, see the Building section of `README_offline.md`.


## Using the slides

| Key | Action |
|---|---|
| <kbd>→</kbd> <kbd>Space</kbd> / <kbd>←</kbd> | next step / back |
| <kbd>A</kbd> | reveal the whole slide |
| number + <kbd>Enter</kbd> | jump to a slide |
| <kbd>S</kbd> slide list · <kbd>F</kbd> full screen | |
| <kbd>[</kbd> <kbd>]</kbd> previous / next lecture · <kbd>L</kbd> open the lab | |
| <kbd>Ctrl</kbd>+<kbd>Enter</kbd> | run the code in a live code box |

Code boxes run Python (MiniPy) and C (MiniC), small interpreters written for this course. Use ⤓ to
download a program and run it with Python 3 or `gcc file.c -lm`.

## Licences

Course content: CC BY-NC-SA 4.0 (`LICENSE.md`). Code: MIT (`LICENSE-CODE.txt`).
Third-party: IBM Plex fonts (SIL OFL 1.1), KaTeX (MIT). See `THIRD-PARTY-NOTICES.md`.
