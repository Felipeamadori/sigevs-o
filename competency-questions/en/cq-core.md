# Competency Questions — Core Subdomain

| ID | Competency Question | Path in the Model | Implementation |
|----|--------------------|--------------------|----------------|
| CQ-CORE-01 | Which rural establishments are registered in the SVO? | Instances of `Establishment` | JPA/SPARQL |
| CQ-CORE-02 | Which animal species are raised in an establishment? | `Establishment` → `AnimalSpecies` | JPA query |
| CQ-CORE-03 | What is the geographic location (coordinates) of an establishment? | `Establishment` → `Address.coordinates` | JPA query |
| CQ-CORE-04 | Which users are linked to a given region/inspectorate? | `Person` → `region` | JPA query |
| CQ-CORE-05 | Which establishments have CAR (Rural Environmental Registry)? | `Establishment` → `codigoCar` | JPA query |
| CQ-CORE-06 | Which establishments are slaughterhouses and what is their inspection type? | `Slaughterhouse` (subkind of `Establishment`) → `inspectionType` | JPA/SPARQL |
| CQ-CORE-07 | What profiles and permissions does a user have in the system? | `Person` → `profile` | JPA query |
