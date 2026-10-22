# Axioms — Cardinality and Uniqueness

| ID | Axiom | Description | DL Notation | Implementation |
|----|-------|-------------|-------------|----------------|
| AX-CARD-01 | A user can only be summoned once for the same response | A professional cannot be duplicated in the summons | `SummonedPerson(x) → ∃!r: summonedFor(x,r)` | `UNIQUE(user_id, response_id)` in `response_convoked_users` |
| AX-CARD-02 | An establishment can be the target of multiple simultaneous investigations | No uniqueness constraint between analysis and establishment | `Establishment(x) → ∃n≥1: InvestigationTarget(t) ∧ targets(t,x)` | Absence of UNIQUE(analysis_id, premise_id) |
| AX-CARD-03 | A team can have multiple members | 1:N cardinality between FieldTeam and TeamMember | `FieldTeam(x) → ∃n≥1: TeamMember(m) ∧ memberOf(m,x)` | `@OneToMany team → team_members` |
| AX-CARD-04 | An establishment can be in multiple operational areas (in different responses) | No uniqueness constraint on premise_id + response_id in area_premises | `Establishment(x) → ∃n≥1: OperationalArea(a) ∧ contains(a,x)` | Analysis of absence of constraint |
| AX-CARD-05 | A sanitary analysis can have multiple targets | 1:N cardinality between SanitaryAnalysis and InvestigationTarget | `SanitaryAnalysis(x) → ∃n≥1: InvestigationTarget(t) ∧ delimits(x,t)` | `@OneToMany(cascade=ALL, orphanRemoval=true)` |
