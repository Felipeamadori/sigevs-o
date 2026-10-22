# Questões de Competência — Subdomínio Resposta Sanitária

| ID | Questão de Competência | Caminho no Modelo | Implementação |
|----|----------------------|--------------------|---------------|
| CQ-RES-01 | Quantos ciclos de vigilância foram executados em uma resposta sanitária? | `SanitaryResponse` → `SurveillanceCycle` | JPA/SPARQL |
| CQ-RES-02 | Quais equipes estão alocadas em cada ciclo de vigilância? | `SurveillanceCycle` → `FieldTeam` | JPA query |
| CQ-RES-03 | Quais profissionais compõem cada equipe e qual sua função? | `FieldTeam` → `TeamMember` → `Person` | JPA/SPARQL |
| CQ-RES-04 | Quais barreiras sanitárias estão ativas em cada ciclo? | `SanitaryBarrier` → `SurveillanceCycle` (many-to-many) | Análise estrutural |
| CQ-RES-05 | Quais zonas (Perifoco, Vigilância, Proteção) estão abertas em cada ciclo? | `ControlZone` → `SurveillanceCycle` (nova zona por ciclo) | Análise estrutural |
| CQ-RES-06 | Qual o histórico de rastreamento GPS de cada equipe? | `GPSTracking` → `FieldTeam` → `TeamMember` → filtro por data | JPA query |
| CQ-RES-07 | Quais equipes estão ativas em cada ciclo? | `FieldTeam` → `SurveillanceCycle` (equipe pertence a um ciclo por vez) | Análise estrutural |
| CQ-RES-08 | Quais áreas operacionais foram delimitadas para cada equipe? | `OperationalArea` → `FieldTeam` + `SurveillanceCycle` | JPA/SPARQL |
| CQ-RES-09 | Uma resposta sanitária possui barreiras em todas as zonas? | `SanitaryBarrier` → `SanitaryResponse` | JPA query |
| CQ-RES-10 | Quais propriedades estão atribuídas a cada área operacional? | `OperationalArea` → `PropertyInArea` → `Establishment` | JPA/SPARQL |
| CQ-RES-11 | Quais barreiras são fixas e quais são móveis? | `SanitaryBarrier` → `type` + `function` | JPA query |
| CQ-RES-12 | Quais veículos estão alocados a cada equipe? | `FieldTeam` → `Vehicle` | JPA query |
| CQ-RES-13 | Onde está localizado o posto de comando da resposta? | `SanitaryResponse` → `CommandPost` | JPA/SPARQL |
| CQ-RES-14 | Quais profissionais foram convocados para a resposta e qual sua função? | `SanitaryResponse` → `SummonedPerson` → `isDirty` + `dirtyUntil` | JPA query |
