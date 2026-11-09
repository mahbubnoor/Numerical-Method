# Numerical Methods (CSE-3107)

Interactive course materials for **CSE-3107 Numerical Methods**, B.Sc. 3rd Year 1st Semester,
Department of CSE, University of Barishal. Md Mahbub E Noor.

**Live site:** `https://<your-github-username>.github.io/<repository-name>/`
(replace the two placeholders after publishing; see below)

25 lectures in 7 modules: floating point and errors, roots of equations, linear systems,
interpolation, numerical differentiation and integration, ODEs, and data fitting and optimisation
for machine learning. Every lecture has an HTML slide deck with live widgets and runnable Python and C
code, and a lab page with a solver for your own problems, coding tasks and practice questions.

Everything is static and self-contained (fonts, KaTeX and the in-browser Python/C interpreters are in
`assets/`), so the same folder also works offline: download it and open `index.html`.

## Publishing this folder with GitHub Pages

1. **Create a repository** on GitHub, e.g. `Numerical-Methods` (Public; GitHub Pages on a free
   account needs a public repository). Do not add a README, licence or .gitignore there; this folder
   already has them.
2. **Upload the files.** The repository root must contain `index.html` (not a sub-folder).
   - *Command line* (recommended; run inside this folder):
     ```
     git init
     git add .
     git commit -m "Course site"
     git branch -M main
     git remote add origin https://github.com/<your-github-username>/<repository-name>.git
     git push -u origin main
     ```
   - *Web browser:* on the empty repository page click **uploading an existing file**, then drag
     **the contents** of this folder (not the folder itself) into the page and commit. The web
     uploader takes at most 100 files per commit: if it complains, upload `assets/` in a second
     commit. Your computer may hide the file `.nojekyll`; if it was not uploaded, use
     **Add file → Create new file**, name it `.nojekyll`, leave it empty and commit.
3. **Turn on Pages:** repository **Settings → Pages → Build and deployment → Source: Deploy from a
   branch**, Branch **main**, folder **/ (root)**, **Save**.
4. Wait one or two minutes. The address appears at the top of the Pages settings
   (`https://<your-github-username>.github.io/<repository-name>/`). Put it in the line at the top of
   this README.

To update the site later, replace the changed files and commit again; Pages redeploys automatically.

## Contents

| Path | Contents |
|---|---|
| `index.html` | Course home: roadmap of all 25 lectures |
| `lectures/` | Slide decks (1920×1080, scaled to any screen) |
| `labs/` | One lab per lecture |
| `assets/` | Viewer, widgets, MiniPy and MiniC interpreters, fonts, KaTeX |

This is the **student edition**: speaker notes and homework answers are not included. Keep the
instructor edition (with `notes/` and the `_source/` build files) out of this public repository,
for example in a separate private repository.

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
