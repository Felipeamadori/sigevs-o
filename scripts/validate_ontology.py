#!/usr/bin/env python3
"""End-to-end validation of the SIGEVS-O ontology.

The script performs three steps:

1. Loads the gUFO/OWL ontology (``SIGEVS-O-complete.ttl``) and populates it
   with a sample outbreak-response scenario (ABox).
2. Runs the HermiT reasoner (through owlready2) to check logical consistency,
   verify the inference of the defined classes and confirm that the
   AX-SEQ-02/AX-SEQ-03 constraint is violated (detected as an inconsistency)
   in a deliberately flawed scenario: a cycle marked as closed while one of
   its properties remains unvisited.
3. Executes the representative SPARQL queries in ``sparql/`` against the
   populated ontology (CQ-CORE-01, CQ-RES-03, CQ-CAM-04) and evaluates
   CQ-INV-01 with a haversine filter equivalent to its GeoSPARQL query.

Requirements: rdflib, owlready2 (and Java, used by HermiT).

Usage::

    python scripts/validate_ontology.py
    python scripts/validate_ontology.py --ontology ontology/SIGEVS-O-complete.ttl
    python scripts/validate_ontology.py --save-populated ontology/SIGEVS-O-populated.ttl

Exit code is 0 when every check passes and 1 otherwise.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import logging
import math
import os
import shutil
import sys
import tempfile
from pathlib import Path

try:
    from rdflib import Graph, Literal, Namespace, OWL, RDFS
    from rdflib.namespace import XSD
except ImportError:
    print("[error] rdflib is required: pip install rdflib")
    sys.exit(2)

SIGEVS = Namespace("https://sigevs.ontologies#")
EX = Namespace("http://example.org/sigevs-sample#")
GUFO_TTL_URL = "https://nemo-ufes.github.io/gufo/gufo.ttl"

DEFAULT_ONTOLOGY = Path(__file__).resolve().parents[1] / "ontology" / "SIGEVS-O-complete.ttl"
SPARQL_DIR = Path(__file__).resolve().parents[1] / "sparql"


def load_query(name: str) -> str:
    """Load a representative query from the sparql/ directory."""
    return (SPARQL_DIR / name).read_text(encoding="utf-8")

# ---------------------------------------------------------------------------
# Sample ABox: a small outbreak-response scenario inspired by the Montenegro
# (2025) HPAI event reported in the paper.
# ---------------------------------------------------------------------------

SAMPLE_ABOX = """
@prefix ex: <http://example.org/sigevs-sample#> .
@prefix sigevs: <https://sigevs.ontologies#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Core -------------------------------------------------------------------
ex:EstabelecimentoFoco a sigevs:Estabelecimento ;
    sigevs:codigoEstabelecimento "SDA-001" ;
    sigevs:nomeEstabelecimento "Granja Sao Joao" ;
    sigevs:coordenadas "POINT(-51.4611 -29.6886)" .

ex:EstabelecimentoVizinho a sigevs:Estabelecimento ;
    sigevs:codigoEstabelecimento "SDA-002" ;
    sigevs:nomeEstabelecimento "Sitio Boa Vista" ;
    sigevs:coordenadas "POINT(-51.4500 -29.6800)" .

ex:EstabelecimentoIntermediario a sigevs:Estabelecimento ;
    sigevs:codigoEstabelecimento "SDA-003" ;
    sigevs:nomeEstabelecimento "Fazenda Tres Pinheiros" ;
    sigevs:coordenadas "POINT(-51.4000 -29.6500)" .

ex:EstabelecimentoDistante a sigevs:Estabelecimento ;
    sigevs:codigoEstabelecimento "SDA-004" ;
    sigevs:nomeEstabelecimento "Fazenda Santa Rita" ;
    sigevs:coordenadas "POINT(-51.2000 -29.5000)" .

# Sanitary investigation --------------------------------------------------
ex:AnaliseHPAI a sigevs:AnaliseSanitaria ;
    sigevs:nomeAnalise "Investigacao HPAI Montenegro" ;
    sigevs:analiseAtiva true ;
    sigevs:criadaEm "2025-05-16T08:00:00"^^xsd:dateTime .

ex:FocoHPAI a sigevs:AlvoInvestigacao ;
    sigevs:nomeAlvo "Foco HPAI" ;
    sigevs:coordenadas "POINT(-51.4611 -29.6886)" ;
    sigevs:alvoDeAnalise ex:AnaliseHPAI ;
    sigevs:alvoInvestigacaoHasZonaControleInvestigacao ex:ZonaPerifocal, ex:ZonaVigilancia, ex:ZonaProtecao .

