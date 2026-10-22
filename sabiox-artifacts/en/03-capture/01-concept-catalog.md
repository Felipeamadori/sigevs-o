# Capture Phase — CAP-CATA (Concept Catalog)

---

## SIGEVS-O Domain Concept Catalog

| Field | Value |
|-------|-------|
| Ontology: | SIGEVS-O — Ontology for Sanitary Event Management |
| Version: | v.01 |
| Date: | 06/23/2026 |
| Sources: | Funcionalidades SIGEVS.md, Source Code (sigevs-api), Iniciativa.md |

---

## Subdomain: Core

### C01 — Establishment

| Field | Value |
|-------|-------|
| **Definition** | Rural productive unit registered in the veterinary service, with unique SDA code, geographic coordinates, exploited species, and address |
| **JPA Entity** | `Estabelecimento.java` |
| **DB Table** | `cadastros.estabelecimento` (id, uuid, ativo, nome_estabelecimento, codigo_estabelecimento UNIQUE, id_endereco FK, tipo, especies text[]) |
| **DTO** | `PremiseDTO`, `PremiseFormDTO` |
| **Controller** | `PremiseController` |
| **Service** | `PremiseService` |
| **Attributes** | codigoEstabelecimento (SDA code), nomeEstabelecimento, tipo (default "Propriedade Rural"), especies (String[]), ativo, coordenadas (via Endereco), carShape (Poligono) |
| **Relationships** | Endereco (N:1), AreaPremise (1:N), GranjaSuino (1:1), GranjaAve (1:1), Frigorifico (1:1), AnalysisTarget (1:N), TemporaryPremise (1:1) |
| **UFO Stereotype** | `<<Kind>>` — independent identity regardless of context |
| **CQs** | CQ-CORE-01, CQ-CORE-02, CQ-CORE-03, CQ-CORE-05 |

---

### C02 — Address

| Field | Value |
|-------|-------|
| **Definition** | Location data of an establishment, including street, municipality, state, and geographic coordinates |
| **JPA Entity** | `Endereco.java` |
| **DB Table** | `cadastros.endereco` (id_endereco, rua, cep, numero, bairro, cidade, uf, latitude, longitude, coord GEOGRAPHY) |
| **DTO** | `AddressDTO` |
| **Attributes** | rua, cep, numero, bairro, cidade, uf, latitude, longitude |
| **Relationships** | Estabelecimento (1:N) |
| **UFO Stereotype** | `<<Kind>>` — entity with its own identity and attributes |
| **CQs** | CQ-CORE-03 |

---

### C03 — Person

| Field | Value |
|-------|-------|
| **Definition** | Individual registered in the official veterinary service, with access credentials, profile, and permissions |
| **JPA Entity** | `Usuario.java` |
| **DB Table** | `cadastros.usuario` (id_usuario, keycloak_subject_id UNIQUE, cpf UNIQUE, nome, email UNIQUE, data_cadastro, ativo, foto, uuid) |
| **DTO** | `UsuarioDTO`, `RegisterUserDTO` |
| **Controller** | `UsuarioController` |
| **Service** | `UsuarioService` |
| **Relationships** | SanitaryAnalysis (1:N), TeamMember (1:N), ResponseConvokedUsers (1:N) |
| **UFO Stereotype** | `<<Kind>>` — independent identity |
| **CQs** | CQ-CORE-04, CQ-CORE-07 |

---

### C04 — Animal Species

| Field | Value |
|-------|-------|
| **Definition** | Categorization of animal species exploited on properties, segmented by type and purpose |
| **Entity** | `SpeciesCategory` (enum) |
| **Values** | AVES (16 subtypes), SUINOS, OVINOS, BOVINOS, OUTROS (26 subtypes) |
| **Used in** | Estabelecimento.especies (String[]), movements, filters |
| **UFO Stereotype** | `<<Kind>>` for species; `<<Subkind>>` for subtypes |
| **CQs** | CQ-CORE-02 |

---

### C05 — Slaughterhouse

| Field | Value |
|-------|-------|
| **Definition** | Slaughter establishment with sanitary inspection type (SIF, SIE, SIM) |
| **JPA Entity** | `Frigorifico.java` |
| **DB Table** | `cadastros.frigorifico` |
| **Relationships** | Estabelecimento (1:1) |
| **Attributes** | sistemaInspecao, numeroInspecao, ativo |
| **UFO Stereotype** | `<<Subkind>>` of Establishment |
| **CQs** | CQ-CORE-06 |

---

### C06 — Specialized Farm

