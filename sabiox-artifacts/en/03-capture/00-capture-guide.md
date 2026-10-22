# Source Code Data Capture Guide — SIGEVS-O

---

## 1. Source Map by Subdomain

### Subdomain: Core

| Source | Location | What to Extract |
|--------|----------|-----------------|
| **Establishment** | `model/registration/Estabelecimento.java` | Attributes, types, relationship with Address |
| **Address** | `model/registration/Endereco.java` | Location attributes |
| **User** | `model/registration/Usuario.java` | Attributes, relationship with Module |
| **Module** | `model/registration/Modulo.java` | Profiles and permissions |
| **State** | `model/registration/Estado.java` | UF |
| **City** | `model/registration/Cidade.java` | Municipalities |
| **Slaughterhouse** | `model/registration/Frigorifico.java` | Inspection type |
| **RuralEnvironmentalRegistry** | `model/registration/CadastroAmbientalRural.java` | CAR |
| **SwineFarm / PoultryFarm** | `model/registration/granja/` | Species-specific specifications |
| **DB Tables** | `cadastros.estabelecimento`, `cadastros.usuario`, `cadastros.endereco`, `cadastros.frigorifico` | Constraints, indexes, column types |
| **Enums** | `enums/SpeciesCategory.java` | Species categories |
| **Controllers** | `PremiseController`, `UsuarioController`, `ModuloController`, `CARController` | Registration endpoints |
| **DTOs** | `dto/premise/PremiseDTO`, `registration/UsuarioDTO` | Transmitted fields |

### Subdomain: Sanitary Investigation

| Source | Location | What to Extract |
|--------|----------|-----------------|
| **SanitaryAnalysis** | `model/SanitaryAnalysis.java` | Central investigation record |
| **AnalysisTarget** | `model/AnalysisTarget.java` | Investigation targets, zones (zone1, zone2, zone3) |
| **AffectedArea** | `model/AffectedArea.java` | Affected geographic areas |
| **Movement*** | `model/movement/Movimentacao*.java` (7 subclasses) | Animal movement (GTA) by species |
| **MovimentacaoAvesView** | `model/movement/MovimentacaoAvesView.java` | Consolidated movement view |
| **DB Tables** | `sigevs.sanitary_analysis`, `sigevs.analysis_targets`, `movimentacao.movimentacao_*` | Constraints, geospatial indexes |
| **Enums** | `ZoneType`, `SpeciesCategory`, `MovementPurpose` | Classifying types |
| **Controllers** | `SanitaryAnalysisController`, `AnimalMovementController` | Endpoints |
| **DTOs** | `SanitaryAnalysisDTO`, `AnalysisTargetDTO`, `MovementDTO`, `MovementFilterDTO` | Transmitted data |

### Subdomain: Sanitary Response

| Source | Location | What to Extract |
|--------|----------|-----------------|
| **SanitaryEventResponse** | `model/SanitaryEventResponse.java` | Central response record |
| **ResponseSurveillanceCycle** | `model/response/ResponseSurveillanceCycle.java` | Surveillance cycles |
| **SurveillanceCycleZone** | `model/response/SurveillanceCycleZone.java` | Zones per cycle |
| **ResponseTeam** | `model/response/ResponseTeam.java` | Field teams |
| **TeamMember** | `model/response/TeamMember.java` | Team members |
| **TeamType** | `model/response/TeamType.java` | Team types |
| **ResponseArea** | `model/response/ResponseArea.java` | Operational areas |
| **AreaPremise** | `model/response/AreaPremise.java` | Properties in area |
| **ResponseBarrier** | `model/response/ResponseBarrier.java` | Sanitary barriers |
| **ResponseVehicle** | `model/response/ResponseVehicle.java` | Vehicles |
| **ResponseCommandPost** | `model/response/ResponseCommandPost.java` | Command post |
| **ResponseConvokedUsers** | `model/response/ResponseConvokedUsers.java` | Convoked users |
| **ResponseRoles** | `model/response/ResponseRoles.java` | Roles/functions |
| **TeamTracking** | `model/response/TeamTracking.java` | GPS tracking |
| **DB Tables** | `sigevs.sanitary_event_response`, `sigevs.response_*`, `sigevs.team_*` | Constraints, indexes |
| **Enums** | `ZoneType`, `ResponseBarrierType`, `ResponseBarrierRole` | Classifiers |
| **Controllers** | `SanitaryEventResponseController`, `ResponseAreaController`, `ResponseBarrierController`, `ResponseTeamController`, `ResponseVehicleController`, `ResponseConvokedUsersController`, `ResponseCommandPostController`, `ResponseSurveillanceCycleController`, `TeamTrackingController` | Endpoints |
| **DTOs** | `SanitaryEventResponseDTO`, `ResponseAreaDTO`, `ResponseBarrierDTO`, `ResponseTeamDTO`, `ResponseVehicleDTO`, `ResponseSurveillanceCycleDTO`, `TeamTrackingDTO`, `TeamStatsDTO` | Transmitted data |

