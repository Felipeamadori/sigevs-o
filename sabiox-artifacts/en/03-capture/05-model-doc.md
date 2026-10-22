# Capture Phase — DOC-MODE (Reference Ontology Document)

---

## Reference Ontology Document — SIGEVS-O

| Field | Value |
|-------|-------|
| Document: | Reference Ontology Document |
| Ontology: | SIGEVS-O — Ontology for Sanitary Event Management in Animal Health Defense |
| Version: | v.01 |
| Date: | 06/24/2026 |

---

## 1. Modeling Language

**OntoUML** — Language for Ontology-Driven Conceptual Modeling based on UFO. Used for constructing the reference ontology with formally defined stereotypes (`<<Kind>>`, `<<Subkind>>`, `<<Role>>`, `<<Event>>`, `<<Relator>>`, `<<Collective>>`, `<<Phase>>`).

---

## 2. Foundational Ontology

**UFO (Unified Foundational Ontology)** — provides the semantic foundation for all concepts, relations, and axioms. UFO's ontological categories guide the classification of each domain concept:

| UFO Category | SIGEVS-O Application |
|--------------|---------------------|
| **Endurant** | Establishment, Person, Address, Barrier, Vehicle, Command Post |
| **Event** | Sanitary Analysis, Surveillance Cycle, Animal Movement, Submission, GPS Tracking |
| **Relator** | CAR, Control Zone, Zone per Cycle, Property in Area |
| **Collective** | Field Team |
| **Role** | Investigation Target, Team Member, Convoked User, Contacting Property |
| **Subkind** | Slaughterhouse, Swine Farm, Poultry Farm |
| **Phase** | Visit Completion (Pending/Complete) |

---

## 3. Concept Criteria

| ID | Criterion | Type |
|----|-----------|------|
| CR-01 | Domain Relevance — concept belongs to animal health defense within SVO scope | Subjective |
| CR-02 | SIGEVS Presence — concept represented in at least one SIGEVS functionality | Objective |
| CR-03 | Subdomain Coverage — concept fits within Core, Investigation, Response, or Field | Objective |
| CR-04 | UFO Classifiable — concept can be mapped to a UFO stereotype | Subjective |
| CR-05 | Domain Recognition — concept defined in recognized sources (SIGEVS, FAO GEMP, legislation) | Objective |

---

## 4. Ontologies to Reuse

*Evaluated during Capture Phase. Pending integration:*

| Ontology | Domain | Analysis | Status |
|----------|--------|----------|--------|
| FAO GEMP | Animal health emergency management | Concepts partially overlap with Sanitary Response subdomain | Pending (see `gemp.md`) |
| AGROVOC | Agriculture/livestock/veterinary thesaurus | Useful for species taxonomy and establishment types | To be evaluated |
| IDO | Infectious disease ontology | Potential alignment for disease-related concepts | To be evaluated |

---

## 5. Modularization

