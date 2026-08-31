#!/usr/bin/env python3
"""Render a contribution activity panel as a self-hosted, animated SVG.

Pulls real data from the GitHub GraphQL API and writes assets/contrib.svg in the
profile's own palette. Run by .github/workflows/contrib-graph.yml; no third-party
widget service is involved, so the panel can never rate-limit on the profile page.
"""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone

LOGIN = os.environ.get("CONTRIB_LOGIN", "Asembris")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
OUT = os.environ.get("CONTRIB_OUT", "assets/contrib.svg")

BG, CARD, LINE = "#080D18", "#0F1A2E", "#1E293B"
MUTED, TEXT, ACCENT, GREEN = "#64748B", "#E2E8F0", "#38BDF8", "#34D399"
LEVELS = ["#0E1626", "#0E3A5C", "#12648F", "#1E93C9", "#38BDF8"]

QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      totalRepositoryContributions
      totalPullRequestReviewContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount weekday } }
      }
    }
  }
}
"""


def fetch():
    if not TOKEN:
        sys.exit("No token. Set the GH_TOKEN secret to a PAT with read:user scope.")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={
            "Authorization": f"bearer {TOKEN}",
            "Content-Type": "application/json",
            "User-Agent": f"{LOGIN}-profile-graph",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload:
        sys.exit("GraphQL error: " + json.dumps(payload["errors"]))
    return payload["data"]["user"]["contributionsCollection"]


def streaks(days):
    longest = current = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] > 0 else 0
        longest = max(longest, run)
    for d in reversed(days):
        if d["contributionCount"] > 0:
            current += 1
        else:
            break
    return longest, current


def level(count, peak):
    if count == 0:
        return 0
    if peak <= 1:
        return 4
    q = count / peak
    return 1 if q <= 0.15 else 2 if q <= 0.35 else 3 if q <= 0.65 else 4


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(cc):
    cal = cc["contributionCalendar"]
    weeks = cal["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    peak = max((d["contributionCount"] for d in days), default=0)
    longest, current = streaks(days)
    total = cal["totalContributions"]
    busiest = max(days, key=lambda d: d["contributionCount"]) if days else None

    CELL, GAP = 14, 3.6
    X0, Y0 = 62, 112
    W, H = 1200, 490
    step = CELL + GAP

    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-label="Contribution activity for {esc(LOGIN)}: {total} contributions in the last year">',
        '  <defs>',
        '    <linearGradient id="acc" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0%" stop-color="{ACCENT}"/><stop offset="100%" stop-color="#818CF8"/></linearGradient>',
        '    <linearGradient id="card" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{CARD}"/><stop offset="100%" stop-color="#0B1220"/></linearGradient>',
        '    <linearGradient id="area" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0%" stop-color="{ACCENT}" stop-opacity="0.34"/>'
        f'<stop offset="100%" stop-color="{ACCENT}" stop-opacity="0"/></linearGradient>',
        '  </defs>',
        f'  <rect width="{W}" height="{H}" rx="14" fill="{BG}"/>',
        f'  <rect x="0" y="0" width="{W}" height="3" rx="1.5" fill="url(#acc)" opacity="0.85"/>',
        '  <g font-family="Segoe UI, Helvetica Neue, Helvetica, Arial, sans-serif">',
        f'    <text x="28" y="40" fill="{MUTED}" font-size="12" font-weight="600" letter-spacing="2.4">CONTRIBUTION ACTIVITY &#183; LAST 12 MONTHS</text>',
        f'    <text x="{W-28}" y="40" fill="#334155" font-size="11.5" text-anchor="end">self-hosted &#183; rebuilt daily by GitHub Actions</text>',
        f'    <text x="28" y="76" fill="{TEXT}" font-size="30" font-weight="700">{total:,}'
        f'<tspan font-size="14" font-weight="400" fill="{MUTED}"> contributions</tspan></text>',
    ]

    # weekday guides
    for i, lbl in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        p.append(f'    <text x="50" y="{Y0 + i*step + 11}" fill="#334155" font-size="10.5" text-anchor="end">{lbl}</text>')

    # month labels
    seen = set()
    MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for wi, w in enumerate(weeks):
        if not w["contributionDays"]:
            continue
        d0 = datetime.strptime(w["contributionDays"][0]["date"], "%Y-%m-%d")
        key = (d0.year, d0.month)
        if d0.day <= 7 and key not in seen:
            seen.add(key)
            p.append(f'    <text x="{X0 + wi*step:.1f}" y="{Y0-10}" fill="#334155" font-size="10.5">{MONTHS[d0.month-1]}</text>')

    # heatmap, sweeping in week by week
    for wi, w in enumerate(weeks):
        for d in w["contributionDays"]:
            x = X0 + wi*step
            y = Y0 + d["weekday"]*step
            fill = LEVELS[level(d["contributionCount"], peak)]
            begin = round(0.35 + wi*0.016, 3)
            p.append(
                f'    <rect x="{x:.1f}" y="{y:.1f}" width="{CELL}" height="{CELL}" rx="3" fill="{fill}" opacity="0">'
                f'<animate attributeName="opacity" values="0;1" dur="0.5s" begin="{begin}s" fill="freeze"/>'
                f'<title>{d["date"]}: {d["contributionCount"]}</title></rect>'
            )

    legend_y = Y0 + 7*step + 22
    p.append(f'    <text x="{X0}" y="{legend_y+11}" fill="#334155" font-size="10.5">Less</text>')
    for i, c in enumerate(LEVELS):
        p.append(f'    <rect x="{X0+34+i*18}" y="{legend_y}" width="13" height="13" rx="3" fill="{c}"/>')
    p.append(f'    <text x="{X0+34+len(LEVELS)*18+6}" y="{legend_y+11}" fill="#334155" font-size="10.5">More</text>')

    # stat tiles
    active = sum(1 for d in days if d["contributionCount"] > 0)
    peak_week = max((sum(d["contributionCount"] for d in w["contributionDays"]) for w in weeks), default=0)
    stats = [
        ("COMMITS", f'{cc["totalCommitContributions"]:,}'),
        ("ACTIVE DAYS", f"{active}"),
        ("LONGEST STREAK", f"{longest} days"),
        ("BUSIEST DAY", f'{busiest["contributionCount"]}' if busiest else "0"),
        ("BUSIEST WEEK", f"{peak_week}"),
        ("REPOS CREATED", f'{cc["totalRepositoryContributions"]:,}'),
    ]
    ty, th = legend_y + 34, 62
    tw = (1200 - 56 - 5*12) / 6
    for i, (k, v) in enumerate(stats):
        x = 28 + i*(tw+12)
        p.append(f'    <rect x="{x:.1f}" y="{ty}" width="{tw:.1f}" height="{th}" rx="10" fill="url(#card)" stroke="{LINE}" stroke-width="1.1"/>')
        p.append(f'    <text x="{x+14:.1f}" y="{ty+23}" fill="{MUTED}" font-size="10" font-weight="600" letter-spacing="1.6">{k}</text>')
        p.append(f'    <text x="{x+14:.1f}" y="{ty+48}" fill="{TEXT}" font-size="21" font-weight="700">{v}</text>')

    # weekly activity line, drawn on load
    ly, lh = ty + th + 26, 84
    weekly = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in weeks]
    wmax = max(weekly) or 1
    lx0, lx1 = 28, 1172
    span = (lx1 - lx0) / max(len(weekly) - 1, 1)
    pts = [(lx0 + i*span, ly + lh - (v/wmax)*lh) for i, v in enumerate(weekly)]
    line = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    area = line + f" L{pts[-1][0]:.1f} {ly+lh} L{pts[0][0]:.1f} {ly+lh} Z"
    p.append(f'    <path d="{area}" fill="url(#area)" opacity="0"><animate attributeName="opacity" values="0;1" dur="0.9s" begin="1.5s" fill="freeze"/></path>')
    p.append(
        f'    <path d="{line}" fill="none" stroke="{ACCENT}" stroke-width="2" stroke-linejoin="round" '
        f'stroke-dasharray="4000" stroke-dashoffset="4000">'
        f'<animate attributeName="stroke-dashoffset" from="4000" to="0" dur="2.2s" begin="0.9s" fill="freeze"/></path>'
    )
    p.append(f'    <text x="28" y="{ly+lh+22}" fill="#334155" font-size="10.5">weekly contribution volume &#183; peak {wmax} in one week</text>')
    stamp = datetime.now(timezone.utc).strftime("%d %b %Y")
    p.append(f'    <text x="{lx1}" y="{ly+lh+22}" fill="#334155" font-size="10.5" text-anchor="end">updated {stamp}</text>')
    p.append('  </g>')
    p.append('</svg>')
    return "\n".join(p) + "\n"


if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(build(fetch()))
    print(f"wrote {OUT}")