### Subdomain: Field Actions

| Source | Location | What to Extract |
|--------|----------|-----------------|
| **PremiseSubmission** | `model/PremiseSubmission.java` | Property submission |
| **BarrierSubmission** | `model/BarrierSubmission.java` | Barrier submission |
| **TemporaryPremise** | `model/TemporaryPremise.java` | Temporary property |
| **EventSystemLog** | `model/EventSystemLog.java` | Audit log |
| **DB Tables** | `sigevs.premise_submissions`, `sigevs.barrier_submissions`, `sigevs.temporary_premises`, `sigevs.event_system_log` | Constraints |
| **Enums** | `SysEventType` | Log event types |
| **Controllers** | `SubmissionController`, `TemporaryPremiseController`, `EventActionsController` | Endpoints |
| **DTOs** | `PremiseSubmissionDTO`, `BarrierSubmissionDTO`, `SubmissionData`, `ResponseSubmissionsDTO`, `TempPremiseSubmissionDTO` | Transmitted data |

---

## 2. Concept Extraction Template

For each identified concept, fill out the following card:

```markdown
## Concept: [Concept Name]

### Subdomain
[Core | Investigation | Response | Field]

### Definition
[Conceptual description of the term in the domain]

### Code Mapping
- **JPA Entity**: [Name.java]
- **DB Table**: [schema.table]
- **DTO**: [NameDTO.java]
- **Controller**: [NameController.java] → [endpoints]
- **Service**: [NameService.java]

### Attributes
| Attribute | Type | Description | UFO Mapping |
|-----------|------|-------------|-------------|
| [name] | [Java type] | [description] | [Quality | Mode | ...]

### Relationships
| Type | Target | Cardinality | Description |
|------|--------|-------------|-------------|
| [@ManyToOne] | [Entity] | [N:1] | [description] |

### Enums Used
- [EnumName]: [relevant values]

### Rules / Constraints
- [Business rule extracted from code / DB]

### Associated Endpoints
- [METHOD] [path]

### Related Competency Questions
- [CQ-XXX-XX]

### Candidate UFO Stereotype
[<<Kind>> | <<Role>> | <<Event>> | <<Relator>> | <<Collective>> | <<Phase>> | <<Quality>>]
```

---

## 3. Enum Catalog

| Enum | Values | Ontological Concept |
|------|--------|---------------------|
| `ZoneType` | `INFECTED` (Perifoco), `BUFFER` (Vigilância), `SURVEILLANCE` (Proteção), `INVESTIGATION` (Investigação) | Control Zone Types |
| `ResponseBarrierType` | `FIXED` (Fixed Post), `MOBILE` (Mobile) | Sanitary Barrier Type |
| `ResponseBarrierRole` | `SANITARY` (Sanitary Barrier), `DIVERSION` (Diversion Barrier) | Barrier Function |
| `SpeciesCategory` | `AVES`, `SUINOS`, `OVINOS`, `BOVINOS`, `OUTROS` (with subtypes) | Animal Species Category |
| `MovementPurpose` | `ABATE`, `ENGORDA`, `OUTROS` | Movement Purpose |
| `SysEventType` | `INSERT`, `UPDATE`, `DELETE`, `DEACTIVATE`, `PROCESS_INFO`, `PROCESS_SUCCESS`, `PROCESS_ERROR`, `API_CALL`, `LOGIN_SUCCESS`, `LOGIN_FAILURE`, `ACCESS`, `ERROR`, `CUSTOM` | Audit Event Type |
| `AsyncTaskStatus` | `READY`, `RUNNING`, `SUCCESS`, `FAILED`, `CANCELLED` | Asynchronous Task Status |
| `TeamType` (BD) | `VIGILANCIA`, `LIMPEZA_DESINFECCAO`, `VACINACAO`, `INVESTIGACAO`, `AVALIACAO`, `DEPOPULACAO`, `BARREIRA` | Field Team Type |
| `ResponseRoles` (BD) | `MEMBRO`, `MODELAGEM_BARREIRA`, `MODELAGEM_VIGILANCIA` | Team Role/Function |

---

## 4. Business Rules Identified from Code

