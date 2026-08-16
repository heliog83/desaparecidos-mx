"""Build the self-contained HTML article from reports/article_draft.md.

Single source of truth is the markdown draft: this converts it, inlines every
figure in reports/figures/article/ as a base64 data URI, and writes one file that
depends on nothing external (required — the Artifact CSP blocks all remote hosts).

The draft's internal scaffolding (working titles, figure production notes) is
dropped; the standfirst and methods note are lifted into their own treatments.

Output: reports/article.html  (~2 MB, mostly embedded PNGs)
Run:    python src/build_page.py
"""
from __future__ import annotations

import base64
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFT = ROOT / "reports" / "article_draft.md"
FIGDIR = ROOT / "reports" / "figures" / "article"
OUT = ROOT / "reports" / "article.html"

TITLE = "The Redacted Crisis"
SUBTITLE = "What Mexico's registry of the disappeared won't let you see"

# Field readout for the hero: exactly what the public registry returns for a
# confidential record. Structure only — no person, no invented identifiers.
HERO_FIELDS = [
    ("ENTIDAD", "JALISCO", False),
    ("FECHA_DESAPARICION", "CONFIDENCIAL", True),
    ("SEXO", "CONFIDENCIAL", True),
    ("EDAD", "CONFIDENCIAL", True),
    ("MUNICIPIO", "CONFIDENCIAL", True),
    ("ESTATUS_VICTIMA", "CONFIDENCIAL", True),
]


def img_uri(name: str) -> str:
    data = base64.b64encode((FIGDIR / name).read_bytes()).decode()
    return f"data:image/png;base64,{data}"


def inline(t: str) -> str:
    """Escape, then re-apply the small markdown subset the draft actually uses."""
    t = html.escape(t)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    # [label](url) first, then any bare URL left over
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
               r'<a href="\2" target="_blank" rel="noopener">\1</a>', t)
    t = re.sub(r"(?<!\")(?<!>)\((https?://[^)\s]+)\)",
               r'(<a href="\1" target="_blank" rel="noopener">\1</a>)', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t, flags=re.S)
    t = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<em>\1</em>", t, flags=re.S)
    return t


def parse_body(md: str) -> str:
    """Convert the article body (§1..§8) into HTML."""
    body = md.split("## 1.", 1)[1]
    body = "## 1." + body.split("## Methods note", 1)[0]

    out: list[str] = []
    # split into blocks on blank lines, keeping order
    for block in re.split(r"\n\s*\n", body.strip()):
        b = block.strip()
        if not b:
            continue

        m = re.match(r"^#{2,3}\s+(\d+b?)\.\s+(.+)$", b, flags=re.S)
        if m:
            num, title = m.group(1), " ".join(m.group(2).split())
            out.append(
                f'<section class="sec">\n'
                f'<p class="eyebrow"><span class="idx">{num}</span></p>\n'
                f"<h2>{inline(title)}</h2>"
            )
            continue

        # A figure marker and its caption share one block (no blank line between them).
        m = re.match(r"^\*\*\[FIG\s+([A-H])\s*[—-]\s*`([^`]+)`\]\*\*\s*(.*)$", b, flags=re.S)
        if m:
            letter, path, rest = m.group(1), m.group(2), m.group(3).strip()
            cap = ""
            if rest.startswith("*Caption:"):
                cap = " ".join(rest.strip().strip("*").replace("Caption:", "", 1).split())
            out.append(
                f'<figure class="plate">\n'
                f'<img src="{img_uri(Path(path).name)}" alt="Figure {letter}" loading="lazy">\n'
                f'<figcaption><span class="figlabel">Fig. {letter}</span> '
                f"{inline(cap)}</figcaption>\n</figure>"
            )
            continue

        # bullet list: items start with "- " and may wrap over several lines
        if b.startswith("- "):
            items, cur = [], []
            for line in b.split("\n"):
                if line.lstrip().startswith("- "):
                    if cur:
                        items.append(" ".join(cur))
                    cur = [line.lstrip()[2:].strip()]
                else:
                    cur.append(line.strip())
            if cur:
                items.append(" ".join(cur))
            lis = "\n".join(f"<li>{inline(' '.join(i.split()))}</li>" for i in items)
            out.append(f"<ul>\n{lis}\n</ul>")
            continue

        out.append(f"<p>{inline(' '.join(b.split()))}</p>")

    hchunks = "\n".join(out)
    # close each section before the next opens, and at the end
    hchunks = hchunks.replace('<section class="sec">', "</section>\n<section class=\"sec\">")
    hchunks = hchunks.replace("</section>\n<section class=\"sec\">", '<section class="sec">', 1)
    return hchunks + "\n</section>"


def parse_methods(md: str) -> str:
    chunk = md.split("## Methods note", 1)[1]
    chunk = chunk.split("---", 1)[0]
    chunk = chunk.split("\n", 1)[1]  # drop the rest of the heading line
    paras = [" ".join(p.split()) for p in re.split(r"\n\s*\n", chunk.strip()) if p.strip()]
    return "\n".join(f"<p>{inline(p)}</p>" for p in paras)


