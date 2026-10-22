# Fase de Setup — DOC-REFE (Documento de Premissas da Ontologia de Referência)

---

## Reference Ontology Document

| Campo | Valor |
|-------|-------|
| Documento: | Reference Ontology Document |
| Ontologia: | SIGEVS-O — Ontology for Sanitary Event Management in Animal Health Defense |
| Versão: | v.01 |
| Data: | 23/06/2026 |

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
| **Kind** | `<<Kind>>` | Estabelecimento, Animal, BarreiraSanitaria, Veiculo — entities with global identity |
| **Subkind** | `<<Subkind>>` | Frigorifico (subkind of Estabelecimento) |
| **Role** | `<<Role>>` | PropriedadeInvestigada, MembroEquipe, UsuarioConvocado — contingent roles |
| **Phase** | `<<Phase>>` | StatusConclusao (Completa/Incompleta), StatusInvestigacao |
| **Event** | `<<Event>>` | FocoSanitario, CicloVigilancia, AnaliseSanitaria, Submissao |
| **Relator** | `<<Relator>>` | ZonaControle — connects outbreak to geographic perimeter |
| **Collective** | `<<Collective>>` | EquipeCampo — group of professionals acting jointly |
| **Quality** | `<<Quality>>` | CoordenadasGeograficas, Nome, Data |
| **Mode** | `<<Mode>>` | Status, Permissao — intrinsic properties |

---

## 3. Concept Criteria (SET-CRIT)

The following criteria determine whether a concept is adherent to the SIGEVS-O domain:

| ID | Criterion | Type | Description |
|----|-----------|------|-------------|
| **CR-01** | Domain Relevance | Subjective | The concept belongs to the animal health defense domain within the scope of the Official Veterinary Service (SVO) |
| **CR-02** | SIGEVS Presence | Objective | The concept is represented in at least one SIGEVS functionality (API, database, code, features as per `Funcionalidades SIGEVS.md`) |
| **CR-03** | Subdomain Coverage | Objective | The concept fits within at least one of the 4 ontology subdomains: Core, Investigação Sanitária, Resposta Sanitária, or Ações em Campo |
| **CR-04** | UFO Classifiable | Subjective | The concept can be mapped to a UFO stereotype (Kind, Role, Event, Relator, Collective, Phase, Quality, Mode) |
| **CR-05** | Domain Recognition | Objective | The concept is defined in a recognized source (veterinary literature, FAO GEMP, SVO/MAPA legislation) |

**Application notes:**
- CR-01 and CR-04 are applied during individual concept analysis from knowledge sources
- CR-02, CR-03, and CR-05 are applied during joint consensus analysis across all sources
- Criteria may be revised as knowledge is enriched and decisions evolve (SABiOx iterative principle)

---

## 4. Ontologies to Reuse (SET-REUS)

O reuso de ontologias existentes não foi adotado na modelagem corrente.
O foco desta fase é a modelagem conceitual do domínio de defesa
sanitária animal da plataforma, priorizando a fidelidade ao domínio e a
aderência à legislação brasileira e aos manuais operacionais do PESA. A
avaliação de reuso de ontologias existentes foi adiada para trabalhos
futuros, quando a ontologia for integrada a outros sistemas e a
potenciais grafos de conhecimento.

**Decision:** Reuse analysis will be conducted during the Capture Phase, specifically in activities CAP-CATA (Catalog Concepts) and CAP-VIEW (Extract Ontology View).

---

## 5. Subdomain Overview

```
     ┌─────────────┐
     │    Core      │ (raiz)
     └──────┬───────┘
            │
     ┌──────▼───────┐
     │ Investigação │
     └──────┬───────┘
            │
     ┌──────▼───────┐     ┌──────────────────┐
     │   Resposta   │────▶│   Ações em Campo │
     └──────────────┘     └──────────────────┘
```

| Subdomain | Concepts | Dependencies |
|-----------|----------|--------------|
| Core | Establishment, Animal, User, Address, Species | None (root) |
| Investigação | Sanitary Analysis, Target, Control Zone, GTA, Contact Properties | Core |
| Resposta | Sanitary Response, Cycle, Team, Barrier, Operational Area, Vehicle, Command Post | Core, Investigação |
| Campo | Property Submission, Barrier Submission, Temporary Property, Audit Log | Core, Resposta |

---

## 6. Version Control

| Version | Date | Description |
|---------|------|-------------|
| v.01 | 23/06/2026 | Premissas iniciais da ontologia de referência SIGEVS-O |

---

## References

- SABiOx Guide 2024-09: Sections 4.1 (SET-LANG), 4.2 (SET-FOUN), 4.3 (SET-CRIT), 4.4 (SET-REUS), 4.5 (DOC-REFE)
- Ontology Specification Document (SIGEVS-O): `../1-requirements/04-doc-spec.md`
- [GBBF+22] UFO — Unified Foundational Ontology
- [GFB+18] OntoUML Language Specification
