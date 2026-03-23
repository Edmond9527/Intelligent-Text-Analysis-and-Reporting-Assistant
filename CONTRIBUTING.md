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

Copy the `template/` directory into the correct activity folder:

```
cases/
└── 2026-03-njupt-winter-battle/    ← your competition's folder
    └── yourteamname-projectslug/   ← your new folder (copy of template/)
        ├── README.md               ← English documentation (required)
        ├── README_ZH.md            ← Chinese documentation (required)
        ├── requirements.txt
        ├── main.ipynb              ← English notebook (required)
        └── main_zh.ipynb           ← Chinese notebook (required)
```

**Folder naming rules:**
- Format: `teamname-projectslug` (e.g. `teamalpha-llmchat`)
- Lowercase letters, numbers, hyphens only — no spaces or special characters
- Keep it short and descriptive

> **Note on awards:** Do NOT add award prefixes (`01-gold-`, `02-silver-`, `03-bronze-`) yourself.
> The organizer will rename folders after competition results are announced.

### 3. Fill in your README.md and README_ZH.md

Both documentation files are required:

- **`README.md`** — English version. Use the template in `template/README.md`. All fields marked `<!-- required -->` must be completed. Write in **English**.
- **`README_ZH.md`** — Chinese version. Use the template in `template/README_ZH.md`. All fields marked `<!-- 必填 -->` must be completed. Write in **Chinese**.

### 4. List your dependencies

Edit `requirements.txt` with any pip packages your notebook needs.

**Do not include:** `torch`, `torchvision`, `rocm`-related packages — these are pre-installed in the Basic GPU Environment.

Leave the file empty (but present) if you have no extra dependencies.

### 5. Test in aup-learning-cloud

Before submitting, verify **both** notebooks run end-to-end:

1. Open aup-learning-cloud → select **Basic GPU Environment**
2. Run all cells in `main.ipynb` (English) from top to bottom — confirm no errors
3. Run all cells in `main_zh.ipynb` (Chinese) from top to bottom — confirm no errors

### 6. Submit a Pull Request

1. Commit and push your changes to your fork
2. Open a Pull Request to this repository
3. GitHub will show a checklist — **check every item before submitting**
4. Wait for the organizer to review and merge

## File Size Limit

Keep your submission under **100MB** total.

For large datasets or model weights, use an external link (Hugging Face, Google Drive, etc.) and reference it in your README.

## Award Markers

After results are announced, the organizer will rename winning submissions:

| Award | Folder prefix | Example |
|-------|--------------|---------|
| 1st place (Gold) | `01-gold-` | `01-gold-teamalpha-llmchat` |
| 2nd place (Silver) | `02-silver-` | `02-silver-teambeta-cvdetect` |
| 3rd place (Bronze) | `03-bronze-` | `03-bronze-teamgamma-robot` |
| No award | _(no prefix)_ | `teamdelta-nlpchat` |

You do not need to include this in your folder name when submitting — the organizer handles this after the competition.

## Questions?

Open a GitHub Issue or contact the competition organizer directly.
