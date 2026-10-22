# Guia de Captura de Dados do Código Fonte — SIGEVS-O

---

## 1. Mapa de Fontes por Subdomínio

### Subdomínio: Core

| Fonte | Localização | O que extrair |
|-------|-------------|---------------|
| **Estabelecimento** | `model/registration/Estabelecimento.java` | Atributos, tipos, relacionamento com Endereco |
| **Endereco** | `model/registration/Endereco.java` | Atributos de localização |
| **Usuario** | `model/registration/Usuario.java` | Atributos, relacionamento com Modulo |
| **Modulo** | `model/registration/Modulo.java` | Perfis e permissões |
| **Estado** | `model/registration/Estado.java` | UF |
| **Cidade** | `model/registration/Cidade.java` | Municípios |
| **Frigorifico** | `model/registration/Frigorifico.java` | Tipo de inspeção |
| **CadastroAmbientalRural** | `model/registration/CadastroAmbientalRural.java` | CAR |
| **GranjaSuino / GranjaAve** | `model/registration/granja/` | Especificações por espécie |
| **Tabelas BD** | `cadastros.estabelecimento`, `cadastros.usuario`, `cadastros.endereco`, `cadastros.frigorifico` | Constraints, índices, tipos de coluna |
| **Enums** | `enums/SpeciesCategory.java` | Categorias de espécies |
| **Controllers** | `PremiseController`, `UsuarioController`, `ModuloController`, `CARController` | Endpoints de cadastro |
| **DTOs** | `dto/premise/PremiseDTO`, `registration/UsuarioDTO` | Campos trafegados |

### Subdomínio: Investigação Sanitária

| Fonte | Localização | O que extrair |
|-------|-------------|---------------|
| **SanitaryAnalysis** | `model/SanitaryAnalysis.java` | Registro central da investigação |
| **AnalysisTarget** | `model/AnalysisTarget.java` | Alvos da investigação, zonas (zone1, zone2, zone3) |
| **AffectedArea** | `model/AffectedArea.java` | Áreas geográficas afetadas |
| **Movimentacao*** | `model/movement/Movimentacao*.java` (7 subclasses) | Movimentação animal (GTA) por espécie |
| **MovimentacaoAvesView** | `model/movement/MovimentacaoAvesView.java` | View consolidada de movimentação |
| **Tabelas BD** | `sigevs.sanitary_analysis`, `sigevs.analysis_targets`, `movimentacao.movimentacao_*` | Constraints, índices geoespaciais |
| **Enums** | `ZoneType`, `SpeciesCategory`, `MovementPurpose` | Tipos classificadores |
| **Controllers** | `SanitaryAnalysisController`, `AnimalMovementController` | Endpoints |
| **DTOs** | `SanitaryAnalysisDTO`, `AnalysisTargetDTO`, `MovementDTO`, `MovementFilterDTO` | Dados trafegados |

### Subdomínio: Resposta Sanitária

| Fonte | Localização | O que extrair |
|-------|-------------|---------------|
| **SanitaryEventResponse** | `model/SanitaryEventResponse.java` | Registro central da resposta |
| **ResponseSurveillanceCycle** | `model/response/ResponseSurveillanceCycle.java` | Ciclos de vigilância |
| **SurveillanceCycleZone** | `model/response/SurveillanceCycleZone.java` | Zonas por ciclo |
| **ResponseTeam** | `model/response/ResponseTeam.java` | Equipes de campo |
| **TeamMember** | `model/response/TeamMember.java` | Membros da equipe |
| **TeamType** | `model/response/TeamType.java` | Tipos de equipe |
| **ResponseArea** | `model/response/ResponseArea.java` | Áreas operacionais |
| **AreaPremise** | `model/response/AreaPremise.java` | Propriedades em área |
| **ResponseBarrier** | `model/response/ResponseBarrier.java` | Barreiras sanitárias |
| **ResponseVehicle** | `model/response/ResponseVehicle.java` | Veículos |
| **ResponseCommandPost** | `model/response/ResponseCommandPost.java` | Posto de comando |
| **ResponseConvokedUsers** | `model/response/ResponseConvokedUsers.java` | Usuários convocados |
| **ResponseRoles** | `model/response/ResponseRoles.java` | Papéis/funções |
| **TeamTracking** | `model/response/TeamTracking.java` | Rastreamento GPS |
| **Tabelas BD** | `sigevs.sanitary_event_response`, `sigevs.response_*`, `sigevs.team_*` | Constraints, índices |
| **Enums** | `ZoneType`, `ResponseBarrierType`, `ResponseBarrierRole` | Classificadores |
| **Controllers** | `SanitaryEventResponseController`, `ResponseAreaController`, `ResponseBarrierController`, `ResponseTeamController`, `ResponseVehicleController`, `ResponseConvokedUsersController`, `ResponseCommandPostController`, `ResponseSurveillanceCycleController`, `TeamTrackingController` | Endpoints |
| **DTOs** | `SanitaryEventResponseDTO`, `ResponseAreaDTO`, `ResponseBarrierDTO`, `ResponseTeamDTO`, `ResponseVehicleDTO`, `ResponseSurveillanceCycleDTO`, `TeamTrackingDTO`, `TeamStatsDTO` | Dados trafegados |

