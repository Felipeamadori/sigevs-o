# Axioms — Dependency

| ID | Axiom | Description | DL Notation | Implementation |
|----|-------|-------------|-------------|----------------|
| AX-DEP-01 | A Surveillance Cycle belongs exclusively to a Sanitary Response | There is no cycle without a response | `SurveillanceCycle(x) → ∃!r: belongsTo(x,r)` | `FOREIGN KEY (response_id)` → `sanitary_event_response` |
| AX-DEP-02 | A Field Team belongs exclusively to a Surveillance Cycle | A team does not exist without a cycle | `FieldTeam(x) → ∃!c: allocatedTo(x,c)` | `FOREIGN KEY (surveillance_cycle_id)` → `response_surveillance_cycle` |
| AX-DEP-03 | An Operational Area belongs to a Field Team and a Zone Per Cycle | Dual dependency on team and zone | `OperationalArea(x) → ∃!t,z: belongsTo(x,t) ∧ belongsTo(x,z)` | `FOREIGN KEY (team_id, cycle_zone_id)` in `response_areas` |
| AX-DEP-04 | A Property in Area belongs to an Operational Area | There is no property in area without an area | `PropertyInArea(x) → ∃a: containedIn(x,a)` | `FOREIGN KEY (area_id)` → `response_areas` |
| AX-DEP-05 | A Property Submission links to a Property in Area and a Field Team | Every submission has area + team | `PropertySubmission(x) → ∃p,t: linksTo(x,p) ∧ performedBy(x,t)` | `FOREIGN KEY (area_premise_id, team_id)` in `premise_submissions` |
| AX-DEP-06 | A Barrier Submission links to a Sanitary Barrier | Every barrier submission has a barrier | `BarrierSubmission(x) → ∃b: linksTo(x,b)` | `FOREIGN KEY (barrier_id)` → `response_barriers` |
| AX-DEP-07 | An Investigation Target depends on a Sanitary Analysis | There is no target without an analysis | `InvestigationTarget(x) → ∃a: dependsOn(x,a)` | `FOREIGN KEY (analysis_id)` in `analysis_targets` |
| AX-DEP-08 | A Sanitary Response depends on a Sanitary Analysis | A response only exists linked to an investigation | `SanitaryResponse(x) → ∃a: basedOn(x,a)` | `FOREIGN KEY (analysis_id)` → `sanitary_analysis` |
| AX-DEP-09 | A Command Post is linked to at most one Sanitary Response (and vice versa) | 1:1 relationship between Response and Command Post | `CommandPost(x) → ≤1r: linkedTo(x,r) ∧ SanitaryResponse(r) → ≤1c: linkedTo(r,c)` | `OneToOne response_command_post → response_id FK UNIQUE` |
