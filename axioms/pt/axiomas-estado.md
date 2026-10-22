# Axiomas — Estado (Lifecycle)

| ID | Axioma | Descrição | Fonte |
|----|--------|-----------|-------|
| AX-STATE-01 | Uma Análise Sanitária pode estar ativa ou inativa | `isActive` booleano | `SanitaryAnalysis.isActive` |
| AX-STATE-02 | Uma Resposta Sanitária pode estar ativa, concluída ou removida (soft delete) | `isActive` + `completed` booleanos | `SanitaryEventResponse.isActive`, `.completed` |
| AX-STATE-03 | Uma Zona de Ciclo pode estar aberta ou fechada | `closed` booleano NOT NULL | `SurveillanceCycleZone.closed` |
| AX-STATE-04 | Uma Propriedade em Área pode estar completa ou pendente | `completed` booleano | `AreaPremise.isCompleted` |
| AX-STATE-05 | Um Usuário Convocado pode estar com status de quarentena (`dirty`) ativo ou não, com data de expiração | `isDirty` + `dirtyUntil` | `ResponseConvokedUsers.isDirty`, `.dirtyUntil` |
| AX-STATE-06 | Um Usuário Convocado pode ter permissão de gestão e/ou observação | Permissões independentes | `ResponseConvokedUsers.isManagement`, `.isObserver` |
