#!/usr/bin/env python3
"""
SIGEVS-O — AX-SEQ-06 (collection time window) check.

AX-SEQ-06: the collection timestamp (``dataHoraColeta``) of a property
submission must lie within the time window [``dataInicioZona``,
``dataFimZona``] of the zone per cycle (``ZonaPorCiclo``) that contains the
operational area of the property in area. A zone without an end date is open.

Date comparison is outside OWL 2 DL, so the rule is enforced by the service
layer (``SubmissionService.validateZoneStatus`` in the SIGEVS API) and checked
here with SPARQL over the competency-question scenario:

1. the valid scenario (from ``validate_cqs.py``) has no submission outside its
   zone window;
2. adding a submission dated after the end of its zone window makes the query
   flag exactly that submission (negative test).

It also checks that the state flags of the events agree with their end
instants (inicio*/fim* properties): a closed cycle has ``fimCiclo``; an active
analysis has no ``encerradaEm``; an active response has no ``fimResposta``.
The state of an event is thus derivable from its temporal extent; the boolean
flags mirror the implementation.

Exit code 0 when all checks pass, 1 otherwise.
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    from rdflib import Graph
except ImportError:  # pragma: no cover
    print("rdflib is required: pip install rdflib")
    sys.exit(2)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_cqs import DEFAULT_ONTOLOGY, SAMPLE_ABOX  # noqa: E402

OUTSIDE_WINDOW = """
PREFIX sigevs: <https://sigevs.ontologies#>
SELECT ?sub ?coleta ?inicio ?fim WHERE {
  ?sub a sigevs:SubmissaoPropriedade ;
       sigevs:dataHoraColeta ?coleta ;
       sigevs:VinculadaA ?pia .
  ?pia sigevs:contidaEmArea ?area .
  ?area sigevs:PertenceA ?zona .
  ?zona sigevs:dataInicioZona ?inicio .
  OPTIONAL { ?zona sigevs:dataFimZona ?fim }
  BIND(SUBSTR(STR(?coleta), 1, 10) AS ?dia)
  FILTER(?dia < SUBSTR(STR(?inicio), 1, 10)
         || (BOUND(?fim) && ?dia > SUBSTR(STR(?fim), 1, 10)))
}
"""

LATE_SUBMISSION = """
@prefix ex: <http://example.org/sigevs-sample#> .
@prefix sigevs: <https://sigevs.ontologies#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
ex:SubForaJanela a sigevs:SubmissaoPropriedade ;
    sigevs:uuidSubmissao "sub-late-0001" ;
    sigevs:dataHoraColeta "2025-05-19T09:00:00"^^xsd:dateTime ;
    sigevs:VinculadaA ex:PIA2 ;
    sigevs:RealizadaPor ex:EquipeA .
"""


_P = "PREFIX sigevs: <https://sigevs.ontologies#> "
EVENT_STATE_QUERIES = {
    "closed cycle <=> fimCiclo": _P + """
        SELECT ?c WHERE { ?c a sigevs:CicloVigilancia ; sigevs:cicloFechado ?f .
          OPTIONAL { ?c sigevs:fimCiclo ?fim }
          FILTER((?f = true && !BOUND(?fim)) || (?f = false && BOUND(?fim))) }""",
    "active analysis <=> no encerradaEm": _P + """
        SELECT ?a WHERE { ?a a sigevs:AnaliseSanitaria ; sigevs:analiseAtiva ?at .
          OPTIONAL { ?a sigevs:encerradaEm ?fim }
          FILTER((?at = true && BOUND(?fim)) || (?at = false && !BOUND(?fim))) }""",
    "active response <=> no fimResposta": _P + """
        SELECT ?r WHERE { ?r a sigevs:RespostaSanitaria ; sigevs:respostaAtiva ?at .
          OPTIONAL { ?r sigevs:fimResposta ?fim }
          FILTER((?at = true && BOUND(?fim)) || (?at = false && !BOUND(?fim))) }""",
}


def flagged(g: Graph) -> set[str]:
    return {str(r.sub).rsplit("#", 1)[-1] for r in g.query(OUTSIDE_WINDOW)}


def main() -> int:
    g = Graph()
    g.parse(str(DEFAULT_ONTOLOGY), format="turtle")
    g.parse(data=SAMPLE_ABOX, format="turtle")
    print("=" * 72)
    print("SIGEVS-O AX-SEQ-06 time-window check")
    print("=" * 72)
    failures = []

    declared = any(True for _ in g.query(
        "PREFIX sigevs: <https://sigevs.ontologies#> PREFIX owl: <http://www.w3.org/2002/07/owl#> "
        "ASK { sigevs:dataHoraColeta a owl:DatatypeProperty }"))
    print(f"  dataHoraColeta declared as datatype property      [{'ok' if declared else 'FAIL'}]")
    if not declared:
        failures.append("dataHoraColeta not declared")

    valid = flagged(g)
    ok = not valid
    print(f"  valid scenario: submissions outside window = {sorted(valid) or 'none'}  [{'ok' if ok else 'FAIL'}]")
    if not ok:
        failures.append(f"valid scenario flagged {sorted(valid)}")

    g.parse(data=LATE_SUBMISSION, format="turtle")
    late = flagged(g)
    ok = late == {"SubForaJanela"}
    print(f"  negative test: flagged = {sorted(late)}  [{'ok' if ok else 'FAIL'}]")
    if not ok:
        failures.append(f"negative test flagged {sorted(late)}")

    # Event temporal state: the state flags must agree with the end instants
    # (a closed cycle has fimCiclo; an active analysis/response has no end).
    for label, query in EVENT_STATE_QUERIES.items():
        bad = sorted(str(r[0]).rsplit("#", 1)[-1] for r in g.query(query))
        ok = not bad
        print(f"  {label:<48} [{'ok' if ok else 'FAIL'}]{'' if ok else ' ' + str(bad)}")
        if not ok:
            failures.append(f"{label}: {bad}")

    print("=" * 72)
    if failures:
        print("RESULT: FAILED")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("RESULT: AX-SEQ-06 AND EVENT STATE CHECKS PASSED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