```
┌─────────────────────────────────────────────────────────────┐
│                     SIGEVS-O                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐  ┌─────┐  │
│  │    Core      │  │ Investigation │  │ Response │  │Field│  │
│  │              │  │              │  │          │  │     │  │
│  │ 4 Kinds      │  │ 2 Events     │  │ 6 Kinds  │  │ 1   │  │
│  │ 3 Subkinds   │  │ 2 Roles      │  │ 3 Events │  │Role │  │
│  │ 1 Relator    │  │ 2 Relators   │  │ 1 Collect│  │ 2   │  │
│  └──────────────┘  │ 1 Kind       │  │ 3 Relat. │  │Events│  │
│                    │ 1 Enum       │  │ 2 Roles  │  └─────┘  │
│                    └──────────────┘  └──────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### Subdomain: Core (8 classes)

| Class | Stereotype | Description |
|-------|------------|-------------|
| Establishment | `<<Kind>>` | Rural productive unit registered in the veterinary service |
| Address | `<<Kind>>` | Geographic address of an establishment |
| Person | `<<Kind>>` | Person registered in the official veterinary service |
| AnimalSpecies | `<<Kind>>` | Animal species classification |
| Slaughterhouse | `<<Subkind>>` | Slaughterhouse (specialization of Establishment) |
| SwineFarm | `<<Subkind>>` | Swine farm (specialization of Establishment) |
| PoultryFarm | `<<Subkind>>` | Poultry farm (specialization of Establishment) |
| CAR | `<<Relator>>` | Rural Environmental Registry connecting establishment to geospatial perimeter |

### Subdomain: Sanitary Investigation (7 classes)

| Class | Stereotype | Description |
|-------|------------|-------------|
| SanitaryAnalysis | `<<Event>>` | Investigation record for disease suspicion |
| InvestigationTarget | `<<Role>>` | Property designated as investigation target |
| AffectedArea | `<<Kind>>` | Geographic region under investigation |
| InvestigationControlZone | `<<Relator>>` | Perimeter zone connecting target to radius/type |
| AnimalMovement | `<<Event>>` | Animal transit record (GTA) between properties |
| ContactingProperty | `<<Role>>` | Property with direct/indirect contact to investigated premise |
| SpeciesCategory | `<<Enumeration>>` | Fixed species categories for sanitary filtering |

### Subdomain: Sanitary Response (14 classes)

| Class | Stereotype | Description |
|-------|------------|-------------|
| SanitaryResponse | `<<Event>>` | Central record of outbreak containment coordination |
| SurveillanceCycle | `<<Event>>` | Numbered round of surveillance in a control zone |
| ZonePerCycle | `<<Relator>>` | Zone delimitation within a specific cycle |
| FieldTeam | `<<Collective>>` | Team of professionals for field operations |
| TeamMember | `<<Role>>` | Person assigned to a field team |
| Function | `<<Kind>>` | Predefined role for team allocation |
| OperationalArea | `<<Kind>>` | Geographic sector assigned to a team within a zone |
| PropertyInArea | `<<Relator>>` | Link between property and operational area with completion status |
| SanitaryBarrier | `<<Kind>>` | Fixed or mobile checkpoint for animal transit control |
| Vehicle | `<<Kind>>` | Vehicle assigned to field teams |
| CommandPost | `<<Kind>>` | Command HQ for the sanitary response operation |
| ConvokedUser | `<<Role>>` | Person mobilized for a sanitary response |
| GPSTracking | `<<Event>>` | GPS tracking record of team displacement |
| TeamType | `<<Kind>>` | Functional classification of field teams |

### Subdomain: Field Actions (3 classes)

| Class | Stereotype | Description |
|-------|------------|-------------|
| PropertySubmission | `<<Event>>` | Form submitted during property visit |
| BarrierSubmission | `<<Event>>` | Form submitted at sanitary barrier |
| TemporaryProperty | `<<Role>>` | Unregistered property found in the field |

---

## 6. Conceptual Model

### 6.1 Generalization Hierarchy

```
<<Kind>> Establishment
    ├── <<Subkind>> Slaughterhouse
    ├── <<Subkind>> SwineFarm
    └── <<Subkind>> PoultryFarm

<<Kind>> Person
    ├── <<Role>> TeamMember        (assumed within FieldTeam)
    └── <<Role>> ConvokedUser     (assumed within SanitaryResponse)

<<Kind>> Establishment
    ├── <<Role>> InvestigationTarget       (during investigation)
    ├── <<Role>> ContactingProperty (when identified via movements)
    └── <<Role>> TemporaryProperty  (when found unregistered)
```

### 6.2 Core Subdomain

```
 ┌───────────────┐         ┌─────────────────┐
 │  Establishment │──1..*──│    Address       │
 │   <<Kind>>     │    1    │   <<Kind>>      │
 ├────────────────┤         ├─────────────────┤
 │ -codigoSDA:Str │         │ -logradouro:Str │
 │ -nome:String   │         │ -cidade:String  │
 │ -especies:List │         │ -uf:String      │
 │ -ativo:Boolean │         │ -coord:Geog     │
 └───────┬────────┘         └─────────────────┘
         │
    ┌────┼──────────────────────┐
    │    │                      │
 ┌──▼──────┐ ┌──────▼─────┐ ┌──▼──────┐
 │Slaught. │ │SwineFarm   │ │PoultryF.│
 │<<Subk.>>│ │<<Subk.>>   │ │<<Subk.>>│
 └─────────┘ └────────────┘ └─────────┘

 ┌────────────────┐
 │   Person        │
 │   <<Kind>>      │
 └────────────────┘

 ┌──────────────────────────┐
 │         CAR              │
 │       <<Relator>>        │
 │ ┌──────────────────────┐ │
 │ │connects Establishment│ │
 │ │to its perimeter      │ │
 │ └──────────────────────┘ │
 └──────────────────────────┘
