# Axioms — Geographic

| ID | Axiom | Description | DL Notation | Implementation |
|----|-------|-------------|-------------|----------------|
| AX-GEO-01 | An investigation target has up to 3 concentric zones (Perifoco, Vigilância, Proteção) + optionally Investigation | zone1 (INFECTED), zone2 (BUFFER), zone3 (SURVEILLANCE) in InvestigationTarget | `InvestigationTarget(x) → ∃z1,z2,z3: hasZone(x,z1) ∧ hasZone(x,z2) ∧ hasZone(x,z3) ∧ (hasZone(x,z4) ∨ ¬hasZone(x,z4))` | `AnalysisTarget.zone1/2/3` + `ZoneType` enum |
| AX-GEO-02 | Coordinates of establishments, targets, and barriers are stored as `GEOGRAPHY` (PostGIS) | Support for geospatial calculations | `Establishment(x) → hasCoord(x,geo) ∧ Geography(geo)` | Columns `coord GEOGRAPHY` in tables |
