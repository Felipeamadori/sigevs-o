# Ontology

This directory contains the gUFO/OWL formalisation of SIGEVS-O.

## Files

| File | Description |
|------|-------------|
| `SIGEVS-O.ttl` | Raw export of the OntoUML model from the Visual Paradigm OntoUML plugin (classes and object properties) |
| `SIGEVS-O-complete.ttl` | Completed formalisation: datatype properties (attributes), inverse relations, `owl:hasKey` axioms and the 31 formal axioms — canonical artifact |
| `sigevs-o.owx` | Protégé OWL/XML serialisation of the completed formalisation (used to obtain the Protégé metrics) |

## How to Load

1. Open Protégé (≥ 5.6.0)
2. File → Open → select `SIGEVS-O-complete.ttl`
3. Load gUFO vocabulary: [https://purl.org/nemo/gufo](https://purl.org/nemo/gufo)
4. Run the HermiT reasoner to verify consistency

To validate the ontology automatically (populate → reason → SPARQL), run:

```bash
python ../scripts/validate_ontology.py
```

## Dependencies

- [gUFO](https://purl.org/nemo/gufo) — Lightweight OWL implementation of UFO
- `rdflib` and `owlready2` (for the validation script)
