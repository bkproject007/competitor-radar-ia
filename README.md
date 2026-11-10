# Competitor Radar AI

GitHub owner: `bkproject007`  
Repository: `https://github.com/bkproject007/competitor-radar-ia`  
Planned website: `https://bkproject007.github.io/competitor-radar-ia/`

Bilingual landing page and Python-based public competitor-page change monitor.

## Run locally

Requires Python 3.12+; no packages to install.

```bash
python -m unittest discover -s tests -v
python -m src.monitor
```

The monitor reads `config/competitors.example.json`, saves hashes to `data/state.json` and writes `reports/latest.md`. On the first run, all successfully checked sites are `baseline`; later runs report `changed` or `unchanged`.

## GitHub Actions

Open **Actions > Monitor public competitor pages > Run workflow**. Reports are downloadable as workflow artifacts. The workflow is also scheduled daily at 12:15 UTC (GitHub may delay scheduled runs). State is restored from Actions cache on a best-effort basis; cache eviction can reset the baseline. For production, use durable storage instead.

## Publish landing page

Go to **Settings > Pages > Build and deployment > Deploy from a branch**, select `main` and `/ (root)`, then Save. The contact email is configured as `bkpersonal@gmail.com`.

## Limitations and safety

- Detects visible text changes, not structured prices or semantic significance.
- Some sites block automated requests; errors are reported, not bypassed.
- Use only sites where monitoring is permitted, respect terms and robots policies, and keep request frequency low.
- No credentials, private client data or API keys should be committed.
- Does not send email or accept payments.

## First publication checklist

1. Use the existing public repository `bkproject007/competitor-radar-ia`.
2. Upload all files including `.github/workflows/monitor.yml`, preferably with GitHub Desktop.
3. Confirm the configured contact email `bkpersonal@gmail.com`.
4. Enable GitHub Pages from `main` and `/ (root)`.
5. Open Actions, run `Monitor public competitor pages`, and inspect the uploaded `competitor-report` artifact.
6. Do not interpret an initial baseline as evidence of competitor changes.
