# MudLab – Development Session Notes

## Summary of Changes (Session ending 2026-02-23)

### Primary Goals Accomplished
1. Created a Windows installer and portable ZIP for MudLab
2. Renamed everything from "PyXRD / 0.8.4" to "MudLab / 0.0.1"
3. Fixed a version mismatch error that blocked loading existing project files
4. Merged V5 branch to main and published GitHub release `v0.0.1`

---

## Files Created / Modified

### `pyxrd.iss` (created at repo root)
Inno Setup 6 script that packages the entire `data/` directory into a Windows installer.
- No admin rights required (`PrivilegesRequired=lowest`)
- Output: `dist\MudLab-0.0.1-Setup.exe`
- Excludes `__pycache__` and `.pyc` files
- Uses LZMA ultra64 compression

### `.github/workflows/build-installer.yml` (created)
GitHub Actions CI/CD workflow:
- Triggers on `v*` tags and manual `workflow_dispatch`
- Installs Inno Setup 6 via Chocolatey
- Builds the `.exe` installer using `pyxrd.iss`
- Creates a portable `.zip` containing `data/`, `README.txt`, `MudLab.bat`
- Uploads both as GitHub Actions artifacts
- Creates a GitHub Release and attaches both files when triggered by a tag

### `MudLab.bat` (created at repo root)
Portable launcher script for the no-install use case.
```bat
@echo off
"%~dp0data\bin\pyxrd.exe"
```
Users extract the ZIP anywhere and double-click this file.

### `data/lib/python3.8/site-packages/pyxrd/__version.py` (modified)
```python
__version__ = "0.0.1"
```
Changed from `0.8.4`.

### `data/lib/python3.8/site-packages/pyxrd/file_parsers/json_parser.py` (modified)
Removed a `RuntimeError` that rejected project files saved by a "newer" program version.
After the rebrand from `0.8.4` → `0.0.1`, all existing project files were blocked.
Replaced with an INFO log that allows loading to continue.

### `README.txt` (modified)
Updated to describe installer and portable options, referencing the GitHub Releases page.

---

## Key Technical Notes

- **Self-contained distribution**: The `data/` directory (≈255 MB) already bundles Python 3.8 + GTK DLLs + PyXRD. No PyInstaller or additional packaging was needed.
- **Version guard removal**: The version check in `json_parser.py` was a forward-compatibility guard (block files from future program versions). Rebranding to a lower version number (`0.0.1`) caused all existing files to appear "from the future". The guard was removed; no data integrity risk.
- **Pyro4 disabled**: `settings.py` uses only `DummyAsyncServerProvider`. Do not re-add `Pyro4AsyncServerProvider`.
- **`.pyc` files**: Always show as modified in `git status` — ignore them, never stage or commit them.

---

## Release Status

**v0.0.1 released successfully.**
Release page: `https://github.com/KazukiNoSuzaku/MudLab/releases/tag/v0.0.1`

Artifacts published:
- `MudLab-0.0.1-Setup.exe` — Windows installer (no admin required)
- `MudLab-0.0.1-Portable.zip` — extract and run `MudLab.bat`

### Workflow fixes applied
- Added `permissions: contents: write` (required for release creation)
- Removed Inno Setup version pin from Chocolatey install
- Fixed `SetupIconFile` path in `pyxrd.iss` (needed `data\` prefix)
- Added separate `AppIconInstalled` define for post-install icon paths
- Fixed `files:` globs in release step to use forward slashes (JS action requirement)

---

## Commit Format
Always use `HHMMddmmyyyy` (e.g. `195023022026` = 19:50 on 23 Feb 2026).