| Field | Value |
|-------|-------|
| **Definition** | Establishment specialized in swine or poultry production, with additional exploitation data |
| **JPA Entity** | `GranjaSuino.java`, `GranjaAve.java` |
| **DB Table** | `cadastros.granja_suino`, `cadastros.granja_ave` |
| **Relationships** | Estabelecimento (1:1) |
| **Attributes (Swine)** | finalidadeExploracao, integradora, registro, finalidadeExploracaoTipo |
| **Attributes (Poultry)** | especieExploracao, formaExploracao, finalidadeProducao, producaoComercial |
| **UFO Stereotype** | `<<Subkind>>` of Establishment |
| **CQs** | CQ-CORE-02 |

---

## Subdomain: Sanitary Investigation

### I01 — Sanitary Analysis

| Field | Value |
|-------|-------|
| **Definition** | Record of opening an epidemiological investigation into a disease suspicion, with filter metadata, authorship, and deadlines |
| **JPA Entity** | `SanitaryAnalysis.java` |
| **DB Table** | `sigevs.sanitary_analysis` (analysis_name, active, created_at, user_creation_id FK, public, show_car, uuid) |
| **DTO** | `SanitaryAnalysisDTO` |
| **Controller** | `SanitaryAnalysisController` |
| **Service** | `SanitaryAnalysisService` |
| **Relationships** | AnalysisTarget (1:N), SanitaryEventResponse (via analysis_id), originalAnalysis (self-ref) |
| **Attributes** | analysisName, isActive, createdAt, isPublic, showCar, metadata (filters JSON) |
| **UFO Stereotype** | `<<Event>>` — marks the start of an investigation |
| **CQs** | CQ-INV-07 |

---

### I02 — Investigation Target

| Field | Value |
|-------|-------|
| **Definition** | Property designated as an investigation focus, with coordinates and zone radii for control |
| **JPA Entity** | `AnalysisTarget.java` |
| **DB Table** | `sigevs.analysis_targets` (premise_id FK, target_name, lat/lng, zone1/2/3, start_date_mov, end_date_mov, input_mov, output_mov, coord GEOGRAPHY) |
| **DTO** | `AnalysisTargetDTO` |
| **Controller** | `SanitaryAnalysisController` |
| **Attributes** | premise, targetName, latitude, longitude, zone1, zone2, zone3, startDateMov, endDateMov, inputMov, outputMov |
| **Relationships** | SanitaryAnalysis (N:1), Estabelecimento (N:1), AffectedArea (N:1) |
| **UFO Stereotype** | `<<Role>>` — role that an Establishment assumes when under investigation |
| **CQs** | CQ-INV-01, CQ-INV-02 |

---

### I03 — Affected Area

| Field | Value |
|-------|-------|
| **Definition** | Geographic region (municipalities, polygons) designated as under investigation |
| **JPA Entity** | `AffectedArea.java` |
| **DB Table** | `sigevs.affected_area` (name, shape jsonb) |
| **DTO** | `AffectedArea` (endpoint returns without shape) |
| **UFO Stereotype** | `<<Kind>>` — geographic region with its own identity |
| **CQs** | CQ-INV-08 |

---

### I04 — Control Zone

| Field | Value |
|-------|-------|
| **Definition** | Geographic perimeter defined around a target, classified as Perifoco (infected), Vigilância (buffer), Proteção (extended surveillance), or Investigação |
| **DB Table** | Represented in the zone1/2/3 fields of `analysis_targets` |
| **Enum** | `ZoneType` — INFECTED("Perifoco"), BUFFER("Vigilancia"), SURVEILLANCE("Protecao"), INVESTIGATION("Investigacao") |
| **DTO** | `TemporaryZoneDTO` (zone, boundaryPoints) |
| **UFO Stereotype** | `<<Relator>>` — connects an outbreak to a geographic perimeter, with its own attributes (type, radius) |
| **CQs** | CQ-INV-01, CQ-INV-06 |

---

### I05 — Animal Movement (GTA)

| Field | Value |
|-------|-------|
| **Definition** | Record of animal transit between properties, with origin, destination, species, quantity, and purpose |
| **JPA Entity** | `Movimentacao` (abstract), `MovimentacaoAves`, `MovimentacaoBovinos`, `MovimentacaoSuinos`, `MovimentacaoOvinos`, `MovimentacaoCaprinos`, `MovimentacaoBubalinos`, `MovimentacaoPerus` |
| **DB Table** | `movimentacao.movimentacao_*` (each species) — composite key (serie, numero, uf_origem) |
| **View** | `movimentacao.vw_movimentacao_aves` |
| **DTO** | `MovementDTO` |
| **Controller** | `AnimalMovementController` |
| **Enum** | `MovementPurpose` (ABATE, ENGORDA, OUTROS) |
| **UFO Stereotype** | `<<Event>>` — movement event between establishments |
| **CQs** | CQ-INV-03 |

