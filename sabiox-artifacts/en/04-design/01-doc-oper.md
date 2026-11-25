# Design Phase — DOC-OPER (Operational Ontology Premise Document)

---

## Operational Ontology Document (Premise)

| Field | Value |
|-------|-------|
| Document: | Operational Ontology Document (Premise) |
| Ontology: | SIGEVS-O — Ontology for Sanitary Event Management in Animal Health Defense |
| Version: | v.02 |
| Date: | 08/07/2026 (v.01); v.02 25/11/2026 (registration phases) |

---

## 1. Encoding Language (DES-LANG)

**OWL 2** encoded through **gUFO** — a lightweight implementation of the Unified Foundational Ontology (UFO) [Almeida et al. 2019].

gUFO was chosen because it preserves, in a practicable OWL ontology, the central ontological distinctions of UFO (Kind, Subkind, Role, Phase, Relator, Event, Collective, etc.), enabling:

- **Automated reasoning** with reasoners such as HermiT;
- **SPARQL query answering** directly over the imported model (Protégé);
- **Semantic consistency** in real-world application scenarios, without requiring the full formalisation of every foundational axiom.

Unlike a "pure" OWL ontology (without grounding), adopting gUFO guarantees that the ontological distinctions captured in the OntoUML conceptual model (Kind, Role, Phase, Relator, Event) are preserved in the operational encoding.

---

## 2. Vocabularies (DES-VOCA)

The following vocabularies/resources were adopted in the operational encoding:

| Vocabulary / Resource | Role |
|-----------------------|------|
| **gUFO** (`http://purl.org/nemo/gufo`) | Provides the UFO stereotype classes (`gufo:Kind`, `gufo:Role`, `gufo:Phase`, `gufo:Relator`, `gufo:Event`, etc.) for typing domain classes |
| **OWL 2 / RDF / RDFS** | Encoding language and modelling primitives (`owl:Class`, `rdfs:subClassOf`, `owl:ObjectProperty`, `owl:DatatypeProperty`) |
| **ontouml-schema** (`https://github.com/tgoprince/ontouml-schema`) | JSON serialisation format of the OntoUML model for tool interchange (Visual Paradigm, ontouml-js) |

**IRIs:** the ontology implements the domain concepts with **Portuguese IRIs** and **English labels (`rdfs:label`)** (e.g., `sigevs:Estabelecimento` with `rdfs:label "Establishment"`). The `sigevs:` prefix points to `https://sigevs.ontologies#`.

No external domain vocabulary (e.g., AGROVOC, IDO) was imported in this version — reuse of domain ontologies remains future work (see `../02-setup/01-setup-references.md`, Section 4).

---

## 3. Ontology Encoding (DES-CODE)

### 3.1 OntoUML → OWL/gUFO Mapping

| OntoUML | OWL/gUFO | Example |
|---------|----------|---------|
| `<<Kind>>` | `owl:Class` typed with `gufo:Kind` | `Establishment rdf:type gufo:Kind` |
| `<<Subkind>>` | `rdfs:subClassOf` (specialisation of the Kind) | `Slaughterhouse rdfs:subClassOf Establishment` |
| `<<Role>>` | `owl:Class` typed with `gufo:Role` | `InvestigationTarget rdf:type gufo:Role` |
| `<<Phase>>` | `owl:Class` typed with `gufo:Phase` (+ `owl:disjointWith` among phases of the same partition) | `RegisteredEstablishment rdf:type gufo:Phase` |
| `<<Relator>>` | `owl:Class` typed with `gufo:Relator` | `PropertyInArea rdf:type gufo:Relator` |
| `<<Event>>` | `owl:Class` typed with `gufo:EventType` | `PropertySubmission rdf:type gufo:EventType` |
| `<<Collective>>` | `owl:Class` typed with `gufo:Collective`/`VariableCollection` | `FieldTeam rdf:type gufo:Collective` |
| Association | `owl:ObjectProperty` | `estabelecimentoHasEndereco` |
| Attribute | `owl:DatatypeProperty` | `nomeEstabelecimento` |
| Generalisation (Role/Phase of Kind) | `rdfs:subClassOf` | `InvestigationTarget rdfs:subClassOf Establishment` |

### 3.2 Encoding Rules

1. **Roles and Phases specialise their Kind** (`rdfs:subClassOf`), dispensing ontologically redundant `material` associations — the roles `AlvoInvestigacao` and `PropriedadeContactante` specialise `Estabelecimento`; `MembroEquipe` and `PessoaConvocada` specialise `Pessoa`; the phases `EstabelecimentoCadastrado` and `EstabelecimentoNaoCadastrado` also specialise `Estabelecimento` (an intrinsic, contingent condition modelled as Phase — not as Role — because it is not relational).
2. **Relators** mediate at least two entities (e.g., `PropertyInArea` mediates `AreaOperacional` and `PropriedadeInspecionada` (a role of `Estabelecimento`), carrying the `visitaConcluida` quality); `ZonaControleInvestigacao` mediates `AlvoInvestigacao` and delimits `AreaOperacional`.
3. **Events** carry timestamps and take part in hierarchical composition relations (e.g., `RespostaSanitaria` has `CicloVigilancia`).
4. **Enums** (ZoneType, BarrierType, BarrierRole, MovementPurpose, plus the `CategoriaEspecie` enumeration) are encoded as individuals of an `Enumeration` class.

---

## 4. Defined Classes (Derived States)

Beyond the 33 domain concepts, four defined classes capture derived states by logical inference:

| Defined Class | Definition |
|---------------|------------|
| `Closed Cycle` | `CicloVigilancia` marked as closed (`cicloFechado = true`), defined by equivalence, with the closure restriction as an additional subsumption axiom (all areas concluded) |
| `Completed Area` | `AreaOperacional` whose properties have all been visited |
| `Visited Property` | `PropriedadeEmArea` with `visitaConcluida = true` |
| `Quarantined Person` | `PessoaConvocada` with active quarantine status |

---

## 5. Version Control

| Version | Date | Description |
|---------|------|-------------|
| v.01 | 08/07/2026 | Premises of the SIGEVS-O operational ontology (gUFO/OWL) |
| v.02 | 25/11/2026 | Replacement of the TemporaryProperty role by the registration phases; AX-GEO-01 (zones: max. 3 concentric; API `INVESTIGATION` outside the model); axiom renumbering (24) |

---

## References

- SABiOx Guide 2024-09: Sections 6.1 (DES-LANG), 6.2 (DES-VOCA), 6.3 (DES-CODE), 6.4 (DOC-OPER)
- Reference Ontology Document (complete): `../03-capture/05-model-doc.md`
- OntoUML Model: `../03-capture/03-ontouml-model.md`
- gUFO: [Almeida et al. 2019] — A Lightweight Implementation of the Unified Foundational Ontology (UFO)