### Subdomínio: Ações em Campo

| Fonte | Localização | O que extrair |
|-------|-------------|---------------|
| **PremiseSubmission** | `model/PremiseSubmission.java` | Submissão de propriedade |
| **BarrierSubmission** | `model/BarrierSubmission.java` | Submissão de barreira |
| **TemporaryPremise** | `model/TemporaryPremise.java` | Propriedade temporária |
| **EventSystemLog** | `model/EventSystemLog.java` | Log de auditoria |
| **Tabelas BD** | `sigevs.premise_submissions`, `sigevs.barrier_submissions`, `sigevs.temporary_premises`, `sigevs.event_system_log` | Constraints |
| **Enums** | `SysEventType` | Tipos de evento de log |
| **Controllers** | `SubmissionController`, `TemporaryPremiseController`, `EventActionsController` | Endpoints |
| **DTOs** | `PremiseSubmissionDTO`, `BarrierSubmissionDTO`, `SubmissionData`, `ResponseSubmissionsDTO`, `TempPremiseSubmissionDTO` | Dados trafegados |

---

## 2. Template de Extração de Conceitos

Para cada conceito identificado, preencher a seguinte ficha:

```markdown
## Conceito: [Nome do Conceito]

### Subdomínio
[Core | Investigação | Resposta | Campo]

### Definição
[Descrição conceitual do termo no domínio]

### Mapeamento no Código
- **Entidade JPA**: [Nome.java]
- **Tabela BD**: [schema.tabela]
- **DTO**: [NomeDTO.java]
- **Controller**: [NomeController.java] → [endpoints]
- **Service**: [NomeService.java]

### Atributos
| Atributo | Tipo | Descrição | Mapeamento UFO |
|----------|------|-----------|----------------|
| [nome] | [tipo Java] | [descrição] | [Quality | Mode | ...]

### Relacionamentos
| Tipo | Target | Cardinalidade | Descrição |
|------|--------|---------------|-----------|
| [@ManyToOne] | [Entidade] | [N:1] | [descrição] |

### Enums Utilizados
- [EnumName]: [valores relevantes]

### Regras / Constraints
- [Regra de negócio extraída do código / BD]

### Endpoints Associados
- [MÉTODO] [path]

### Questões de Competência Relacionadas
- [CQ-XXX-XX]

### Estereótipo UFO Candidato
[<<Kind>> | <<Role>> | <<Event>> | <<Relator>> | <<Collective>> | <<Phase>> | <<Quality>>]
```

---

## 3. Catálogo de Enums

