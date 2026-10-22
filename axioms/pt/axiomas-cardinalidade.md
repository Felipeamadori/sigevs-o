# Axiomas — Cardinalidade e Unicidade

| ID | Axioma | Descrição | Fonte |
|----|--------|-----------|-------|
| AX-CARD-01 | Um usuário só pode ser convocado uma única vez para uma mesma resposta | Um profissional não pode ser duplicado na convocação | `UNIQUE(user_id, response_id)` em `response_convoked_users` |
| AX-CARD-02 | Um estabelecimento pode ser alvo de múltiplas investigações simultaneamente | Não há restrição de unicidade entre análise e estabelecimento | Ausência de UNIQUE(analysis_id, premise_id) |
| AX-CARD-03 | Uma equipe pode ter múltiplos membros | Cardinalidade 1:N entre Team e TeamMember | `@OneToMany team → team_members` |
| AX-CARD-04 | Um estabelecimento pode estar em múltiplas áreas operacionais (em diferentes respostas) | Sem restrição de unicidade premise_id + response_id em area_premises | Análise de ausência de constraint |
| AX-CARD-05 | Uma análise sanitária pode ter múltiplos alvos | Cardinalidade 1:N entre SanitaryAnalysis e InvestigationTarget | `@OneToMany(cascade=ALL, orphanRemoval=true)` |