---

### I06 — Contacting Property

| Field | Value |
|-------|-------|
| **Definition** | Property that had direct contact (direct movement) or indirect contact (movement chain) with an investigated property |
| **JPA Entity** | No dedicated entity — calculated dynamically via movements |
| **Controller** | `SanitaryAnalysisController.POST /find-all-premises/by-targets` |
| **UFO Stereotype** | `<<Role>>` — role that an Establishment assumes when identified as contacting |
| **CQs** | CQ-INV-04, CQ-INV-05 |

---

### I07 — Species Category (for investigation)

| Field | Value |
|-------|-------|
| **Definition** | Classification of animal species into sanitary categories (poultry, swine, ovine, bovine, others) |
| **Enum** | `SpeciesCategory` |
| **DTO** | `MovementFilterDTO` (species list), `AnalysisMetadataDTO` (speciesFilter, explorationFilter) |
| **UFO Stereotype** | `<<Enumeration>>` — fixed sanitary classification values |
| **CQs** | CQ-INV-09 |

---

## Subdomain: Sanitary Response

### R01 — Sanitary Response

| Field | Value |
|-------|-------|
| **Definition** | Central record of the coordination of outbreak containment, with identifier, phase, deadlines, and status |
| **JPA Entity** | `SanitaryEventResponse.java` |
| **DB Table** | `sigevs.sanitary_event_response` (identifier, due_date, analysis_id FK, user_creation_id FK, public, active, completed, phase_id, uuid, response_connector_uuid) |
| **DTO** | `SanitaryEventResponseDTO` |
| **Controller** | `SanitaryEventResponseController` |
| **Service** | `SanitaryEventResponseService` |
| **Relationships** | SanitaryAnalysis (N:1), ResponseSurveillanceCycle (1:N), ResponseCommandPost (1:1), ResponseConvokedUsers (1:N) |
| **UFO Stereotype** | `<<Event>>` — central event that organizes containment |
| **CQs** | CQ-RES-01, CQ-RES-09, CQ-RES-13 |

---

### R02 — Surveillance Cycle

| Field | Value |
|-------|-------|
| **Definition** | Numbered sweep round in a control zone, with defined period and completion status |
| **JPA Entity** | `ResponseSurveillanceCycle.java` |
| **DB Table** | `sigevs.response_surveillance_cycle` (cycle_number UNIQUE c/ response_id, completed) |
| **DTO** | `ResponseSurveillanceCycleDTO` |
| **Controller** | `ResponseSurveillanceCycleController` |
| **Service** | `ResponseSurveillanceCycleService` |
| **Relationships** | SanitaryEventResponse (N:1), SurveillanceCycleZone (1:N), ResponseTeam (1:N) |
| **Constraint** | UNIQUE(cycle_number, response_id) → sequential cycles |
| **UFO Stereotype** | `<<Event>>` — time-bounded event that organizes field operations |
| **CQs** | CQ-RES-01, CQ-RES-05 |

---

### R03 — Zone per Cycle

| Field | Value |
|-------|-------|
| **Definition** | Geospatial delimitation of each zone (Perifoco, Vigilância, Proteção) within a specific cycle |
| **JPA Entity** | `SurveillanceCycleZone.java` |
| **DB Table** | `sigevs.surveillance_cycle_zone` (zone tipo ZoneType, start_date, end_date, closed NOT NULL, boundary_points jsonb) |
| **DTO** | `SurveillanceCycleZoneDTO` |
| **Enum** | `ZoneType` |
| **UFO Stereotype** | `<<Relator>>` — connects cycle to zone with its own attributes (dates, closure) |
| **CQs** | CQ-RES-05 |

---

### R04 — Field Team

| Field | Value |
|-------|-------|
| **Definition** | Group of professionals allocated to a surveillance cycle, with type, sector, color, and members |
| **JPA Entity** | `ResponseTeam.java` |
| **DB Table** | `sigevs.response_teams` (team_name, team_type_id FK, surveillance_cycle_id FK, active) |
| **DTO** | `ResponseTeamDTO` |
| **Controller** | `ResponseTeamController` |
| **Service** | `ResponseTeamService` |
| **Relationships** | ResponseSurveillanceCycle (N:1), TeamMember (1:N), ResponseVehicle (1:N), ResponseBarrier (1:N), ResponseArea (1:N) |
| **UFO Stereotype** | `<<Collective>>` — collective of professionals with joint action |
| **CQs** | CQ-RES-02, CQ-RES-07 |