| Enum | Valores | Conceito Ontológico |
|------|---------|---------------------|
| `ZoneType` | `INFECTED` (Perifoco), `BUFFER` (Vigilância), `SURVEILLANCE` (Proteção), `INVESTIGATION` (Investigação) | Tipos de Zona de Controle |
| `ResponseBarrierType` | `FIXED` (Posto Fixo), `MOBILE` (Volantes) | Tipo de Barreira Sanitária |
| `ResponseBarrierRole` | `SANITARY` (Barreira Sanitária), `DIVERSION` (Barreira de Desvio) | Função da Barreira |
| `SpeciesCategory` | `AVES`, `SUINOS`, `OVINOS`, `BOVINOS`, `OUTROS` (com subtipos) | Categoria de Espécie Animal |
| `MovementPurpose` | `ABATE`, `ENGORDA`, `OUTROS` | Finalidade de Movimentação |
| `SysEventType` | `INSERT`, `UPDATE`, `DELETE`, `DEACTIVATE`, `PROCESS_INFO`, `PROCESS_SUCCESS`, `PROCESS_ERROR`, `API_CALL`, `LOGIN_SUCCESS`, `LOGIN_FAILURE`, `ACCESS`, `ERROR`, `CUSTOM` | Tipo de Evento de Auditoria |
| `AsyncTaskStatus` | `READY`, `RUNNING`, `SUCCESS`, `FAILED`, `CANCELLED` | Status de Tarefa Assíncrona |
| `TeamType` (BD) | `VIGILANCIA`, `LIMPEZA_DESINFECCAO`, `VACINACAO`, `INVESTIGACAO`, `AVALIACAO`, `DEPOPULACAO`, `BARREIRA` | Tipo de Equipe de Campo |
| `ResponseRoles` (BD) | `MEMBRO`, `MODELAGEM_BARREIRA`, `MODELAGEM_VIGILANCIA` | Papel/Função em Equipe |

---

## 4. Regras de Negócio Identificadas do Código

| ID | Regra | Fonte | Subdomínio |
|----|-------|-------|------------|
| BR-01 | Uma equipe só pode estar alocada a um ciclo por vez | `UNIQUE(team_id, cycle_id)` → `UNIQUE(user_id, response_id)` em convoked_users | Resposta |
| BR-02 | Um foco pode ter até três zonas concêntricas: Perifoco, Vigilância e Proteção | `ZoneType` enum + campos zone1/2/3 em AnalysisTarget | Investigação |
| BR-03 | Uma área operacional é concluída quando todas as suas propriedades forem visitadas | `is_completed` em AreaPremise; lógica em EventActionsService | Campo |
| BR-04 | Um ciclo de vigilância pertence exclusivamente a uma resposta sanitária | `FOREIGN KEY (response_id)` em response_surveillance_cycle | Resposta |
| BR-05 | Os ciclos de vigilância seguem uma ordenação sequencial dentro de uma resposta | `UNIQUE(cycle_number, response_id)` | Resposta |
| BR-06 | Uma propriedade só pode estar em uma zona por ciclo | Estrutura de área → propriedade → zona → ciclo | Resposta |
| BR-07 | Um ciclo só pode ser fechado após todas as áreas serem concluídas | Lógica no EventActionsService | Resposta |
| BR-08 | Um usuário só pode ser convocado uma vez por resposta | `UNIQUE(user_id, response_id)` em convoked_users | Resposta |
| BR-09 | Submissão de propriedade vincula-se a uma area_premise + equipe | `FOREIGN KEY (area_premise_id, team_id)` | Campo |
| BR-10 | Submissão de barreira vincula-se a uma barreira específica | `FOREIGN KEY (barrier_id)` em barrier_submissions | Campo |
| BR-11 | Propriedade temporária pode ser vinculada a um estabelecimento existente posteriormente | `premise_id` FK opcional em temporary_premises | Campo |
| BR-12 | Cada investigation possui um tipo de zona adicional "Investigação" além das três zonas padrão | `INVESTIGATION` em ZoneType | Investigação |
| BR-13 | Uma resposta sanitária pode ter um posto de comando (0 ou 1) | `OneToOne` response_command_post → response | Resposta |
| BR-14 | O rastreamento GPS de equipes é feito por período (start/end time) | `TeamTracking` com createdAt + endTime | Resposta |
| BR-15 | Os módulos definem as permissões de acesso dos usuários | `@ManyToMany Usuario ↔ Modulo` via `usuario_modulos` | Core |

---

## 5. Matriz de Rastreabilidade

### Template