| ID | Rule | Source | Subdomain |
|----|------|--------|-----------|
| BR-01 | A team can only be allocated to one cycle at a time | `UNIQUE(team_id, cycle_id)` → `UNIQUE(user_id, response_id)` in convoked_users | Response |
| BR-02 | An outbreak can have up to three concentric zones: Perifoco, Vigilância, and Proteção | `ZoneType` enum + zone1/2/3 fields in AnalysisTarget | Investigation |
| BR-03 | An operational area is completed when all its properties have been visited | `is_completed` in AreaPremise; logic in EventActionsService | Field |
| BR-04 | A surveillance cycle belongs exclusively to one sanitary response | `FOREIGN KEY (response_id)` in response_surveillance_cycle | Response |
| BR-05 | Surveillance cycles follow a sequential ordering within a response | `UNIQUE(cycle_number, response_id)` | Response |
| BR-06 | A property can only be in one zone per cycle | Area structure → property → zone → cycle | Response |
| BR-07 | A cycle can only be closed after all areas are completed | Logic in EventActionsService | Response |
| BR-08 | A user can only be convoked once per response | `UNIQUE(user_id, response_id)` in convoked_users | Response |
| BR-09 | Property submission links to an area_premise + team | `FOREIGN KEY (area_premise_id, team_id)` | Field |
| BR-10 | Barrier submission links to a specific barrier | `FOREIGN KEY (barrier_id)` in barrier_submissions | Field |
| BR-11 | Temporary property can be linked to an existing establishment later | `premise_id` FK optional in temporary_premises | Field |
| BR-12 | Each investigation has an additional "Investigation" zone type beyond the three standard zones | `INVESTIGATION` in ZoneType | Investigation |
| BR-13 | A sanitary response can have a command post (0 or 1) | `OneToOne` response_command_post → response | Response |
| BR-14 | GPS tracking of teams is done by period (start/end time) | `TeamTracking` with createdAt + endTime | Response |
| BR-15 | Modules define user access permissions | `@ManyToMany Usuario ↔ Modulo` via `usuario_modulos` | Core |

---

## 5. Traceability Matrix

### Template

```
[Concept]
├─ JPA Entity: [Name.java]
├─ DB Table: [schema.table]
├─ Endpoints:
│   ├─ [METHOD] [path]
│   └─ [METHOD] [path]
├─ DTO: [NameDTO.java]
├─ Service: [NameService.java]
└─ CQs: [IDs]
```

### Completed Examples

```
Sanitary Outbreak (SanitaryAnalysis → SanitaryEventResponse)
├─ JPA Entities: SanitaryAnalysis.java, SanitaryEventResponse.java
├─ DB Tables: sigevs.sanitary_analysis, sigevs.sanitary_event_response
├─ Endpoints:
│   ├─ POST /sanitary-analysis
│   ├─ POST /event-response
│   ├─ GET  /event-response/{uuid}
│   └─ GET  /sanitary-analysis/{uuid}
├─ DTOs: SanitaryAnalysisDTO, SanitaryEventResponseDTO
├─ Services: SanitaryAnalysisService, SanitaryEventResponseService
└─ CQs: CQ-INV-01, CQ-INV-07

Surveillance Cycle
├─ JPA Entity: ResponseSurveillanceCycle.java
├─ DB Table: sigevs.response_surveillance_cycle
├─ Endpoints:
│   ├─ GET  /event-response/{uuid}/cycles
│   ├─ POST /event-response/{uuid}/cycles
│   ├─ POST /event-response/{uuid}/cycles/{roundNumber}/replicate
│   └─ PUT  /event-response/{uuid}/cycles/{roundNumber}
├─ DTO: ResponseSurveillanceCycleDTO
├─ Service: ResponseSurveillanceCycleService
└─ CQs: CQ-RES-01, CQ-RES-05

Field Team
├─ JPA Entities: ResponseTeam.java, TeamMember.java
├─ DB Tables: sigevs.response_teams, sigevs.team_members
├─ Endpoints:
│   ├─ POST /teams/{uuid}
│   ├─ GET  /teams/{uuid}
│   └─ DELETE /teams/{id}
├─ DTOs: ResponseTeamDTO, TeamMemberDTO
├─ Service: ResponseTeamService
└─ CQs: CQ-RES-02, CQ-RES-03, CQ-RES-07

Sanitary Barrier
├─ JPA Entity: ResponseBarrier.java
├─ DB Table: sigevs.response_barriers
├─ Enums: ResponseBarrierType, ResponseBarrierRole
├─ Endpoints:
│   ├─ POST /barriers
│   ├─ DELETE /barriers/{id}
│   ├─ GET  /barriers/by-team/{teamId}
│   └─ GET  /barriers/by-focus-response/{uuid}
├─ DTO: ResponseBarrierDTO
├─ Service: ResponseBarrierService
└─ CQs: CQ-RES-04, CQ-RES-09, CQ-RES-11
```

---

## 6. Directory Structure of Relevant Code

