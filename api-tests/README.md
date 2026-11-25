# API Unit Tests (examples)

Examples of the automated unit tests that bind SIGEVS-O to the
implementation (SIGEVS API, Java 21 / Spring Boot 3): one test per
competency question (36) plus the tests of the collection time-window axiom
AX-SEQ-06 (6), 42 in total.

| File | Scope | Tests |
|------|-------|-------|
| `CoreCompetencyQuestionsTest.java` | Core | 7 (CQ-CORE-01..07) |
| `InvestigationCompetencyQuestionsTest.java` | Sanitary Investigation | 9 (CQ-INV-01..09) |
| `ResponseCompetencyQuestionsTest.java` | Sanitary Response | 14 (CQ-RES-01..14) |
| `FieldActionsCompetencyQuestionsTest.java` | Field Actions | 6 (CQ-CAM-01..06) |
| `CollectionTimeWindowAxiomTest.java` | Axiom AX-SEQ-06 | 6 |

## What the tests bind

- **Model paths**: each competency-question test exercises, with mocked
  collaborators and no database, the implementation path that answers the
  question (e.g. `ResponseCommandPostService` for CQ-RES-13,
  `EventActionsService` visit completion/reopen for CQ-CAM-02, haversine radius
  query for CQ-INV-01).
- **Formal axioms**:
  - AX-SEQ-01 (unique cycle per response) and AX-CARD-01 (single summons per
    person per response) are checked through the service-level rejection of
    duplicates; their `UNIQUE(cycle_number, response_id)` and
    `UNIQUE(user_id, response_id)` constraints exist in the database schema but
    are not exercised by tests that run without a database.
  - AX-SEQ-03/AX-SEQ-04 (visit completion and reopen) are bound to the
    `visitaConcluida` attribute.
  - AX-SEQ-06 (collection time window) is bound to
    `SubmissionService.validateZoneStatus`: a collection before the start or
    after the end of the zone-per-cycle window is rejected; a collection inside
    the window passes (the end date is inclusive in America/Sao_Paulo time); a
    zone without dates is open unless it is closed.
- **Enumerated types**: ZoneType, ResponseBarrierType/Role, MovementPurpose
  and SpeciesCategory are pinned by dedicated assertions, preventing silent
  drift between the ontology and the code.

The suite runs without external infrastructure (42/42 passing) and is part of
the API build routine:

```bash
./mvnw test -Dtest='*CompetencyQuestionsTest,CollectionTimeWindowAxiomTest'
```

It complements the Python validation scripts in `scripts/` (SPARQL answers
over a populated scenario, TBox structure checks, model/OWL sync, HermiT
reasoning, and the AX-SEQ-06 and event-state checks of
`validate_time_window.py`).
