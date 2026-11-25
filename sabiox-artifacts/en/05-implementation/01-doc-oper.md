# Implementation Phase — DOC-OPER (Operational Ontology Document)

---

## Operational Ontology Document

| Field | Value |
|-------|-------|
| Document: | Operational Ontology Document |
| Ontology: | SIGEVS-O — Ontology for Sanitary Event Management in Animal Health Defense |
| Version: | v.02 |
| Date: | 15/07/2026 (v.01); v.02 25/11/2026 (registration phases) |

---

## 1. Coded Concepts (IMP-CONC)

The 33 domain concepts of the OntoUML model (32 classes and the `CategoriaEspecie` enumeration) were encoded as OWL classes typed with the gUFO stereotypes:

| Subdomain | Classes | Stereotypes |
|------------|---------|--------------|
| **Core** (9) | Estabelecimento, Endereco, Pessoa, EspecieAnimal, Frigorifico, GranjaAve, GranjaSuino, EstabelecimentoCadastrado, EstabelecimentoNaoCadastrado | 4 Kind, 3 Subkind, 2 Phase |
| **Investigation** (7) | AnaliseSanitaria, AlvoInvestigacao, AreaAfetada, ZonaControleInvestigacao, MovimentacaoAnimal, PropriedadeContactante, CategoriaEspecie | 2 Event, 2 Role, 1 Relator, 1 Kind, 1 Enumeration |
| **Response** (14) | RespostaSanitaria, CicloVigilancia, ZonaPorCiclo, EquipeCampo, MembroEquipe, Funcao, AreaOperacional, PropriedadeEmArea, BarreiraSanitaria, Veiculo, PostoComando, PessoaConvocada, RastreamentoGPS, TipoEquipe | 3 Event, 2 Relator, 1 Collective, 2 Role, 6 Kind |
| **Field Actions** (2) | SubmissaoPropriedade, SubmissaoBarreira | 2 Event |

Each class received `rdf:type gufo:<Stereotype>` (e.g., `Establishment rdf:type gufo:Kind`, `InvestigationTarget rdf:type gufo:Role`, `PropertyInArea rdf:type gufo:Relator`, `PropertySubmission rdf:type gufo:Event`).

Beyond the 33 domain concepts, four defined classes capture derived states: `Closed Cycle`, `Completed Area`, `Visited Property` and `Quarantined Person` — totalling **37 named classes**.

### Mapping to the SIGEVS System (ODSE)

In parallel, the conceptual model was translated into the structures of the decoupled SIGEVS system (Spring Boot backend):

| OntoUML Stereotype | SIGEVS Structure |
|---------------------|---------------------|
| `<<Kind>>` | JPA entity with its own table and independent identity |
| `<<Subkind>>` | JPA entity with inheritance / 1:1 relation to the Kind |
| `<<Role>>`/`<<Phase>>` (specialising the Kind) | JPA entity referencing the Kind (no extra associative table) |
| `<<Relator>>` | Associative table with its own attributes (e.g., `area_premises.completed`) |
| `<<Event>>` | JPA entity with a timestamp |
| `<<Collective>>` | JPA entity with a member collection (`team_members`) |
| `<<Enumeration>>` | Java enum (`ZoneType`, `SpeciesCategory`, etc.) |

---

## 2. Coded Relations (IMP-RELC)

The model's 31 relations were encoded as `owl:ObjectProperty` (and, in the system, as JPA associations / FKs):

| Relation Type | OWL Encoding | SIGEVS Encoding |
|-----------------|-----------------|--------------------|
| Simple association | `owl:ObjectProperty` (e.g., `estabelecimentoHasEndereco`) | `@ManyToOne` / FK |
| Mediation relation (`<<mediation>>`) | `owl:ObjectProperty` with Relator domain | Associative table with attributes |
| Composition (`<<memberOf>>`) | `owl:ObjectProperty` | `@OneToMany` (e.g., `EquipeCampo → MembroEquipe`) |
| Generalisation (`<<Subkind>>`/`<<Role>>`/`<<Phase>>`) | `rdfs:subClassOf` | JPA inheritance or Kind reference |

Examples of encoded object properties: `estabelecimentoHasEndereco`, `analiseSanitariaHasAlvoInvestigacao`, `Aloca`, `CompostaPor`, `Contem`, `VinculadaA`.

---

## 3. Coded Axioms (IMP-AXIO)

The model's 25 formal axioms were encoded in two layers:

### 3.1 OWL Axioms (logical reasoning)

