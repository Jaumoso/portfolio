# Portfolio

Source of **[jaumoso.github.io/portfolio](https://jaumoso.github.io/portfolio/)** — my homelab, infrastructure and side projects.

Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and deployed to GitHub Pages by GitHub Actions.

## How it stays up to date

- `data/services.yml` — hand-written metadata for every self-hosted stack (category, description, what I use it for).
- `scripts/generate_services.py` — reads the list of active (`selfhosted/`) and retired (`unused/`) stacks from [Jaumoso/homelab](https://github.com/Jaumoso/homelab), merges it with the metadata and writes `docs/homelab/services.md`.
- `scripts/check_sensitive.py` — blocks a deploy if the site contains IP addresses, tokens, keys, home/mount paths or any pattern from the `SENSITIVE_PATTERNS` secret.
- `.github/workflows/deploy.yml` — runs weekly, on push, on demand and when the homelab repo sends a `homelab-updated` dispatch: regenerate → check → commit → build → deploy.

## Local development

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_services.py      # or --local ../homelab
python scripts/check_sensitive.py
mkdocs serve
```

## One-time setup

1. **Settings → Pages → Source: GitHub Actions.**
2. **Settings → Secrets → Actions → `SENSITIVE_PATTERNS`**: one regex per line with private values that must never be published (real IPs, usernames, ports, hostnames).
3. *(Optional)* trigger a rebuild when the homelab repo changes — add this step to a workflow in `Jaumoso/homelab`, with a fine-grained token (`contents: write` on this repo) stored as `PORTFOLIO_DISPATCH_TOKEN`:

   ```yaml
   - run: |
       curl -fsS -X POST \
         -H "Authorization: Bearer ${{ secrets.PORTFOLIO_DISPATCH_TOKEN }}" \
         -H "Accept: application/vnd.github+json" \
         https://api.github.com/repos/Jaumoso/portfolio/dispatches \
         -d '{"event_type":"homelab-updated"}'
   ```