ex:ZonaPerifocal a sigevs:ZonaControleInvestigacao ;
    sigevs:tipoZona "INFECTED" ;
    sigevs:raio 3.0 .

ex:ZonaVigilancia a sigevs:ZonaControleInvestigacao ;
    sigevs:tipoZona "BUFFER" ;
    sigevs:raio 10.0 .

ex:ZonaProtecao a sigevs:ZonaControleInvestigacao ;
    sigevs:tipoZona "SURVEILLANCE" ;
    sigevs:raio 15.0 .

# Sanitary response -------------------------------------------------------
ex:RespostaMontenegro a sigevs:RespostaSanitaria ;
    sigevs:identificadorResposta "RESP-2025-001" ;
    sigevs:respostaAtiva true ;
    sigevs:respostaConcluida false ;
    sigevs:BaseadaEm ex:AnaliseHPAI ;
    sigevs:Tem ex:PostoComando1 .

ex:PostoComando1 a sigevs:PostoComando ;
    sigevs:nomePosto "QG Montenegro" ;
    sigevs:postoDaResposta ex:RespostaMontenegro .

ex:Ciclo1 a sigevs:CicloVigilancia ;
    sigevs:numeroCiclo 1 ;
    sigevs:cicloFechado true ;
    sigevs:cicloPertenceAResposta ex:RespostaMontenegro .

ex:ZonaCiclo1 a sigevs:ZonaPorCiclo ;
    sigevs:zonaFechada true ;
    sigevs:zonaDoCiclo ex:Ciclo1 .

ex:EquipeA a sigevs:EquipeCampo ;
    sigevs:nomeEquipe "Equipe A" ;
    sigevs:equipeAlocadaEm ex:Ciclo1 ;
    sigevs:CompostaPor ex:JoaoSilva, ex:AnaPereira .

ex:EquipeB a sigevs:EquipeCampo ;
    sigevs:nomeEquipe "Equipe B" ;
    sigevs:equipeAlocadaEm ex:Ciclo1 ;
    sigevs:CompostaPor ex:CarlosSouza .

ex:JoaoSilva a sigevs:Pessoa, sigevs:MembroEquipe, sigevs:PessoaConvocada ;
    sigevs:keycloakSubjectId "kc-001" ;
    sigevs:cpf "11111111111" ;
    sigevs:nomePessoa "Joao Silva" ;
    sigevs:email "joao.silva@example.org" ;
    sigevs:emQuarentena false ;
    sigevs:permissaoGestao true ;
    sigevs:permissaoObservacao false ;
    sigevs:Convoca ex:RespostaMontenegro .

ex:AnaPereira a sigevs:Pessoa, sigevs:MembroEquipe ;
    sigevs:keycloakSubjectId "kc-002" ;
    sigevs:cpf "22222222222" ;
    sigevs:nomePessoa "Ana Pereira" ;
    sigevs:email "ana.pereira@example.org" .

ex:CarlosSouza a sigevs:Pessoa, sigevs:MembroEquipe ;
    sigevs:keycloakSubjectId "kc-003" ;
    sigevs:cpf "33333333333" ;
    sigevs:nomePessoa "Carlos Souza" ;
    sigevs:email "carlos.souza@example.org" .

# Operational areas and properties ---------------------------------------
ex:AreaA a sigevs:AreaOperacional ;
    sigevs:nomeArea "Area A" ;
    sigevs:PertenceA ex:ZonaCiclo1 ;
    sigevs:areaDaEquipe ex:EquipeA ;
    sigevs:Contem ex:PIA1, ex:PIA2 .

ex:AreaB a sigevs:AreaOperacional ;
    sigevs:nomeArea "Area B" ;
    sigevs:PertenceA ex:ZonaCiclo1 ;
    sigevs:areaDaEquipe ex:EquipeB ;
    sigevs:Contem ex:PIA3 .

ex:PIA1 a sigevs:PropriedadeEmArea ;
    sigevs:visitaConcluida true ;
    sigevs:contidaEmArea ex:AreaA ;
    sigevs:RefereSeA ex:EstabelecimentoFoco .

ex:PIA2 a sigevs:PropriedadeEmArea ;
    sigevs:visitaConcluida true ;
    sigevs:contidaEmArea ex:AreaA ;
    sigevs:RefereSeA ex:EstabelecimentoVizinho .

