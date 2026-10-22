# SPARQL Queries

Verified SPARQL queries for representative competency questions.

## Queries

| File | CQ | Description |
|------|----|-------------|
| `cq-core-01.rq` | CQ-CORE-01 | Registered establishments |
| `cq-inv-01.rq` | CQ-INV-01 | Properties within risk zone (GeoSPARQL) |
| `cq-res-03.rq` | CQ-RES-03 | Field team members |
| `cq-cam-04.rq` | CQ-CAM-04 | Temporary properties |

## How to Execute

### In Protégé

1. Open `SIGEVS-O-complete.ttl` in Protégé
2. Go to **Window → Tabs → SPARQL Query**
3. Paste the query content
4. Click **Execute**

### In a Triple Store

```bash
curl -H "Accept: application/sparql-results+json" \
     --data-urlencode query@cq-core-01.rq \
     http://localhost:3030/sigevs/query
```

## Notes

- `cq-inv-01.rq` uses GeoSPARQL functions (`geof:distance`)
- Production system uses PostGIS (`ST_DWithin`) instead of OWL reasoner
