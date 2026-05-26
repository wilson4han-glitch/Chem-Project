const HALF_REACTIONS = [
  { id: 'zn', label: 'Zn²⁺/Zn', E0: -0.76, ion: 'Zn²⁺', metal: 'Zn', name: 'Zinc',     charge: 2, molarMass: 65.38,  color: '#8a9ba8', solutionColor: 'rgba(180,210,220,0.45)' },
  { id: 'cu', label: 'Cu²⁺/Cu', E0: +0.34, ion: 'Cu²⁺', metal: 'Cu', name: 'Copper',   charge: 2, molarMass: 63.55,  color: '#b87333', solutionColor: 'rgba(100,180,220,0.45)' },
  { id: 'ag', label: 'Ag⁺/Ag',  E0: +0.80, ion: 'Ag⁺',  metal: 'Ag', name: 'Silver',   charge: 1, molarMass: 107.87, color: '#c0c0c0', solutionColor: 'rgba(220,220,230,0.35)' },
  { id: 'fe', label: 'Fe²⁺/Fe', E0: -0.44, ion: 'Fe²⁺', metal: 'Fe', name: 'Iron',     charge: 2, molarMass: 55.85,  color: '#cd853f', solutionColor: 'rgba(205,133,63,0.35)' },
  { id: 'ni', label: 'Ni²⁺/Ni', E0: -0.25, ion: 'Ni²⁺', metal: 'Ni', name: 'Nickel',   charge: 2, molarMass: 58.69,  color: '#708090', solutionColor: 'rgba(100,180,100,0.35)' },
  { id: 'pb', label: 'Pb²⁺/Pb', E0: -0.13, ion: 'Pb²⁺', metal: 'Pb', name: 'Lead',     charge: 2, molarMass: 207.2,  color: '#696969', solutionColor: 'rgba(180,180,190,0.35)' },
  { id: 'au', label: 'Au³⁺/Au', E0: +1.50, ion: 'Au³⁺', metal: 'Au', name: 'Gold',     charge: 3, molarMass: 196.97, color: '#FFD700', solutionColor: 'rgba(255,215,0,0.25)' },
  { id: 'sn', label: 'Sn²⁺/Sn', E0: -0.14, ion: 'Sn²⁺', metal: 'Sn', name: 'Tin',      charge: 2, molarMass: 118.71, color: '#8b9dc3', solutionColor: 'rgba(150,170,210,0.35)' },
  { id: 'al', label: 'Al³⁺/Al', E0: -1.66, ion: 'Al³⁺', metal: 'Al', name: 'Aluminum', charge: 3, molarMass: 26.98,  color: '#b0c4de', solutionColor: 'rgba(190,210,230,0.35)' },
  // charge:1 treats this as H⁺ + e⁻ → ½H₂, which gives the correct Nernst Q.
  // molarMass:1.008 (mass of ½H₂ per electron) keeps Faraday's law consistent with charge:1.
  { id: 'h2', label: 'H⁺/H₂',  E0:  0.00, ion: 'H⁺',   metal: 'Pt', name: 'Hydrogen', charge: 1, molarMass: 1.008,  type: 'gas',
    reductionStr: '2H⁺ + 2e⁻ → H₂   (reduction)',
    oxidationStr: 'H₂ → 2H⁺ + 2e⁻   (oxidation)',
    color: '#e0e0e0', solutionColor: 'rgba(220,220,220,0.30)' },
];

function getById(id) {
  return HALF_REACTIONS.find(r => r.id === id);
}

// E°cell = E°cathode - E°anode
function calcStandardCellPotential(cathode, anode) {
  return cathode.E0 - anode.E0;
}

// Nernst equation: E = E° - (0.0592/n) * log10(Q)
// Q = [anode ion]^(n/nAnode) / [cathode ion]^(n/nCathode)  (LCM-balanced)
function calcNernstPotential(cathode, anode, concCathode, concAnode) {
  const E0 = calcStandardCellPotential(cathode, anode);
  const nAnode = anode.charge;
  const nCathode = cathode.charge;
  const n = lcm(nAnode, nCathode);
  const safeCathode = Math.max(concCathode, 1e-15);
  const safeAnode   = Math.max(concAnode,   1e-15);
  const Q = Math.pow(safeAnode, n / nAnode) / Math.pow(safeCathode, n / nCathode);
  if (Q <= 0) return E0;
  return E0 - (0.0592 / n) * Math.log10(Q);
}

function lcm(a, b) {
  return (a * b) / gcd(a, b);
}
function gcd(a, b) {
  return b === 0 ? a : gcd(b, a % b);
}

function getHalfReactionString(hr, isAnode) {
  if (isAnode  && hr.oxidationStr) return hr.oxidationStr;
  if (!isAnode && hr.reductionStr) return hr.reductionStr;
  const n = hr.charge;
  if (isAnode) {
    return `${hr.metal} → ${hr.ion} + ${n}e⁻   (oxidation)`;
  } else {
    return `${hr.ion} + ${n}e⁻ → ${hr.metal}   (reduction)`;
  }
}
