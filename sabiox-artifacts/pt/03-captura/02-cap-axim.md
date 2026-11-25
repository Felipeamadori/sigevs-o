# Fase de Captura — CAP-AXIM (Identificação de Axiomas)

---

## Axiomas da Ontologia SIGEVS-O

Os axiomas representam **restrições** e **regras de inferência** do domínio, independentes de implementação. São **25 axiomas formais** em seis categorias. Não são axiomas: declarações de ausência de restrição (registradas como decisões de modelagem, MD-01/MD-02), cardinalidades de atributos do estado persistido (nível de implementação) e mecanismos técnicos — estes constam apenas da tabela de rastreabilidade.

---

## 1. Axiomas de Identidade (4)

| ID | Axioma | Descrição | Fonte / Formalização |
|----|--------|-----------|-------|
| AX-ID-01 | Todo Estabelecimento **cadastrado** (fase EstabelecimentoCadastrado) possui um código SDA único | Unidades não cadastradas (fase EstabelecimentoNaoCadastrado) não possuem código SDA e são identificadas pelo registro de campo | `owl:hasKey(codigoEstabelecimento)`; `UNIQUE(codigo_estabelecimento)` em `cadastros.estabelecimento` |
| AX-ID-02 | Uma Pessoa é identificada pelo CPF (e pelas credenciais de acesso no sistema) | Identidade do conceito vs. credencial do sistema | `owl:hasKey(cpf)`; `UNIQUE(cpf)` em `cadastros.usuario` |
| AX-ID-03 | Uma movimentação animal é identificada pelo documento GTA (série, número, UF de origem) | Cada GTA é única por série-número-UF de origem | `owl:hasKey(serie, numeroGTA, ufOrigem)`; `PK` nas tabelas `movimentacao.*` |
| AX-ID-04 | A existência de um Frigorífico pressupõe a existência de um Estabelecimento de abate classificado com um dos tipos de inspeção (SIF, SIE ou SIM) | Especialização decorrente da classificação | `rdfs:subClassOf`; coluna de especialização |

---

## 2. Axiomas de Dependência (9)

| ID | Axioma | Descrição | Fonte / Formalização |
|----|--------|-----------|-------|
| AX-DEP-01 | Um Ciclo de Vigilância pertence exclusivamente a uma Resposta Sanitária | Não existe ciclo sem resposta | `owl:cardinality 1` (cicloPertenceAResposta); `FOREIGN KEY (response_id)` |
| AX-DEP-02 | Uma Equipe de Campo pertence exclusivamente a um Ciclo de Vigilância | Equipe não existe sem ciclo | `owl:cardinality 1` (equipeAlocadaEm); `FOREIGN KEY (surveillance_cycle_id)` |
| AX-DEP-03 | Uma Área Operacional pertence a uma Equipe e a uma Zona por Ciclo | Dependência dupla de equipe e zona | `owl:cardinality 1` (areaDaEquipe, PertenceA); FKs em `response_areas` |
| AX-DEP-04 | Uma Propriedade em Área pertence a uma Área Operacional | Não existe propriedade em área sem área | `owl:cardinality 1` (contidaEmArea); `FOREIGN KEY (area_id)` |
| AX-DEP-05 | Uma Submissão de Propriedade vincula-se a uma Propriedade em Área e a uma Equipe | Toda submissão tem área + equipe | `owl:cardinality 1` (VinculadaA, RealizadaPor); FKs em `premise_submissions` |
| AX-DEP-06 | Uma Submissão de Barreira vincula-se a uma Barreira Sanitária | Toda submissão de barreira tem barreira | `owl:cardinality 1`; `FOREIGN KEY (barrier_id)` |
| AX-DEP-07 | Um Alvo de Investigação depende de uma Análise Sanitária | Não existe alvo sem análise | `owl:cardinality 1` (alvoDeAnalise); `FOREIGN KEY (analysis_id)` |
| AX-DEP-08 | Uma Resposta Sanitária depende de uma Análise Sanitária | Resposta só existe vinculada a uma investigação | `owl:cardinality 1` (BaseadaEm); `FOREIGN KEY (analysis_id)` |
| AX-DEP-09 | Um Posto de Comando está vinculado a no máximo uma Resposta Sanitária (e vice-versa) | Relação 1:1 entre Resposta e Posto de Comando | `owl:maxCardinality 1` (Tem, postoDaResposta); `OneToOne ... UNIQUE` |

---

## 3. Axiomas de Sequência e Temporalidade (6)

