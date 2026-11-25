# Axiomas — Estado (Lifecycle)

| ID | Axioma | Descrição | Fonte |
|----|--------|-----------|-------|
| AX-ATTR-01 | Uma Análise Sanitária pode estar ativa ou inativa | `isActive` booleano | `SanitaryAnalysis.isActive` |
| AX-ATTR-02 | Uma Resposta Sanitária pode estar ativa, concluída ou removida (soft delete) | `isActive` + `completed` booleanos | `SanitaryEventResponse.isActive`, `.completed` |
| AX-ATTR-03 | Uma Zona de Ciclo pode estar aberta ou fechada | `closed` booleano NOT NULL | `SurveillanceCycleZone.closed` |
| AX-ATTR-04 | Uma Propriedade em Área pode estar completa ou pendente | `completed` booleano | `AreaPremise.isCompleted` |
| AX-STATE-01 | Um Usuário Convocado pode estar com status de quarentena (`dirty`) ativo ou não, com data de expiração | `isDirty` + `dirtyUntil` | `ResponseConvokedUsers.isDirty`, `.dirtyUntil` |
| AX-STATE-02 | Um Usuário Convocado pode ter permissão de gestão e/ou observação | Permissões independentes | `ResponseConvokedUsers.isManagement`, `.isObserver` |


> Nota: `AX-ATTR-*` são cardinalidades de atributos do estado persistido (nível de implementação), não axiomas do modelo conceitual; os axiomas de estado do modelo são `AX-STATE-01` (quarentena) e `AX-STATE-02` (permissões).
