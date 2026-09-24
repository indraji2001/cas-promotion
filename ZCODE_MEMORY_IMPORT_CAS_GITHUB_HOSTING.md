# ZCode Portable Memory — CAS GitHub Pages Hosting Workflow

> **How to use this file with a new ZCode account/install:**
> 1. Keep this file anywhere on your computer (it is a plain Markdown text file).
> 2. In a new ZCode session, say: *"Read ZCODE_MEMORY_IMPORT_CAS_GITHUB_HOSTING.md in the project folder, learn it, and save it to your persistent memory."*
> 3. The new account's ZCode will read it and store it in its own memory directory, and will apply it from then on.
>
> (There is currently no automatic import/sync of memories between ZCode accounts — memory files are stored per-account, per-project on the local machine at `C:\Users\<you>\.zcode\cli\memories\`. This file is the manual bridge.)

---

## Learned Workflow: Hosting a large (>10 MB) interactive HTML app on GitHub Pages with a WhatsApp rich preview card

**Source:** `COMPLETE_ZCODE_GITHUB_HOSTING_MANUAL.txt` in this folder, prepared by Dr. Indrajit Chakraborty & Antigravity AI Engineering, September 2026. Read that manual for full detail before doing any hosting work.

**Why this matters:** Early in the project, ZCode implied the task was impossible. The actual blocker was only missing GitHub authentication — not a technical limitation. Once the user approved the one-time device code, the entire pipeline was executable by an agent. Future updates must be applied unaided.

### Step-by-step pipeline

1. **Check authentication first:** `gh auth status`. If not logged in, have the user run
   `gh auth login --web -h github.com -p https`
   and approve the 8-character device code at https://github.com/login/device in their browser. This is the ONLY step requiring the user. Offer this proactively the moment a GitHub task is blocked on credentials.
2. **Wire up credentials:** `gh auth setup-git` (Git then authenticates via the stored token, no prompts).
3. **Initialize repo:** `git init -b main`. Create a `.gitignore` immediately — privacy safeguard:
   `*.pdf`, `*.py`, `*.json`, `*.bat`, `*.ps1`, `__pycache__/`, `.vscode/`, `.zcodeignore`
   (source PDFs, OCR caches, and local scripts must never go public).
4. **Cover screenshot:** render page 1 of the HTML with Playwright headless Chromium at exactly 1200×630 px → save as `cas-og.jpg`, JPEG quality ~88, MUST be under 300 KB.
5. **Open Graph tags** in `<head>` of the HTML (absolute HTTPS URLs, no relative paths):
   `og:type`, `og:site_name`, `og:title`, `og:description`, `og:url`, `og:image` + `og:image:secure_url` / `type` / `width` (1200) / `height` (630) / `alt`, plus `twitter:card` = `summary_large_image` with matching title/description/image.
6. **Dual-file strategy:** the named file uses underscores (no `%20` in shared links) AND an identical copy named `index.html` at repo root so the base URL doesn't 404.
7. **Push via Git CLI packfile protocol** (handles >10 MB reliably, unlike the web uploader's 10 MB limit or the REST contents API's 25 MB cap):
   `gh repo create <user>/<repo> --public --source=. --remote=origin --push`
8. **Activate Pages via REST API** — creating the repo does NOT enable Pages:
   `gh api --method POST /repos/<user>/<repo>/pages -f "source[branch]=main" -f "source[path]=/"`
   Poll `gh api repos/<user>/<repo>/pages` until `"status": "built"`.
9. **Verify like a crawler:** fetch the live URL with User-Agent `facebookexternalhit/1.1` and confirm HTTP 200 and that all OG tags appear in the first ~8 KB of the response.
10. **Future updates:** `update_github.bat` in this folder does 1-click sync (copies named HTML → `index.html`, commits with timestamp, pushes; GitHub Pages rebuilds in ~60 seconds).

### WhatsApp preview rules

- Link must be HTTPS (GitHub Pages provides valid SSL).
- `og:image` must be an ABSOLUTE URL; image ≥300×200 px, ideally 1200×630; under 300 KB; JPEG or PNG. Otherwise WhatsApp silently drops the preview card.
- **Unfurl pause:** after pasting a link, wait 2–3 seconds until the preview card appears above the input box before pressing Send.
- **Cache bypass:** WhatsApp caches failed/no-preview results per chat for days. Re-share with a cache-busting query (e.g. `?v=2`) or in a fresh chat ("Message yourself").

### Current deployment (for reference)

- Repository: https://github.com/indraji2001/cas-promotion
- Live root: https://indraji2001.github.io/cas-promotion/
- Live named file: https://indraji2001.github.io/cas-promotion/CAS_2026_Govt-Aided_Colleges_Interactive_Presentation.html