```
[Conceito]
├─ Entidade JPA: [Nome.java]
├─ Tabela BD: [schema.tabela]
├─ Endpoints:
│   ├─ [MÉTODO] [path]
│   └─ [MÉTODO] [path]
├─ DTO: [NomeDTO.java]
├─ Service: [NomeService.java]
└─ CQs: [IDs]
```

### Exemplos Preenchidos

```
Foco Sanitário (SanitaryAnalysis → SanitaryEventResponse)
├─ Entidades JPA: SanitaryAnalysis.java, SanitaryEventResponse.java
├─ Tabelas BD: sigevs.sanitary_analysis, sigevs.sanitary_event_response
├─ Endpoints:
│   ├─ POST /sanitary-analysis
│   ├─ POST /event-response
│   ├─ GET  /event-response/{uuid}
│   └─ GET  /sanitary-analysis/{uuid}
├─ DTOs: SanitaryAnalysisDTO, SanitaryEventResponseDTO
├─ Service: SanitaryAnalysisService, SanitaryEventResponseService
└─ CQs: CQ-INV-01, CQ-INV-07

Ciclo de Vigilância
├─ Entidade JPA: ResponseSurveillanceCycle.java
├─ Tabela BD: sigevs.response_surveillance_cycle
├─ Endpoints:
│   ├─ GET  /event-response/{uuid}/cycles
│   ├─ POST /event-response/{uuid}/cycles
│   ├─ POST /event-response/{uuid}/cycles/{roundNumber}/replicate
│   └─ PUT  /event-response/{uuid}/cycles/{roundNumber}
├─ DTO: ResponseSurveillanceCycleDTO
├─ Service: ResponseSurveillanceCycleService
└─ CQs: CQ-RES-01, CQ-RES-05

Equipe de Campo
├─ Entidade JPA: ResponseTeam.java, TeamMember.java
├─ Tabela BD: sigevs.response_teams, sigevs.team_members
├─ Endpoints:
│   ├─ POST /teams/{uuid}
│   ├─ GET  /teams/{uuid}
│   └─ DELETE /teams/{id}
├─ DTOs: ResponseTeamDTO, TeamMemberDTO
├─ Service: ResponseTeamService
└─ CQs: CQ-RES-02, CQ-RES-03, CQ-RES-07

Barreira Sanitária
├─ Entidade JPA: ResponseBarrier.java
├─ Tabela BD: sigevs.response_barriers
├─ Enums: ResponseBarrierType, ResponseBarrierRole
├─ Endpoints:
│   ├─ POST /barriers
│   ├─ DELETE /barriers/{id}
│   ├─ GET  /barriers/by-team/{teamId}
│   └─ GET  /barriers/by-focus-response/{uuid}
├─ DTO: ResponseBarrierDTO
├─ Service: ResponseBarrierService
└─ CQs: CQ-RES-04, CQ-RES-09, CQ-RES-11
```

---

## 6. Estrutura de Diretórios do Código Relevante

