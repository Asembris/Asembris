HEAD = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 {h}" width="1200" height="{h}" role="img" aria-label="{alt}">
  <defs>
    <linearGradient id="acc" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#38BDF8"/><stop offset="100%" stop-color="#818CF8"/>
    </linearGradient>
    <linearGradient id="node" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#0F1A2E"/><stop offset="100%" stop-color="#0B1220"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="{h}" rx="12" fill="#080D18"/>
  <rect x="0" y="0" width="1200" height="3" rx="1.5" fill="url(#acc)" opacity="0.85"/>
  <g font-family="Segoe UI, Helvetica Neue, Helvetica, Arial, sans-serif">
    <text x="28" y="38" fill="#64748B" font-size="12" font-weight="600" letter-spacing="2.4">{label}</text>
'''
FOOT = '''  </g>
</svg>
'''
CYCLE = 6.0

def pipeline(path, label, alt, nodes, note, h=190, extra=''):
    n = len(nodes); pad, gap = 28, 16
    w = (1200 - pad*2 - gap*(n-1)) / n
    y, bh = 58, 74
    mid = y + bh/2
    out = HEAD.format(h=h, label=label, alt=alt)

    # travelling packet, drawn behind the nodes so it reads as flow through the chain
    for k, delay in enumerate([0, 2.0, 4.0]):
        out += (f'    <circle r="4" fill="#38BDF8" opacity="0">\n'
                f'      <animate attributeName="opacity" values="0;0.9;0.9;0;0" keyTimes="0;0.04;0.28;0.33;1" dur="{CYCLE}s" begin="{delay}s" repeatCount="indefinite"/>\n'
                f'      <animateMotion dur="{CYCLE}s" begin="{delay}s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;0.32;1" calcMode="linear" path="M{pad} {mid} L{1200-pad} {mid}"/>\n    </circle>\n')

    for i, (title, sub, kind) in enumerate(nodes):
        x = pad + i*(w+gap)
        t0 = (i / n) * 0.32
        if kind == 'gate':   base, sw, tc, hi = '#38BDF8', 1.7, '#7DD3FC', '#7DD3FC'
        elif kind == 'verify': base, sw, tc, hi = '#34D399', 1.5, '#6EE7B7', '#6EE7B7'
        else:                base, sw, tc, hi = '#334155', 1.2, '#E2E8F0', '#38BDF8'
        out += (f'    <rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{bh}" rx="10" fill="url(#node)" stroke="{base}" stroke-width="{sw}">\n'
                f'      <animate attributeName="stroke" values="{base};{hi};{base}" keyTimes="0;0.5;1" dur="0.9s" begin="{t0*CYCLE:.2f}s;{t0*CYCLE+2:.2f}s;{t0*CYCLE+4:.2f}s" fill="remove"/>\n'
                f'    </rect>\n')
        out += f'    <text x="{x+w/2:.1f}" y="{y+32}" fill="{tc}" font-size="13.5" font-weight="600" text-anchor="middle">{title}</text>\n'
        fs = 11.5
        while len(sub) * fs * 0.54 > (w - 14) and fs > 8.5: fs -= 0.5
        out += f'    <text x="{x+w/2:.1f}" y="{y+52}" fill="#64748B" font-size="{fs}" text-anchor="middle">{sub}</text>\n'
        if i < n-1:
            ax = x + w
            out += f'    <path d="M{ax+2:.1f} {mid} L{ax+gap-4:.1f} {mid}" stroke="#475569" stroke-width="1.5"/>\n'
            out += f'    <path d="M{ax+gap-8:.1f} {mid-4} L{ax+gap-3:.1f} {mid} L{ax+gap-8:.1f} {mid+4} Z" fill="#475569"/>\n'

    out += f'    <rect x="28" y="{y+bh+22}" width="3" height="20" rx="1.5" fill="url(#acc)"/>\n'
    out += f'    <text x="42" y="{y+bh+37}" fill="#94A3B8" font-size="13.5">{note}</text>\n'
    out += extra + FOOT
    open(path, 'w').write(out)

pipeline('pipe-sentinel.svg', 'SPLUNK SENTINEL &#183; PIPELINE',
    'Splunk Sentinel pipeline: alert, triage, ReAct kill chain reconstruction, parallel enrichment, synthesis, report',
    [('ALERT','Splunk ingest','n'),('TRIAGE','classify &amp; score','n'),('RECONSTRUCT','ReAct, max 3 loops','n'),
     ('ENRICH','intel + ATT&amp;CK, parallel','n'),('SYNTHESIZE','RAG-grounded','n'),('REPORT','PDF + write-back','verify')],
    'Every SPL query passes a three-layer guardrail; every action lands in a SHA-256-chained audit log.')

pipeline('pipe-attest.svg', 'ATTEST &#183; VERDICT PATH',
    'Attest verdict path: claim, deterministic checkers, three-valued verdict, human approval, DataHub write-back',
    [('CLAIM','explicit URN required','n'),('CHECKERS','date math, set membership','gate'),
     ('VERDICT','three-valued, no confidence','gate'),('HUMAN','per-claim approval','n'),
     ('DATAHUB','content-addressed assertion','verify')],
    'No model touches the verdict. A verdict that spends tokens is auto-FLAGGED and cannot be approved.')

# ---- CareLoop: pipeline plus the adversarial barrier band ----
BAND_Y = 196
WALL_X = 792
band = f'''    <line x1="28" y1="{BAND_Y-18}" x2="1172" y2="{BAND_Y-18}" stroke="#1E293B" stroke-width="1"/>
    <text x="28" y="{BAND_Y+6}" fill="#64748B" font-size="12" font-weight="600" letter-spacing="2.4">ADVERSARIAL CORPUS</text>
    <text x="232" y="{BAND_Y+6}" fill="#475569" font-size="12">320 attempts replayed against the shipped rules.yaml</text>