---

### R05 — Team Type

| Field | Value |
|-------|-------|
| **Definition** | Functional classification of field teams (surveillance, cleaning, vaccination, investigation, assessment, depopulation, barrier) |
| **JPA Entity** | `TeamType.java` |
| **DB Table** | `sigevs.team_types` (type_name UNIQUE, label, sector, color) |
| **DTO** | `TeamTypeDTO` |
| **UFO Stereotype** | `<<Kind>>` — type of collective |
| **CQs** | CQ-RES-02 |

---

### R06 — Team Member

| Field | Value |
|-------|-------|
| **Definition** | Person linked to a field team with a specific function |
| **JPA Entity** | `TeamMember.java` |
| **DB Table** | `sigevs.team_members` (team_id FK, user_id FK, role_id FK, active) |
| **DTO** | `TeamMemberDTO` |
| **UFO Stereotype** | `<<Role>>` — role that a User assumes within a FieldTeam |
| **CQs** | CQ-RES-03 |

---

### R07 — Team Role

| Field | Value |
|-------|-------|
| **Definition** | Predefined role that guides allocation and responsibilities of a professional (member, barrier modeling, surveillance modeling) |
| **JPA Entity** | `ResponseRoles.java` |
| **DB Table** | `sigevs.response_roles` (role_name UNIQUE, label) |
| **Values** | MEMBRO, MODELAGEM_BARREIRA, MODELAGEM_VIGILANCIA |
| **UFO Stereotype** | `<<Kind>>` — type of function |
| **CQs** | CQ-RES-03 |

---

### R08 — Operational Area

| Field | Value |
|-------|-------|
| **Definition** | Geographic sector assigned to a team within a cycle zone, with polygon delimitation |
| **JPA Entity** | `ResponseArea.java` |
| **DB Table** | `sigevs.response_areas` (team_id FK, area_name, color, boundary_points jsonb, cycle_zone_id FK) |
| **DTO** | `ResponseAreaDTO` |
| **Controller** | `ResponseAreaController` |
| **Service** | `ResponseAreaService` |
| **Relationships** | ResponseTeam (N:1), SurveillanceCycleZone (N:1), AreaPremise (1:N) |
| **UFO Stereotype** | `<<Kind>>` — geographic subdivision with its own identity |
| **CQs** | CQ-RES-08, CQ-RES-10 |

---

### R09 — Property in Area

| Field | Value |
|-------|-------|
| **Definition** | Link between a property and an operational area, with visit completion control |
| **JPA Entity** | `AreaPremise.java` |
| **DB Table** | `sigevs.area_premises` (premise_id FK, area_id FK, completed) |
| **DTO** | `AreaPremiseDTO` |
| **Relationships** | ResponseArea (N:1), Estabelecimento (N:1), PremiseSubmission (1:N) |
| **Attributes** | isCompleted (Boolean) |
| **UFO Stereotype** | `<<Relator>>` — connects property to area with completion attribute |
| **CQs** | CQ-RES-10 |

---

### R10 — Sanitary Barrier

| Field | Value |
|-------|-------|
| **Definition** | Fixed or mobile post for animal transit inspection, with sanitary function (inspection) or diversion (redirect) |
| **JPA Entity** | `ResponseBarrier.java` |
| **DB Table** | `sigevs.response_barriers` (barrier_name, type FIXED/MOBILE, role SANITARY/DIVERSION, lat/lng, team_id FK, coord GEOGRAPHY) |
| **DTO** | `ResponseBarrierDTO` |
| **Controller** | `ResponseBarrierController` |
| **Service** | `ResponseBarrierService` |
| **Enums** | `ResponseBarrierType` (FIXED, MOBILE), `ResponseBarrierRole` (SANITARY, DIVERSION) |
| **Relationships** | ResponseTeam (N:1), BarrierSubmission (1:N) |
| **UFO Stereotype** | `<<Kind>>` — physical entity with its own identity |
| **CQs** | CQ-RES-04, CQ-RES-09, CQ-RES-11 |

---

### R11 — Vehicle / Patrol Car

| Field | Value |
|-------|-------|
| **Definition** | Fleet of vehicles linked to field teams, with plate, model, color, and type |
| **JPA Entity** | `ResponseVehicle.java` |
| **DB Table** | `sigevs.response_vehicles` (license_plate, model, color, brand, year, vehicle_type, team_id FK) |
| **DTO** | `ResponseVehicleDTO` |
| **Controller** | `ResponseVehicleController` |
| **Service** | `ResponseVehicleService` |
| **UFO Stereotype** | `<<Kind>>` — physical entity with its own identity |
| **CQs** | CQ-RES-12 |