```
src/main/java/br/com/pdsars/sigevs/
├── model/
│   ├── SanitaryAnalysis.java
│   ├── AnalysisTarget.java
│   ├── AffectedArea.java
│   ├── SanitaryEventResponse.java
│   ├── PremiseSubmission.java
│   ├── BarrierSubmission.java
│   ├── TemporaryPremise.java
│   ├── EventSystemLog.java
│   ├── response/
│   │   ├── ResponseSurveillanceCycle.java
│   │   ├── SurveillanceCycleZone.java
│   │   ├── ResponseTeam.java
│   │   ├── TeamMember.java
│   │   ├── TeamType.java
│   │   ├── ResponseArea.java
│   │   ├── AreaPremise.java
│   │   ├── ResponseBarrier.java
│   │   ├── ResponseVehicle.java
│   │   ├── ResponseCommandPost.java
│   │   ├── ResponseConvokedUsers.java
│   │   ├── ResponseRoles.java
│   │   └── TeamTracking.java
│   ├── movement/
│   │   ├── Movimentacao.java (abstract)
│   │   ├── MovimentacaoAves.java
│   │   ├── MovimentacaoBovinos.java
│   │   ├── MovimentacaoSuinos.java
│   │   ├── MovimentacaoOvinos.java
│   │   ├── MovimentacaoCaprinos.java
│   │   ├── MovimentacaoBubalinos.java
│   │   ├── MovimentacaoPerus.java
│   │   └── MovimentacaoAvesView.java
│   ├── registration/
│   │   ├── Estabelecimento.java
│   │   ├── Endereco.java
│   │   ├── Usuario.java
│   │   ├── Modulo.java
│   │   ├── Estado.java
│   │   ├── Cidade.java
│   │   ├── Frigorifico.java
│   │   ├── CadastroAmbientalRural.java
│   │   └── granja/
│   │       ├── GranjaSuino.java
│   │       └── GranjaAve.java
│   └── spread/
│       ├── Scenario.java
│       └── ControlActions.java
├── enums/
│   ├── ZoneType.java
│   ├── SysEventType.java
│   ├── SpeciesCategory.java
│   ├── ResponseBarrierType.java
│   ├── ResponseBarrierRole.java
│   └── MovementPurpose.java
├── dto/
│   ├── SanitaryEventResponseDTO.java
│   ├── SanitaryAnalysisDTO.java
│   └── ... (demais DTOs)
├── controller/
│   ├── SanitaryEventResponseController.java
│   ├── SanitaryAnalysisController.java
│   └── ... (demais controllers)
└── service/
    ├── SanitaryEventResponseService.java
    ├── SanitaryAnalysisService.java
    └── ... (demais services)

src/main/resources/db/migration/
├── V202508101530__init_database.sql
├── V202508121430__create_schema_sigevs.sql
├── V202508131400__insert_initial_data.sql
├── V202508141000__async_table.sql
├── V202511111430__add_new_imports.sql
├── V202511180000__add_export_types.sql
├── V202512081050__create_fk_temp_premise.sql
└── V202512281430__create_schema_spread.sql
```

---

## 7. Glossário de Termos do Código → Conceitos Ontológicos

| Termo no Código | Conceito Ontológico | Subdomínio |
|-----------------|---------------------|------------|
| `Estabelecimento` / `premise` | Estabelecimento Rural | Core |
| `Usuario` / `user` | Profissional do SVO | Core |
| `Endereco` | Endereço / Localização | Core |
| `Modulo` | Módulo / Permissão de Acesso | Core |
| `Frigorifico` | Frigorífico / Abatedouro | Core |
| `GranjaSuino` / `GranjaAve` | Granja Especializada | Core |
| `SanitaryAnalysis` | Análise Sanitária | Investigação |
| `AnalysisTarget` | Alvo de Investigação | Investigação |
| `AffectedArea` | Área Afetada | Investigação |
| `ZoneType` (INFECTED/BUFFER/SURVEILLANCE/INVESTIGATION) | Tipo de Zona de Controle | Investigação |
| `Movimentacao` (e subclasses) | Movimentação Animal / GTA | Investigação |
| `SanitaryEventResponse` | Resposta Sanitária | Resposta |
| `ResponseSurveillanceCycle` | Ciclo de Vigilância | Resposta |
| `SurveillanceCycleZone` | Zona por Ciclo | Resposta |
| `ResponseTeam` | Equipe de Campo | Resposta |
| `TeamMember` | Membro de Equipe | Resposta |
| `TeamType` (VIGILANCIA, BARREIRA, etc.) | Tipo de Equipe | Resposta |
| `ResponseArea` | Área Operacional | Resposta |
| `AreaPremise` | Propriedade em Área | Resposta |
| `ResponseBarrier` | Barreira Sanitária | Resposta |
| `ResponseVehicle` | Veículo / Viatura | Resposta |
| `ResponseCommandPost` | Posto de Comando | Resposta |
| `ResponseConvokedUsers` | Usuário Convocado | Resposta |
| `ResponseRoles` (MEMBRO, MODELAGEM_*) | Função em Equipe | Resposta |
| `TeamTracking` | Rastreamento GPS | Resposta |
| `PremiseSubmission` | Submissão de Propriedade | Campo |
| `BarrierSubmission` | Submissão de Barreira | Campo |
| `TemporaryPremise` | Propriedade Temporária | Campo |
| `EventSystemLog` | Log de Auditoria | Campo |
