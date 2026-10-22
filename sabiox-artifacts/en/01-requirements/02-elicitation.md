# Requirements Phase — REQ-ELIC (Requirements Elicitation)

---

## Functional Requirements — Competency Questions (CQs)

### Subdomain: Core (Registration and Geolocation)

| ID | Competency Question |
|----|---------------------|
| CQ-CORE-01 | Which rural establishments are registered in the SVO? |
| CQ-CORE-02 | Which animal species are exploited at an establishment? |
| CQ-CORE-03 | What is the geographic location (coordinates) of an establishment? |
| CQ-CORE-04 | Which users are linked to a given region/inspection unit? |
| CQ-CORE-05 | Which establishments have a CAR (Rural Environmental Registry)? |
| CQ-CORE-06 | Which establishments are slaughterhouses and what type of sanitary inspection do they have? |
| CQ-CORE-07 | What profiles and permissions does a user have in the system? |

---

### Subdomain: Investigation (Sanitary Analysis)

| ID | Competency Question |
|----|---------------------|
| CQ-INV-01 | Which properties are within the surveillance radius of an active outbreak? |
| CQ-INV-02 | Can a property be the target of more than one investigation at the same time? |
| CQ-INV-03 | What is the animal movement history (GTAs) of a property during the investigation period? |
| CQ-INV-04 | What are the direct contacting properties of an investigated property? |
| CQ-INV-05 | What are the indirect contacting properties of an investigated property? |
| CQ-INV-06 | Which control zones have been defined for an investigation? |
| CQ-INV-07 | What is the current status of a sanitary investigation? |
| CQ-INV-08 | Which geographic areas (municipalities) are affected by an investigation? |
| CQ-INV-09 | Which species categories are involved in an investigation? |

---

### Subdomain: Response (Containment Management)

| ID | Competency Question |
|----|---------------------|
| CQ-RES-01 | Which surveillance cycles belong to a sanitary response? |
| CQ-RES-02 | Which teams are allocated to a given surveillance cycle? |
| CQ-RES-03 | Which professionals (members) compose a field team? |
| CQ-RES-04 | Can a sanitary barrier be active in multiple cycles simultaneously? |
| CQ-RES-05 | Can a control zone be redefined between cycles? |
| CQ-RES-06 | Which professionals were in the field on a given date? |
| CQ-RES-07 | Can a team be allocated to more than one cycle simultaneously? |
| CQ-RES-08 | Which operational area is assigned to each team in a cycle? |
| CQ-RES-09 | Which sanitary barriers are active in a response? |
| CQ-RES-10 | Which properties are within an operational area? |
| CQ-RES-11 | What is the type of a sanitary barrier (fixed/mobile) and its function (sanitary/diversion)? |
| CQ-RES-12 | Which vehicles are linked to a team? |
| CQ-RES-13 | What is the command post associated with a sanitary response? |
| CQ-RES-14 | Which users were convoked for a response and what is their quarantine status? |

---

### Subdomain: Field (Collection and Monitoring)

| ID | Competency Question |
|----|---------------------|
| CQ-CAM-01 | Which properties were visited (submitted) in a cycle? |
| CQ-CAM-02 | What is the completion status of a property in an operational area? |
| CQ-CAM-03 | Which submissions were made by a team during a period? |
| CQ-CAM-04 | Which temporary properties were registered during the operation? |
| CQ-CAM-05 | What is the audit history of a submission or operation? |
| CQ-CAM-06 | Which files were attached to a submission? |

---

## Non-Functional Requirements (NFRs)

| ID | Non-Functional Requirement |
|----|----------------------------|
| RNF-01 | The ontology must be modular to facilitate reuse by other ontologies |
| RNF-02 | The ontology must be grounded in a foundational ontology (UFO) |
| RNF-03 | The ontology must be expressed in OntoUML as the reference ontology |
| RNF-04 | The ontology must be encodable in OWL/gUFO as the operational ontology |
| RNF-05 | The ontology must be defined from recognized knowledge sources (SIGEVS, FAO GEMP, SVO legislation) |
| RNF-06 | The ontology must represent consensual domain knowledge (validation with experts) |
| RNF-07 | The ontology must support reasoning about control zones and geospatial relationships |
| RNF-08 | The ontology must be extensible to new types of diseases and control measures |
| RNF-09 | The ontology vocabulary must be aligned with Brazilian animal health defense domain terminology |
