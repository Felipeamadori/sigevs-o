# Capture Phase — CAP-AXIM (Axiom Identification)

---

## SIGEVS-O Ontology Axioms

Axioms represent domain **restrictions** and **inference rules**, independent of implementation. There are **25 formal axioms** in six categories. The following are not axioms: declarations of the absence of a restriction (recorded as modelling decisions, MD-01/MD-02), attribute cardinalities of persisted state (implementation level), and technical mechanisms — these appear only in the traceability table.

---

## 1. Identity Axioms (4)

| ID | Axiom | Description | Source / Formalisation |
|----|--------|-----------|-------|
| AX-ID-01 | Every **registered** Establishment (phase EstabelecimentoCadastrado) has a unique SDA code | Unregistered units (phase EstabelecimentoNaoCadastrado) have no SDA code and are identified by field records | `owl:hasKey(codigoEstabelecimento)`; `UNIQUE(codigo_estabelecimento)` in `cadastros.estabelecimento` |
| AX-ID-02 | A Person is identified by their CPF (and by system access credentials) | Concept identity vs. system credential | `owl:hasKey(cpf)`; `UNIQUE(cpf)` in `cadastros.usuario` |
| AX-ID-03 | An animal movement is identified by the GTA document (series, number, origin state) | Each GTA is unique per series-number-origin state | `owl:hasKey(serie, numeroGTA, ufOrigem)`; `PK` in `movimentacao.*` tables |
| AX-ID-04 | The existence of a Slaughterhouse presupposes the existence of an establishment classified under one of the inspection types (SIF, SIE or SIM) | Specialisation derived from the classification | `rdfs:subClassOf`; specialisation column |

---

## 2. Dependency Axioms (9)

| ID | Axiom | Description | Source / Formalisation |
|----|--------|-----------|-------|
| AX-DEP-01 | A Surveillance Cycle belongs exclusively to one Sanitary Response | No cycle without a response | `owl:cardinality 1` (cicloPertenceAResposta); `FOREIGN KEY (response_id)` |
| AX-DEP-02 | A Field Team belongs exclusively to one Surveillance Cycle | No team without a cycle | `owl:cardinality 1` (equipeAlocadaEm); `FOREIGN KEY (surveillance_cycle_id)` |
| AX-DEP-03 | An Operational Area belongs to a Team and to a Zone per Cycle | Double dependency on team and zone | `owl:cardinality 1` (areaDaEquipe, PertenceA); FKs in `response_areas` |
| AX-DEP-04 | A Property in Area belongs to an Operational Area | No property-in-area without an area | `owl:cardinality 1` (contidaEmArea); `FOREIGN KEY (area_id)` |
| AX-DEP-05 | A Property Submission links to a Property in Area and to a Team | Every submission has area + team | `owl:cardinality 1` (VinculadaA, RealizadaPor); FKs in `premise_submissions` |
| AX-DEP-06 | A Barrier Submission links to a Sanitary Barrier | Every barrier submission has a barrier | `owl:cardinality 1`; `FOREIGN KEY (barrier_id)` |
| AX-DEP-07 | An Investigation Target depends on a Sanitary Analysis | No target without an analysis | `owl:cardinality 1` (alvoDeAnalise); `FOREIGN KEY (analysis_id)` |
| AX-DEP-08 | A Sanitary Response depends on a Sanitary Analysis | A response only exists linked to an investigation | `owl:cardinality 1` (BaseadaEm); `FOREIGN KEY (analysis_id)` |
| AX-DEP-09 | A Command Post is linked to at most one Sanitary Response (and vice versa) | 1:1 relation between Response and Command Post | `owl:maxCardinality 1` (Tem, postoDaResposta); `OneToOne response_command_post → response_id FK UNIQUE` |

---

## 3. Sequence and Temporality Axioms (6)