ex:PIA3 a sigevs:PropriedadeEmArea ;
    sigevs:visitaConcluida true ;
    sigevs:contidaEmArea ex:AreaB ;
    sigevs:RefereSeA ex:EstabelecimentoIntermediario .

ex:Submissao1 a sigevs:SubmissaoPropriedade ;
    sigevs:uuidSubmissao "sub-0001" ;
    sigevs:VinculadaA ex:PIA1 ;
    sigevs:RealizadaPor ex:EquipeA .

# Field actions -----------------------------------------------------------
ex:Temporaria1 a sigevs:PropriedadeTemporaria ;
    sigevs:nomeContato "Maria Souza" ;
    sigevs:cpfCnpj "44444444444" ;
    sigevs:telefone "+55 55 99999-0000" ;
    sigevs:coordenadas "POINT(-51.4600 -29.6870)" .

ex:BarreiraBR287 a sigevs:BarreiraSanitaria ;
    sigevs:nomeBarreira "Barreira BR-287" ;
    sigevs:tipoBarreira "FIXED" ;
    sigevs:papelBarreira "SANITARY" ;
    sigevs:coordenadas "POINT(-51.4300 -29.6700)" .

ex:SubmissaoBarreira1 a sigevs:SubmissaoBarreira ;
    sigevs:uuidSubmissaoBarreira "sub-bar-0001" ;
    sigevs:submissaoBarreiraHasBarreiraSanitaria ex:BarreiraBR287 .
