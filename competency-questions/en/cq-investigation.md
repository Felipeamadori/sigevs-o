# Competency Questions — Investigation Subdomain

| ID | Competency Question | Path in the Model | Implementation |
|----|--------------------|--------------------|----------------|
| CQ-INV-01 | Which properties are within the surveillance radius of an active outbreak? | `InvestigationTarget` → `ControlZone.radius` → establishments in buffer | PostGIS/GeoSPARQL |
| CQ-INV-02 | Can a property be the target of more than one investigation simultaneously? | `InvestigationTarget` (no UNIQUE constraint on analysis_id + premise_id) | Structural analysis |
| CQ-INV-03 | What is the animal movement history (GTAs) of a property during the investigation period? | `AnimalMovement` (origin/destination = `Establishment`) | JPA/SPARQL |
| CQ-INV-04 | Which are the direct contact properties of an investigated property? | `InvestigationTarget` → `ContactingProperty` (direct) | JPA query |
| CQ-INV-05 | Which are the indirect contact properties of an investigated property? | `InvestigationTarget` → `IndirectContactProperty` | JPA query |
| CQ-INV-06 | Which control zones were defined for an investigation? | `InvestigationTarget` → `ControlZone` | JPA/SPARQL |
| CQ-INV-07 | What is the current status of a sanitary investigation? | `SanitaryAnalysis` → `isActive` | JPA query |
| CQ-INV-08 | Which geographic areas (municipalities) are affected by an investigation? | `InvestigationTarget` → `Address` → municipality | JPA query |
| CQ-INV-09 | Which species categories are involved in an investigation? | `InvestigationTarget` → `AnimalSpecies` | JPA query |
