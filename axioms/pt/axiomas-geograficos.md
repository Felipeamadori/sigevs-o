# Axiomas — Geográficos

| ID | Axioma | Descrição | Fonte |
|----|--------|-----------|-------|
| AX-GEO-01 | Um alvo de investigação possui até três zonas concêntricas (Perifoco, Vigilância, Proteção); o tipo INVESTIGATION é um mecanismo de API, fora do modelo conceitual | zone1 (INFECTED), zone2 (BUFFER), zone3 (SURVEILLANCE) em AnalysisTarget | `AnalysisTarget.zone1/2/3` + `ZoneType` enum |
| AX-GEO-02 | As coordenadas de estabelecimentos, alvos e barreiras são armazenadas como `GEOGRAPHY` (PostGIS) | Suporte a cálculos geoespaciais | Colunas `coord GEOGRAPHY` nas tabelas |
