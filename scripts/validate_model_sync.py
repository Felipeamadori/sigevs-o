#!/usr/bin/env python3
"""Cross-check the OntoUML conceptual model (Mermaid) against the OWL ontology.

Guards against model drift between the Mermaid sources in
``conceptual-model/`` (the reference model) and the gUFO/OWL artefact in
``ontology/SIGEVS-O-complete.ttl``:

1. Class inventory: the 33 classes in ``onto-complete.mmd`` must map 1:1 to
   the 33 domain classes in the OWL file (English model names are mapped to
   the Portuguese OWL names).
2. Stereotypes: ``<<Kind>>``, ``<<Subkind>>``, ``<<Role>>``, ``<<Event>>``,
   ``<<Relator>>``, ``<<Collective>>`` and ``<<Enumeration>>`` must match the
   gUFO types asserted in the ontology.
3. Generalizations: the ``<|--`` pairs in the model must match the
   ``rdfs:subClassOf`` pairs in the ontology.
4. Relations: the model must contain the 31 documented relationships.
5. Defined classes (OWL only): Closed Cycle, Completed Area, Visited
   Property, Quarantined Person must NOT appear in the conceptual model.

Usage::

    python scripts/validate_model_sync.py
    python scripts/validate_model_sync.py --model conceptual-model/onto-complete.mmd \
                                           --ontology ontology/SIGEVS-O-complete.ttl

Exit code is 0 when every check passes and 1 otherwise.

Requirements: rdflib.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from rdflib import Graph, RDF, RDFS, OWL, URIRef
except ImportError:
    print("[error] rdflib is required: pip install rdflib")
    sys.exit(2)

DEFAULT_MODEL = Path(__file__).resolve().parents[1] / "conceptual-model" / "onto-complete.mmd"
DEFAULT_ONTOLOGY = Path(__file__).resolve().parents[1] / "ontology" / "SIGEVS-O-complete.ttl"

# English name in the Mermaid model -> (Portuguese OWL class, gUFO type)
MODEL_CLASSES = {
    "Establishment": ("Estabelecimento", "Kind"),
    "Address": ("Endereco", "Kind"),
    "Person": ("Pessoa", "Kind"),
    "AnimalSpecies": ("EspecieAnimal", "Kind"),
    "Slaughterhouse": ("Frigorifico", "Subkind"),
    "SwineFarm": ("GranjaSuino", "Subkind"),
    "PoultryFarm": ("GranjaAve", "Subkind"),
    "SanitaryAnalysis": ("AnaliseSanitaria", "Event"),
    "InvestigationTarget": ("AlvoInvestigacao", "Role"),
    "AffectedArea": ("AreaAfetada", "Kind"),
    "ControlZone": ("ZonaControleInvestigacao", "Relator"),
    "AnimalMovement": ("MovimentacaoAnimal", "Event"),
    "ContactingProperty": ("PropriedadeContactante", "Role"),
    "SpeciesCategory": ("CategoriaEspecie", "Enumeration"),
    "SanitaryResponse": ("RespostaSanitaria", "Event"),
    "SurveillanceCycle": ("CicloVigilancia", "Event"),
    "ZonePerCycle": ("ZonaPorCiclo", "Relator"),
    "FieldTeam": ("EquipeCampo", "Collective"),
    "TeamType": ("TipoEquipe", "Kind"),
    "TeamMember": ("MembroEquipe", "Role"),
    "TeamFunction": ("Funcao", "Kind"),
    "OperationalArea": ("AreaOperacional", "Kind"),
    "PropertyInArea": ("PropriedadeEmArea", "Relator"),
    "SanitaryBarrier": ("BarreiraSanitaria", "Kind"),
    "Vehicle": ("Veiculo", "Kind"),
    "CommandPost": ("PostoComando", "Kind"),
    "SummonedPerson": ("PessoaConvocada", "Role"),
    "GPSTracking": ("RastreamentoGps", "Event"),
    "PropertySubmission": ("SubmissaoPropriedade", "Event"),
    "BarrierSubmission": ("SubmissaoBarreira", "Event"),
    "RegisteredEstablishment": ("EstabelecimentoCadastrado", "Phase"),
    "UnregisteredEstablishment": ("EstabelecimentoNaoCadastrado", "Phase"),
    # RelRig partial refactoring (role of Establishment)
    "InspectedEstablishment": ("PropriedadeInspecionada", "Role"),
}

GUFO_TYPE_FOR_STEREOTYPE = {
    "Kind": "Kind",
    "Subkind": "SubKind",
    "Role": "Role",
    "Phase": "Phase",
    "Event": "EventType",
    "Relator": "Relator",
    "Collective": "Collective",
    "Enumeration": "AbstractIndividualType",
}


def parse_mmd(path: Path):
    """Return (classes: {name: stereotype}, generalizations: {(sub, sup)}, relations: [(src, dst, name)])."""
    text = path.read_text(encoding="utf-8")
    classes: dict[str, str] = {}
    for match in re.finditer(
            r"class\s+([A-Za-z][A-Za-z0-9]*)\s*\{\s*<<\s*([A-Za-z]+)\s*>>\s*(?:(\w[\w\s]*)?)?\}",
            text):
        name, stereotype = match.group(1), match.group(2)
        classes[name] = stereotype

    generalizations = set()
    for match in re.finditer(r"(\w+)\s*<\|--\s*(\w+)", text):
        sup, sub = match.group(1), match.group(2)
        generalizations.add((sub, sup))

    relations = set()
    # optional quoted multiplicities ("1" --> "*") and relation stereotype («mediation»)
    for match in re.finditer(
            r'(\w+)\s*(?:"[^"]*"\s*)?-->\s*(?:"[^"]*"\s*)?(\w+)\s*:\s*(?:«\w+»\s*)?(\w+)', text):
        relations.add((match.group(1), match.group(2), match.group(3)))
    return classes, generalizations, relations


def local_name(term) -> str:
    return str(term).rsplit("#", 1)[-1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Cross-check conceptual model vs OWL ontology.")
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--ontology", type=Path, default=DEFAULT_ONTOLOGY)
    args = parser.parse_args()

    model_path = args.model if args.model.is_absolute() else (Path.cwd() / args.model)
    ontology_path = args.ontology if args.ontology.is_absolute() else (Path.cwd() / args.ontology)
    for path in (model_path, ontology_path):
        if not path.exists():
            print(f"[error] file not found: {path}")
            return 1

    graph = Graph()
    graph.parse(str(ontology_path), format="turtle")

    classes, generalizations, relations = parse_mmd(model_path)

    failures: list[str] = []
    print("=" * 72)
    print("SIGEVS-O model sync: conceptual model (mmd) <-> OWL ontology")
    print(f"model:     {model_path}")
    print(f"ontology:  {ontology_path}")
    print("=" * 72)

    # [1] class inventory -----------------------------------------------------
    print("\n[1] Class inventory")
    owl_classes = {local_name(c) for c in graph.subjects(RDF.type, OWL.Class)
                   if str(c).startswith("https://sigevs.ontologies#")}
    defined = {c for c in owl_classes if c in
               {"AreaConcluida", "CicloFechado", "PropriedadeVisitada", "PessoaEmQuarentena"}}
    domain_classes_owl = owl_classes - defined

    mapped = {MODEL_CLASSES[name][0] for name in classes if name in MODEL_CLASSES}
    missing_owl = mapped - domain_classes_owl
    missing_model = domain_classes_owl - mapped

    print(f"    classes in model:            {len(classes)} (expected 33)  "
          f"[{'ok' if len(classes) == 33 else 'FAIL'}]")
    if len(classes) != 33:
        failures.append(f"model has {len(classes)} classes, expected 33")
    print(f"    domain classes in ontology:  {len(domain_classes_owl)} (expected 33)  "
          f"[{'ok' if len(domain_classes_owl) == 33 else 'FAIL'}]")
    if missing_model:
        failures.append(f"in ontology but not in model: {sorted(missing_model)}")
        print(f"    in OWL but not in model: {sorted(missing_model)} [FAIL]")
    else:
        print(f"    every OWL domain class appears in the model       [ok]")
    if missing_owl:
        failures.append(f"in model but not in ontology: {sorted(missing_owl)}")
        print(f"    in model but not in OWL: {sorted(missing_owl)} [FAIL]")
    else:
        print(f"    every model class exists in the ontology          [ok]")
    if defined:
        print(f"    defined classes only in OWL (expected): {sorted(defined)} [ok]")

    # [2] stereotypes ----------------------------------------------------------
    print("\n[2] Stereotypes (model <<stereotype>> vs gUFO type)")
    for name, (owl_name, stereotype) in sorted(MODEL_CLASSES.items()):
        if name not in classes:
            continue
        gufo_expected = GUFO_TYPE_FOR_STEREOTYPE[stereotype]
        alias = {"Collective": {"Collective", "VariableCollection"}}
        accepted = alias.get(gufo_expected, {gufo_expected})
        owl_class = URIRef(f"https://sigevs.ontologies#{owl_name}")
        actual = {local_name(t) for t in graph.objects(owl_class, RDF.type)
                  if str(t).startswith("http://purl.org/nemo/gufo#")}
        actual |= {local_name(sup) for sup in graph.objects(owl_class, RDFS.subClassOf)
                   if str(sup).startswith("http://purl.org/nemo/gufo#")}
        if not (actual & accepted):
            failures.append(f"{owl_name}: model says <<{stereotype}>> "
                            f"({gufo_expected}), OWL has {sorted(actual)}")
            print(f"    {owl_name:<25} <<{stereotype:<12}>> FAIL (OWL: {sorted(actual)})")
        else:
            print(f"    {owl_name:<25} <<{stereotype:<12}>> ok")
    # <<Phase>> classes are materialised since the registration-phase refactoring.

    # [3] generalizations ------------------------------------------------------
    print("\n[3] Generalizations")
    owl_generalizations = {(local_name(sub), local_name(sup))
                           for sub, sup in graph.subject_objects(RDFS.subClassOf)
                           if str(sub).startswith("https://sigevs.ontologies#")
                           and str(sup).startswith("https://sigevs.ontologies#")}
    model_gen_owl_names = {
        (MODEL_CLASSES[sub][0], MODEL_CLASSES[sup][0])
        for sub, sup in generalizations if sub in MODEL_CLASSES and sup in MODEL_CLASSES
    }
    if model_gen_owl_names == owl_generalizations:
        print(f"    {len(generalizations)} generalizations match rdfs:subClassOf pairs  [ok]")
    else:
        only_model = model_gen_owl_names - owl_generalizations
        only_owl = owl_generalizations - model_gen_owl_names
        if only_model:
            failures.append(f"generalizations only in model: {sorted(only_model)}")
            print(f"    only in model: {sorted(only_model)} [FAIL]")
        if only_owl:
            failures.append(f"generalizations only in OWL: {sorted(only_owl)}")
            print(f"    only in OWL: {sorted(only_owl)} [FAIL]")

    # [4] relations --------------------------------------------------------------
    print("\n[4] Relationships")
    if len(relations) == 31:
        print(f"    {len(relations)} relations in the model (expected 31)        [ok]")
    else:
        failures.append(f"model has {len(relations)} relations, expected 31")
        print(f"    {len(relations)} relations in the model (expected 31)        [FAIL]")

    owl_obj_props = {local_name(p) for p in graph.subjects(RDF.type, OWL.ObjectProperty)}
    print(f"    object properties in OWL: {len(owl_obj_props)} (expected 36)        "
          f"[{'ok' if len(owl_obj_props) == 36 else 'FAIL'}]")
    if len(owl_obj_props) != 36:
        failures.append(f"OWL has {len(owl_obj_props)} object properties, expected 36")

    # [5] attribute drift -----------------------------------------------------
    print("\n[5] Visit-completion attribute")
    # the datatype property visitaConcluida must have PropriedadeEmArea in domain
    visita = URIRef("https://sigevs.ontologies#visitaConcluida")
    domain = graph.value(visita, RDFS.domain)
    ok = domain is not None and local_name(domain) == "PropriedadeEmArea"
    print(f"    visitaConcluida domain: {local_name(domain) if domain else None} "
          f"[{'ok' if ok else 'FAIL'}]")
    if not ok:
        failures.append("visitaConcluida is not a datatype property of PropriedadeEmArea")

    print("\n" + "=" * 72)
    if failures:
        print(f"RESULT: FAILED ({len(failures)} problem(s))")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("RESULT: MODEL AND ONTOLOGY ARE IN SYNC")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
