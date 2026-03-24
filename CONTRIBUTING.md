# Contributing Your Project

Thank you for participating! Follow these steps to submit your notebook project to the case gallery.

[中文版本](./CONTRIBUTING_ZH.md)

## Prerequisites

- A GitHub account
- Your project tested and running on **aup-learning-cloud Basic GPU Environment**

## Submission Steps

### 1. Fork this repository

Click **Fork** (top-right of this page) to create your own copy.

### 2. Create your project folder

Copy the `template/` directory into the correct activity folder. The final structure in this repo (after awards are announced) looks like this:

```
cases/
└── 2026-03-njupt-winter-battle/         ← activity folder
    ├── README.md                         ← activity overview & award list
    ├── 01-gold-teamalpha-llmchat/        ← 1st place (renamed by organizer)
    ├── 02-silver-teambeta-cvdetect/      ← 2nd place (renamed by organizer)
    ├── 03-bronze-teamgamma-robot/        ← 3rd place (renamed by organizer)
    └── teamdelta-nlpchat/                ← general submission (no prefix)
        ├── README.md                     ← English documentation (required)
        ├── README_ZH.md                  ← Chinese documentation (required)
        ├── requirements.txt
        ├── main.ipynb                    ← English notebook (required)
        ├── main_zh.ipynb                 ← Chinese notebook (required)
        └── assets/                       ← screenshots, GIFs (optional)
```

**Name your folder according to your result:**

| Result | Folder name format | Example |
|--------|--------------------|---------|
| 1st place (Gold) | `01-gold-teamname-projectslug` | `01-gold-teamalpha-llmchat` |
| 2nd place (Silver) | `02-silver-teamname-projectslug` | `02-silver-teambeta-cvdetect` |
| 3rd place (Bronze) | `03-bronze-teamname-projectslug` | `03-bronze-teamgamma-robot` |
| No award / workshop | `teamname-projectslug` | `teamdelta-nlpchat` |

> **Not submitting for a competition?** Just use `teamname-projectslug` with no prefix — same as the no-award format above.

**Naming rules:**
- Lowercase letters, numbers, hyphens only — no spaces or special characters
- Keep it short and descriptive (e.g. `teamalpha-llmchat`, `smith-image-caption`)

### 3. Fill in your README.md and README_ZH.md

Both documentation files are required:

- **`README.md`** — English version. Use the template in `template/README.md`. All fields marked `<!-- required -->` must be completed. Write in **English**.
- **`README_ZH.md`** — Chinese version. Use the template in `template/README_ZH.md`. All fields marked `<!-- 必填 -->` must be completed. Write in **Chinese**.

### 4. Add screenshots, GIFs, and demos (recommended)

Visuals make your project stand out. Include them in your `README.md` and `README_ZH.md`.

**What to include:**

| Type | Recommended content |
|------|-------------------|
| Screenshots | UI screenshots, inference results, charts |
| GIF | Short demo of the workflow (10–30 s) |
| Video | Link to an external video (Bilibili, YouTube) |

**How to include media in your README:**

```markdown
![demo](./assets/demo.gif)
![result](./assets/result.png)
```

Put all media files in an `assets/` folder inside your project directory.

**Video → GIF conversion tip:**

If your demo video is large, extract the key part and convert it to GIF:

```bash
# ffmpeg: trim from 0:05, duration 20 s, scale to 720px wide, 15 fps
ffmpeg -ss 00:00:05 -t 20 -i demo.mp4 \
  -vf "fps=15,scale=720:-1:flags=lanczos" \
  -loop 0 assets/demo.gif
```

> Keep each GIF under **10 MB** and the total `assets/` folder under **50 MB**.

### 5. List your dependencies

Edit `requirements.txt` with any pip packages your notebook needs.

**Do not include:** `torch`, `torchvision`, `rocm`-related packages — these are pre-installed in the Basic GPU Environment.

Leave the file empty (but present) if you have no extra dependencies.

### 6. Test in aup-learning-cloud

Before submitting, verify **both** notebooks run end-to-end:

1. Open aup-learning-cloud → select **Basic GPU Environment**
2. Run all cells in `main.ipynb` (English) from top to bottom — confirm no errors
3. Run all cells in `main_zh.ipynb` (Chinese) from top to bottom — confirm no errors

### 7. Submit a Pull Request

1. Commit and push your changes to your fork
2. Open a Pull Request to this repository
3. GitHub will show a checklist — **check every item before submitting**
4. Wait for the organizer to review and merge

## File Size Limit

Keep your submission under **100MB** total.

For large datasets or model weights, use an external link (Hugging Face, Google Drive, etc.) and reference it in your README.

## Questions?

Open a GitHub Issue or contact the competition organizer directly.