'''
LANE_TOP, LANES = BAND_Y + 26, 5
for i in range(LANES):
    ly = LANE_TOP + i*17
    band += f'    <line x1="60" y1="{ly}" x2="{WALL_X-10}" y2="{ly}" stroke="#141F33" stroke-width="1"/>\n'

# the wall
band += f'''    <rect x="{WALL_X}" y="{LANE_TOP-16}" width="6" height="{LANES*17+8}" rx="3" fill="#38BDF8" opacity="0.9">
      <animate attributeName="opacity" values="0.55;1;0.55" dur="2.4s" repeatCount="indefinite"/>
    </rect>
    <text x="{WALL_X+3}" y="{LANE_TOP-26}" fill="#7DD3FC" font-size="11.5" font-weight="600" text-anchor="middle">POLICY</text>
    <text x="{WALL_X-14}" y="{LANE_TOP+LANES*17+6}" fill="#F87171" font-size="12" text-anchor="end">320 blocked</text>
    <text x="{WALL_X+16}" y="{LANE_TOP+LANES*17+6}" fill="#6EE7B7" font-size="12">0 authorized</text>
'''

TRAVEL = 0.33  # fraction of the 6s cycle spent in flight
for k in range(24):
    lane = k % LANES
    begin = round((k * 0.23) % 5.5, 2)
    ly = LANE_TOP + lane*17
    band += f'''    <circle r="3" fill="#F87171" opacity="0">
      <animate attributeName="opacity" values="0;0.95;0.95;0;0" keyTimes="0;0.03;0.30;0.35;1" dur="6s" begin="{begin}s" repeatCount="indefinite"/>
      <animateMotion dur="6s" begin="{begin}s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;{TRAVEL};1" calcMode="linear" path="M60 {ly} L{WALL_X-12} {ly}"/>
    </circle>
    <circle cx="{WALL_X-3}" cy="{ly}" r="3" fill="#F87171" opacity="0">
      <animate attributeName="opacity" values="0;0.75;0;0" keyTimes="0;0.02;0.09;1" dur="6s" begin="{round(begin + 6*TRAVEL, 2)}s" repeatCount="indefinite"/>
      <animate attributeName="r" values="2;10;2;2" keyTimes="0;0.02;0.09;1" dur="6s" begin="{round(begin + 6*TRAVEL, 2)}s" repeatCount="indefinite"/>
    </circle>
'''

pipeline('pipe-careloop.svg', 'CARELOOP &#183; AUTHORITY MODEL',
    'CareLoop authority model: agent proposes, deterministic policy engine authorises, provider acts, an independent re-read confirms. 320 adversarial attempts all blocked at the policy wall.',
    [('AGENT','proposes, holds no tools','n'),('POLICY ENGINE','rules.yaml, 2 checkpoints','gate'),
     ('PROVIDER','the only actor with reach','n'),('RE-READ','external state confirms','verify')],
    'Two independent enforcement points. Facts carry {source_doc, page, trust_level} provenance.',
    h=330, extra=band)
print('generated')
