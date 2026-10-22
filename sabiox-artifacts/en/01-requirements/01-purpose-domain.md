# Requirements Phase — REQ-PURP (Purpose) and REQ-DOMN (Domain)

---

## Ontology Specification Document — v.01

| Field | Value |
|-------|-------|
| Ontology | SIGEVS-O — Ontology for Veterinary Sanitary Event Management |
| Date | 06/23/2026 |
| Version | v.01 |
| Responsible | Ontology Engineer |
| Participant | Ontology Owner (PO SIGEVS) |

---

## 1. Ontology Purpose (REQ-PURP)

### 1.1. What (what the ontology represents)

The ontology represents the domain concepts of **animal health defense** within the scope of the **Official Veterinary Services (SVO)**, covering:

- Epidemiological investigation of disease suspicions
- Operational management of sanitary outbreak containment
- Coordination of surveillance cycles, field teams, sanitary barriers, and operational areas
- Data collection and monitoring in the field

### 1.2. For What (what the ontology will be useful for)

To ensure that the implicit domain knowledge embedded in the SIGEVS platform is explicitly documented, understood, integrated, and amenable to formal reasoning, serving as:

- Official conceptual documentation of the animal health defense domain
- Foundation for Domain-Driven Design in SIGEVS evolution
- Reference for integration with other systems (SVO, MAPA)
- Onboarding material for new developers
- Foundation for domain Knowledge Graphs
- Implementation-independent source of truth

### 1.3. Why (why the ontology should be built)

The Geoanalysis Module, from which SIGEVS was derived, evolved without formal conceptual modeling, resulting in domain semantics issues that motivated the ontology's construction. SIGEVS, in turn, was decoupled with this conceptual modeling as its foundation, so these issues served as justification for the development of SIGEVS-O:

- Ambiguous domain concepts (e.g., what distinguishes "outbreak" from "suspicion"?)
- Business rules hidden in code
- APIs that reflect technical decisions rather than business concepts
- Database that mixes persistence with domain semantics
- Difficulty integrating with other systems
- Steep learning curve for new developers
- Lack of an implementation-independent conceptual source of truth

---

## 2. Ontology Domain (REQ-DOMN)

### 2.1. Domain Definition

Animal health defense within the scope of the Official Veterinary Services (SVO), covering the complete cycle of sanitary event management:

1. **Registration and Geolocation** — cadastral base of rural establishments, addresses, exploited species, and SVO users
2. **Epidemiological Investigation** — recording and tracking of disease suspicions, control zone definition, animal movement tracing, and identification of contacting properties
3. **Outbreak Response** — coordination of sanitary containment through surveillance cycles, team allocation, barrier deployment, operational areas, and command posts
4. **Field Actions** — data collection at properties and barriers, form submission, visit completion control, and auditing

### 2.2. Horizontal Dimension (external boundaries)

**In scope:**
- Registration and georeferencing of rural establishments
- Management of animal species and productive segments
- Investigation of target disease suspicions
- Definition and management of control zones (Perifoco, Vigilância, Proteção)
- Animal movement tracing (GTAs) and contacting properties
- Coordination of surveillance cycles
- Allocation and management of field teams
- Deployment and operation of sanitary barriers
- Field data collection (submissions)
- User, profile, and permission management

**Out of scope:**
- Laboratory processing of biological samples
- Vaccine production and distribution logistics
- Human health (except where it intersects animal health defense via notification)
- Non-domestic wildlife management
- Financial, budgetary, or compensation aspects
- International trade and certification of animal-origin products
- Animal welfare (except when directly related to sanitary control)
- Predictive epidemiological simulation (SEIR-VD) and disease propagation modeling

### 2.3. Vertical Dimension (level of detail)

**In scope:**
- Conceptual level of the sanitary defense business domain
- Structural entities (establishments, animals, equipment)
- Business events (notification, confirmation, cycle closure)
- Roles assumed by entities (investigated property, infected property)
- Domain relationships and rules
- Concept lifecycles (suspect → investigated → confirmed → cleared → closed)

**Out of scope:**
- Implementation details (REST APIs, database tables, DTOs, Java classes)
- Individual animal tracking (operates at the property/herd level)
- User interface and user experience (UX/UI)
- IT infrastructure details
- Routing and logistics optimization algorithms

---

## 3. Initial Glossary

| Term | Definition |
|------|-----------|
| Establishment | Rural productive unit registered in the veterinary service, with SDA code, geographic coordinates, and exploited species |
| Property | Synonym for Establishment in the operational context |
| Sanitary Outbreak | Property where the occurrence of a target disease has been confirmed |
| Control Zone | Geographic perimeter defined around an outbreak |
| Perifoco | Innermost zone around the outbreak (infected) |
| Vigilância | Intermediate buffer zone |
| Proteção | Outermost extended surveillance zone |
| Surveillance Cycle | Numbered sweep round in a control zone |
| GTA | Animal Transit Guide — document for animal movement |
| Field Team | Group of professionals allocated to surveillance operations |
| Sanitary Barrier | Animal transit inspection post |
| Operational Area | Geographic sector assigned to a team within a zone |
| Sanitary Analysis | Investigation record for a disease suspicion |
| Sanitary Response | Central record of outbreak containment coordination |
| Submission | Form completed during a property visit or barrier inspection |

---

## 4. References

- Document: "Iniciativa - Modelagem Ontológica SIGEVS.md"
- Document: "Funcionalidades SIGEVS.md"
- SABiOx Guide (v.2024-09): Sections 3.1 (REQ-PURP) and 3.2 (REQ-DOMN)
