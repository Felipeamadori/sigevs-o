# Axioms — State (Lifecycle)

| ID | Axiom | Description | DL Notation | Implementation |
|----|-------|-------------|-------------|----------------|
| AX-STATE-01 | A Sanitary Analysis can be active or inactive | `isActive` boolean | `SanitaryAnalysis(x) → isActive(x) ∨ ¬isActive(x)` | `SanitaryAnalysis.isActive` |
| AX-STATE-02 | A Sanitary Response can be active, completed, or removed (soft delete) | `isActive` + `completed` booleans | `SanitaryResponse(x) → (isActive(x) ∨ completed(x) ∨ removed(x))` | `SanitaryEventResponse.isActive`, `.completed` |
| AX-STATE-03 | A Zone Per Cycle can be open or closed | `closed` boolean NOT NULL | `ZonePerCycle(x) → isOpen(x) ∨ isClosed(x)` | `SurveillanceCycleZone.closed` |
| AX-STATE-04 | A Property in Area can be completed or pending | `completed` boolean | `PropertyInArea(x) → isCompleted(x) ∨ isPending(x)` | `AreaPremise.isCompleted` |
| AX-STATE-05 | A Summoned Person can have active quarantine (`dirty`) status or not, with expiry date | `isDirty` + `dirtyUntil` | `SummonedPerson(x) → (isDirty(x) ∧ hasDirtyUntil(x,t)) ∨ ¬isDirty(x)` | `ResponseConvokedUsers.isDirty`, `.dirtyUntil` |
| AX-STATE-06 | A Summoned Person can have management and/or observer permissions | Independent permissions | `SummonedPerson(x) → (hasManagement(x) ∨ hasObserver(x))` | `ResponseConvokedUsers.isManagement`, `.isObserver` |