def hero_record() -> str:
    rows = []
    for field, value, redacted in HERO_FIELDS:
        cls = "val redacted" if redacted else "val"
        rows.append(f'<div class="frow"><dt>{field}</dt><dd class="{cls}">{value}</dd></div>')
    return "\n".join(rows)


def ascii_safe(s: str) -> str:
    """Escape every non-ASCII char to a numeric entity.

    The page carries em-dashes and Spanish names (Michoacán, Teuchitlán, María),
    and is viewed both from a local static server and from the Artifact host. Rather
    than depend on either declaring UTF-8, make the bytes ASCII so the encoding
    cannot matter.
    """
    return "".join(c if ord(c) < 128 else f"&#{ord(c)};" for c in s)


def build() -> str:
    md = DRAFT.read_text(encoding="utf-8")
    return ascii_safe(TEMPLATE.format(
        title=TITLE,
        subtitle=SUBTITLE,
        hero=hero_record(),
        body=parse_body(md),
        methods=parse_methods(md),
    ))


TEMPLATE = """<title>{title}</title>
<style>
  /* ---- tokens: light is the base, dark redefines tokens only ---- */
  :root {{
    /* --muted is darker than it looks like it needs to be: captions and the
       methods note run at 13.5-14px, so they need >=4.5:1 on --ground, not 3:1. */
    --ground:#E7E9E6; --plate:#FFFFFF; --ink:#22201E; --muted:#585D59;
    --redact:#7A1F1F; --collective:#3C6E91; --rule:#CBCFC9; --plate-edge:#D5D8D2;
    --serif:'Iowan Old Style',Palatino,'Palatino Linotype',Charter,Georgia,serif;
    --mono:ui-monospace,'SF Mono',Menlo,Consolas,monospace;
    --sans:-apple-system,'Helvetica Neue',Helvetica,Arial,sans-serif;
  }}
  @media (prefers-color-scheme:dark) {{
    :root:not([data-theme="light"]) {{
      --ground:#151817; --ink:#E3E6E2; --muted:#8E948F;
      --redact:#C4706A; --collective:#84ABC6; --rule:#2E3331; --plate-edge:#343937;
    }}
  }}
  :root[data-theme="dark"] {{
    --ground:#151817; --ink:#E3E6E2; --muted:#8E948F;
    --redact:#C4706A; --collective:#84ABC6; --rule:#2E3331; --plate-edge:#343937;
  }}

  * {{ box-sizing:border-box; }}
  body {{
    margin:0; background:var(--ground); color:var(--ink);
    font-family:var(--serif); font-size:19px; line-height:1.62;
    -webkit-font-smoothing:antialiased;
  }}
  .wrap {{ max-width:1120px; margin:0 auto; padding:0 28px 96px; }}
  .col {{ max-width:34em; }}

  /* ---- masthead ---- */
  header.mast {{ padding:64px 0 8px; }}
  .kicker {{
    font-family:var(--mono); font-size:11px; letter-spacing:.16em; text-transform:uppercase;
    color:var(--muted); margin:0 0 22px; display:flex; flex-wrap:wrap; gap:10px 16px; align-items:center;
  }}
  .chip {{ border:1px solid var(--rule); padding:3px 8px; }}
  a {{ color:inherit; text-decoration:underline; text-underline-offset:2px;
       text-decoration-color:var(--muted); }}
  a:hover {{ text-decoration-color:var(--redact); }}
  a:focus-visible {{ outline:2px solid var(--redact); outline-offset:2px; }}
  h1 {{
    font-size:clamp(2.4rem,6vw,4.1rem); line-height:1.03; margin:0 0 18px;
    font-weight:600; letter-spacing:-.015em; text-wrap:balance; max-width:15ch;
  }}
  .subtitle {{
    font-size:clamp(1.15rem,2.4vw,1.5rem); color:var(--muted); margin:0 0 40px;
    max-width:26ch; line-height:1.3; text-wrap:balance; font-weight:400;
  }}
  .standfirst {{ font-size:1.16rem; line-height:1.6; max-width:33em; margin:0 0 44px; }}
  .standfirst strong {{ font-weight:600; }}

  /* ---- hero: one registry record as the public sees it ---- */
  .record {{
    background:var(--plate); border:1px solid var(--plate-edge);
    padding:26px 28px 24px; max-width:36em; margin:0 0 14px; color:#22201E;
  }}
  .record .rlabel {{
    font-family:var(--mono); font-size:10.5px; letter-spacing:.15em; text-transform:uppercase;
    color:#6B706C; margin:0 0 18px; padding-bottom:12px; border-bottom:1px solid #E2E5E0;
  }}
  dl.fields {{ margin:0; display:flex; flex-direction:column; gap:11px; }}
  .frow {{ display:grid; grid-template-columns:minmax(0,15em) 1fr; gap:14px; align-items:baseline; }}
  dl.fields dt {{
    font-family:var(--mono); font-size:11.5px; letter-spacing:.06em; color:#6B706C;
    text-transform:uppercase; overflow-wrap:anywhere;
  }}
  dl.fields dd {{ margin:0; font-family:var(--mono); font-size:13px; letter-spacing:.04em; color:#22201E; }}
  dl.fields dd.redacted {{ color:#7A1F1F; }}
  .record-note {{
    font-family:var(--sans); font-size:13.5px; color:var(--muted); max-width:36em;
    margin:0 0 60px; line-height:1.5;
  }}

  /* ---- sections ---- */
  .sec {{ padding-top:52px; }}
  .eyebrow {{ margin:0 0 14px; display:flex; align-items:center; gap:12px; }}
  .idx {{
    font-family:var(--mono); font-size:11px; letter-spacing:.18em; color:var(--muted);
    border:1px solid var(--rule); padding:4px 9px; text-transform:uppercase;
  }}
  .eyebrow::after {{ content:""; flex:1; height:1px; background:var(--rule); }}
  h2 {{
    font-size:clamp(1.55rem,3.2vw,2.15rem); line-height:1.15; margin:0 0 26px;
    font-weight:600; letter-spacing:-.01em; max-width:20ch; text-wrap:balance;
  }}
  .sec p {{ max-width:34em; margin:0 0 21px; }}
  .sec ul {{
    max-width:34em; margin:0 0 24px; padding:0; list-style:none;
    display:flex; flex-direction:column; gap:15px;
  }}
  .sec li {{ position:relative; padding-left:22px; }}
  .sec li::before {{
    content:""; position:absolute; left:0; top:.62em;
    width:9px; height:1.5px; background:var(--redact);
  }}
  em {{ font-style:italic; }}
  strong {{ font-weight:600; }}
  code {{ font-family:var(--mono); font-size:.86em; letter-spacing:.02em; }}

  /* ---- figure plates ---- */
  figure.plate {{ margin:38px 0 40px; }}
  figure.plate img {{
    display:block; width:100%; height:auto; background:var(--plate);
    border:1px solid var(--plate-edge); padding:14px;
  }}
  figcaption {{
    font-family:var(--sans); font-size:13.5px; line-height:1.5; color:var(--muted);
    margin-top:13px; max-width:44em;
  }}
  .figlabel {{
    font-family:var(--mono); font-size:11px; letter-spacing:.13em; text-transform:uppercase;
    color:var(--redact); margin-right:9px;
  }}

  /* ---- methods ---- */
  .methods {{ margin-top:76px; border-top:2px solid var(--ink); padding-top:26px; }}
  .methods h2 {{ font-size:1.2rem; margin-bottom:18px; max-width:none; }}
  .methods p {{
    font-family:var(--sans); font-size:14px; line-height:1.62; color:var(--muted);
    max-width:44em; margin:0 0 15px;
  }}
  .methods strong {{ color:var(--ink); font-weight:600; }}
  footer {{
    margin-top:56px; padding-top:22px; border-top:1px solid var(--rule);
    font-family:var(--mono); font-size:11px; letter-spacing:.1em; text-transform:uppercase;
    color:var(--muted); display:flex; flex-wrap:wrap; gap:8px 20px;
  }}

  @media (max-width:640px) {{
    body {{ font-size:17.5px; }}
    .wrap {{ padding:0 20px 72px; }}
    header.mast {{ padding-top:40px; }}
    .frow {{ grid-template-columns:1fr; gap:3px; }}
    figure.plate img {{ padding:9px; }}
  }}
  @media (prefers-reduced-motion:reduce) {{ * {{ animation:none !important; transition:none !important; }} }}
</style>

<div class="wrap">
  <header class="mast">
    <p class="kicker">
      <span>Data investigation</span>
      <span class="chip">RNPDNO</span>
      <span class="chip">Mexico</span>
    </p>
    <h1>{title}</h1>
    <p class="subtitle">{subtitle}</p>
    <p class="standfirst">Mexico's official registry recorded 134,268 people as disappeared
      or not located on 15 August 2026. For one in three of them, the public record contains
      a single fact: the state where they vanished. This is the story of who decides that —
      and of the two very different ways a person can go missing from the data itself.</p>

    <div class="record">
      <p class="rlabel">What a confidential record contains</p>
      <dl class="fields">
{hero}
      </dl>
    </div>
    <p class="record-note">The field structure above is illustrative, not one person's
      file — but it is everything the public registry returns for 36.8% of unresolved
      cases. One field survives.</p>
  </header>

  <main>
{body}

    <section class="methods">
      <h2>Methods and limits</h2>
{methods}
    </section>
  </main>

  <footer>
    <span>Stage 1 of 2</span>
    <span>Figures reproducible from source</span>
    <span>Data consulted 2026-08-15</span>
  </footer>
</div>
"""


def main() -> None:
    out = build()
    OUT.write_text(out, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}  ({len(out.encode()) / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
