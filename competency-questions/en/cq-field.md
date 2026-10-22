# Competency Questions — Field Actions Subdomain

| ID | Competency Question | Path in the Model | Implementation |
|----|--------------------|--------------------|----------------|
| CQ-CAM-01 | Which properties were visited (submitted) in a cycle? | `PropertyInArea` → `PropertySubmission` | JPA/SPARQL FILTER |
| CQ-CAM-02 | What is the completion status of a property in an operational area? | `PropertyInArea.isCompleted` | JPA query |
| CQ-CAM-03 | Which submissions were made by a team in a given period? | `PropertySubmission` → `FieldTeam` + date range | JPA query |
| CQ-CAM-04 | Which temporary properties were registered during the operation? | Instances of `TemporaryProperty` | JPA/SPARQL |
| CQ-CAM-05 | What is the audit history of a submission or operation? | `PropertySubmission` → audit log | JPA query |
| CQ-CAM-06 | Which files were attached to a submission? | `PropertySubmission` → `file` (bytea) | JPA query |