```

### 6.3 Sanitary Investigation Subdomain

```
 ┌───────────────────┐         ┌─────────────────────┐
 │  SanitaryAnalysis  │────*────│   Person            │
 │    <<Event>>       │    1    │   <<Kind>>          │
 ├───────────────────┤         └─────────────────────┘
 │ -nome:String      │
 │ -ativa:Boolean    │──1────*──┌─────────────────────┐
 │ -criadaEm:DateTime│         │ InvestigationTarget │
 └───────────────────┘         │    <<Role>>         │
                               ├─────────────────────┤
 ┌──────────────────┐          │ -lat/lng:BigDecimal │
 │  AffectedArea    │──*──*──│ -zone1/2/3:Integer  │
 │   <<Kind>>       │         │ -dataMov:LocalDate  │
 └──────────────────┘         └──────────┬──────────┘
                                         │*        1
                                   ┌─────▼──────────┐
                                   │  Establishment  │
                                   │   <<Kind>>      │
                                   └─────────────────┘

 ┌─────────────────────────┐
 │InvestigationControlZone │
 │      <<Relator>>        │
 ├─────────────────────────┤
 │ -tipo:ZoneType          │
 │ -raio:Integer           │
 └─────────────────────────┘

 ┌──────────────────────┐       ┌──────────────────────┐
 │  AnimalMovement      │──*──1│  Establishment       │
 │    <<Event>>          │ (origin and destination)    │
 ├──────────────────────┤       └──────────────────────┘
 │ -serie,numero,uf:PK  │
 │ -especie,quantidade  │
 │ -finalidade:enum     │
 └──────────────────────┘

 ┌────────────────────────┐
 │  ContactingProperty     │
 │      <<Role>>          │
 ├────────────────────────┤
 │ -tipo:Direct/Indirect  │
 │ (matter: Establishm.) │
 └────────────────────────┘
```

### 6.4 Sanitary Response Subdomain

```
 ┌──────────────────────┐         ┌───────────────────────┐
 │   SanitaryResponse    │────1───│   SanitaryAnalysis    │
 │     <<Event>>         │    *   │     <<Event>>         │
 ├──────────────────────┤         └───────────────────────┘
 │ -identificador:String│
 │ -dataVencimento:Date │──1──*──┌────────────────────────┐
 │ -ativa,concluida:Bool│        │    SurveillanceCycle   │
 └──────────┬───────────┘        │      <<Event>>         │
            │                    ├────────────────────────┤
       ┌────┴────┐               │ -numeroCiclo:Integer   │
       │         │               │ -concluido:Boolean     │
 ┌─────▼────┐ ┌──▼────────┐     └───────────┬────────────┘
 │CommandP. │ │Convoked    │                 │
 │<<Kind>>  │ │User        │            ┌────┴────┐
 └─────────┘ │ <<Role>>   │            │         │
             └────────────┘      ┌─────▼──┐ ┌───▼────────┐
                                 │ZonePer │ │FieldTeam   │
                                 │ Cycle  │ │<<Collect.>>│
 ┌──────────────────────┐        │<<Relat>>│ └──┬──┬──┬──┘
 │   OperationalArea    │        └────────┘    │  │  │
 │     <<Kind>>         │          ↑           │  │  │
 ├──────────────────────┤          │*           │  │  │
 │ -nome,cor,String     │──────────┘           │  │  │
 │ -boundary:Polygon    │                      │  │  │
 └──────────┬───────────┘            ┌─────────┘  │  │
            │                       │            │  │
       ┌────┴────┐            ┌─────▼──┐  ┌──────┘  │
       │         │            │Team    │  │         │
 ┌─────▼────┐    │            │Member  │  │         │
 │Property. │    │            │<<Role>>│  │         │
 │ In Area  │    │            └──┬──────┘  │         │
 │<<Relator>>│   │               │         │         │
 ├──────────┤    │               │*        │         │
 │-concluída│    │          ┌────▼──┐  ┌──┴───┐  ┌──┴────┐
 │:Boolean  │    │          │Func.  │  │Vehic.│  │Barrier│
 └────┬─────┘    │          │<<Kind>>│  │<<Kind>>│ │<<Kind>>│
      │*         │          └───────┘  └───────┘  └───────┘
 ┌────▼──────┐   │
 │Establish.│   │
 │<<Kind>>   │   │
 └───────────┘   │
                 │
 ┌───────────────┴────────────────────────────────────────┐
 │                  GPSTracking                            │
 │                    <<Event>>                            │
 ├────────────────────────────────────────────────────────┤
 │ -dataInicio,fim:DateTime                                │
 │ -coordenadas:LatLng[*]                                  │
 └────────────────────────────────────────────────────────┘
