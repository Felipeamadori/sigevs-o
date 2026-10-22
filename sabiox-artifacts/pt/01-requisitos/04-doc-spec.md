# Fase de Requisitos — DOC-SPEC (Documento de Especificação da Ontologia)

---

## Ontology Specification Document

| Campo | Valor |
|-------|-------|
| Documento: | Ontology Specification Document |
| Ontologia: | SIGEVS-O — Ontology for Sanitary Event Management in Animal Health Defense |
| Versão: | v.01 |
| Data: | 23/06/2026 |

---

## 1. Purpose of the Ontology

The purpose of the ontology is to represent the concepts of **animal health defense and sanitary event management**, covering epidemiological investigation, outbreak containment, and field operations, so that these concepts can be interpreted and identified in a unique way across the SIGEVS platform and related systems. This is motivated by the fact that the SIGEVS system has evolved over many years without formal conceptual modeling, resulting in ambiguous domain concepts, business rules hidden in implementation code, and difficulties for system integration, evolution, and new developer onboarding.

---

## 2. Ontology Domain

Animal health defense within the scope of the Official Veterinary Services (SVO), covering the complete lifecycle of sanitary event management: from property registration and geolocation, through epidemiological investigation of suspected diseases, operational coordination of outbreak response (surveillance cycles, teams, barriers, areas), to field data collection.

---

## 3. Ontology Dimension

### Horizontal Dimension

The domain covers the lifecycle of sanitary event management: property registration, epidemiological investigation, operational outbreak response, and field actions.

**Does NOT cover:** predictive epidemiological simulation (SEIR-VD), laboratory sample processing, vaccine production logistics, human healthcare, wildlife management, financial/compensation aspects, international trade certification, or animal welfare (except where directly related to sanitary control).

### Vertical Dimension

The ontology represents concepts at the **business domain level** of animal health defense — structural entities, events, roles, and relationships of veterinary operations.

**Does NOT cover:** implementation details (APIs, database tables, DTOs, Java classes), individual animal tracking (operates at property/herd level), user interface details, or IT infrastructure.

---

## 4. Subdomains

| # | Subdomain | Definition | Dependencies |
|---|-----------|------------|--------------|
| 1 | **Core** | Fundamental entities: Establishment, Animal, User, Address, Species | None (root) |
| 2 | **Investigação Sanitária** | Epidemiological investigation of disease suspicions, target definition, control zones, animal movement tracking | Core |
| 3 | **Resposta Sanitária** | Operational coordination of outbreak containment: surveillance cycles, teams, barriers, operational areas | Core, Investigação |
| 4 | **Ações em Campo** | Field data collection: property/barrier submissions, visit completion, temporary properties, audit log | Core, Resposta |

---

## 5. Functional Requirements (Competency Questions)

### Subdomain: Core

| ID | Competency Question |
|----|---------------------|
| CQ-CORE-01 | Which rural establishments are registered in the SVO? |
| CQ-CORE-02 | Which animal species are raised in an establishment? |
| CQ-CORE-03 | What is the geographic location (coordinates) of an establishment? |
| CQ-CORE-04 | Which users are linked to a given region/inspectorate? |
| CQ-CORE-05 | Which establishments have CAR (Rural Environmental Registry)? |
| CQ-CORE-06 | Which establishments are slaughterhouses and what is their inspection type? |
| CQ-CORE-07 | What profiles and permissions does a user have in the system? |

### Subdomain: Investigação Sanitária

| ID | Competency Question |
|----|---------------------|
| CQ-INV-01 | Which properties are within the surveillance radius of an active outbreak? |
| CQ-INV-02 | Can a property be the target of more than one investigation simultaneously? |
| CQ-INV-03 | What is the animal movement history (GTAs) of a property during the investigation period? |
| CQ-INV-04 | Which are the direct contact properties of an investigated property? |
| CQ-INV-05 | Which are the indirect contact properties of an investigated property? |
| CQ-INV-06 | Which control zones were defined for an investigation? |
| CQ-INV-07 | What is the current status of a sanitary investigation? |
| CQ-INV-08 | Which geographic areas (municipalities) are affected by an investigation? |
| CQ-INV-09 | Which species categories are involved in an investigation? |

### Subdomain: Resposta Sanitária

| ID | Competency Question |
|----|---------------------|
| CQ-RES-01 | Which surveillance cycles belong to a sanitary response? |
| CQ-RES-02 | Which teams are allocated to a given surveillance cycle? |
| CQ-RES-03 | Which professionals (members) make up a field team? |
| CQ-RES-04 | Can a sanitary barrier be active in multiple cycles simultaneously? |
| CQ-RES-05 | Can a control zone be redefined between cycles? |
| CQ-RES-06 | Which professionals were in the field on a given date? |
| CQ-RES-07 | Can a team be allocated to more than one cycle simultaneously? |
| CQ-RES-08 | Which operational area is assigned to each team in a cycle? |
| CQ-RES-09 | Which sanitary barriers are active in a response? |
| CQ-RES-10 | Which properties are within an operational area? |
| CQ-RES-11 | What is the type (fixed/mobile) and function (sanitary/detour) of a sanitary barrier? |
| CQ-RES-12 | Which vehicles are linked to a team? |
| CQ-RES-13 | Which command post is associated with a sanitary response? |
| CQ-RES-14 | Which users were mobilized for a response and what is their quarantine status? |

### Subdomain: Ações em Campo

| ID | Competency Question |
|----|---------------------|
| CQ-CAM-01 | Which properties were visited (submitted) in a cycle? |
| CQ-CAM-02 | What is the completion status of a property in an operational area? |
| CQ-CAM-03 | Which submissions were made by a team in a given period? |
| CQ-CAM-04 | Which temporary properties were registered during the operation? |
| CQ-CAM-05 | What is the audit history of a submission or operation? |
| CQ-CAM-06 | Which files were attached to a submission? |

---

## 6. Non-Functional Requirements

| ID | Non-Functional Requirement |
|----|---------------------------|
| RNF-01 | The ontology shall be modular to facilitate reuse by other ontologies |
| RNF-02 | The ontology shall be grounded in a foundational ontology (UFO) |
| RNF-03 | The reference ontology shall be expressed in OntoUML |
| RNF-04 | The ontology shall be encodable in OWL/gUFO as an operational ontology |
| RNF-05 | The ontology shall be defined from recognized knowledge sources (SIGEVS, FAO GEMP, SVO legislation) |
| RNF-06 | The ontology shall represent consensual domain knowledge (validate with domain experts) |
| RNF-07 | The ontology shall support reasoning about control zones and geospatial relationships |
| RNF-08 | The ontology shall be extensible for new disease types and control measures |
| RNF-09 | The ontology vocabulary shall align with Brazilian animal health defense terminology |

---

## 7. Version Control

| Version | Date | Description |
|---------|------|-------------|
| v.01 | 23/06/2026 | Versão inicial da especificação |
| v.02 | 23/06/2026 | Removido subdomínio de Simulação Epidemiológica do escopo |