| ID | Axiom | Description | Source / Formalisation |
|----|--------|-----------|-------|
| AX-SEQ-01 | The surveillance cycles of a response form a total ordered sequence, without gaps or repetitions | Cycle number unique per response | `owl:hasKey(numeroCiclo, cicloPertenceAResposta)`; `UNIQUE(cycle_number, response_id)` |
| AX-SEQ-02 | A cycle can only be closed when all its operational areas are concluded | `Closed Cycle` is a defined class by equivalence (closed cycle) with the closure restriction as subsumption (all areas concluded); also validated in the service | `owl:equivalentClass` + `owl:allValuesFrom AreaConcluida`; `EventActionsService` |
| AX-SEQ-03 | An operational area is concluded when all its properties have been visited | Defined class `Completed Area` | `owl:equivalentClass` (allValuesFrom + minCardinality 1) |
| AX-SEQ-04 | A concluded property in area can be reopened | Permitted state transition | `EventActionsService.POST /visit/{id}/reopen` (natural/service only) |
| AX-SEQ-05 | Every GPS tracking has a start instant; the end is optional while the event is ongoing | Continuous event in time | `owl:cardinality 1` (inicioRastreamento) + `owl:maxCardinality 1` (fimRastreamento) |
| AX-SEQ-06 | A property submission is only accepted inside the time window of the zone per cycle that contains the property's operational area | Window [start date, end date] of the zone; a zone without end date is open | Service (`SubmissionService.validateZoneStatus`); `dataHoraColeta`, `dataInicioZona`, `dataFimZona`; checked by `validate_time_window.py` (date comparison is outside OWL 2 DL) |

---

## 4. Cardinality and Uniqueness Axioms (3)

| ID | Axiom | Description | Source / Formalisation |
|----|--------|-----------|-------|
| AX-CARD-01 | A professional can only be summoned once for the same response | A professional cannot be duplicated in a summons | `owl:hasKey(keycloakSubjectId, Convoca)`; `UNIQUE(user_id, response_id)` |
| AX-CARD-02 | A team has at least one member and may have several | 1:N cardinality between Field Team and Team Member | `owl:minCardinality 1` (CompostaPor); `@OneToMany team → team_members` |
| AX-CARD-03 | A sanitary analysis may have multiple targets and an establishment may be the target of multiple simultaneous analyses | 1:N cardinality between Sanitary Analysis and Investigation Target | `owl:minCardinality 1` (analiseSanitariaHasAlvoInvestigacao); absence of UNIQUE(analysis_id, premise_id) |

---

## 5. State Axioms (2)

| ID | Axiom | Description | Source / Formalisation |
|----|--------|-----------|-------|
| AX-STATE-01 | A Summoned Person may be in quarantine, a temporal situation with a predicted validity that ceases at a determined date | Defined class `Quarantined Person` (emQuarentena = true) + validity | `owl:equivalentClass` + `owl:cardinality 1` (quarentenaAte); `ResponseConvokedUsers.isDirty/.dirtyUntil` |
| AX-STATE-02 | A Summoned Person may independently hold management and/or observer permissions | Independent permissions | `owl:cardinality 1` (permissaoGestao, permissaoObservacao); `isManagement`, `isObserver` |

**Note:** the implementation's persisted states (active-analysis, active/completed-response, open/closed-zone, visit-completed flags) are attribute cardinalities at the implementation level, not axioms of the conceptual model.

---

## 6. Geographic Axioms (1)

| ID | Axiom | Description | Source / Formalisation |
|----|--------|-----------|-------|
| AX-GEO-01 | An Investigation Target is mediated by up to three concentric Control Zones (Perifoco, Vigilância, Proteção), ordered by increasing radius around the target | In the system: `INFECTED` (Perifoco), `BUFFER` (Vigilância), `SURVEILLANCE` (Proteção); `INVESTIGATION` is an API-level mechanism, outside the model | `owl:maxCardinality 3` (alvoInvestigacaoHasZonaControleInvestigacao) |

**Note:** geospatial support (`GEOGRAPHY`/PostGIS columns, `ST_DWithin` queries) is an implementation mechanism, not an axiom — see the traceability table.

---

## Map: Axioms × Subdomains

| Subdomain | Axioms |
|------------|---------|
| Core | AX-ID-01, AX-ID-02, AX-ID-04 |
| Sanitary Investigation | AX-ID-03, AX-DEP-07, AX-DEP-08, AX-CARD-03, AX-GEO-01 |
| Sanitary Response | AX-DEP-01, AX-DEP-02, AX-DEP-03, AX-DEP-09, AX-SEQ-01, AX-SEQ-02, AX-SEQ-05, AX-CARD-01, AX-CARD-02, AX-STATE-01, AX-STATE-02 |
| Field Actions | AX-DEP-04, AX-DEP-05, AX-DEP-06, AX-SEQ-03, AX-SEQ-04, AX-SEQ-06 |

---

## References

- Source code: JPA entities, Flyway migrations, services
- Document `Funcionalidades SIGEVS.md`
- Concept Catalog (CAP-CATA): `01-cap-cata.md`
