# Axiomas — Geográficos

| ID | Axioma | Descrição | Fonte |
|----|--------|-----------|-------|
| AX-GEO-01 | Um alvo de investigação possui até 3 zonas concêntricas (Perifoco, Vigilância, Proteção) + opcionalmente Investigação | zone1 (INFECTED), zone2 (BUFFER), zone3 (SURVEILLANCE) em AnalysisTarget | `AnalysisTarget.zone1/2/3` + `ZoneType` enum |
| AX-GEO-02 | As coordenadas de estabelecimentos, alvos e barreiras são armazenadas como `GEOGRAPHY` (PostGIS) | Suporte a cálculos geoespaciais | Colunas `coord GEOGRAPHY` nas tabelas |
