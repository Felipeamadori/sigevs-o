# Axiomas — Dependência

| ID | Axioma | Descrição | Fonte |
|----|--------|-----------|-------|
| AX-DEP-01 | Um Ciclo de Vigilância pertence exclusivamente a uma Resposta Sanitária | Não existe ciclo sem resposta | `FOREIGN KEY (response_id)` → `sanitary_event_response` |
| AX-DEP-02 | Uma Equipe de Campo pertence exclusivamente a um Ciclo de Vigilância | Equipe não existe sem ciclo | `FOREIGN KEY (surveillance_cycle_id)` → `response_surveillance_cycle` |
| AX-DEP-03 | Uma Área Operacional pertence a uma Equipe e a uma Zona de Ciclo | Dependência dupla de equipe e zona | `FOREIGN KEY (team_id, cycle_zone_id)` em `response_areas` |
| AX-DEP-04 | Uma Propriedade em Área pertence a uma Área Operacional | Não existe propriedade em área sem área | `FOREIGN KEY (area_id)` → `response_areas` |
| AX-DEP-05 | Uma Submissão de Propriedade vincula-se a uma Propriedade em Área e a uma Equipe | Toda submissão tem área + equipe | `FOREIGN KEY (area_premise_id, team_id)` em `premise_submissions` |
| AX-DEP-06 | Uma Submissão de Barreira vincula-se a uma Barreira Sanitária | Toda submissão de barreira tem barreira | `FOREIGN KEY (barrier_id)` → `response_barriers` |
| AX-DEP-07 | Um Alvo de Investigação depende de uma Análise Sanitária | Não existe alvo sem análise | `FOREIGN KEY (analysis_id)` em `analysis_targets` |
| AX-DEP-08 | Uma Resposta Sanitária depende de uma Análise Sanitária | Resposta só existe vinculada a uma investigação | `FOREIGN KEY (analysis_id)` → `sanitary_analysis` |
| AX-DEP-09 | Um Posto de Comando está vinculado a no máximo uma Resposta Sanitária (e vice-versa) | Relação 1:1 entre Resposta e Posto de Comando | `OneToOne response_command_post → response_id FK UNIQUE` |
