# Setup Phase — DOC-REFE (Reference Ontology Premises Document)

---

## Reference Ontology Document

| Field | Value |
|-------|-------|
| Document: | Reference Ontology Document |
| Ontology: | SIGEVS-O — Ontology for Sanitary Event Management in Animal Health Defense |
| Version: | v.01 |
| Date: | 06/23/2026 |

---

## 1. Modeling Language (SET-LANG)

**OntoUML** — Language for Ontology-Driven Conceptual Modeling.

OntoUML is a conceptual modeling language based on the Unified Foundational Ontology (UFO) that provides a set of ontologically well-founded primitives (stereotypes) for representing domain concepts with formal semantics. It is the recommended language for building reference ontologies within the SABiOx method.

**Key features adopted:**
- Multi-level modeling with <<Kind>>, <<Subkind>>, <<Role>>, <<Phase>> for types
- <<Event>> for domain events
- <<Relator>> for relationships with identity
- <<Collective>> for groups
- <<Quality>> for intrinsic properties
- Formal constraints via OCL or FOL

---

## 2. Foundational Ontology (SET-FOUN)

**UFO (Unified Foundational Ontology)** — as defined by [GBBF+22].

UFO is a foundational ontology characterized in modal logic and cognitive psychology that aims to provide a higher semantic level about the world in a conceptual model of a given knowledge domain. It systematizes notions of:

- Types and their instances
- Objects and their intrinsic properties
- The relationship between identity and classification
- Distinctions between types and their relationships
- Part-whole relationships
- Events and participation

**Adopted UFO stereotypes for SIGEVS-O:**

| UFO Category | Stereotype | Application in SIGEVS |
|--------------|------------|----------------------|
| **Kind** | `<<Kind>>` | Establishment, Animal, SanitaryBarrier, Vehicle — entities with global identity |
| **Subkind** | `<<Subkind>>` | Slaughterhouse (subkind of Establishment) |
| **Role** | `<<Role>>` | InvestigatedProperty, TeamMember, ConvokedUser — contingent roles |
| **Phase** | `<<Phase>>` | CompletionStatus (Complete/Incomplete), InvestigationStatus |
| **Event** | `<<Event>>` | SanitaryOutbreak, SurveillanceCycle, SanitaryAnalysis, Submission |
| **Relator** | `<<Relator>>` | ControlZone — connects outbreak to geographic perimeter |
| **Collective** | `<<Collective>>` | FieldTeam — group of professionals acting jointly |
| **Quality** | `<<Quality>>` | GeographicCoordinates, Name, Date |
| **Mode** | `<<Mode>>` | Status, Permission — intrinsic properties |

---

## 3. Concept Criteria (SET-CRIT)

The following criteria determine whether a concept is adherent to the SIGEVS-O domain:

| ID | Criterion | Type | Description |
|----|-----------|------|-------------|
| **CR-01** | Domain Relevance | Subjective | The concept belongs to the animal health defense domain within the scope of the Official Veterinary Service (SVO) |
| **CR-02** | SIGEVS Presence | Objective | The concept is represented in at least one SIGEVS functionality (API, database, code, features as per `Funcionalidades SIGEVS.md`) |
| **CR-03** | Subdomain Coverage | Objective | The concept fits within at least one of the 4 ontology subdomains: Core, Sanitary Investigation, Sanitary Response, or Field Actions |
| **CR-04** | UFO Classifiable | Subjective | The concept can be mapped to a UFO stereotype (Kind, Role, Event, Relator, Collective, Phase, Quality, Mode) |
| **CR-05** | Domain Recognition | Objective | The concept is defined in a recognized source (veterinary literature, FAO GEMP, SVO/MAPA legislation) |

**Application notes:**
- CR-01 and CR-04 are applied during individual concept analysis from knowledge sources
- CR-02, CR-03, and CR-05 are applied during joint consensus analysis across all sources
- Criteria may be revised as knowledge is enriched and decisions evolve (SABiOx iterative principle)

---

## 4. Ontologies to Reuse (SET-REUS)

Reuse of existing ontologies was not adopted in the current modeling.
The focus of this phase is the conceptual modeling of the animal health defense domain of the platform, prioritizing domain fidelity and adherence to Brazilian legislation and PESA operational manuals. The evaluation of existing ontology reuse was postponed for future work, when the ontology is integrated with other systems and potential knowledge graphs.

**Decision:** Reuse analysis will be conducted during the Capture Phase, specifically in activities CAP-CATA (Catalog Concepts) and CAP-VIEW (Extract Ontology View).

---

## 5. Subdomain Overview

```
     ┌─────────────┐
     │    Core      │ (root)
     └──────┬───────┘
            │
     ┌──────▼───────┐
     │ Investigation │
     └──────┬───────┘
            │
     ┌──────▼───────┐     ┌──────────────────┐
     │   Response   │────▶│  Field Actions   │
     └──────────────┘     └──────────────────┘
```

| Subdomain | Concepts | Dependencies |
|-----------|----------|--------------|
| Core | Establishment, Animal, User, Address, Species | None (root) |
| Investigation | Sanitary Analysis, Target, Control Zone, GTA, Contact Properties | Core |
| Response | Sanitary Response, Cycle, Team, Barrier, Operational Area, Vehicle, Command Post | Core, Investigation |
| Field | Property Submission, Barrier Submission, Temporary Property, Audit Log | Core, Response |

---

## 6. Version Control

| Version | Date | Description |
|---------|------|-------------|
| v.01 | 06/23/2026 | Initial premises of the SIGEVS-O reference ontology |

---

## References

- SABiOx Guide 2024-09: Sections 4.1 (SET-LANG), 4.2 (SET-FOUN), 4.3 (SET-CRIT), 4.4 (SET-REUS), 4.5 (DOC-REFE)
- Ontology Specification Document (SIGEVS-O): `../1-requirements/04-doc-spec.md`
- [GBBF+22] UFO — Unified Foundational Ontology
- [GFB+18] OntoUML Language Specification
