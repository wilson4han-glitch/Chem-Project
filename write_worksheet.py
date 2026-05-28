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
doc = service.documents().create(body={'title': 'AP Chem Electrochem Sim Worksheet'}).execute()
DOC_ID = doc['documentId']
print(f"Created doc — ID: {DOC_ID}")
print(f"Open at: https://docs.google.com/document/d/{DOC_ID}/edit")

# ── content definition ────────────────────────────────────────────────────────
# Each entry: (text, style)
# style: 'h1' | 'h2' | 'h3' | 'normal' | 'bold_normal'
DIVIDER = '━' * 62

sections = [
    ("AP Chemistry — Electrochemistry Simulation Worksheet", "h1"),
    ("Name: ________________________________  Period: ______  Date: __________", "normal"),
    ("", "normal"),
    ("Open the simulation at: index.html (file provided by your teacher)", "normal"),
    ("", "normal"),
    ("Instructions: For each section, record your predictions BEFORE running the simulation, then verify using the sim. Show all calculations.", "bold_normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    ("SECTION 1 — ANATOMY OF A GALVANIC CELL", "h2"),
    ("[ Galvanic Cell tab  |  Anode: Zn  |  Cathode: Cu  |  Both concentrations: 1.00 M ]", "italic"),
    ("", "normal"),
    ("Before you press Play, examine the simulation and answer the following:", "normal"),
    ("", "normal"),
    ("1.  Label the following on the diagram your teacher provides (or sketch the cell below):", "normal"),
    ("    a. Anode electrode     b. Cathode electrode     c. Direction of electron flow through the wire", "normal"),
    ("    d. Salt bridge     e. Cation migration direction     f. Anion migration direction", "normal"),
    ("", "normal"),
    ("2.  Write the half-reaction occurring at the anode (oxidation):", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("3.  Write the half-reaction occurring at the cathode (reduction):", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("4.  Write the overall balanced cell reaction:", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("5.  Calculate E°cell.  Show your work.", "normal"),
    ("", "normal"),
    ("    E°cell  =  E°cathode  −  E°anode  =  ____________  −  ____________  =  ____________ V", "normal"),
    ("", "normal"),
    ("6.  Based on the sign of E°cell, is this reaction spontaneous? What is the sign of ΔG°?", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("NOW press Play and observe.", "bold_normal"),
    ("", "normal"),
    ("7.  What does the voltmeter read?  ____________ V", "normal"),
    ("", "normal"),
    ("8.  Does it match your calculation?  If not, explain any discrepancy:", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    ("SECTION 2 — PREDICTING AND RANKING CELL POTENTIALS", "h2"),
    ("[ Galvanic Cell tab — change electrodes as directed ]", "italic"),
    ("", "normal"),
    ("Predict E°cell for each pair WITHOUT using the simulation first. Then verify.", "normal"),
    ("", "normal"),
    ("E° values (vs. SHE):", "bold_normal"),
    ("    Zn²⁺/Zn = −0.76 V  |  Fe²⁺/Fe = −0.44 V  |  Ni²⁺/Ni = −0.25 V  |  Pb²⁺/Pb = −0.13 V", "normal"),
    ("    H⁺/H₂ = 0.00 V  |  Cu²⁺/Cu = +0.34 V  |  Ag⁺/Ag = +0.80 V  |  Au³⁺/Au = +1.50 V", "normal"),
    ("", "normal"),
    ("Pair A:  Anode = Zn  |  Cathode = Cu", "bold_normal"),
    ("    Predicted E°cell: ___________V          Simulated voltage: ___________V", "normal"),
    ("", "normal"),
    ("Pair B:  Anode = Fe  |  Cathode = Ag", "bold_normal"),
    ("    Predicted E°cell: ___________V          Simulated voltage: ___________V", "normal"),
    ("", "normal"),
    ("Pair C:  Anode = Pb  |  Cathode = Ni", "bold_normal"),
    ("    Predicted E°cell: ___________V          Simulated voltage: ___________V", "normal"),
    ("", "normal"),
    ("9.  Rank the three cells from highest to lowest voltage:", "normal"),
    ("", "normal"),
    ("    _______ > _______ > _______", "normal"),
    ("", "normal"),
    ("10.  What single factor determines which electrode becomes the anode versus the cathode?", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("11.  Could you build a spontaneous galvanic cell using two copper electrodes? Explain.", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    ("SECTION 3 — THE NERNST EQUATION & CONCENTRATION EFFECTS", "h2"),
    ("[ Galvanic Cell tab  |  Anode: Zn  |  Cathode: Cu ]", "italic"),
    ("", "normal"),
    ("The Nernst equation:  E  =  E°  −  (0.0592 / n) × log₁₀(Q)", "bold_normal"),
    ("For the Zn | Cu cell:  Q  =  [Zn²⁺] / [Cu²⁺]", "normal"),
    ("", "normal"),
    ("Part A — Vary anode concentration (hold cathode at 1.00 M)", "h3"),
    ("Set each anode concentration, record the simulated voltage, then calculate the expected voltage using the Nernst equation. Show one full sample calculation below the table.", "normal"),
    ("", "normal"),
    (" [Zn²⁺] (M)    Q    Predicted E (V)    Simulated E (V)", "normal"),
    ("    0.10", "normal"),
    ("    0.50", "normal"),
    ("    1.00", "normal"),
    ("    2.00", "normal"),
    ("", "normal"),
    ("Sample Nernst calculation (show work for any one row):", "normal"),
    ("", "normal"),
    ("    ___________________________________________________________________", "normal"),
    ("    ___________________________________________________________________", "normal"),
    ("", "normal"),
    ("12.  As [Zn²⁺] increases, does cell voltage increase or decrease? Explain in terms of Q:", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("Part B — Vary cathode concentration (hold anode at 1.00 M)", "h3"),
    ("", "normal"),
    (" [Cu²⁺] (M)    Q    Predicted E (V)    Simulated E (V)", "normal"),
    ("    0.10", "normal"),
    ("    0.50", "normal"),
    ("    1.00", "normal"),
    ("    2.00", "normal"),
    ("", "normal"),
    ("13.  To maximize cell voltage, should [Cu²⁺] be high or low? Should [Zn²⁺] be high or low?", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("14.  If Q = 1, what does the Nernst equation predict for E?  What does Q = 1 mean physically?", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("15.  At what value of Q would E = 0?  What electrochemical concept does this represent?", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    ("SECTION 4 — CELL DEPLETION AND EQUILIBRIUM", "h2"),
    ("[ Galvanic Cell tab  |  Anode: Zn  |  Cathode: Cu  |  Set cathode [Cu²⁺] to 0.05 M  |  Use high speed ]", "italic"),
    ("", "normal"),
    ("16.  Before pressing Play: predict what will happen to cell voltage over time as the reaction proceeds.", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("Now press Play and watch until the cell depletes.", "bold_normal"),
    ("", "normal"),
    ("17.  Describe what happened to the voltmeter reading as the cell ran:", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("18.  What does the Cell Depleted state mean in chemical terms? What species was consumed?", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("19.  At the moment the cell is depleted:", "normal"),
    ("    a.  What is ΔG for the reaction?   ___________", "normal"),
    ("    b.  What is E for the reaction?    ___________", "normal"),
    ("    c.  How does Q compare to K at this moment?   ___________", "normal"),
    ("", "normal"),
    ("20.  Explain in 2–3 sentences how the death of a galvanic cell is related to the concept of equilibrium:", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    ("SECTION 5A — THE ELECTROLYTIC CELL: DRIVING NON-SPONTANEOUS REACTIONS", "h2"),
    ("[ Electrolytic Cell tab  |  Anode: Cu  |  Cathode: Zn  |  Both concentrations: 1.00 M ]", "italic"),
    ("", "normal"),
    ("21.  The simulation shows a battery driving the cell. What is the minimum voltage the battery must supply? (read from the simulation)", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("22.  Compare this minimum voltage to the E°cell you calculated in Section 1 for the same Zn|Cu pair. What relationship do you notice?", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("23.  Fill in the comparison table:", "normal"),
    ("", "normal"),
    ("                       Galvanic Cell          Electrolytic Cell", "normal"),
    ("    Sign of ΔG         _______________        _______________", "normal"),
    ("    Sign of E°cell     _______________        _______________", "normal"),
    ("    Energy source       chemical rxn           _______________", "normal"),
    ("    Anode process      _______________        _______________", "normal"),
    ("    Cathode process    _______________        _______________", "normal"),
    ("", "normal"),
    ("24.  What is deposited onto the cathode in this setup?  Why does plating occur at the cathode and not the anode?", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    ("SECTION 5B — FARADAY'S LAW OF ELECTROLYSIS", "h2"),
    ("[ Electrolytic Cell tab  |  Cathode: Cu  |  Current: 4.0 A ]", "italic"),
    ("", "normal"),
    ("Faraday's Law:   m  =  (M × I × t) / (n × F)", "bold_normal"),
    ("where  M = molar mass (g/mol),  I = current (A),  t = time (s),  n = electrons transferred,  F = 96,485 C/mol", "normal"),
    ("", "normal"),
    ("25.  For copper plating (M = 63.55 g/mol, n = 2), calculate the mass deposited in 120 seconds at 4.0 A. Show full work.", "normal"),
    ("", "normal"),
    ("    ___________________________________________________________________", "normal"),
    ("    ___________________________________________________________________", "normal"),
    ("", "normal"),
    ("    Predicted mass: ___________g", "normal"),
    ("", "normal"),
    ("Now run the simulation for 120 simulated seconds and record the displayed mass.", "bold_normal"),
    ("", "normal"),
    ("    Simulated mass:  ___________g", "normal"),
    ("", "normal"),
    ("26.  Now change the current to 8.0 A. Predict the mass deposited in the same 120 seconds:", "normal"),
    ("", "normal"),
    ("    Predicted mass: ___________g          Simulated mass: ___________g", "normal"),
    ("", "normal"),
    ("27.  When you doubled the current from 4.0 A to 8.0 A, what happened to the mass deposited? Is the relationship linear? Explain using Faraday's Law:", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("28.  Which variable in Faraday's Law represents the number of moles of electrons transferred? How does this value relate to the half-reaction?", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    ("SECTION 5C — DESIGN CHALLENGE", "h2"),
    ("[ Electrolytic Cell tab  |  Anode: Au  |  Cathode: Ag  |  Use any current ]", "italic"),
    ("", "normal"),
    ("You need to deposit exactly 1.00 g of silver onto a piece of jewelry.", "normal"),
    ("Silver:  M = 107.87 g/mol,  n = 1", "bold_normal"),
    ("", "normal"),
    ("29.  Choose a current setting available in the simulation and calculate the time (in seconds) needed to deposit 1.00 g. Show all work.", "normal"),
    ("", "normal"),
    ("    Current chosen: ___________A", "normal"),
    ("", "normal"),
    ("    ___________________________________________________________________", "normal"),
    ("    ___________________________________________________________________", "normal"),
    ("", "normal"),
    ("    Calculated time: ___________s", "normal"),
    ("", "normal"),
    ("30.  Verify using the simulation. How close was your prediction?", "normal"),
    ("", "normal"),
    ("    Simulated mass after your calculated time: ___________g", "normal"),
    ("    Percent error: ___________%", "normal"),
    ("", "normal"),
    ("31.  If the jewelry shop wants to cut the plating time in half, what must they do to the current? Justify mathematically.", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    ("SYNTHESIS — NO SIMULATION ALLOWED", "h2"),
    ("Answer the following without using the simulation. Show all reasoning.", "italic"),
    ("", "normal"),
    ("32.  A galvanic cell has E°cell = +0.46 V at standard conditions, but the voltmeter reads +0.38 V during operation.", "normal"),
    ("    a.  Is Q greater than 1, less than 1, or equal to 1? Justify using the Nernst equation.", "normal"),
    ("", "normal"),
    ("        _________________________________________________________________", "normal"),
    ("        _________________________________________________________________", "normal"),
    ("", "normal"),
    ("    b.  Which half-cell is being depleted as the cell runs — anode or cathode? How do you know?", "normal"),
    ("", "normal"),
    ("        _________________________________________________________________", "normal"),
    ("", "normal"),
    ("33.  A student wants to electroplate iron with gold  (Au³⁺/Au, E° = +1.50 V)  using an iron anode  (Fe²⁺/Fe, E° = −0.44 V).", "normal"),
    ("    a.  Calculate the minimum voltage the external power supply must provide.", "normal"),
    ("", "normal"),
    ("        _________________________________________________________________", "normal"),
    ("", "normal"),
    ("    b.  Is this cell galvanic or electrolytic? How do you know without using a simulation?", "normal"),
    ("", "normal"),
    ("        _________________________________________________________________", "normal"),
    ("", "normal"),
    ("    c.  Write the balanced overall reaction for this electrolysis:", "normal"),
    ("", "normal"),
    ("        _________________________________________________________________", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),
    ("— End of Worksheet —", "italic"),
]

# ── step 2: insert all text in one request ────────────────────────────────────
full_text = '\n'.join(text for text, _ in sections)

service.documents().batchUpdate(documentId=DOC_ID, body={'requests': [{
    'insertText': {'location': {'index': 1}, 'text': full_text}
}]}).execute()
print("Text inserted")

# ── step 3: apply paragraph + text styles ─────────────────────────────────────
# Re-fetch to get accurate indices
doc = service.documents().get(documentId=DOC_ID).execute()

# Build a map: line_number (0-based) -> start index in doc
content = doc['body']['content']
para_starts = []
for elem in content:
    if 'paragraph' in elem:
        para_starts.append(elem['startIndex'])

requests = []

HEADING_MAP = {
    'h1': 'HEADING_1',
    'h2': 'HEADING_2',
    'h3': 'HEADING_3',
    'normal': 'NORMAL_TEXT',
    'bold_normal': 'NORMAL_TEXT',
    'italic': 'NORMAL_TEXT',
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

    # H1 — also set font size 18
    if style == 'h1' and text:
        requests.append({
            'updateTextStyle': {
                'range': {'startIndex': start, 'endIndex': end - 1},
                'textStyle': {'fontSize': {'magnitude': 18, 'unit': 'PT'}},
                'fields': 'fontSize'
            }
        })

# Send in batches of 50 to stay under API limits
BATCH = 50
for i in range(0, len(requests), BATCH):
    service.documents().batchUpdate(
        documentId=DOC_ID,
        body={'requests': requests[i:i+BATCH]}
    ).execute()

print(f"Formatting applied ({len(requests)} style requests across {len(sections)} paragraphs)")
print("Done — open the Google Doc to see the result.")
