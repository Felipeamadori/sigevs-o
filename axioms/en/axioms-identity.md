# Axioms — Identity

| ID | Axiom | Description | DL Notation | Implementation |
|----|-------|-------------|-------------|----------------|
| AX-ID-01 | `establishmentCode` is globally unique | Every registered Establishment (phase RegisteredEstablishment) has a unique SDA code; unregistered units (phase UnregisteredEstablishment) have no SDA code and are identified by field records | `Establishment(x) → ∃!c: hasCode(x,c)` | `UNIQUE(establishment_code)` in `cadastros.establishment` |
| AX-ID-04 | Every Establishment with `type = "Slaughterhouse"` has a Slaughterhouse record | The existence of Slaughterhouse depends on the existence of an Establishment with that classification | `Slaughterhouse(x) → Establishment(x)` | `Slaughterhouse.id_establishment FK` |
| AX-ID-02 | A Person is identified by `keycloak_subject_id` and alternatively by `cpf` and `email` | Unique identities across three dimensions (Keycloak, CPF, email) | `Person(x) → ∃!k: hasKeycloakId(x,k) ∧ ∃!c: hasCPF(x,c) ∧ ∃!e: hasEmail(x,e)` | `UNIQUE(keycloak_subject_id, cpf, email)` in `cadastros.usuario` |
| AX-ID-03 | An animal movement is identified by the triple `(series, number, origin_state)` | Each GTA is unique by series-number-state of origin | `AnimalMovement(x) → ∃!s,n,u: hasTriple(x,s,n,u)` | `PK(series, number, uf_origin)` in `movimentacao.*` |