---

### R12 — Command Post

| Field | Value |
|-------|-------|
| **Definition** | Operations headquarters (HQ) of the response operation, with address, coordinates, and notes |
| **JPA Entity** | `ResponseCommandPost.java` |
| **DB Table** | `sigevs.response_command_post` (response_id FK UNIQUE, name, address, notes, lat/lng) |
| **DTO** | `ResponseCommandPostDTO` |
| **Controller** | `ResponseCommandPostController` |
| **Relationship** | SanitaryEventResponse (1:1) |
| **UFO Stereotype** | `<<Kind>>` — physical entity with location |
| **CQs** | CQ-RES-13 |

---

### R13 — Convoked Person

| Field | Value |
|-------|-------|
| **Definition** | Person mobilized for a sanitary response, with function, quarantine status, permissions (management/observation), and link to team member |
| **JPA Entity** | `ResponseConvokedUsers.java` |
| **DB Table** | `sigevs.response_convoked_users` (user_id FK, response_id FK, dirty UNIQUE, active, dirty_until, management, observer, role_id FK, UNIQUE(user_id, response_id)) |
| **DTO** | `ResponseConvokedUsersDTO` |
| **Controller** | `ResponseConvokedUsersController` |
| **Service** | `ResponseConvokedUsersService` |
| **UFO Stereotype** | `<<Role>>` — role that a Person assumes in a response (generalizes Person with restrictedTo = kind) |
| **CQs** | CQ-RES-14 |

---

### R14 — Team GPS Tracking

| Field | Value |
|-------|-------|
| **Definition** | Record of the geographic displacement of field teams, with coordinates, accuracy, and timestamps |
| **JPA Entity** | `TeamTracking.java` |
| **DB Table** | `sigevs.team_tracking` (team_id, response_id, user_id, label, metadata jsonb, created_at, end_time, uuid) |
| **DTO** | `TeamTrackingDTO` |
| **Controller** | `TeamTrackingController` |
| **Service** | `TeamTrackingService` |
| **UFO Stereotype** | `<<Event>>` — continuous tracking event |
| **CQs** | CQ-RES-06 |

---

## Subdomain: Field Actions

### F01 — Property Submission

| Field | Value |
|-------|-------|
| **Definition** | Form completed during a property visit, linked to the area and responsible team |
| **JPA Entity** | `PremiseSubmission.java` |
| **DB Table** | `sigevs.premise_submissions` (area_premise_id FK, submission_uuid UNIQUE, team_id FK) |
| **DTO** | `PremiseSubmissionDTO`, `SubmissionData` |
| **Controller** | `SubmissionController.POST /submission/premise` |
| **UFO Stereotype** | `<<Event>>` — data collection event |
| **CQs** | CQ-CAM-01, CQ-CAM-03 |

---

### F02 — Barrier Submission

| Field | Value |
|-------|-------|
| **Definition** | Form completed at a sanitary barrier, with inspection data |
| **JPA Entity** | `BarrierSubmission.java` |
| **DB Table** | `sigevs.barrier_submissions` (barrier_id FK, submission_uuid UNIQUE) |
| **DTO** | `BarrierSubmissionDTO` |
| **Controller** | `SubmissionController.POST /submission/barrier` |
| **UFO Stereotype** | `<<Event>>` — data collection event |
| **CQs** | CQ-CAM-03 |

---

### F03 — Temporary Property

| Field | Value |
|-------|-------|
| **Definition** | Unregistered unit found in the field, recorded with contact, CPF/CNPJ, and coordinates |
| **JPA Entity** | `TemporaryPremise.java` |
| **DB Table** | `sigevs.temporary_premises` (uuid, contact_name, cpf_cnpj, phone_number, lat/lng, premise_id FK optional) |
| **DTO** | `TempPremiseSubmissionDTO` |
| **Controller** | `TemporaryPremiseController`, `SubmissionController.POST /submission/temporary-premise` |
| **UFO Stereotype** | `<<Role>>` — establishment not formally registered |
| **CQs** | CQ-CAM-04 |

---

### F04 — Visit Completion

| Field | Value |
|-------|-------|
| **Definition** | Finalization status of a property inspection within an operational area |
| **Entity** | `AreaPremise.isCompleted` (Boolean) |
| **Endpoints** | `EventActionsController.POST /visit/{id}/complete`, `POST /visit/{id}/reopen` |
| **UFO Stereotype** | `<<Phase>>` — binary phase (complete/incomplete) |
| **CQs** | CQ-CAM-01, CQ-CAM-02 |

---
