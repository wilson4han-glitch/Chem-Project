import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES    = ['https://www.googleapis.com/auth/documents']
BASE      = os.path.dirname(os.path.abspath(__file__))
TOKEN     = os.path.join(BASE, 'token.json')
# ── auth ──────────────────────────────────────────────────────────────────────
creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
if creds.expired and creds.refresh_token:
    creds.refresh(Request())
service = build('docs', 'v1', credentials=creds)

# ── step 1: create a new doc ──────────────────────────────────────────────────
doc = service.documents().create(body={'title': 'AP Chem Electrochem Sim Worksheet — ANSWER KEY'}).execute()
DOC_ID = doc['documentId']
print(f"Created doc — ID: {DOC_ID}")
print(f"Open at: https://docs.google.com/document/d/{DOC_ID}/edit")

# ── content definition ────────────────────────────────────────────────────────
DIVIDER = '━' * 62

sections = [
    ("AP Chemistry — Electrochemistry Simulation Worksheet", "h1"),
    ("ANSWER KEY — For Teacher Use", "h1_red"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    # ── SECTION 1 ──────────────────────────────────────────────────────────────
    ("SECTION 1 — ANATOMY OF A GALVANIC CELL", "h2"),
    ("[ Anode: Zn  |  Cathode: Cu  |  Both concentrations: 1.00 M ]", "italic"),
    ("", "normal"),

    ("Q1.  Labels:", "bold_normal"),
    ("    a. Anode — Zn electrode (left beaker, labeled \"−\")", "normal"),
    ("    b. Cathode — Cu electrode (right beaker, labeled \"+\")", "normal"),
    ("    c. Electron flow — anode → wire → cathode (left to right through external circuit)", "normal"),
    ("    d. Salt bridge — the U-tube connecting the two beakers", "normal"),
    ("    e. Cation migration — toward cathode (right)", "normal"),
    ("    f. Anion migration — toward anode (left)", "normal"),
    ("", "normal"),

    ("Q2.  Anode half-reaction (oxidation):", "bold_normal"),
    ("    Zn(s)  →  Zn²⁺(aq)  +  2e⁻         E° = −0.76 V", "normal"),
    ("", "normal"),

    ("Q3.  Cathode half-reaction (reduction):", "bold_normal"),
    ("    Cu²⁺(aq)  +  2e⁻  →  Cu(s)          E° = +0.34 V", "normal"),
    ("", "normal"),

    ("Q4.  Overall balanced cell reaction:", "bold_normal"),
    ("    Zn(s)  +  Cu²⁺(aq)  →  Zn²⁺(aq)  +  Cu(s)", "normal"),
    ("", "normal"),

    ("Q5.  E°cell calculation:", "bold_normal"),
    ("    E°cell  =  E°cathode  −  E°anode  =  (+0.34)  −  (−0.76)  =  +1.10 V", "normal"),
    ("", "normal"),

    ("Q6.  Spontaneity:", "bold_normal"),
    ("    E°cell = +1.10 V (positive) → reaction is spontaneous. ΔG° is negative.", "normal"),
    ("    ΔG° = −nFE° = −(2)(96,485)(1.10) ≈ −212,000 J ≈ −212 kJ", "normal"),
    ("", "normal"),

    ("Q7.  Voltmeter reading:  1.10 V  (standard conditions, Q = 1)", "bold_normal"),
    ("", "normal"),

    ("Q8.  The reading matches the calculated E°cell exactly because both concentrations are 1.00 M (standard conditions). Q = [Zn²⁺]/[Cu²⁺] = 1.00/1.00 = 1, so the Nernst correction term log(Q) = 0.", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    # ── SECTION 2 ──────────────────────────────────────────────────────────────
    ("SECTION 2 — PREDICTING AND RANKING CELL POTENTIALS", "h2"),
    ("", "normal"),

    ("Pair A:  Anode = Zn  |  Cathode = Cu", "bold_normal"),
    ("    E°cell = E°(Cu) − E°(Zn) = (+0.34) − (−0.76) = +1.10 V", "normal"),
    ("", "normal"),

    ("Pair B:  Anode = Fe  |  Cathode = Ag", "bold_normal"),
    ("    E°cell = E°(Ag) − E°(Fe) = (+0.80) − (−0.44) = +1.24 V", "normal"),
    ("", "normal"),

    ("Pair C:  Anode = Pb  |  Cathode = Ni", "bold_normal"),
    ("    E°cell = E°(Ni) − E°(Pb) = (−0.25) − (−0.13) = −0.12 V", "normal"),
    ("    Note: This value is negative — the reaction as labeled is non-spontaneous.", "italic"),
    ("", "normal"),

    ("Q9.  Ranking highest to lowest:", "bold_normal"),
    ("    B (+1.24 V)  >  A (+1.10 V)  >  C (−0.12 V)", "normal"),
    ("", "normal"),

    ("Q10.  The relative standard reduction potentials (E°) determine anode vs. cathode. The electrode with the more negative (lower) E° is oxidized (anode); the electrode with the more positive (higher) E° is reduced (cathode).", "normal"),
    ("", "normal"),

    ("Q11.  No. Two copper electrodes in identical solutions produce E°cell = 0 V because there is no difference in reduction potential. No net reaction occurs and no current flows. (A concentration cell with two different [Cu²⁺] values would produce a tiny voltage, but at identical concentrations the answer is zero.)", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    # ── SECTION 3 ──────────────────────────────────────────────────────────────
    ("SECTION 3 — THE NERNST EQUATION & CONCENTRATION EFFECTS", "h2"),
    ("E°cell (Zn|Cu) = +1.10 V,  n = 2,  E = 1.10 − (0.0592/2) × log(Q)  =  1.10 − 0.0296 × log(Q)", "italic"),
    ("Q = [Zn²⁺] / [Cu²⁺]", "italic"),
    ("", "normal"),

    ("Part A — Vary [Zn²⁺], hold [Cu²⁺] = 1.00 M", "h3"),
    ("", "normal"),
    (" [Zn²⁺]    Q        log(Q)    Predicted E (V)", "bold_normal"),
    ("    0.10 M    0.10     −1.000    1.10 − 0.0296×(−1.000) = 1.130 V", "normal"),
    ("    0.50 M    0.50     −0.301    1.10 − 0.0296×(−0.301) = 1.109 V", "normal"),
    ("    1.00 M    1.00      0.000    1.10 − 0.0296×(0.000)  = 1.100 V", "normal"),
    ("    2.00 M    2.00     +0.301    1.10 − 0.0296×(+0.301) = 1.091 V", "normal"),
    ("", "normal"),

    ("Sample calculation for [Zn²⁺] = 0.10 M:", "bold_normal"),
    ("    Q = 0.10 / 1.00 = 0.10", "normal"),
    ("    E = 1.10 − (0.0592/2) × log(0.10) = 1.10 − 0.0296 × (−1) = 1.10 + 0.0296 = 1.130 V", "normal"),
    ("", "normal"),

    ("Q12.  As [Zn²⁺] increases, Q increases, so log(Q) increases, so the correction term (0.0296 × log Q) becomes larger and E decreases. A higher product concentration (Zn²⁺) shifts Q away from equilibrium in the product direction, reducing the thermodynamic driving force.", "normal"),
    ("", "normal"),

    ("Part B — Vary [Cu²⁺], hold [Zn²⁺] = 1.00 M", "h3"),
    ("", "normal"),
    (" [Cu²⁺]    Q = 1/[Cu²⁺]    log(Q)    Predicted E (V)", "bold_normal"),
    ("    0.10 M    10.0           +1.000    1.10 − 0.0296×(+1.000) = 1.070 V", "normal"),
    ("    0.50 M     2.00          +0.301    1.10 − 0.0296×(+0.301) = 1.091 V", "normal"),
    ("    1.00 M     1.00           0.000    1.100 V", "normal"),
    ("    2.00 M     0.50          −0.301    1.10 − 0.0296×(−0.301) = 1.109 V", "normal"),
    ("", "normal"),

    ("Q13.  To maximize voltage: [Cu²⁺] should be HIGH (lowers Q) and [Zn²⁺] should be LOW (also lowers Q). Both changes minimize Q, keeping E well above E°.", "normal"),
    ("", "normal"),

    ("Q14.  If Q = 1: log(1) = 0, so E = E° = 1.10 V. Q = 1 means every ion is at its standard-state concentration (1 M) — these are the definition of standard conditions.", "normal"),
    ("", "normal"),

    ("Q15.  E = 0 when Q = K (equilibrium). Setting E = 0:", "bold_normal"),
    ("    0 = 1.10 − (0.0592/2) × log(K)", "normal"),
    ("    log(K) = (2 × 1.10) / 0.0592 = 37.16     →     K ≈ 1.4 × 10³⁷", "normal"),
    ("    This Q = K condition represents equilibrium — the point where the cell is fully depleted and can no longer do electrical work.", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    # ── SECTION 4 ──────────────────────────────────────────────────────────────
    ("SECTION 4 — CELL DEPLETION AND EQUILIBRIUM", "h2"),
    ("[ Zn|Cu, initial [Cu²⁺] = 0.05 M, [Zn²⁺] = 1.00 M ]", "italic"),
    ("", "normal"),

    ("Q16.  Prediction: As the reaction proceeds, Cu²⁺ is consumed and Zn²⁺ is produced, so Q increases continuously. By the Nernst equation, rising Q lowers E. The voltage will decline until E → 0 when Q = K.", "normal"),
    ("    Initial E: Q = 1.00/0.05 = 20.0 → E = 1.10 − 0.0296×log(20) = 1.10 − 0.0385 ≈ 1.062 V", "normal"),
    ("", "normal"),

    ("Q17.  The voltmeter reading decreased steadily from its initial value (~1.06 V) toward zero as Cu²⁺ was depleted, eventually dropping to ≈ 0 V when the cell died.", "normal"),
    ("", "normal"),

    ("Q18.  \"Cell depleted\" means the reaction has reached equilibrium (Q = K). The species consumed was Cu²⁺ — all available Cu²⁺ was reduced to solid Cu metal at the cathode.", "normal"),
    ("", "normal"),

    ("Q19.  At the moment of depletion:", "bold_normal"),
    ("    a. ΔG = 0  (at equilibrium, no free energy available)", "normal"),
    ("    b. E = 0 V", "normal"),
    ("    c. Q = K  (reaction quotient equals equilibrium constant)", "normal"),
    ("", "normal"),

    ("Q20.  A galvanic cell produces electricity because the reaction is not yet at equilibrium (Q < K). As the cell operates, reactants are consumed and products accumulate, driving Q toward K. When Q = K, ΔG = 0 and E = 0 — no more net reaction occurs. A dead battery is a cell that has reached chemical equilibrium; it is not that the chemicals are gone, but that the driving force has vanished.", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    # ── SECTION 5A ─────────────────────────────────────────────────────────────
    ("SECTION 5A — THE ELECTROLYTIC CELL", "h2"),
    ("", "normal"),

    ("Q21.  Minimum battery voltage = 1.10 V  (equal in magnitude to the spontaneous E°cell for the same Zn|Cu pair).", "normal"),
    ("", "normal"),

    ("Q22.  The minimum voltage equals the E°cell from Section 1 (1.10 V). To drive a non-spontaneous reaction you must supply at least as much energy as the spontaneous reverse reaction would release. The two values are equal in magnitude but opposite in sign.", "normal"),
    ("", "normal"),

    ("Q23.  Comparison table:", "bold_normal"),
    ("", "normal"),
    ("                       Galvanic Cell          Electrolytic Cell", "normal"),
    ("    Sign of ΔG         Negative (−)           Positive (+)", "normal"),
    ("    Sign of E°cell     Positive (+)           Negative (−)", "normal"),
    ("    Energy source      Chemical rxn           External electricity", "normal"),
    ("    Anode process      Oxidation              Oxidation", "normal"),
    ("    Cathode process    Reduction              Reduction", "normal"),
    ("", "normal"),

    ("Q24.  Copper (Cu) is deposited. Plating occurs at the cathode because the cathode receives electrons from the external circuit, which reduce Cu²⁺ ions from solution (Cu²⁺ + 2e⁻ → Cu) onto the cathode surface. The anode undergoes oxidation (dissolution), not deposition.", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    # ── SECTION 5B ─────────────────────────────────────────────────────────────
    ("SECTION 5B — FARADAY'S LAW OF ELECTROLYSIS", "h2"),
    ("m = (M × I × t) / (n × F)     where F = 96,485 C/mol", "italic"),
    ("", "normal"),

    ("Q25.  Cu plating at 4.0 A for 120 s  (M = 63.55 g/mol, n = 2):", "bold_normal"),
    ("    m = (63.55 × 4.0 × 120) / (2 × 96,485)", "normal"),
    ("    m = 30,504 / 192,970", "normal"),
    ("    m = 0.158 g", "normal"),
    ("", "normal"),

    ("Q26.  Cu plating at 8.0 A for 120 s:", "bold_normal"),
    ("    m = (63.55 × 8.0 × 120) / (2 × 96,485) = 61,008 / 192,970 = 0.316 g", "normal"),
    ("", "normal"),

    ("Q27.  Doubling the current from 4.0 A to 8.0 A doubled the mass (0.158 g → 0.316 g). The relationship is linear: m ∝ I. From Faraday's Law, m = (M/nF) × I × t — with M, n, F, t all constant, mass scales directly with current.", "normal"),
    ("", "normal"),

    ("Q28.  The variable n (number of electrons transferred per mole of substance plated) represents moles of electrons. It comes directly from the balanced half-reaction: Cu²⁺ + 2e⁻ → Cu gives n = 2. For silver (Ag⁺ + e⁻ → Ag), n = 1.", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    # ── SECTION 5C ─────────────────────────────────────────────────────────────
    ("SECTION 5C — DESIGN CHALLENGE", "h2"),
    ("Target: deposit exactly 1.00 g Ag  (M = 107.87 g/mol, n = 1)", "italic"),
    ("", "normal"),

    ("Q29.  Solving for time given current I:", "bold_normal"),
    ("    1.00 = (107.87 × I × t) / (1 × 96,485)", "normal"),
    ("    I × t = 96,485 / 107.87 = 894.5 A·s", "normal"),
    ("", "normal"),
    ("    At 2.0 A:  t = 894.5 / 2.0 = 447 s  (≈ 7.5 min)", "normal"),
    ("    At 4.0 A:  t = 894.5 / 4.0 = 224 s  (≈ 3.7 min)", "normal"),
    ("    At 8.0 A:  t = 894.5 / 8.0 = 112 s  (≈ 1.9 min)", "normal"),
    ("    (Any of the above current choices is acceptable — show full work for the chosen value.)", "italic"),
    ("", "normal"),

    ("Q30.  The simulation should return a mass ≈ 1.00 g, giving a percent error near 0%. Faraday's Law is exact; any small discrepancy reflects rounding in the time entered.", "normal"),
    ("", "normal"),

    ("Q31.  To halve the time, they must double the current. From m = (M × I × t)/(nF): if m and all constants are fixed, then I × t = constant. Halving t requires doubling I:", "normal"),
    ("    If t_new = t/2, then I_new = (I × t) / (t/2) = 2I", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    # ── SYNTHESIS ──────────────────────────────────────────────────────────────
    ("SYNTHESIS", "h2"),
    ("", "normal"),

    ("Q32.  E°cell = +0.46 V, actual E = +0.38 V  (E < E°)", "bold_normal"),
    ("", "normal"),
    ("    a.  Q > 1. From E = E° − (0.0592/n) × log(Q):", "normal"),
    ("        0.38 = 0.46 − (0.0592/n) × log(Q)  →  (0.0592/n) × log(Q) = +0.08  →  log(Q) > 0  →  Q > 1.", "normal"),
    ("        Q > 1 means product concentrations are elevated relative to reactant concentrations (or the cell has partially discharged).", "normal"),
    ("", "normal"),
    ("    b.  The cathode half-cell is being depleted. The cathode reactant (the oxidizing agent in solution) is consumed as the cell operates, causing [cathode ion] to fall and Q to rise. We know this because Q = [product]/[reactant] increasing indicates the cathode reactant is shrinking.", "normal"),
    ("", "normal"),

    ("Q33.  Electroplate iron with gold: cathode = Au³⁺ + 3e⁻ → Au  (E° = +1.50 V); anode = Fe → Fe²⁺ + 2e⁻  (E° = −0.44 V)", "bold_normal"),
    ("", "normal"),
    ("    a.  E°cell = E°(cathode) − E°(anode) = (+1.50) − (−0.44) = +1.94 V", "normal"),
    ("        E°cell is POSITIVE → the reaction is spontaneous. No external supply is needed;", "normal"),
    ("        gold will spontaneously plate onto iron (cementation reaction). If a student intends", "normal"),
    ("        to run it as an electrolytic cell in reverse, the supply must exceed 1.94 V.", "normal"),
    ("", "normal"),
    ("    b.  This cell is GALVANIC, not electrolytic — E°cell = +1.94 V > 0 means the reaction", "normal"),
    ("        is spontaneous. Au³⁺ is a far stronger oxidizing agent than Fe²⁺; iron will", "normal"),
    ("        dissolve and gold will plate spontaneously without any external power.", "normal"),
    ("", "normal"),
    ("    c.  Balanced overall reaction (LCM of n=3 and n=2 is 6 electrons):", "normal"),
    ("        Cathode ×2:  2Au³⁺(aq) + 6e⁻  →  2Au(s)", "normal"),
    ("        Anode   ×3:  3Fe(s)           →  3Fe²⁺(aq) + 6e⁻", "normal"),
    ("        Overall:     3Fe(s)  +  2Au³⁺(aq)  →  3Fe²⁺(aq)  +  2Au(s)", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),
    ("— End of Answer Key —", "italic"),
]

# ── step 2: insert all text in one request ────────────────────────────────────
full_text = '\n'.join(text for text, _ in sections)

service.documents().batchUpdate(documentId=DOC_ID, body={'requests': [{
    'insertText': {'location': {'index': 1}, 'text': full_text}
}]}).execute()
print("Text inserted")

# ── step 3: apply paragraph + text styles ─────────────────────────────────────
doc = service.documents().get(documentId=DOC_ID).execute()

content = doc['body']['content']
para_starts = []
for elem in content:
    if 'paragraph' in elem:
        para_starts.append(elem['startIndex'])

requests = []

HEADING_MAP = {
    'h1':         'HEADING_1',
    'h1_red':     'HEADING_1',
    'h2':         'HEADING_2',
    'h3':         'HEADING_3',
    'normal':     'NORMAL_TEXT',
    'bold_normal':'NORMAL_TEXT',
    'italic':     'NORMAL_TEXT',
}

for i, (text, style) in enumerate(sections):
    if i >= len(para_starts):
        break
    start = para_starts[i]
    end   = para_starts[i + 1] if i + 1 < len(para_starts) else start + len(text) + 1

    # Paragraph style
    named = HEADING_MAP.get(style, 'NORMAL_TEXT')
    requests.append({
        'updateParagraphStyle': {
            'range': {'startIndex': start, 'endIndex': end},
            'paragraphStyle': {'namedStyleType': named},
            'fields': 'namedStyleType'
        }
    })

    # Bold
    if style == 'bold_normal' and text:
        requests.append({
            'updateTextStyle': {
                'range': {'startIndex': start, 'endIndex': end - 1},
                'textStyle': {'bold': True},
                'fields': 'bold'
            }
        })

    # Italic
    if style == 'italic' and text:
        requests.append({
            'updateTextStyle': {
                'range': {'startIndex': start, 'endIndex': end - 1},
                'textStyle': {'italic': True},
                'fields': 'italic'
            }
        })

    # H1 — font size 18
    if style in ('h1', 'h1_red') and text:
        requests.append({
            'updateTextStyle': {
                'range': {'startIndex': start, 'endIndex': end - 1},
                'textStyle': {'fontSize': {'magnitude': 18, 'unit': 'PT'}},
                'fields': 'fontSize'
            }
        })

    # "ANSWER KEY" subtitle — red foreground
    if style == 'h1_red' and text:
        requests.append({
            'updateTextStyle': {
                'range': {'startIndex': start, 'endIndex': end - 1},
                'textStyle': {
                    'foregroundColor': {
                        'color': {'rgbColor': {'red': 0.8, 'green': 0.0, 'blue': 0.0}}
                    }
                },
                'fields': 'foregroundColor'
            }
        })

# Send in batches of 50
BATCH = 50
for i in range(0, len(requests), BATCH):
    service.documents().batchUpdate(
        documentId=DOC_ID,
        body={'requests': requests[i:i+BATCH]}
    ).execute()

print(f"Formatting applied ({len(requests)} style requests across {len(sections)} paragraphs)")
print("Done — open the Google Doc to see the result.")
