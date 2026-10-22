# Competency Questions — Response Subdomain

| ID | Competency Question | Path in the Model | Implementation |
|----|--------------------|--------------------|----------------|
| CQ-RES-01 | Which surveillance cycles belong to a sanitary response? | `SanitaryResponse` → `SurveillanceCycle` | JPA/SPARQL |
| CQ-RES-02 | Which teams are allocated to a given surveillance cycle? | `SurveillanceCycle` → `FieldTeam` | JPA query |
| CQ-RES-03 | Which professionals (members) make up a field team? | `FieldTeam` → `TeamMember` → `Person` | JPA/SPARQL |
| CQ-RES-04 | Can a sanitary barrier be active in multiple cycles simultaneously? | `SanitaryBarrier` → `SurveillanceCycle` (many-to-many) | Structural analysis |
| CQ-RES-05 | Can a control zone be redefined between cycles? | `ControlZone` → `SurveillanceCycle` (new zone per cycle) | Structural analysis |
| CQ-RES-06 | Which professionals were in the field on a given date? | `GPSTracking` → `FieldTeam` → `TeamMember` → date filter | JPA query |
| CQ-RES-07 | Can a team be allocated to more than one cycle simultaneously? | `FieldTeam` → `SurveillanceCycle` (team can belong to one cycle at a time) | Structural analysis |
| CQ-RES-08 | Which operational area is assigned to each team in a cycle? | `OperationalArea` → `FieldTeam` + `SurveillanceCycle` | JPA/SPARQL |
| CQ-RES-09 | Which sanitary barriers are active in a response? | `SanitaryBarrier` → `SanitaryResponse` | JPA query |
| CQ-RES-10 | Which properties are within an operational area? | `OperationalArea` → `PropertyInArea` → `Establishment` | JPA/SPARQL |
| CQ-RES-11 | What is the type (fixed/mobile) and function (sanitary/detour) of a sanitary barrier? | `SanitaryBarrier` → `type` + `function` | JPA query |
| CQ-RES-12 | Which vehicles are linked to a team? | `FieldTeam` → `Vehicle` | JPA query |
| CQ-RES-13 | Which command post is associated with a sanitary response? | `SanitaryResponse` → `CommandPost` | JPA/SPARQL |
| CQ-RES-14 | Which users were mobilized for a response and what is their quarantine status? | `SanitaryResponse` → `SummonedPerson` → `isDirty` + `dirtyUntil` | JPA query |
