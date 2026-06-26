# Contributing & Workflow

How this portfolio is developed, committed, and deployed. Read this before
making changes so commits stay clean and deploys stay boring.

---

## Branches

| Branch | Purpose |
|---|---|
| `main` | Clean, **forkable** base for the MLH cohort. Don't push personal content here. |
| `simplistic-redesign` | My personal branch — this is what the **live VPS serves**. |

Friends fork `main`. You work and deploy from your personal branch.

---

## Commit conventions — [Conventional Commits](https://www.conventionalcommits.org/)

Format:

```
<type>(optional scope): <short, lowercase, imperative description>
```

**Types:**

| Type | Use for |
|---|---|
| `feat` | new content/feature (a new section, page, work entry) |
| `fix` | a bug fix |
| `docs` | documentation only (this file, README) |
| `style` | visual/CSS or formatting that doesn't change behavior |
| `refactor` | code restructure, no behavior change |
| `chore` | tooling, deps, config, deploy scripts |
| `perf` / `test` / `ci` / `build` | as needed |

**Examples (from this repo's history going forward):**

```
feat: add week 1 page
feat: add production engineering tools to skills
fix: correct python-dotenv version pin
style: center content column
docs: add contributing + deploy workflow
chore(deploy): add /upd-port skill and deploy script
```

Rules of thumb: one logical change per commit, present-tense imperative
("add", not "added"), no trailing period, keep the subject under ~72 chars.

---

## Local development

```bash
source python3-virtualenv/bin/activate
flask --app app run --debug      # http://127.0.0.1:5000, auto-reloads on save
```

Where things live:

- **Content/data** (name, bio, work, education, skills, places, week 1): `app/__init__.py`
- **Pages**: `app/templates/` (`index.html`, `hobbies.html`, `week1.html`, shared `base.html`)
- **Social icons**: `app/templates/icons/*.svg`
- **Styles**: `app/static/styles/main.css`
- **Images/logos**: `app/static/img/`

---

## Deploying (the full update flow)

### One-time setup
```bash
cp scripts/deploy.example.env .deploy.env   # then fill in VPS_HOST etc. (gitignored)
ssh-add --apple-use-keychain ~/.ssh/id_ed25519   # cache the key passphrase once
```

### Every update
1. Make changes locally, check them at `http://127.0.0.1:5000`.
2. Deploy — either:
   - **`/upd-port`** (the Claude Code skill), or
   - `bash scripts/deploy.sh "feat: describe the change"`
3. That single command:
   - commits any pending changes on the **current branch** (use a Conventional Commit message),
   - pushes to `origin/<branch>`,
   - SSHes into the VPS, `git reset --hard origin/<branch>`, reinstalls deps,
   - restarts Flask in the `portfolio` `tmux` session.
4. Live at **http://thomas-lenh-portfolio.duckdns.org:5000**

### Manual fallback (if the script is ever unavailable)
```bash
# local
git add -A && git commit -m "feat: ..." && git push

# on the server
ssh root@<droplet-ip>
cd ~/mlh-portfolio-site
git pull
source python3-virtualenv/bin/activate
pip install -r requirements.txt          # only if requirements changed
tmux kill-session -t portfolio
tmux new-session -d -s portfolio "cd ~/mlh-portfolio-site && source python3-virtualenv/bin/activate && flask run --host=0.0.0.0"
```

---

## DuckDNS

- Domain: `thomas-lenh-portfolio.duckdns.org` → the droplet's (static) IP, port `5000`.
- The DigitalOcean IP is static, so no auto-updater is needed.
- If it stops resolving (`SERVFAIL`/`NXDOMAIN`), go to [duckdns.org](https://www.duckdns.org),
  confirm the IP, click **update ip**, then flush your local DNS:
  `sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder`.

---

## Secrets

- `.deploy.env` holds the VPS host + key password. It is **gitignored** and must
  never be committed — this repo gets forked.
- `.env` (Flask `URL` etc.) is also gitignored.
