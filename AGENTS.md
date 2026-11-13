# Academic homepage

- Read `DIRECTORY_GUIDE.md` for the repository layout.
- Preserve the static HTML / GitHub Pages setup and the existing forest-green visual identity.
- Personal facts must come from the user's public homepage, README, or explicit user updates. Do not infer awards, skills, degrees, authorship contributions, or acceptance status from research projects.
- `cv.html` is the editable CV source. Run `scripts/build_cv.py` after changing its content; include the regenerated `assets/pdf/Jiantao_Shen_CV.pdf` in the same eventual change.
- Publication and education changes should be reflected in both the homepage and CV.
- Local QA belongs in ignored `work/`; never publish it. No Git commit or push without user authorization.
- This is document / static-web work. GPU, CUDA and PyTorch are not applicable.

## Verified local tooling

The Codex bundled Python has ReportLab and pypdf; no Conda environment or package changes are required. Discover the current bundled runtime again if the versioned path below is unavailable.

```powershell
$cvPython = 'C:\Program Files\WindowsApps\OpenAI.CodexPrimaryRuntime.v26-1111-574-0_26.1111.574.0_x64__3k8sg7r9htsxt\dependencies\python\python.exe'
& $cvPython scripts/build_cv.py
& $cvPython -m http.server 8765 --bind 127.0.0.1
```

Run these commands from `D:\Project_github\jiantaoshen12.github.io`. Preview `http://127.0.0.1:8765/` and `/cv.html`. Before delivery, check homepage/CV links, narrow-screen layout, and the rendered PDF.
