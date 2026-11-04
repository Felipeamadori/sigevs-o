# SPARQL Queries

Executable SPARQL queries for representative competency questions.

## Queries

| File | CQ | Description |
|------|----|-------------|
| `cq-core-01.rq` | CQ-CORE-01 | Registered establishments |
| `cq-inv-01.rq` | CQ-INV-01 | Properties within the risk zone (spatial query) |
| `cq-res-03.rq` | CQ-RES-03 | Field team members |
| `cq-cam-04.rq` | CQ-CAM-04 | Temporary properties |

The queries use the ontology IRIs (Portuguese local names); the ontology attaches English labels through `rdfs:label`.

## Sample data

The ontology file contains the TBox only. The queries are meant to be executed against the sample outbreak-response scenario (ABox) used in the paper. The merged ontology + ABox is available in `../ontology/SIGEVS-O-populated.ttl` and can be regenerated with:

```bash
python scripts/validate_ontology.py --save-populated ontology/SIGEVS-O-populated.ttl
```

## How to Execute

### Apache Jena

```bash
arq --data ontology/SIGEVS-O-populated.ttl \
    --query sparql/cq-core-01.rq
```

The three non-spatial queries run with standard SPARQL 1.1. `cq-inv-01.rq` requires GeoSPARQL support: with Apache Jena, add `jena-geosparql` and its dependencies to the classpath (when using the Java API, call `GeoSPARQLConfig.setupMemoryIndex()` before executing the query).

Jena does not convert angular coordinates (degrees) to linear units in `geof:distance`, so `cq-inv-01.rq` uses Jena's `spatialF:distance`, which selects the great-circle distance for geographic coordinates. On an engine with full GeoSPARQL 1.1 support (e.g., RDF4J or GraphDB), replace it with the standard call:

```sparql
FILTER(geof:distance(?alvoGeom, ?propGeom, uom:kilometre) <= ?raio)
```

### Protégé

1. Open `ontology/SIGEVS-O-populated.ttl`.
2. Load the gUFO vocabulary: [https://purl.org/nemo/gufo](https://purl.org/nemo/gufo).
3. Run `cq-core-01.rq`, `cq-res-03.rq` and `cq-cam-04.rq` in the **SPARQL Query** tab.

Protégé's SPARQL tab does not provide GeoSPARQL functions, so `cq-inv-01.rq` must be executed in a GeoSPARQL-enabled engine.

### Triple store

```bash
curl -H "Accept: application/sparql-results+json" \
     --data-urlencode query@sparql/cq-core-01.rq \
     http://localhost:3030/sigevs/query
```

## Verification

The queries were executed against `SIGEVS-O-populated.ttl` and returned:

| Query | Result |
|-------|--------|
| `cq-core-01.rq` | 4 establishments |
| `cq-inv-01.rq` | 2 establishments in the INFECTED zone (Granja Sao Joao and Sitio Boa Vista) |
| `cq-res-03.rq` | 3 field-team members |
| `cq-cam-04.rq` | 1 temporary property |

`cq-inv-01.rq` was verified with Apache Jena 5.6.0; the other queries were verified with Apache Jena and rdflib.
