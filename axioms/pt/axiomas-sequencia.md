# Axiomas — Sequência e Temporalidade

| ID | Axioma | Descrição | Fonte |
|----|--------|-----------|-------|
| AX-SEQ-01 | Os ciclos de vigilância seguem uma ordenação sequencial dentro de uma resposta | `cycle_number` é sequencial e único por resposta | `UNIQUE(cycle_number, response_id)` |
| AX-SEQ-02 | Um ciclo só pode ser fechado quando todas as suas áreas operacionais estiverem concluídas | Regra de negócio validada no Service | `EventActionsService` / `ResponseSurveillanceCycleService` |
| AX-SEQ-03 | Uma área operacional é concluída quando todas as suas propriedades são visitadas | `completed` em área deriva de `isCompleted` nas propriedades | `EventActionsService.POST /visit/{id}/complete` |
| AX-SEQ-04 | Uma propriedade em área pode ser reaberta após concluída | Transição de estado permitida | `EventActionsService.POST /visit/{id}/reopen` |
| AX-SEQ-05 | O rastreamento GPS de equipe tem início (`createdAt`) e fim (`endTime`) opcional | Tracking é um evento contínuo no tempo | `TeamTracking.createdAt + endTime` |
