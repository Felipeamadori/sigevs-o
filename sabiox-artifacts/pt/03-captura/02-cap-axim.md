# Fase de Captura — CAP-AXIM (Identificação de Axiomas)

---

## Axiomas da Ontologia SIGEVS-O

Os axiomas representam **restrições** e **regras de inferência** do domínio que o modelo conceitual não consegue capturar apenas com relacionamentos e cardinalidades. Estão organizados em: **Axiomas de Identidade**, **Axiomas de Dependência**, **Axiomas de Sequência/Temporalidade** e **Axiomas de Cardinalidade**.

---

## 1. Axiomas de Identidade

| ID | Axioma | Descrição | Fonte |
|----|--------|-----------|-------|
| AX-ID-01 | `codigoEstabelecimento` é único globalmente | Todo Estabelecimento possui um código SDA único que o identifica perante o SVO | `UNIQUE(codigo_estabelecimento)` em `cadastros.estabelecimento` |
| AX-ID-02 | Todo estabelecimento com `tipo = "Frigorífico"` possui um registro em `Frigorifico` | A existência de Frigorifico depende da existência de um Estabelecimento com essa classificação | `Frigorifico.id_estabelecimento FK` |
| AX-ID-03 | Uma Pessoa é identificada por `keycloak_subject_id` e alternativamente por `cpf` e `email` | Identidades únicas nas três dimensões (Keycloak, CPF, email) | `UNIQUE(keycloak_subject_id, cpf, email)` em `cadastros.usuario` |
| AX-ID-04 | Uma movimentação animal é identificada pela tripla `(serie, numero, uf_origem)` | Cada GTA é única por série-número-UF de origem | `PK(serie, numero, uf_origem)` nas tabelas `movimentacao.*` |

---

## 2. Axiomas de Dependência

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

---

## 3. Axiomas de Sequência e Temporalidade

| ID | Axioma | Descrição | Fonte |
|----|--------|-----------|-------|
| AX-SEQ-01 | Os ciclos de vigilância seguem uma ordenação sequencial dentro de uma resposta | `cycle_number` é sequencial e único por resposta | `UNIQUE(cycle_number, response_id)` |
| AX-SEQ-02 | Um ciclo só pode ser fechado quando todas as suas áreas operacionais estiverem concluídas | Regra de negócio validada no Service | `EventActionsService` / `ResponseSurveillanceCycleService` |
| AX-SEQ-03 | Uma área operacional é concluída quando todas as suas propriedades são visitadas | `completed` em área deriva de `isCompleted` nas propriedades | `EventActionsService.POST /visit/{id}/complete` |
| AX-SEQ-04 | Uma propriedade em área pode ser reaberta após concluída | Transição de estado permitida | `EventActionsService.POST /visit/{id}/reopen` |
| AX-SEQ-05 | O rastreamento GPS de equipe tem início (`createdAt`) e fim (`endTime`) opcional | Tracking é um evento contínuo no tempo | `TeamTracking.createdAt + endTime` |

---

## 4. Axiomas de Cardinalidade e Unicidade

| ID | Axioma | Descrição | Fonte |
|----|--------|-----------|-------|
| AX-CARD-01 | Um usuário só pode ser convocado uma única vez para uma mesma resposta | Um profissional não pode ser duplicado na convocação | `UNIQUE(user_id, response_id)` em `response_convoked_users` |
| AX-CARD-02 | Um estabelecimento pode ser alvo de múltiplas investigações simultaneamente | Não há restrição de unicidade entre análise e estabelecimento | Ausência de UNIQUE(analysis_id, premise_id) |
| AX-CARD-03 | Uma equipe pode ter múltiplos membros | Cardinalidade 1:N entre Team e TeamMember | `@OneToMany team → team_members` |
| AX-CARD-04 | Um estabelecimento pode estar em múltiplas áreas operacionais (em diferentes respostas) | Sem restrição de unicidade premise_id + response_id em area_premises | Análise de ausência de constraint |
| AX-CARD-05 | Uma análise sanitária pode ter múltiplos alvos | Cardinalidade 1:N entre SanitaryAnalysis e AnalysisTarget | `@OneToMany(cascade=ALL, orphanRemoval=true)` |

---

## 5. Axiomas de Estado (Lifecycle)

| ID | Axioma | Descrição | Fonte |
|----|--------|-----------|-------|
| AX-STATE-01 | Uma Análise Sanitária pode estar ativa ou inativa | `isActive` booleano | `SanitaryAnalysis.isActive` |
| AX-STATE-02 | Uma Resposta Sanitária pode estar ativa, concluída ou removida (soft delete) | `isActive` + `completed` booleanos | `SanitaryEventResponse.isActive`, `.completed` |
| AX-STATE-03 | Uma Zona de Ciclo pode estar aberta ou fechada | `closed` booleano NOT NULL | `SurveillanceCycleZone.closed` |
| AX-STATE-04 | Uma Propriedade em Área pode estar completa ou pendente | `completed` booleano | `AreaPremise.isCompleted` |
| AX-STATE-05 | Um Usuário Convocado pode estar com status de quarentena (`dirty`) ativo ou não, com data de expiração | `isDirty` + `dirtyUntil` | `ResponseConvokedUsers.isDirty`, `.dirtyUntil` |
| AX-STATE-06 | Um Usuário Convocado pode ter permissão de gestão e/ou observação | Permissões independentes | `ResponseConvokedUsers.isManagement`, `.isObserver` |

---

## 6. Axiomas Geográficos

| ID | Axioma | Descrição | Fonte |
|----|--------|-----------|-------|
| AX-GEO-01 | Um alvo de investigação possui até 3 zonas concêntricas (Perifoco, Vigilância, Proteção) + opcionalmente Investigação | zone1 (INFECTED), zone2 (BUFFER), zone3 (SURVEILLANCE) em AnalysisTarget | `AnalysisTarget.zone1/2/3` + `ZoneType` enum |
| AX-GEO-02 | As coordenadas de estabelecimentos, alvos e barreiras são armazenadas como `GEOGRAPHY` (PostGIS) | Suporte a cálculos geoespaciais | Colunas `coord GEOGRAPHY` nas tabelas |

---



## Mapa: Axiomas × Subdomínios

| Subdomínio | Axiomas |
|------------|---------|
| Core | AX-ID-01, AX-ID-02, AX-ID-03 |
| Investigação Sanitária | AX-ID-04, AX-DEP-07, AX-DEP-08, AX-CARD-02, AX-CARD-05, AX-GEO-01, AX-GEO-02, AX-STATE-01 |
| Resposta Sanitária | AX-DEP-01, AX-DEP-02, AX-DEP-03, AX-DEP-04, AX-DEP-09, AX-SEQ-01, AX-SEQ-02, AX-SEQ-03, AX-SEQ-04, AX-CARD-01, AX-CARD-03, AX-STATE-02, AX-STATE-03, AX-STATE-05, AX-STATE-06 |
| Ações em Campo | AX-DEP-05, AX-DEP-06, AX-SEQ-03, AX-SEQ-04, AX-STATE-04 |

---

## Referências

- Código fonte: entidades JPA, migrations Flyway, services
- Documento `Funcionalidades SIGEVS.md`
- Catálogo de Conceitos (CAP-CATA): `01-cap-cata.md`
