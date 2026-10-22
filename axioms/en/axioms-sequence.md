# Axioms — Sequence and Temporality

| ID | Axiom | Description | DL Notation | Implementation |
|----|-------|-------------|-------------|----------------|
| AX-SEQ-01 | Surveillance cycles follow sequential ordering within a response | `cycleNumber` is sequential and unique per response | `SurveillanceCycle(x) → ∃!n: hasNumber(x,n)` | `UNIQUE(cycle_number, response_id)` |
| AX-SEQ-02 | A cycle can only be closed when all its operational areas are completed | Business rule validated in Service | `SurveillanceCycle(x, closed=true) → ∀a: OperationalArea(a) ∧ belongsTo(a,x) → isCompleted(a)` | `EventActionsService` / `ResponseSurveillanceCycleService` |
| AX-SEQ-03 | An operational area is completed when all its properties are visited | `completed` in area derives from `isCompleted` in properties | `OperationalArea(x, completed=true) → ∀p: PropertyInArea(p) ∧ containedIn(p,x) → isCompleted(p)` | `EventActionsService.POST /visit/{id}/complete` |
| AX-SEQ-04 | A property in area can be reopened after completion | Allowed state transition | `PropertyInArea(x) → canTransition(x, completed, pending)` | `EventActionsService.POST /visit/{id}/reopen` |
| AX-SEQ-05 | GPS tracking of a team has start (`createdAt`) and optional end (`endTime`) | Tracking is a continuous event in time | `GPSTracking(x) → hasStart(x,t) ∧ (hasEnd(x,t') ∨ ¬hasEnd(x,t'))` | `TeamTracking.createdAt + endTime` |