| ID | Axioma | Descrição | Fonte / Formalização |
|----|--------|-----------|-------|
| AX-SEQ-01 | Os ciclos de vigilância de uma resposta formam uma sequência total ordenada, sem lacunas nem repetições | Número do ciclo único por resposta | `owl:hasKey(numeroCiclo, cicloPertenceAResposta)`; `UNIQUE(cycle_number, response_id)` |
| AX-SEQ-02 | Um ciclo só pode ser fechado quando todas as suas áreas operacionais estiverem concluídas | `Closed Cycle` é classe definida por equivalência (ciclo fechado) com a restrição de fechamento como subsunção (todas as áreas concluídas); validada também no serviço | `owl:equivalentClass` + `owl:allValuesFrom AreaConcluida`; `EventActionsService` |
| AX-SEQ-03 | Uma área operacional está concluída quando todas as suas propriedades foram visitadas | Classe definida `Completed Area` | `owl:equivalentClass` (allValuesFrom + minCardinality 1) |
| AX-SEQ-04 | Uma propriedade em área concluída pode ser reaberta | Transição de estado permitida | `EventActionsService.POST /visit/{id}/reopen` (apenas natural/serviço) |
| AX-SEQ-05 | Todo rastreamento GPS possui um instante de início; o fim é opcional enquanto o evento está em curso | Evento contínuo no tempo | `owl:cardinality 1` (inicioRastreamento) + `owl:maxCardinality 1` (fimRastreamento) |
| AX-SEQ-06 | A coleta de uma Submissão de Propriedade só é aceita dentro da janela temporal da Zona por Ciclo que contém a área da propriedade | Janela [data de início, data de fim] da zona; zona sem data de fim está aberta | Serviço (`SubmissionService.validateZoneStatus`); `dataHoraColeta`, `dataInicioZona`, `dataFimZona`; verificado por `validate_time_window.py` (comparação de datas fora do OWL 2 DL) |

---

## 4. Axiomas de Cardinalidade e Unicidade (3)

| ID | Axioma | Descrição | Fonte / Formalização |
|----|--------|-----------|-------|
| AX-CARD-01 | Um profissional só pode ser convocado uma única vez para uma mesma resposta | Um profissional não pode ser duplicado na convocação | `owl:hasKey(keycloakSubjectId, Convoca)`; `UNIQUE(user_id, response_id)` |
| AX-CARD-02 | Uma equipe possui ao menos um membro e pode possuir vários | Cardinalidade 1:N entre Equipe de Campo e Membro de Equipe | `owl:minCardinality 1` (CompostaPor); `@OneToMany team → team_members` |
| AX-CARD-03 | Uma análise sanitária pode ter múltiplos alvos e um estabelecimento pode ser alvo de múltiplas análises simultâneas | Cardinalidade 1:N entre Análise Sanitária e Alvo de Investigação | `owl:minCardinality 1` (analiseSanitariaHasAlvoInvestigacao); ausência de UNIQUE(analysis_id, premise_id) |

---

## 5. Axiomas de Estado (2)

| ID | Axioma | Descrição | Fonte / Formalização |
|----|--------|-----------|-------|
| AX-STATE-01 | Uma Pessoa Convocada pode estar em quarentena, situação temporal com validade prevista, que cessa em uma data determinada | Classe definida `Quarantined Person` (emQuarentena = true) + validade | `owl:equivalentClass` + `owl:cardinality 1` (quarentenaAte); `ResponseConvokedUsers.isDirty/.dirtyUntil` |
| AX-STATE-02 | Uma Pessoa Convocada pode exercer, de forma independente, permissões de gestão e de observação | Permissões independentes | `owl:cardinality 1` (permissaoGestao, permissaoObservacao); `isManagement`, `isObserver` |

**Nota:** os estados persistidos da implementação (sinalizadores de análise ativa, resposta ativa/concluída, zona aberta/fechada, visita concluída) são cardinalidades de atributos em nível de implementação, não axiomas do modelo conceitual.

---

## 6. Axiomas Geográficos (1)

| ID | Axioma | Descrição | Fonte / Formalização |
|----|--------|-----------|-------|
| AX-GEO-01 | Um Alvo de Investigação é mediatizado por até três Zonas de Controle concêntricas (Perifoco, Vigilância e Proteção), ordenadas por raio crescente em torno do alvo | No sistema: `INFECTED` (Perifoco), `BUFFER` (Vigilância), `SURVEILLANCE` (Proteção); `INVESTIGATION` é mecanismo de API, fora do modelo | `owl:maxCardinality 3` (alvoInvestigacaoHasZonaControleInvestigacao) |

**Nota:** o suporte geoespacial (colunas `GEOGRAPHY`/PostGIS, consultas `ST_DWithin`) é um mecanismo de implementação, não axioma — consta da tabela de rastreabilidade.

---

## Mapa: Axiomas × Subdomínios

| Subdomínio | Axiomas |
|------------|---------|
| Core | AX-ID-01, AX-ID-02, AX-ID-04 |
| Investigação Sanitária | AX-ID-03, AX-DEP-07, AX-DEP-08, AX-CARD-03, AX-GEO-01 |
| Resposta Sanitária | AX-DEP-01, AX-DEP-02, AX-DEP-03, AX-DEP-09, AX-SEQ-01, AX-SEQ-02, AX-SEQ-05, AX-CARD-01, AX-CARD-02, AX-STATE-01, AX-STATE-02 |
| Ações em Campo | AX-DEP-04, AX-DEP-05, AX-DEP-06, AX-SEQ-03, AX-SEQ-04, AX-SEQ-06 |

---

## Referências

- Código fonte: entidades JPA, migrations Flyway, services
- Documento `Funcionalidades SIGEVS.md`
- Catálogo de Conceitos (CAP-CATA): `01-cap-cata.md`
