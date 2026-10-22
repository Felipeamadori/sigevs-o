# Requirements Phase — REQ-SUBD (Subdomain Identification)

---

## SIGEVS-O Ontology Subdomains

The subdomains were identified from the analysis of the 5 SIGEVS functional areas (document `Funcionalidades SIGEVS.md`) and the grouping of Competency Questions (REQ-ELIC). Each subdomain represents a cohesive module of the ontology, enabling distributed development and selective reuse.

---

### 1. Subdomain: **Core**

**Definition:** Foundational and transversal entities of the animal health defense domain. Serves as an anchor for all other subdomains.

**Key concepts:**
- Establishment (Kind)
- Animal / Species / Productive Segment
- User / Professional
- Address / Municipality / State
- Geographic Coordinates
- CAR (Rural Environmental Registry)
- Slaughterhouse

**Associated CQs:** CQ-CORE-01 to CQ-CORE-07

**Dependencies:** None (root module)

---

### 2. Subdomain: **Sanitary Investigation**

**Definition:** Epidemiological investigation process for disease suspicions, including target definition, control zones, animal movement tracing, and identification of contacting properties.

**Key concepts:**
- Sanitary Analysis (Event)
- Investigation Target (Role)
- Control Zone (Relator) — Perifoco, Vigilância, Proteção, Investigação
- Animal Movement / GTA (Event)
- Direct / Indirect Contacting Property
- Affected Area
- Species Category

**Associated CQs:** CQ-INV-01 to CQ-INV-09

**Dependencies:** Core

---

### 3. Subdomain: **Sanitary Response**

**Definition:** Operational coordination of outbreak containment, including surveillance cycles, team allocation, barrier deployment, operational areas, vehicles, and command posts.

**Key concepts:**
- Sanitary Response (Event)
- Surveillance Cycle (Event)
- Zone per Cycle
- Field Team (Collective)
- Team Member (Role)
- Role (veterinarian, assistant, technician)
- Operational Area
- Property in Area
- Sanitary Barrier (Kind) — fixed/mobile, sanitary/diversion
- Vehicle / Patrol Car
- Command Post
- Convoked User
- GPS Tracking

**Associated CQs:** CQ-RES-01 to CQ-RES-14

**Dependencies:** Core, Sanitary Investigation

---

### 4. Subdomain: **Field Actions**

**Definition:** Operational data collection at properties and barriers, including form submission, visit completion control, temporary property registration, and auditing.

**Key concepts:**
- Property Submission (Event)
- Barrier Submission (Event)
- Temporary Property
- Visit Completion (Phase)
- Audit Log

**Associated CQs:** CQ-CAM-01 to CQ-CAM-06

**Dependencies:** Core, Sanitary Response

---

## Subdomain Dependency Diagram

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
     │   Response   │────▶│   Field Actions  │
     └──────────────┘     └──────────────────┘
```

---

## Modularization Strategy

Adopt a **partitioning** strategy, where each subdomain is treated as an independent module with its own classes and relationships, maintaining minimal dependency interfaces. Integration between modules will occur through association and specialization of Core concepts.

During the **Setup** phase, we will decide on ontologies to reuse (e.g., FAO GEMP, AGROVOC) that may anchor specific domain concepts.
