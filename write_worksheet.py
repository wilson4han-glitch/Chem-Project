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
    ("Instructions: Record your predictions BEFORE running the simulation, then verify. Show all calculations.", "bold_normal"),
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
    ("2.  Write the half-reactions:", "normal"),
    ("    Anode (oxidation):    _________________________________________________", "normal"),
    ("    Cathode (reduction):  _________________________________________________", "normal"),
    ("", "normal"),
    ("3.  Write the overall balanced cell reaction:", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("4.  Calculate E°cell.  Show your work.", "normal"),
    ("", "normal"),
    ("    E°cell  =  E°cathode  −  E°anode  =  ____________  −  ____________  =  ____________ V", "normal"),
    ("", "normal"),
    ("5.  Based on the sign of E°cell, is this reaction spontaneous? What is the sign of ΔG°?", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("NOW press Play and observe.", "bold_normal"),
    ("", "normal"),
    ("6.  What does the voltmeter read?  ____________ V     Does the ΔG panel confirm your answer to Q5?  ____________", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    ("SECTION 2 — PREDICTING CELL POTENTIALS", "h2"),
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
    ("7.  Which pair produces more voltage, and why does a larger difference in E° values give more voltage?", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("8.  What single factor determines which electrode becomes the anode versus the cathode?", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    ("SECTION 3 — THE NERNST EQUATION & CONCENTRATION EFFECTS", "h2"),
    ("[ Galvanic Cell tab  |  Anode: Zn  |  Cathode: Cu ]", "italic"),
    ("", "normal"),
    ("The Nernst equation:  E  =  E°  −  (0.0592 / n) × log₁₀(Q)     where Q = [Zn²⁺] / [Cu²⁺]", "bold_normal"),
    ("", "normal"),
    ("Vary anode [Zn²⁺] — hold cathode [Cu²⁺] at 1.00 M. Record simulated voltage, then calculate E with the Nernst equation.", "normal"),
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
    ("9.  As [Zn²⁺] increases, does cell voltage increase or decrease? Explain using Q:", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("10.  To maximize cell voltage, should [Cu²⁺] (cathode) be high or low? Should [Zn²⁺] (anode) be high or low?", "normal"),
    ("    Adjust the cathode slider on the sim to test your prediction, then explain using Q.", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("11.  At what value of Q would E = 0? What electrochemical concept does this represent?", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    ("SECTION 4 — CELL DEPLETION AND EQUILIBRIUM", "h2"),
    ("[ Galvanic Cell tab  |  Anode: Zn  |  Cathode: Cu  |  Set cathode [Cu²⁺] to 0.05 M  |  Use high speed ]", "italic"),
    ("", "normal"),
    ("12.  Before pressing Play: predict what will happen to cell voltage over time as the reaction proceeds.", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("Now press Play and watch until the EQUILIBRIUM REACHED overlay appears.", "bold_normal"),
    ("", "normal"),
    ("13.  Describe what happened to the voltmeter reading as the cell ran:", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("14.  At the moment equilibrium is reached:", "normal"),
    ("    a.  What is E?   ___________     b.  What is ΔG?   ___________     c.  How does Q compare to K?   ___________", "normal"),
    ("", "normal"),
    ("15.  Why does the simulation label this state \"EQUILIBRIUM REACHED\" rather than just \"battery dead\"?", "normal"),
    ("    What does it mean chemically when E → 0?", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    ("SECTION 5A — THE ELECTROLYTIC CELL: DRIVING NON-SPONTANEOUS REACTIONS", "h2"),
    ("[ Electrolytic Cell tab  |  Anode: Cu  |  Cathode: Zn  |  Both concentrations: 1.00 M ]", "italic"),
    ("", "normal"),
    ("16.  The simulation shows a battery driving the cell. What minimum voltage is required? (read from the simulation)", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("17.  Compare this to the E°cell from Section 1 (Zn | Cu galvanic cell). What relationship do you notice?", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("18.  What is deposited onto the cathode? Why does plating occur at the cathode and not the anode?", "normal"),
    ("", "normal"),
    ("    _________________________________________________________________", "normal"),
    ("", "normal"),
    ("Now set cathode [Zn²⁺] to 0.10 M and run until the SOLUTION EXHAUSTED overlay appears.", "bold_normal"),
    ("", "normal"),
    ("19.  a.  What total mass was deposited?   ___________g", "normal"),
    ("    b.  Why does plating stop when the cathode solution is exhausted?", "normal"),
    ("", "normal"),
    ("        _________________________________________________________________", "normal"),
    ("", "normal"),
    ("    c.  How is SOLUTION EXHAUSTED different from the EQUILIBRIUM REACHED state in the galvanic cell?", "normal"),
    ("", "normal"),
    ("        _________________________________________________________________", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    ("SECTION 5B — FARADAY'S LAW OF ELECTROLYSIS", "h2"),
    ("[ Electrolytic Cell tab  |  Cathode: Cu  |  Current: 4.0 A ]", "italic"),
    ("", "normal"),
    ("Faraday's Law:   m  =  (M × I × t) / (n × F)", "bold_normal"),
    ("where  M = molar mass (g/mol),  I = current (A),  t = time (s),  n = electrons transferred,  F = 96,485 C/mol", "normal"),
    ("", "normal"),
    ("20.  For copper plating (M = 63.55 g/mol, n = 2), calculate the mass deposited in 120 seconds at 4.0 A. Show full work.", "normal"),
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
    ("21.  Change the current to 8.0 A. Predict and verify the mass deposited in the same 120 seconds:", "normal"),
    ("", "normal"),
    ("    Predicted mass: ___________g          Simulated mass: ___________g", "normal"),
    ("", "normal"),
    ("22.  You need to deposit exactly 1.00 g of silver  (M = 107.87 g/mol, n = 1)  at a current of 3.0 A.", "normal"),
    ("    Calculate the required time, then verify with the simulation. Show all work.", "normal"),
    ("", "normal"),
    ("    ___________________________________________________________________", "normal"),
    ("    ___________________________________________________________________", "normal"),
    ("", "normal"),
    ("    Calculated time: ___________s          Simulated mass after that time: ___________g", "normal"),
    ("", "normal"),
    (DIVIDER, "normal"),
    ("", "normal"),

    ("SYNTHESIS — NO SIMULATION ALLOWED", "h2"),
    ("Answer the following without using the simulation. Show all reasoning.", "italic"),
    ("", "normal"),
    ("23.  A galvanic cell has E°cell = +0.46 V at standard conditions, but the voltmeter reads +0.38 V during operation.", "normal"),
    ("    a.  Is Q greater than 1, less than 1, or equal to 1? Justify using the Nernst equation.", "normal"),
    ("", "normal"),
    ("        _________________________________________________________________", "normal"),
    ("        _________________________________________________________________", "normal"),
    ("", "normal"),
    ("    b.  Which half-cell is being depleted as the cell runs — anode or cathode? How do you know?", "normal"),
    ("", "normal"),
    ("        _________________________________________________________________", "normal"),
    ("", "normal"),
    ("24.  A student electroplates iron with gold  (Au³⁺/Au, E° = +1.50 V)  using an iron anode  (Fe²⁺/Fe, E° = −0.44 V).", "normal"),
    ("    a.  Calculate the minimum voltage the external supply must provide.", "normal"),
    ("", "normal"),
    ("        _________________________________________________________________", "normal"),
    ("", "normal"),
    ("    b.  Write the balanced overall reaction for this electrolysis:", "normal"),
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
