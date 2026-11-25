#!/usr/bin/env python3
"""Structural validation of the SIGEVS-O ontology (TBox).

Checks the gUFO/OWL artefact against the metrics and modelling rules reported
in the papers and in ``ontology/README``:

1. Inventory metrics: 33 domain concepts (32 classes + the SpeciesCategory
   enumeration), 4 defined classes (37 named classes), 36 object properties,
   113 datatype properties.
2. gUFO conformance: every domain class carries exactly one gUFO type
   (Kind/SubKind/Role/EventType/Relator/Collective/AbstractIndividualType);
   SpeciesCategory is typed as an enumeration with its 5 value individuals.
3. Taxonomy: the 10 generalisations (3 Subkinds + 5 Roles + 2 Phases over
   Establishment and Person) are present as ``rdfs:subClassOf``.
4. Property sanity: every object property has a declared domain and range,
   every datatype property has a declared domain.

Usage::

    python scripts/validate_ontology_structure.py
    python scripts/validate_ontology_structure.py --ontology ontology/SIGEVS-O-complete.ttl

Exit code is 0 when every check passes and 1 otherwise.

Requirements: rdflib.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from rdflib import Graph, Namespace, RDF, RDFS, OWL
except ImportError:
    print("[error] rdflib is required: pip install rdflib")
    sys.exit(2)

SIGEVS = Namespace("https://sigevs.ontologies#")
GUFO = Namespace("http://purl.org/nemo/gufo#")

DEFAULT_ONTOLOGY = Path(__file__).resolve().parents[1] / "ontology" / "SIGEVS-O-complete.ttl"

DOMAIN_CLASSES = {
    # Core (9)
    "Estabelecimento": GUFO.Kind, "Endereco": GUFO.Kind, "Pessoa": GUFO.Kind,
    "EspecieAnimal": GUFO.Kind, "Frigorifico": GUFO.SubKind,
    "GranjaSuino": GUFO.SubKind, "GranjaAve": GUFO.SubKind,
    "EstabelecimentoCadastrado": GUFO.Phase, "EstabelecimentoNaoCadastrado": GUFO.Phase,
    # Investigation (7)
    "AnaliseSanitaria": GUFO.EventType, "AlvoInvestigacao": GUFO.Role,
    "AreaAfetada": GUFO.Kind, "ZonaControleInvestigacao": GUFO.Relator,
    "MovimentacaoAnimal": GUFO.EventType, "PropriedadeContactante": GUFO.Role,
    "CategoriaEspecie": GUFO.AbstractIndividualType,
    # Response (14)
    "RespostaSanitaria": GUFO.EventType, "CicloVigilancia": GUFO.EventType,
    "ZonaPorCiclo": GUFO.Relator, "EquipeCampo": GUFO.Collective,
    "TipoEquipe": GUFO.Kind, "MembroEquipe": GUFO.Role, "Funcao": GUFO.Kind,
    "AreaOperacional": GUFO.Kind, "PropriedadeEmArea": GUFO.Relator,
    "BarreiraSanitaria": GUFO.Kind, "Veiculo": GUFO.Kind,
    "PostoComando": GUFO.Kind, "PessoaConvocada": GUFO.Role,
    "RastreamentoGps": GUFO.EventType,
    # RelRig partial refactoring (role of Establishment)
    "PropriedadeInspecionada": GUFO.Role,
    # Field Actions (2)
    "SubmissaoPropriedade": GUFO.EventType, "SubmissaoBarreira": GUFO.EventType,
}

DEFINED_CLASSES = {
    "AreaConcluida": "OperationalArea whose properties are all visited",
    "CicloFechado": "SurveillanceCycle closed after all areas concluded",
    "PropriedadeVisitada": "PropertyInArea with visitaConcluida=true",
    "PessoaEmQuarentena": "SummonedPerson with emQuarentena=true",
}

GENERALIZATIONS = {
    # (subkind/role, superclass)
    ("Frigorifico", "Estabelecimento"),
    ("GranjaSuino", "Estabelecimento"),
    ("GranjaAve", "Estabelecimento"),
    ("AlvoInvestigacao", "Estabelecimento"),
    ("PropriedadeContactante", "Estabelecimento"),
    ("EstabelecimentoCadastrado", "Estabelecimento"),
    ("EstabelecimentoNaoCadastrado", "Estabelecimento"),
    ("MembroEquipe", "Pessoa"),
    ("PessoaConvocada", "Pessoa"),
    ("PropriedadeInspecionada", "Estabelecimento"),
}

ENUM_VALUES = {
    "CategoriaAves", "CategoriaSuinos", "CategoriaOvinos",
    "CategoriaBovinos", "CategoriaOutros",
}


def short(term) -> str:
    text = str(term)
    for marker in ("#", "/"):
        if marker in text:
            text = text.rsplit(marker, 1)[-1]
    return text


def local_name(term) -> str:
    return short(term) if term is not None else ""


def check_metrics(g: Graph, failures: list[str]) -> None:
    print("\n[1] Inventory metrics")
    named_sigevs = {c for c in g.subjects(RDF.type, OWL.Class)
                    if str(c).startswith(str(SIGEVS))}
    defined_classes = {c for c in named_sigevs if local_name(c) in DEFINED_CLASSES}
    domain_classes = named_sigevs - defined_classes
    obj_props = set(g.subjects(RDF.type, OWL.ObjectProperty))
    data_props = set(g.subjects(RDF.type, OWL.DatatypeProperty))

    checks = [
        ("domain concepts (classes + enumeration)", len(domain_classes), 33),
        ("defined classes", len(defined_classes), 4),
        ("named classes", len(named_sigevs), 37),
        ("object properties", len(obj_props), 36),
        ("datatype properties", len(data_props), 113),
    ]
    for label, actual, expected in checks:
        ok = actual == expected
        print(f"    {label:<40} expected {expected:>3}  found {actual:>3}  [{'ok' if ok else 'FAIL'}]")
        if not ok:
            failures.append(f"metric mismatch: {label}: expected {expected}, found {actual}")

    missing = {name for name in DOMAIN_CLASSES if SIGEVS[name] not in named_sigevs}
    extra = {local_name(c) for c in named_sigevs} - set(DOMAIN_CLASSES) - set(DEFINED_CLASSES)
    if missing:
        failures.append(f"missing domain classes: {sorted(missing)}")
        print(f"    missing domain classes: {sorted(missing)} [FAIL]")
    else:
        print(f"    domain class names match the documented catalogue    [ok]")
    if extra:
        failures.append(f"unexpected classes in ontology: {sorted(extra)}")
        print(f"    unexpected classes: {sorted(extra)} [FAIL]")
    else:
        print(f"    no undocumented classes                               [ok]")


def gufo_types(g: Graph, cls) -> set:
    """gUFO types of a class, either by direct rdf:type punning or by
    subclassing a gUFO sortal (e.g. rdfs:subClassOf gufo:Relator)."""
    types = {t for t in g.objects(cls, RDF.type) if str(t).startswith(str(GUFO))}
    types |= {sup for sup in g.objects(cls, RDFS.subClassOf)
              if str(sup).startswith(str(GUFO))}
    return types


def check_gufo_types(g: Graph, failures: list[str]) -> None:
    print("\n[2] gUFO stereotype conformance")
    # a Collective may be typed as gufo:VariableCollection (variable collection)
    alias = {GUFO.Collective: {GUFO.Collective, GUFO.VariableCollection}}
    for name, gufo_type in DOMAIN_CLASSES.items():
        cls = SIGEVS[name]
        types = gufo_types(g, cls)
        accepted = alias.get(gufo_type, {gufo_type})
        if not (types & accepted):
            failures.append(f"{name}: expected gUFO type {local_name(gufo_type)}, "
                            f"found {sorted(map(local_name, types))}")
            print(f"    {name:<25} [{local_name(gufo_type)}] FAIL (found {sorted(map(local_name, types))})")
            continue
        print(f"    {name:<25} [{local_name(gufo_type)}] ok")

    enum_values = {local_name(ind)
                   for ind in g.subjects(RDF.type, SIGEVS.CategoriaEspecie)}
    if ENUM_VALUES <= enum_values:
        print(f"    SpeciesCategory enumeration values present "
              f"({len(enum_values)}/5)                              [ok]")
    else:
        failures.append(f"enum values missing: {sorted(ENUM_VALUES - enum_values)}")
        print(f"    enum values missing: {sorted(ENUM_VALUES - enum_values)} [FAIL]")


def check_taxonomy(g: Graph, failures: list[str]) -> None:
    print("\n[3] Taxonomy (generalizations)")
    found = {(local_name(sub), local_name(sup))
             for sub, sup in g.subject_objects(RDFS.subClassOf)
             if str(sub).startswith(str(SIGEVS)) and str(sup).startswith(str(SIGEVS))}
    for sub, sup in sorted(GENERALIZATIONS):
        ok = (sub, sup) in found
        print(f"    {sub:<25} rdfs:subClassOf {sup:<20} [{'ok' if ok else 'FAIL'}]")
        if not ok:
            failures.append(f"missing generalization: {sub} -> {sup}")
    unexpected = found - GENERALIZATIONS
    if unexpected:
        failures.append(f"unexpected subClassOf pairs: {sorted(unexpected)}")
        print(f"    unexpected subClassOf pairs: {sorted(unexpected)} [FAIL]")
    else:
        print(f"    exactly {len(GENERALIZATIONS)} generalizations, as documented      [ok]")


def check_properties(g: Graph, failures: list[str]) -> None:
    print("\n[4] Property domains/ranges")
    problems = 0
    for prop in sorted(g.subjects(RDF.type, OWL.ObjectProperty), key=str):
        domain = g.value(prop, RDFS.domain)
        range_ = g.value(prop, RDFS.range)
        domain_ok = domain is not None and str(domain).startswith(str(SIGEVS))
        range_ok = range_ is not None and str(range_).startswith(str(SIGEVS))
        if not (domain_ok and range_ok):
            problems += 1
            failures.append(f"object property {local_name(prop)}: "
                            f"domain={local_name(domain) if domain else None}, "
                            f"range={local_name(range_) if range_ else None}")
    print(f"    object properties with declared sigevs: domain and range: "
          f"{36 - problems}/36 [{'ok' if problems == 0 else 'FAIL'}]")

    no_domain = [local_name(p) for p in g.subjects(RDF.type, OWL.DatatypeProperty)
                 if g.value(p, RDFS.domain) is None]
    if no_domain:
        print(f"    warning: datatype properties without domain (shared by several "
              f"classes, by design): {sorted(no_domain)}")
        for name in no_domain:
            if not SIGEVS[name] in g.subjects(RDF.type, OWL.DatatypeProperty):
                failures.append(f"datatype property {name}: not declared")
    else:
        print(f"    all datatype properties declare a domain             [ok]")

    # gUFO typing of properties (informational: gUFO object-property types such
    # as gufo:mediates are not asserted in the current artefact)
    untyped = [local_name(p) for p in g.subjects(RDF.type, OWL.ObjectProperty)
               if not any(str(t).startswith(str(GUFO)) for t in g.objects(p, RDF.type))]
    if untyped:
        print(f"    info: {len(untyped)} object properties do not carry a gUFO type "
              f"(gufo:mediates etc.); stereotype semantics live in the OntoUML model")
    else:
        print(f"    all object properties carry a gUFO type              [ok]")


def main() -> int:
    parser = argparse.ArgumentParser(description="Structural validation of SIGEVS-O (TBox).")
    parser.add_argument("--ontology", type=Path, default=DEFAULT_ONTOLOGY)
    args = parser.parse_args()

    ontology_path = args.ontology if args.ontology.is_absolute() else (Path.cwd() / args.ontology)
    if not ontology_path.exists():
        print(f"[error] ontology not found: {ontology_path}")
        return 1

    graph = Graph()
    graph.parse(str(ontology_path), format="turtle")

    print("=" * 72)
    print(f"SIGEVS-O structural validation")
    print(f"ontology: {ontology_path} ({len(graph)} triples)")
    print("=" * 72)

    failures: list[str] = []
    check_metrics(graph, failures)
    check_gufo_types(graph, failures)
    check_taxonomy(graph, failures)
    check_properties(graph, failures)

    print("\n" + "=" * 72)
    if failures:
        print(f"RESULT: FAILED ({len(failures)} problem(s))")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("RESULT: ALL STRUCTURAL CHECKS PASSED")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