"""

# ---------------------------------------------------------------------------
# Competency-question queries (adapted to the ontology IRIs; see the note at
# the end of the report about the paper listings).
# ---------------------------------------------------------------------------

CQ_CORE_01 = load_query("cq-core-01.rq")

# CQ-INV-01 is evaluated in Python because the GeoSPARQL query in
# sparql/cq-inv-01.rq requires a spatial engine; this query retrieves the
# candidate pairs and the haversine filter is applied below.
CQ_INV_01 = """
PREFIX sigevs: <https://sigevs.ontologies#>
SELECT ?alvo ?tipo ?raio ?alvoCoord ?estabelecimento ?nome ?coord WHERE {
  ?alvo a sigevs:AlvoInvestigacao ;
        sigevs:coordenadas ?alvoCoord ;
        sigevs:alvoInvestigacaoHasZonaControleInvestigacao ?zona .
  ?zona sigevs:tipoZona ?tipo ;
        sigevs:raio ?raio .
  ?estabelecimento a sigevs:Estabelecimento ;
                   sigevs:nomeEstabelecimento ?nome ;
                   sigevs:coordenadas ?coord .
}
ORDER BY ?tipo ?nome
"""

CQ_RES_03 = load_query("cq-res-03.rq")

CQ_CAM_04 = load_query("cq-cam-04.rq")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def parse_wkt_point(wkt: str):
    """Parse 'POINT(lon lat)' into (lat, lon)."""
    inner = wkt.strip()
    for prefix in ("POINT(", "POINT ("):
        if inner.upper().startswith(prefix.upper()):
            inner = inner[len(prefix):]
            break
    inner = inner.rstrip(")").strip()
    lon, lat = (float(value) for value in inner.split())
    return lat, lon


def haversine_km(a, b) -> float:
    lat1, lon1 = a
    lat2, lon2 = b
    radius = 6371.0088
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    h = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * radius * math.asin(math.sqrt(h))


def short(term) -> str:
    text = str(term)
    for marker in ("#", "/"):
        if marker in text:
            text = text.rsplit(marker, 1)[-1]
    return text


def print_table(headers, rows) -> None:
    widths = [len(header) for header in headers]
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(str(cell)))
    line = "  ".join(str(header).ljust(widths[i]) for i, header in enumerate(headers))
    print(line)
    print("-" * len(line))
    for row in rows:
        print("  ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row)))


def load_ontology(path: Path) -> Graph:
    graph = Graph()
    graph.parse(str(path), format="turtle")
    return graph


def populate(graph: Graph) -> Graph:
    populated = Graph()
    for triple in graph:
        populated.add(triple)
    populated.parse(data=SAMPLE_ABOX, format="turtle")
    return populated


def reason(populated: Graph, gufo_path, gufo_url: str, verbose: bool = True):
    """Run HermiT over the ontology + ABox (and gUFO, when available)."""
    try:
        import owlready2
        from owlready2 import get_ontology, sync_reasoner_hermit, OwlReadyInconsistentOntologyError
    except ImportError:
        print("[error] owlready2 is required: pip install owlready2")
        return None, None, None, 0, False

    merged = Graph()
    for triple in populated:
        merged.add(triple)
    for triple in list(merged.triples((None, OWL.imports, None))):
        merged.remove(triple)

    gufo_loaded = False
    try:
        source = str(gufo_path) if gufo_path else gufo_url
        merged.parse(source, format="turtle")
        gufo_loaded = True
    except Exception as exc:  # noqa: BLE001 - network/local file may be unavailable
        if verbose:
            print(f"[warn] gUFO could not be loaded ({exc}); reasoning without gUFO axioms")

    patched = 0
    for triple in list(merged.triples((None, RDFS.range, XSD.date))):
        merged.remove(triple)
        merged.add((triple[0], triple[1], XSD.dateTime))
        patched += 1

    workdir = Path(tempfile.mkdtemp(prefix="sigevs-validate-"))
    previous = os.getcwd()
    try:
        os.chdir(workdir)
        merged_file = workdir / "sigevs-merged.owl"
        merged.serialize(merged_file, format="xml")

        onto = get_ontology(merged_file.name).load()
        buffer = io.StringIO()
        consistent = True
        with contextlib.redirect_stdout(buffer), contextlib.redirect_stderr(buffer):
            logging.getLogger("owlready2").setLevel(logging.ERROR)
            try:
                with onto:
                    sync_reasoner_hermit(infer_property_values=False)
            except OwlReadyInconsistentOntologyError:
                consistent = False
        if not consistent and verbose:
            print(buffer.getvalue())
        unsat = sorted(cls.name for cls in onto.inconsistent_classes())
        return onto, consistent, unsat, patched, gufo_loaded
    except Exception as exc:  # noqa: BLE001
        print(f"[error] reasoning failed: {type(exc).__name__}: {exc}")
        return None, None, None, patched, gufo_loaded
    finally:
        os.chdir(previous)
        with contextlib.suppress(Exception):
            shutil.rmtree(workdir)


def instances_of(onto, class_name: str):
    if onto is None:
        return []
    cls = None
    for candidate in onto.classes():
        if candidate.name == class_name:
            cls = candidate
            break
    if cls is None:
        return []
    return sorted(individual.name for individual in cls.instances())


def negative_test(populated: Graph, gufo_path, gufo_url: str):
    """Close the cycle while leaving one property unvisited; HermiT must detect it.

    AX-SEQ-02/AX-SEQ-03 encode 'a cycle is closed only when all of its
    properties are visited'. Under the open-world semantics of OWL, the
    universal restriction cannot *infer* area completion, but it must detect a
    contradiction when a cycle is asserted as closed while a property inside it
    is explicitly not visited.
    """
    broken = Graph()
    for triple in populated:
        broken.add(triple)
    for triple in list(broken.triples((EX.PIA2, SIGEVS.visitaConcluida, None))):
        broken.remove(triple)
    broken.add((EX.PIA2, SIGEVS.visitaConcluida, Literal(False)))

    _, consistent, _, _, _ = reason(broken, gufo_path, gufo_url, verbose=False)
    return consistent


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SIGEVS-O: populate, reason and query.")
    parser.add_argument("--ontology", type=Path, default=DEFAULT_ONTOLOGY, help="Path to SIGEVS-O-complete.ttl")
    parser.add_argument("--gufo", type=Path, default=None, help="Optional local copy of gufo.ttl")
    parser.add_argument("--gufo-url", default=GUFO_TTL_URL, help="URL used to fetch gUFO when --gufo is not given")
    parser.add_argument("--save-populated", type=Path, default=None, help="Write the populated ontology (Turtle)")
    args = parser.parse_args()

    failures = []

    print("=" * 72)
    print("SIGEVS-O validation: populate -> reason -> SPARQL")
    print("=" * 72)

    ontology_path = args.ontology if args.ontology.is_absolute() else (Path.cwd() / args.ontology)
    if not ontology_path.exists():
        print(f"[error] ontology not found: {ontology_path}")
        return 1

    graph = load_ontology(ontology_path)
    print(f"\n[1/3] Ontology loaded: {ontology_path}")
    print(f"      triples: {len(graph)}")

    populated = populate(graph)
    print(f"\n[2/3] ABox populated with the sample outbreak scenario")
    print(f"      triples with individuals: {len(populated)}")
    if args.save_populated:
        populated.serialize(args.save_populated, format="turtle")
        print(f"      populated ontology saved to: {args.save_populated}")

    onto, consistent, unsat, patched, gufo_loaded = reason(populated, args.gufo, args.gufo_url)
    print(f"\n[3/3] HermiT reasoning")
    print(f"      gUFO axioms: {'loaded' if gufo_loaded else 'NOT loaded (domain-only check)'}")
    if patched:
        print(f"      note: {patched} gUFO xsd:date range(s) adapted for HermiT (OWL 2 datatype map)")
    if consistent is None:
        failures.append("reasoning did not complete")
        print("      result: FAILED TO RUN")
    elif not consistent:
        failures.append("ontology is inconsistent")
        print("      result: INCONSISTENT")
    else:
        print("      result: CONSISTENT")
        print(f"      unsatisfiable classes: {len(unsat)} {unsat}")
        if unsat:
            failures.append("unsatisfiable classes detected")

    if onto is not None:
        print("\n      Inference checks (defined classes):")
        expected = {
            "PropriedadeVisitada": {"PIA1", "PIA2", "PIA3"},
            "CicloFechado": {"Ciclo1"},
        }
        for class_name, wanted in expected.items():
            found = set(instances_of(onto, class_name))
            ok = wanted <= found
            status = "ok" if ok else "FAIL"
            print(f"        {class_name:<20} instances={sorted(found)} [{status}]")
            if not ok:
                failures.append(f"{class_name}: expected {sorted(wanted)}, found {sorted(found)}")
        print("        note: AreaConcluida uses a universal restriction ('all properties")
        print("              visited'), which cannot be inferred under open-world semantics;")
        print("              AX-SEQ-02/03 are validated by the negative test below.")

    print("\n      Negative test (AX-SEQ-02/03 constraint):")
    broken_consistent = negative_test(populated, args.gufo, args.gufo_url)
    if broken_consistent is None:
        failures.append("negative test did not complete")
        print("        result: FAILED TO RUN")
    elif broken_consistent:
        failures.append("negative test: inconsistent scenario was NOT detected")
        print("        result: FAIL (closed cycle with an unvisited property was accepted)")
    else:
        print("        result: ok (inconsistency correctly detected when a closed cycle")
        print("              contains a property with visitaConcluida=false)")

    print("\n" + "=" * 72)
    print("SPARQL competency questions")
    print("=" * 72)

    rows = [(short(row.estabelecimento), str(row.nome)) for row in populated.query(CQ_CORE_01)]
    print("\nCQ-CORE-01: Which establishments are registered?")
    print_table(["Establishment", "Name"], rows)
    if not rows:
        failures.append("CQ-CORE-01 returned no rows")

    print("\nCQ-INV-01: Which establishments fall within each risk zone? (haversine filter)")
    zone_results = {}
    for row in populated.query(CQ_INV_01):
        target_point = parse_wkt_point(str(row.alvoCoord))
        property_point = parse_wkt_point(str(row.coord))
        distance = haversine_km(target_point, property_point)
        radius = float(row.raio)
        if distance <= radius:
            zone_results.setdefault(str(row.tipo), []).append((str(row.nome), round(distance, 2)))
    for zone_type in sorted(zone_results):
        print(f"      zone {zone_type}:")
        for name, distance in sorted(zone_results[zone_type]):
            print(f"        - {name} ({distance} km)")
    if "INFECTED" not in zone_results:
        failures.append("CQ-INV-01 found no establishments in the INFECTED zone")

    rows = [
        (short(row.nomeEquipe), short(row.membro), str(row.nomeMembro))
        for row in populated.query(CQ_RES_03)
    ]
    print("\nCQ-RES-03: Who are the members of each field team?")
    print_table(["Team", "Member", "Name"], rows)
    if not rows:
        failures.append("CQ-RES-03 returned no rows")

    rows = [(short(row.propriedadeTemporaria), str(row.contato)) for row in populated.query(CQ_CAM_04)]
    print("\nCQ-CAM-04: Which temporary properties were identified?")
    print_table(["Temporary property", "Contact"], rows)
    if not rows:
        failures.append("CQ-CAM-04 returned no rows")

    print("\n" + "=" * 72)
    if failures:
        print("RESULT: FAILED")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print("RESULT: ALL CHECKS PASSED")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