```

### 6.5 Field Actions Subdomain

```
 ┌──────────────────────┐        ┌──────────────────────┐
 │ PropertySubmission    │──*──1─│ PropertyInArea       │
 │     <<Event>>         │        │    <<Relator>>       │
 ├──────────────────────┤        └──────────────────────┘
 │ -uuid:UUID           │
 │ -dataHora:DateTime   │──*──1─┌──────────────────────┐
 └──────────────────────┘        │   FieldTeam          │
                                 │  <<Collective>>      │
 ┌──────────────────────┐        └──────────────────────┘
 │  BarrierSubmission    │──*──1─┌──────────────────────┐
 │     <<Event>>         │        │  SanitaryBarrier    │
 ├──────────────────────┤        │    <<Kind>>         │
 │ -uuid:UUID           │        └──────────────────────┘
 │ -dataHora:DateTime   │
 └──────────────────────┘        ┌──────────────────────┐
                                  │ TemporaryProperty    │
                                  │     <<Role>>         │
                                  ├──────────────────────┤
                                  │ -contact,cpf,phone   │
                                  │ -lat/lng            │
                                  │ (matter:Establish.) │
                                  └──────────────────────┘
```

---

## 7. Model Axioms

### Identity Axioms

| ID | Axiom |
|----|-------|
| AX-ID-01 | Each `Establishment` has a unique `codigoSDA` |
| AX-ID-02 | Each `Person` is uniquely identified by `keycloak_subject_id`, `cpf`, and `email` |
| AX-ID-03 | Each `AnimalMovement` is identified by the triple `(serie, numero, ufOrigem)` |
| AX-ID-04 | Each `PropertySubmission` and `BarrierSubmission` is identified by a unique `uuid` |
| AX-ID-05 | A `SurveillanceCycle` is uniquely identified by `(numeroCiclo, SanitaryResponse)` |

### Dependency Axioms

| ID | Axiom |
|----|-------|
| AX-DEP-01 | Every `SurveillanceCycle` belongs exclusively to one `SanitaryResponse` |
| AX-DEP-02 | Every `FieldTeam` belongs exclusively to one `SurveillanceCycle` |
| AX-DEP-03 | Every `OperationalArea` belongs to one `FieldTeam` and one `ZonePerCycle` |
| AX-DEP-04 | Every `PropertyInArea` belongs to exactly one `OperationalArea` |
| AX-DEP-05 | Every `PropertySubmission` is linked to one `PropertyInArea` and one `FieldTeam` |
| AX-DEP-06 | Every `BarrierSubmission` is linked to one `SanitaryBarrier` |
| AX-DEP-07 | Every `InvestigationTarget` depends on exactly one `SanitaryAnalysis` |
| AX-DEP-08 | Every `SanitaryResponse` depends on exactly one `SanitaryAnalysis` |

### Sequence & Temporal Axioms

| ID | Axiom |
|----|-------|
| AX-SEQ-01 | Surveillance cycles are numbered sequentially within a response: `UNIQUE(numeroCiclo, response_id)` |
| AX-SEQ-02 | A cycle can only be closed when all its operational areas are completed |
| AX-SEQ-03 | An operational area is completed when all its properties have been visited |

### Cardinality & Uniqueness Axioms

| ID | Axiom |
|----|-------|
| AX-CARD-01 | A professional can only be convoked once per response: `UNIQUE(user_id, response_id)` |
| AX-CARD-02 | An establishment can be the target of multiple simultaneous investigations (no uniqueness constraint) |
| AX-CARD-03 | A team can have multiple members (1:N) |
| AX-CARD-04 | A response can have at most one Command Post (1:1) |

### State Axioms

| ID | Axiom | States |
|----|-------|--------|
| AX-STATE-01 | `SanitaryAnalysis` can be active or inactive | `{ativa, inativa}` |
| AX-STATE-02 | `SanitaryResponse` can be active, completed, or soft-deleted | `{ativa, concluida}` |
| AX-STATE-03 | `ZonePerCycle` can be open or closed | `{aberta, fechada}` |
| AX-STATE-04 | `PropertyInArea` can be complete or pending (`isCompleted`) | `{pendente, completa}` |

---

## 8. Model Dictionary

### Core

| Concept | Definition |
|---------|-----------|
| **Establishment** | Rural productive unit registered in the veterinary service, with unique SDA code |
| **Address** | Location data of an establishment (street, municipality, UF, coordinates) |
| **Person** | Individual registered in the Official Veterinary Service (SVO) with access credentials |
| **Animal Species** | Classification of exploited animal species (bovine, swine, poultry, ovine, caprine) |
| **Slaughterhouse** | Slaughter establishment with sanitary inspection type (SIF, SIE, SIM) |
| **Swine Farm** | Establishment specialized in swine production |
| **Poultry Farm** | Establishment specialized in poultry production |
| **CAR** | Public registry of the geospatial perimeter of the rural property |

### Sanitary Investigation

| Concept | Definition |
|---------|-----------|
| **Sanitary Analysis** | Record of opening an epidemiological investigation into a disease suspicion |
| **Investigation Target** | Property designated as the investigation focus, with coordinates and zone radii |
| **Affected Area** | Geographic region (municipalities, polygons) under investigation |
| **Control Zone** | Geographic perimeter around a target (Perifoco, Vigilância, Proteção, Investigação) |
| **Animal Movement** | Animal transit record (GTA) between properties, by species |
| **Contacting Property** | Property with direct or indirect contact to an investigated property |
| **Species Category** | Sanitary classification of species (poultry, swine, ovine, bovine, others) |

### Sanitary Response

| Concept | Definition |
|---------|-----------|
| **Sanitary Response** | Central record of outbreak containment coordination |
| **Surveillance Cycle** | Numbered sweep round in a control zone |
| **Zone per Cycle** | Geospatial delimitation of each zone within a specific cycle |
| **Field Team** | Group of professionals allocated to surveillance operations |
| **Team Member** | Person linked to a team with a specific function |
| **Function** | Predefined role (member, barrier modeling, surveillance modeling) |
| **Operational Area** | Geographic sector assigned to a team within a zone |
| **Property in Area** | Link between property and operational area with completion control |
| **Sanitary Barrier** | Fixed or mobile post for animal transit inspection |
| **Vehicle** | Patrol car linked to field teams |
| **Command Post** | HQ of the response operation, with address and coordinates |
| **Convoked User** | Person mobilized for a response with specific permissions |
| **GPS Tracking** | Record of team displacement in the field |
| **Team Type** | Functional classification (surveillance, barrier, vaccination, etc.) |

### Field Actions

| Concept | Definition |
|---------|-----------|
| **Property Submission** | Form completed during a property visit |
| **Barrier Submission** | Form completed at a sanitary barrier |
| **Temporary Property** | Unregistered unit found in the field |

---

## 9. Verification (Competency Question × Model)

| CQ | Answer Path |
|----|-------------|
| CQ-CORE-01 | `Establishment` instances |
| CQ-CORE-02 | `Establishment.especies` |
| CQ-CORE-03 | `Establishment → Address.coordenadas` |
| CQ-INV-01 | `InvestigationTarget → Establishment` filtered by zone radius |
| CQ-INV-03 | `AnimalMovement(origin/destination = Establishment)` |
| CQ-RES-01 | `SanitaryResponse → SurveillanceCycle` |
| CQ-RES-02 | `SurveillanceCycle → FieldTeam` |
| CQ-RES-03 | `FieldTeam → TeamMember → Person` |
| CQ-RES-09 | `SanitaryResponse → SurveillanceCycle → FieldTeam → Barrier` |
| CQ-CAM-01 | `OperationalArea → PropertyInArea → PropertySubmission` |
| CQ-CAM-02 | `PropertyInArea.concluida` |

*Complete verification table in `03-ontouml-model.md` Section 8.*

---

## 10. Version Control

| Version | Date | Description |
|---------|------|-------------|
| v.01 | 06/24/2026 | Complete version of the SIGEVS-O reference ontology |
| v.02 | 07/04/2026 | Renamed Professional→Person; removed ModuleAccess and AuditLog; SpeciesCategory as Enumeration; total 32 classes |

---

## 11. References

- Ontology Specification Document: `../1-requirements/04-doc-spec.md`
- Reference Ontology Premises: `../2-setup/01-doc-refe.md`
- Concept Catalog: `01-cap-cata.md`
- Axioms: `02-cap-axim.md`
- OntoUML Model: `03-ontouml-model.md`
- OntoUML JSON (ontouml-schema): `04-sigevs-o.ontouml.json`
- Capture Guide: `00-capture-guide.md`
- Source Code: `C:\LUMAC\sigevs-api\`
