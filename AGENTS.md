# Agent instructions — Desaparecidos MX

These instructions apply to Codex, Claude Code and any other coding agent working in
this repository. Read `CLAUDE.md` for research context, but treat the rules below as
the current delivery contract.

## Local-first article contract

1. **Git is the source of truth.** Edit `reports/article_draft.md`, data, figures or
   build code; never hand-edit a hosted copy of the article.
2. **Do not use Claude Artifacts.** Do not invoke an `Artifact` tool, publish to a
   `claude.ai/code/artifact/...` URL, or present an Artifact URL as the canonical
   article. That surface is agent-specific and can drift from the repository.
3. **Build and validate locally:**

   ```bash
   python3 src/build_page.py
   python3 src/check_article.py
   ```

   Publication or handoff is blocked unless both commands succeed. Both are
   standard-library only and work on a clean checkout: the publication data is
   committed under `data/publication_freezes/`, and the checker hash-verifies it
   before comparing the HTML against it. Do not repoint the build at
   `data/processed/` — that directory is mutable and `src/fetch_flow.py` overwrites
   it with live figures that do not match the pinned article.
4. **Preview the generated file locally:**

   ```bash
   python3 -m http.server 8794 --directory reports
   ```

   Open `http://127.0.0.1:8794/article.html`.
5. **Commit the complete unit.** Commit source prose, build code, figures and the
   generated `reports/article.html` together. Never copy an HTML file from another
   checkout or worktree.
6. **External publication requires an explicit user request.** If requested later,
   publish the exact validated `reports/article.html` through an agent-neutral host
   chosen by the user. Do not silently substitute Claude Artifacts.
7. **Preserve user work.** Ignore unrelated dirty files, especially local editor or
   launch configuration, unless the user explicitly asks to change them.

Full workflow: [docs/working-with-agents.md](docs/working-with-agents.md).
