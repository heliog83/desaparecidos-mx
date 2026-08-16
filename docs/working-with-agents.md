# Working with Claude, Codex and other agents

This project is deliberately **agent-neutral**. Claude Code and Codex can both edit,
build and review it because the complete article lives in ordinary repository files.
No proprietary artifact surface is part of the workflow.

## Source of truth

The article has one directed build path:

```text
processed CSVs + article_draft.md + figure scripts
                         ↓
                src/build_page.py
                         ↓
              reports/article.html
                         ↓
                src/check_article.py
```

- Narrative source: `reports/article_draft.md`
- Data sources: `data/processed/`
- Static figures: `reports/figures/article/`
- Interactive code: `src/article_interactive.css` and
  `src/article_interactive.js`
- Generated deliverable: `reports/article.html`

The HTML is reproducible output. It must never acquire independent edits.

## Required agent workflow

From the repository root:

```bash
python src/build_page.py
python src/check_article.py
python -m http.server 8794 --directory reports
```

Open:

```text
http://127.0.0.1:8794/article.html
```

The checker compares the embedded chart data and headline values against the processed
CSVs. If it fails, fix the source prose or data; do not patch the generated HTML.

## Worktrees

Agents may work in separate Git worktrees. Before building or handing off, confirm the
current path with `git rev-parse --show-toplevel`. Never publish a similarly named file
from another checkout. The source, generated HTML and validation command must all come
from the same Git worktree and commit.

## Prohibited workflow

- Do not invoke Claude Code's `Artifact` tool.
- Do not create, update or pin a Claude Artifact version.
- Do not use a `claude.ai/code/artifact/...` URL as documentation or the canonical
  reading link.
- Do not paste a generated article into a chat and ask a model to reconstruct it.
- Do not recompute headline figures by hand during publication.
- Do not copy `reports/article.html` between the main checkout and a worktree.

These restrictions exist because an earlier Artifact update published stale data from
the main checkout while the corrected build lived in a worktree.

## External hosting, if requested later

Public hosting is a separate task and requires an explicit user decision. Prefer a
host that accepts ordinary static HTML and can be updated by either agent—for example,
GitHub Pages, Cloudflare Pages or another user-selected static host. Deploy only the
exact HTML that passed `src/check_article.py`, and keep the Git commit as the audit
trail.

Until such a host is selected, the canonical reading copy is the validated local file:
`reports/article.html`.