- **Identity axioms** (AX-ID-*): uniqueness restrictions (`owl:hasKey`; e.g., unique SDA code for registered establishments; GTA identified by `(serie, numero, ufOrigem)`).
- **Dependency axioms** (AX-DEP-*): existential restrictions (e.g., every `CicloVigilancia` belongs to a `RespostaSanitaria`).
- **Sequence axioms** (AX-SEQ-*): sequential ordering of cycles; cycle closure conditioned on area completion (AX-SEQ-02, subsumption over the defined class `Closed Cycle`) and area completion (AX-SEQ-03, defined class `Completed Area`).
- **State axioms** (AX-STATE-01/02): quarantine (defined class `Quarantined Person`) and independent permissions.
- **Geographic axiom** (AX-GEO-01): target→zone mediation with 1..4 cardinality.

### 3.2 Database / Service Restrictions (SIGEVS)

| Axiom | SIGEVS Encoding |
|--------|-----------------------|
| AX-SEQ-01 (sequential cycles) | `UNIQUE(cycle_number, response_id)` + check on cycle creation |
| AX-CARD-01 (single summons) | `UNIQUE(user_id, response_id)` in `response_convoked_users` |
| AX-DEP-* (dependencies) | `FOREIGN KEY` (e.g., `response_id` in `response_surveillance_cycle`) |
| AX-STATE-01 (quarantine) | Flag + expiry date (`isDirty`, `dirtyUntil`) |
| Persisted states (implementation level) | `NOT NULL` columns (`closed`, `completed`, `active`) |
| CQ-INV-01 (properties in risk zone) | PostGIS `ST_DWithin` query with geospatial buffers |

**Geolocation:** spatial attributes (coordinates, polygons) were encoded with the PostGIS `geography` type, enabling spatial queries (ST_DWithin) that replace a runtime OWL reasoner, meeting performance requirements.

---

## 4. Operational Ontology Metrics

| Metric | Value |
|---------|-------|
| Domain concepts (32 classes + 1 enumeration) | 33 |
| Defined classes (derived states) | 4 |
| **Total named classes** | **37** |
| Object properties | 36 |
| Datatype properties | 113 |
| Individuals (enums + type declarations) | 34 |
| OWL class restrictions | 42 |
| Keys (`owl:hasKey`) | 7 |
| Property chains | 1 |
| Logical axioms (rdflib script; v.01: 402 — Protégé reported 401) | 421 |
| Declarations (rdflib script; v.01: 214) | 225 |
| Total axioms (rdflib script; v.01: 867) | 910 |

---

## 5. Verification (EVA-OPER)

The operational ontology was verified through two paths:

1. **SPARQL queries** — the competency questions were answered over the populated model; the official queries are in `sparql/cq-*.rq` (run in Protégé and, for the spatial one, in Apache Jena with `jena-geosparql`). Examples:

```sparql
# CQ-CORE-01: Which establishments are registered?
PREFIX sigevs: <https://sigevs.ontologies#>

SELECT ?estabelecimento ?nome WHERE {
  ?estabelecimento a sigevs:EstabelecimentoCadastrado ;
                   sigevs:nomeEstabelecimento ?nome .
}
ORDER BY ?nome
```

```sparql
# CQ-RES-03: Members of each field team
PREFIX sigevs: <https://sigevs.ontologies#>

SELECT ?equipe ?nomeEquipe ?membro ?nomeMembro WHERE {
  ?equipe a sigevs:EquipeCampo ;
          sigevs:nomeEquipe ?nomeEquipe ;
          sigevs:CompostaPor ?membro .
  ?membro a sigevs:MembroEquipe ;
          sigevs:nomePessoa ?nomeMembro .
}
ORDER BY ?nomeEquipe ?nomeMembro
```

2. **HermiT reasoning** (via owlready2, with gUFO loaded) — after populating the ontology with a sample outbreak scenario, the reasoner confirmed **logical consistency** (0 unsatisfiable classes) and inferred the expected class memberships (`Visited Property` and `Closed Cycle`). The sequence restrictions AX-SEQ-02 and AX-SEQ-03 were additionally validated with a deliberately flawed scenario (closed cycle with an unvisited property), and the reasoner correctly detected the resulting inconsistency. Suites: `scripts/validate_ontology.py` and `scripts/validate_cqs.py` (36/36 CQs: 29 SPARQL, 4 structural, 3 at the application layer).

---

## 6. Version Control

| Version | Date | Description |
|---------|------|-------------|
| v.01 | 15/07/2026 | SIGEVS-O operational ontology encoded in gUFO/OWL and verified |
| v.02 | 25/11/2026 | Registration phases replacing the TemporaryProperty role; AX-GEO-01 1..4; 24 axioms; 36 named classes; 43 restrictions |

---

## References

- SABiOx Guide 2024-09: Sections 7.1 (IMP-CONC), 7.2 (IMP-RELC), 7.3 (IMP-AXIO), 7.4 (DOC-OPER), 7.6 (EVA-OPER)
- Operational Ontology Premise: `../04-design/01-doc-oper.md`
- Reference Ontology Document (complete): `../03-capture/05-model-doc.md`
- Axioms: `../03-capture/02-cap-axim.md`
- Classes and Relations: `../conceptual-model/relacoes-sigevs.md` (repository)
