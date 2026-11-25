# -*- coding: utf-8 -*-
"""Métricas estilo Protégé para uma ontologia OWL/Turtle.

Classifica cada tripla em:
  - axioma lógico        (SubClassOf, EquivalentClasses, DisjointClasses,
                          InverseProperties, Domain/Range, HasKey, Chain, etc.)
  - axioma de declaração (Declaration de Class/ObjectProperty/DatatypeProperty/
                          NamedIndividual/AnnotationProperty)
  - asserção de anotação (rdfs:label, rdfs:comment, owl:versionInfo, etc.)
  - diretivas de ontologia (imports — não contadas como axioma)

Uso:  python metrics_protege.py [arquivo.ttl]
      python metrics_protege.py --git <revisao> [arquivo.ttl]
"""
import io, os, sys
from rdflib import Graph, Namespace, URIRef, BNode, RDF, RDFS, OWL

OWL = Namespace("http://www.w3.org/2002/07/owl#")

ANNOTATION_PREDS = {RDFS.label, RDFS.comment, OWL.versionInfo, RDFS.seeAlso,
                    OWL.backwardCompatibleWith, OWL.incompatibleWith,
                    OWL.priorVersion, OWL.creator, OWL.created, OWL.modified}

DECL_TYPES = {OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty,
              OWL.AnnotationProperty, OWL.NamedIndividual}

LOGICAL_PREDS = {RDFS.subClassOf, OWL.equivalentClass, OWL.disjointWith,
                 RDFS.domain, RDFS.range, OWL.inverseOf, OWL.hasKey,
                 OWL.propertyChainAxiom, OWL.unionOf, OWL.intersectionOf,
                 OWL.oneOf, OWL.disjointUnionOf, OWL.transitiveOver}


def contar(caminho):
    g = Graph()
    g.parse(caminho, format="turtle")
    # classes declaradas (para identificar ClassAssertions)
    classes = {s for s in g.subjects(RDF.type, OWL.Class)}
    logicos = declaracoes = anotacoes = diretivas = 0
    detalhe = {}
    for s, p, o in g:
        if p == RDF.type and o in DECL_TYPES:
            declaracoes += 1
            detalhe["decl"] = detalhe.get("decl", 0) + 1
        elif p == RDF.type and o in classes:
            # ClassAssertion: axioma lógico (indivíduo instanciando classe)
            logicos += 1
            detalhe["classAssertion"] = detalhe.get("classAssertion", 0) + 1
        elif p == RDF.type and not isinstance(s, BNode):
            # punning/typagem gUFO (ex.: :X a gufo:Kind) — ClassAssertion lógica
            logicos += 1
            detalhe["classAssertion(gufo)"] = detalhe.get("classAssertion(gufo)", 0) + 1
        elif p in ANNOTATION_PREDS and not isinstance(s, BNode):
            anotacoes += 1
        elif p in LOGICAL_PREDS:
            # oneOf/unionOf/intersectionOf dentro de bnode são parte da
            # expressão do axioma que os contém (equivalentClass/subClassOf)
            if p in {OWL.oneOf, OWL.unionOf, OWL.intersectionOf} and isinstance(s, BNode):
                continue  # contabilizados junto com o axioma que referencia o bnode
            logicos += 1
            k = str(p).split("#")[-1]
            detalhe[k] = detalhe.get(k, 0) + 1
        elif p == OWL.imports:
            diretivas += 1
        elif p == RDF.type and o == OWL.Ontology:
            pass  # declaração do cabeçalho da ontologia (não conta)
        elif p == RDF.type and o == OWL.Restriction:
            pass  # expressão anônima: parte do axioma que a referencia
        elif isinstance(s, BNode) or isinstance(o, BNode) and p != RDF.type:
            # triplas de expressões anônimas (restrições): parte do axioma pai
            pass
        else:
            # qualquer outra: conta como anotação desconhecida
            anotacoes += 1
            detalhe["OUTRA:" + str(p).split("#")[-1]] = detalhe.get("OUTRA:" + str(p).split("#")[-1], 0) + 1
    return logicos, declaracoes, anotacoes, diretivas, detalhe


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--git":
        import subprocess
        rev = args[1]
        arquivo = args[2] if len(args) > 2 else "ontology/SIGEVS-O-complete.ttl"
        conteudo = subprocess.run(
            ["git", "-C", r"E:\Projetos\sigevs-o", "show", f"{rev}:{arquivo}"],
            capture_output=True).stdout.decode("utf-8")
        caminho = os.path.abspath("_metricas_tmp.ttl")
        open(caminho, "w", encoding="utf-8", newline="").write(conteudo)
    else:
        caminho = args[0] if args else "ontology/SIGEVS-O-complete.ttl"
    if not os.path.isabs(caminho):
        caminho = os.path.abspath(os.path.join(r"E:\Projetos\sigevs-o", caminho))
    classes_declaradas = {s for s, _, o in g_triples(caminho) if _ is None} if False else None
    l, d, a, i, det = contar(caminho)
    print(f"Arquivo: {caminho}")
    print(f"  Axiomas lógicos:        {l}")
    print(f"  Axiomas de declaração:  {d}")
    print(f"  Asserções de anotação:  {a}")
    print(f"  Diretivas (imports):    {i}")
    print(f"  TOTAL (lógico+decl+anot): {l + d + a}")
    print("  Detalhe lógico:", {k: v for k, v in sorted(det.items())})