```
src/main/java/br/com/pdsars/sigevs/
├── model/
│   ├── SanitaryAnalysis.java
│   ├── AnalysisTarget.java
│   ├── AffectedArea.java
│   ├── SanitaryEventResponse.java
│   ├── PremiseSubmission.java
│   ├── BarrierSubmission.java
│   ├── TemporaryPremise.java
│   ├── EventSystemLog.java
│   ├── response/
│   │   ├── ResponseSurveillanceCycle.java
│   │   ├── SurveillanceCycleZone.java
│   │   ├── ResponseTeam.java
│   │   ├── TeamMember.java
│   │   ├── TeamType.java
│   │   ├── ResponseArea.java
│   │   ├── AreaPremise.java
│   │   ├── ResponseBarrier.java
│   │   ├── ResponseVehicle.java
│   │   ├── ResponseCommandPost.java
│   │   ├── ResponseConvokedUsers.java
│   │   ├── ResponseRoles.java
│   │   └── TeamTracking.java
│   ├── movement/
│   │   ├── Movimentacao.java (abstract)
│   │   ├── MovimentacaoAves.java
│   │   ├── MovimentacaoBovinos.java
│   │   ├── MovimentacaoSuinos.java
│   │   ├── MovimentacaoOvinos.java
│   │   ├── MovimentacaoCaprinos.java
│   │   ├── MovimentacaoBubalinos.java
│   │   ├── MovimentacaoPerus.java
│   │   └── MovimentacaoAvesView.java
│   ├── registration/
│   │   ├── Estabelecimento.java
│   │   ├── Endereco.java
│   │   ├── Usuario.java
│   │   ├── Modulo.java
│   │   ├── Estado.java
│   │   ├── Cidade.java
│   │   ├── Frigorifico.java
│   │   ├── CadastroAmbientalRural.java
│   │   └── granja/
│   │       ├── GranjaSuino.java
│   │       └── GranjaAve.java
│   └── spread/
│       ├── Scenario.java
│       └── ControlActions.java
├── enums/
│   ├── ZoneType.java
│   ├── SysEventType.java
│   ├── SpeciesCategory.java
│   ├── ResponseBarrierType.java
│   ├── ResponseBarrierRole.java
│   └── MovementPurpose.java
├── dto/
│   ├── SanitaryEventResponseDTO.java
│   ├── SanitaryAnalysisDTO.java
│   └── ... (remaining DTOs)
├── controller/
│   ├── SanitaryEventResponseController.java
│   ├── SanitaryAnalysisController.java
│   └── ... (remaining controllers)
└── service/
    ├── SanitaryEventResponseService.java
    ├── SanitaryAnalysisService.java
    └── ... (remaining services)

src/main/resources/db/migration/
├── V202508101530__init_database.sql
├── V202508121430__create_schema_sigevs.sql
├── V202508131400__insert_initial_data.sql
├── V202508141000__async_table.sql
├── V202511111430__add_new_imports.sql
├── V202511180000__add_export_types.sql
├── V202512081050__create_fk_temp_premise.sql
└── V202512281430__create_schema_spread.sql
```

---

## 7. Code Term → Ontological Concept Glossary

| Code Term | Ontological Concept | Subdomain |
|-----------|---------------------|-----------|
| `Estabelecimento` / `premise` | Rural Establishment | Core |
| `Usuario` / `user` | SVO Professional | Core |
| `Endereco` | Address / Location | Core |
| `Modulo` | Module / Access Permission | Core |
| `Frigorifico` | Slaughterhouse | Core |
| `GranjaSuino` / `GranjaAve` | Specialized Farm | Core |
| `SanitaryAnalysis` | Sanitary Analysis | Investigation |
| `AnalysisTarget` | Investigation Target | Investigation |
| `AffectedArea` | Affected Area | Investigation |
| `ZoneType` (INFECTED/BUFFER/SURVEILLANCE/INVESTIGATION) | Control Zone Type | Investigation |
| `Movimentacao` (and subclasses) | Animal Movement / GTA | Investigation |
| `SanitaryEventResponse` | Sanitary Response | Response |
| `ResponseSurveillanceCycle` | Surveillance Cycle | Response |
| `SurveillanceCycleZone` | Zone per Cycle | Response |
| `ResponseTeam` | Field Team | Response |
| `TeamMember` | Team Member | Response |
| `TeamType` (VIGILANCIA, BARREIRA, etc.) | Team Type | Response |
| `ResponseArea` | Operational Area | Response |
| `AreaPremise` | Property in Area | Response |
| `ResponseBarrier` | Sanitary Barrier | Response |
| `ResponseVehicle` | Vehicle / Patrol Car | Response |
| `ResponseCommandPost` | Command Post | Response |
| `ResponseConvokedUsers` | Convoked User | Response |
| `ResponseRoles` (MEMBRO, MODELAGEM_*) | Team Role | Response |
| `TeamTracking` | GPS Tracking | Response |
| `PremiseSubmission` | Property Submission | Field |
| `BarrierSubmission` | Barrier Submission | Field |
| `TemporaryPremise` | Temporary Property | Field |
| `EventSystemLog` | Audit Log | Field |
