# Fase de Captura — CAP-CATA (Catálogo de Conceitos)

---

## Catálogo de Conceitos do Domínio SIGEVS-O

| Campo | Valor |
|-------|-------|
| Ontologia: | SIGEVS-O — Ontology for Sanitary Event Management |
| Versão: | v.01 |
| Data: | 23/06/2026 |
| Fontes: | Funcionalidades SIGEVS.md, Código Fonte (sigevs-api), Iniciativa.md |

---

## Subdomínio: Core

### C01 — Estabelecimento

| Campo | Valor |
|-------|-------|
| **Definição** | Unidade produtiva rural cadastrada no serviço veterinário, com código SDA único, coordenadas geográficas, espécies exploradas e endereço |
| **Entidade JPA** | `Estabelecimento.java` |
| **Tabela BD** | `cadastros.estabelecimento` (id, uuid, ativo, nome_estabelecimento, codigo_estabelecimento UNIQUE, id_endereco FK, tipo, especies text[]) |
| **DTO** | `PremiseDTO`, `PremiseFormDTO` |
| **Controller** | `PremiseController` |
| **Service** | `PremiseService` |
| **Atributos** | codigoEstabelecimento (código SDA), nomeEstabelecimento, tipo (default "Propriedade Rural"), especies (String[]), ativo, coordenadas (via Endereco), carShape (Poligono) |
| **Relacionamentos** | Endereco (N:1), AreaPremise (1:N), GranjaSuino (1:1), GranjaAve (1:1), Frigorifico (1:1), AnalysisTarget (1:N), TemporaryPremise (1:1) |
| **Estereótipo UFO** | `<<Kind>>` — identidade própria independente de contexto |
| **CQs** | CQ-CORE-01, CQ-CORE-02, CQ-CORE-03, CQ-CORE-05 |

---

### C02 — Endereço

| Campo | Valor |
|-------|-------|
| **Definição** | Dados de localização de um estabelecimento, incluindo logradouro, município, estado e coordenadas geográficas |
| **Entidade JPA** | `Endereco.java` |
| **Tabela BD** | `cadastros.endereco` (id_endereco, rua, cep, numero, bairro, cidade, uf, latitude, longitude, coord GEOGRAPHY) |
| **DTO** | `AddressDTO` |
| **Atributos** | rua, cep, numero, bairro, cidade, uf, latitude, longitude |
| **Relacionamentos** | Estabelecimento (1:N) |
| **Estereótipo UFO** | `<<Kind>>` — entidade com identidade e atributos próprios |
| **CQs** | CQ-CORE-03 |

---

### C03 — Pessoa

| Campo | Valor |
|-------|-------|
| **Definição** | Pessoa física cadastrada no serviço veterinário oficial, com credenciais de acesso, perfil e permissões |
| **Entidade JPA** | `Usuario.java` |
| **Tabela BD** | `cadastros.usuario` (id_usuario, keycloak_subject_id UNIQUE, cpf UNIQUE, nome, email UNIQUE, data_cadastro, ativo, foto, uuid) |
| **DTO** | `UsuarioDTO`, `RegisterUserDTO` |
| **Controller** | `UsuarioController` |
| **Service** | `UsuarioService` |
| **Relacionamentos** | SanitaryAnalysis (1:N), TeamMember (1:N), ResponseConvokedUsers (1:N) |
| **Estereótipo UFO** | `<<Kind>>` — identidade própria |
| **CQs** | CQ-CORE-04, CQ-CORE-07 |

---

### C04 — Espécie Animal

| Campo | Valor |
|-------|-------|
| **Definição** | Categorização das espécies animais exploradas nas propriedades, segmentada por tipo e finalidade |
| **Entidade** | `SpeciesCategory` (enum) |
| **Valores** | AVES (16 subtipos), SUINOS, OVINOS, BOVINOS, OUTROS (26 subtipos) |
| **Uso em** | Estabelecimento.especies (String[]), movimentações, filters |
| **Estereótipo UFO** | `<<Kind>>` para espécies; `<<Subkind>>` para subtipos |
| **CQs** | CQ-CORE-02 |

---

### C05 — Frigorífico

| Campo | Valor |
|-------|-------|
| **Definição** | Estabelecimento de abate com tipo de inspeção sanitária (SIF, SIE, SIM) |
| **Entidade JPA** | `Frigorifico.java` |
| **Tabela BD** | `cadastros.frigorifico` |
| **Relacionamentos** | Estabelecimento (1:1) |
| **Atributos** | sistemaInspecao, numeroInspecao, ativo |
| **Estereótipo UFO** | `<<Subkind>>` de Estabelecimento |
| **CQs** | CQ-CORE-06 |

---

### C06 — Granja Especializada

| Campo | Valor |
|-------|-------|
| **Definição** | Estabelecimento especializado em produção suína ou avícola, com dados adicionais de exploração |
| **Entidade JPA** | `GranjaSuino.java`, `GranjaAve.java` |
| **Tabela BD** | `cadastros.granja_suino`, `cadastros.granja_ave` |
| **Relacionamentos** | Estabelecimento (1:1) |
| **Atributos (Suíno)** | finalidadeExploracao, integradora, registro, finalidadeExploracaoTipo |
| **Atributos (Ave)** | especieExploracao, formaExploracao, finalidadeProducao, producaoComercial |
| **Estereótipo UFO** | `<<Subkind>>` de Estabelecimento |
| **CQs** | CQ-CORE-02 |

---

## Subdomínio: Investigação Sanitária

### I01 — Análise Sanitária

| Campo | Valor |
|-------|-------|
| **Definição** | Registro de abertura de uma investigação epidemiológica sobre suspeita de doença, com metadados de filtro, autoria e prazos |
| **Entidade JPA** | `SanitaryAnalysis.java` |
| **Tabela BD** | `sigevs.sanitary_analysis` (analysis_name, active, created_at, user_creation_id FK, public, show_car, uuid) |
| **DTO** | `SanitaryAnalysisDTO` |
| **Controller** | `SanitaryAnalysisController` |
| **Service** | `SanitaryAnalysisService` |
| **Relacionamentos** | AnalysisTarget (1:N), SanitaryEventResponse (via analysis_id), originalAnalysis (self-ref) |
| **Atributos** | analysisName, isActive, createdAt, isPublic, showCar, metadata (filters JSON) |
| **Estereótipo UFO** | `<<Event>>` — marca o início de uma investigação |
| **CQs** | CQ-INV-07 |

---

### I02 — Alvo de Investigação

| Campo | Valor |
|-------|-------|
| **Definição** | Propriedade delimitada como foco de investigação, com coordenadas e raios de zona para controle |
| **Entidade JPA** | `AnalysisTarget.java` |
| **Tabela BD** | `sigevs.analysis_targets` (premise_id FK, target_name, lat/lng, zone1/2/3, start_date_mov, end_date_mov, input_mov, output_mov, coord GEOGRAPHY) |
| **DTO** | `AnalysisTargetDTO` |
| **Controller** | `SanitaryAnalysisController` |
| **Atributos** | premise, targetName, latitude, longitude, zone1, zone2, zone3, startDateMov, endDateMov, inputMov, outputMov |
| **Relacionamentos** | SanitaryAnalysis (N:1), Estabelecimento (N:1), AffectedArea (N:1) |
| **Estereótipo UFO** | `<<Role>>` — papel que um Estabelecimento assume quando sob investigação |
| **CQs** | CQ-INV-01, CQ-INV-02 |

---

### I03 — Área Afetada

| Campo | Valor |
|-------|-------|
| **Definição** | Região geográfica (municípios, polígonos) delimitada como sob investigação |
| **Entidade JPA** | `AffectedArea.java` |
| **Tabela BD** | `sigevs.affected_area` (name, shape jsonb) |
| **DTO** | `AffectedArea` (endpoint retorna sem shape) |
| **Estereótipo UFO** | `<<Kind>>` — região geográfica com identidade própria |
| **CQs** | CQ-INV-08 |

---

### I04 — Zona de Controle

| Campo | Valor |
|-------|-------|
| **Definição** | Perímetro geográfico definido ao redor de um alvo, classificado em Perifoco (infectada), Vigilância (buffer), Proteção (vigilância ampliada) ou Investigação |
| **Tabela BD** | Representada nos campos zone1/2/3 de `analysis_targets` |
| **Enum** | `ZoneType` — INFECTED("Perifoco"), BUFFER("Vigilancia"), SURVEILLANCE("Protecao"), INVESTIGATION("Investigacao") |
| **DTO** | `TemporaryZoneDTO` (zone, boundaryPoints) |
| **Estereótipo UFO** | `<<Relator>>` — conecta um foco a um perímetro geográfico, com atributos próprios (tipo, raio) |
| **CQs** | CQ-INV-01, CQ-INV-06 |

---

### I05 — Movimentação Animal (GTA)

| Campo | Valor |
|-------|-------|
| **Definição** | Registro de trânsito de animais entre propriedades, com origem, destino, espécie, quantidade e finalidade |
| **Entidade JPA** | `Movimentacao` (abstract), `MovimentacaoAves`, `MovimentacaoBovinos`, `MovimentacaoSuinos`, `MovimentacaoOvinos`, `MovimentacaoCaprinos`, `MovimentacaoBubalinos`, `MovimentacaoPerus` |
| **Tabela BD** | `movimentacao.movimentacao_*` (cada espécie) — chave composta (serie, numero, uf_origem) |
| **View** | `movimentacao.vw_movimentacao_aves` |
| **DTO** | `MovementDTO` |
| **Controller** | `AnimalMovementController` |
| **Enum** | `MovementPurpose` (ABATE, ENGORDA, OUTROS) |
| **Estereótipo UFO** | `<<Event>>` — evento de movimentação entre estabelecimentos |
| **CQs** | CQ-INV-03 |

---

### I06 — Propriedade Contactante

| Campo | Valor |
|-------|-------|
| **Definição** | Propriedade que teve contato direto (movimentação direta) ou indireto (cadeia de movimentações) com uma propriedade investigada |
| **Entidade JPA** | Não há entidade própria — calculado dinamicamente via movimentações |
| **Controller** | `SanitaryAnalysisController.POST /find-all-premises/by-targets` |
| **Estereótipo UFO** | `<<Role>>` — papel que um Estabelecimento assume quando identificado como contactante |
| **CQs** | CQ-INV-04, CQ-INV-05 |

---

### I07 — Categoria de Espécie (para investigação)

| Campo | Valor |
|-------|-------|
| **Definição** | Classificação das espécies animais em categorias sanitárias (aves, suínos, ovinos, bovinos, outros) |
| **Enum** | `SpeciesCategory` |
| **DTO** | `MovementFilterDTO` (species list), `AnalysisMetadataDTO` (speciesFilter, explorationFilter) |
| **Estereótipo UFO** | `<<Enumeration>>` — valores fixos de classificação sanitária |
| **CQs** | CQ-INV-09 |

---

## Subdomínio: Resposta Sanitária

### R01 — Resposta Sanitária

| Campo | Valor |
|-------|-------|
| **Definição** | Registro central da coordenação de contenção de um foco sanitário, com identificador, fase, prazos e status |
| **Entidade JPA** | `SanitaryEventResponse.java` |
| **Tabela BD** | `sigevs.sanitary_event_response` (identifier, due_date, analysis_id FK, user_creation_id FK, public, active, completed, phase_id, uuid, response_connector_uuid) |
| **DTO** | `SanitaryEventResponseDTO` |
| **Controller** | `SanitaryEventResponseController` |
| **Service** | `SanitaryEventResponseService` |
| **Relacionamentos** | SanitaryAnalysis (N:1), ResponseSurveillanceCycle (1:N), ResponseCommandPost (1:1), ResponseConvokedUsers (1:N) |
| **Estereótipo UFO** | `<<Event>>` — evento central que organiza a contenção |
| **CQs** | CQ-RES-01, CQ-RES-09, CQ-RES-13 |

---

### R02 — Ciclo de Vigilância

| Campo | Valor |
|-------|-------|
| **Definição** | Rodada numerada de varredura em zona de controle, com período definido e status de conclusão |
| **Entidade JPA** | `ResponseSurveillanceCycle.java` |
| **Tabela BD** | `sigevs.response_surveillance_cycle` (cycle_number UNIQUE c/ response_id, completed) |
| **DTO** | `ResponseSurveillanceCycleDTO` |
| **Controller** | `ResponseSurveillanceCycleController` |
| **Service** | `ResponseSurveillanceCycleService` |
| **Relacionamentos** | SanitaryEventResponse (N:1), SurveillanceCycleZone (1:N), ResponseTeam (1:N) |
| **Constraint** | UNIQUE(cycle_number, response_id) → ciclos sequenciais |
| **Estereótipo UFO** | `<<Event>>` — evento delimitado no tempo que organiza operações de campo |
| **CQs** | CQ-RES-01, CQ-RES-05 |

---

### R03 — Zona por Ciclo

| Campo | Valor |
|-------|-------|
| **Definição** | Delimitação geoespacial de cada zona (Perifoco, Vigilância, Proteção) dentro de um ciclo específico |
| **Entidade JPA** | `SurveillanceCycleZone.java` |
| **Tabela BD** | `sigevs.surveillance_cycle_zone` (zone tipo ZoneType, start_date, end_date, closed NOT NULL, boundary_points jsonb) |
| **DTO** | `SurveillanceCycleZoneDTO` |
| **Enum** | `ZoneType` |
| **Estereótipo UFO** | `<<Relator>>` — conecta ciclo a zona com atributos próprios (datas, fechamento) |
| **CQs** | CQ-RES-05 |

---

### R04 — Equipe de Campo

| Campo | Valor |
|-------|-------|
| **Definição** | Grupo de profissionais alocados a um ciclo de vigilância, com tipo, setor, cor e membros |
| **Entidade JPA** | `ResponseTeam.java` |
| **Tabela BD** | `sigevs.response_teams` (team_name, team_type_id FK, surveillance_cycle_id FK, active) |
| **DTO** | `ResponseTeamDTO` |
| **Controller** | `ResponseTeamController` |
| **Service** | `ResponseTeamService` |
| **Relacionamentos** | ResponseSurveillanceCycle (N:1), TeamMember (1:N), ResponseVehicle (1:N), ResponseBarrier (1:N), ResponseArea (1:N) |
| **Estereótipo UFO** | `<<Collective>>` — coletivo de profissionais com atuação conjunta |
| **CQs** | CQ-RES-02, CQ-RES-07 |

---

### R05 — Tipo de Equipe

| Campo | Valor |
|-------|-------|
| **Definição** | Classificação funcional da equipe de campo (vigilância, limpeza, vacinação, investigação, avaliação, despovoamento, barreira) |
| **Entidade JPA** | `TeamType.java` |
| **Tabela BD** | `sigevs.team_types` (type_name UNIQUE, label, sector, color) |
| **DTO** | `TeamTypeDTO` |
| **Estereótipo UFO** | `<<Kind>>` — tipo de coletivo |
| **CQs** | CQ-RES-02 |

---

### R06 — Membro de Equipe

| Campo | Valor |
|-------|-------|
| **Definição** | Pessoa vinculada a uma equipe de campo com função específica |
| **Entidade JPA** | `TeamMember.java` |
| **Tabela BD** | `sigevs.team_members` (team_id FK, user_id FK, role_id FK, active) |
| **DTO** | `TeamMemberDTO` |
| **Estereótipo UFO** | `<<Role>>` — papel que um Usuario assume dentro de uma EquipeCampo |
| **CQs** | CQ-RES-03 |

---

### R07 — Função em Equipe

| Campo | Valor |
|-------|-------|
| **Definição** | Papel predefinido que orienta a alocação e responsabilidades de um profissional (membro, modelagem de barreira, modelagem de vigilância) |
| **Entidade JPA** | `ResponseRoles.java` |
| **Tabela BD** | `sigevs.response_roles` (role_name UNIQUE, label) |
| **Valores** | MEMBRO, MODELAGEM_BARREIRA, MODELAGEM_VIGILANCIA |
| **Estereótipo UFO** | `<<Kind>>` — tipo de função |
| **CQs** | CQ-RES-03 |

---

### R08 — Área Operacional

| Campo | Valor |
|-------|-------|
| **Definição** | Setor geográfico atribuído a uma equipe dentro de uma zona de ciclo, com delimitação de polígono |
| **Entidade JPA** | `ResponseArea.java` |
| **Tabela BD** | `sigevs.response_areas` (team_id FK, area_name, color, boundary_points jsonb, cycle_zone_id FK) |
| **DTO** | `ResponseAreaDTO` |
| **Controller** | `ResponseAreaController` |
| **Service** | `ResponseAreaService` |
| **Relacionamentos** | ResponseTeam (N:1), SurveillanceCycleZone (N:1), AreaPremise (1:N) |
| **Estereótipo UFO** | `<<Kind>>` — subdivisão geográfica com identidade própria |
| **CQs** | CQ-RES-08, CQ-RES-10 |

---

### R09 — Propriedade em Área

| Campo | Valor |
|-------|-------|
| **Definição** | Vínculo entre propriedade e área operacional, com controle de conclusão de visita |
| **Entidade JPA** | `AreaPremise.java` |
| **Tabela BD** | `sigevs.area_premises` (premise_id FK, area_id FK, completed) |
| **DTO** | `AreaPremiseDTO` |
| **Relacionamentos** | ResponseArea (N:1), Estabelecimento (N:1), PremiseSubmission (1:N) |
| **Atributos** | isCompleted (Boolean) |
| **Estereótipo UFO** | `<<Relator>>` — conecta propriedade a área com atributo de conclusão |
| **CQs** | CQ-RES-10 |

---

### R10 — Barreira Sanitária

| Campo | Valor |
|-------|-------|
| **Definição** | Posto fixo ou volante para fiscalização de trânsito animal, com função sanitária (fiscalização) ou de desvio (redirecionamento) |
| **Entidade JPA** | `ResponseBarrier.java` |
| **Tabela BD** | `sigevs.response_barriers` (barrier_name, type FIXED/MOBILE, role SANITARY/DIVERSION, lat/lng, team_id FK, coord GEOGRAPHY) |
| **DTO** | `ResponseBarrierDTO` |
| **Controller** | `ResponseBarrierController` |
| **Service** | `ResponseBarrierService` |
| **Enums** | `ResponseBarrierType` (FIXED, MOBILE), `ResponseBarrierRole` (SANITARY, DIVERSION) |
| **Relacionamentos** | ResponseTeam (N:1), BarrierSubmission (1:N) |
| **Estereótipo UFO** | `<<Kind>>` — entidade física com identidade própria |
| **CQs** | CQ-RES-04, CQ-RES-09, CQ-RES-11 |

---

### R11 — Veículo / Viatura

| Campo | Valor |
|-------|-------|
| **Definição** | Frota de veículos vinculada às equipes de campo, com placa, modelo, cor e tipo |
| **Entidade JPA** | `ResponseVehicle.java` |
| **Tabela BD** | `sigevs.response_vehicles` (license_plate, model, color, brand, year, vehicle_type, team_id FK) |
| **DTO** | `ResponseVehicleDTO` |
| **Controller** | `ResponseVehicleController` |
| **Service** | `ResponseVehicleService` |
| **Estereótipo UFO** | `<<Kind>>` — entidade física com identidade própria |
| **CQs** | CQ-RES-12 |

---

### R12 — Posto de Comando

| Campo | Valor |
|-------|-------|
| **Definição** | Quartel general (QG) da operação de resposta, com endereço, coordenadas e observações |
| **Entidade JPA** | `ResponseCommandPost.java` |
| **Tabela BD** | `sigevs.response_command_post` (response_id FK UNIQUE, name, address, notes, lat/lng) |
| **DTO** | `ResponseCommandPostDTO` |
| **Controller** | `ResponseCommandPostController` |
| **Relacionamento** | SanitaryEventResponse (1:1) |
| **Estereótipo UFO** | `<<Kind>>` — entidade física com localização |
| **CQs** | CQ-RES-13 |

---

### R13 — Pessoa Convocada

| Campo | Valor |
|-------|-------|
| **Definição** | Pessoa mobilizada para uma resposta sanitária, com função, status de quarentena, permissões (gestão/observação) e vínculo a membro de equipe |
| **Entidade JPA** | `ResponseConvokedUsers.java` |
| **Tabela BD** | `sigevs.response_convoked_users` (user_id FK, response_id FK, dirty UNIQUE, active, dirty_until, management, observer, role_id FK, UNIQUE(user_id, response_id)) |
| **DTO** | `ResponseConvokedUsersDTO` |
| **Controller** | `ResponseConvokedUsersController` |
| **Service** | `ResponseConvokedUsersService` |
| **Estereótipo UFO** | `<<Role>>` — papel que uma Pessoa assume em uma resposta (generaliza Pessoa com restrictedTo = kind) |
| **CQs** | CQ-RES-14 |

---

### R14 — Rastreamento GPS de Equipe

| Campo | Valor |
|-------|-------|
| **Definição** | Registro do deslocamento geográfico das equipes em campo, com coordenadas, precisão e timestamps |
| **Entidade JPA** | `TeamTracking.java` |
| **Tabela BD** | `sigevs.team_tracking` (team_id, response_id, user_id, label, metadata jsonb, created_at, end_time, uuid) |
| **DTO** | `TeamTrackingDTO` |
| **Controller** | `TeamTrackingController` |
| **Service** | `TeamTrackingService` |
| **Estereótipo UFO** | `<<Event>>` — evento de rastreamento contínuo |
| **CQs** | CQ-RES-06 |

---

## Subdomínio: Ações em Campo

### F01 — Submissão de Propriedade

| Campo | Valor |
|-------|-------|
| **Definição** | Formulário preenchido na visita a uma propriedade, vinculado à área e equipe responsável |
| **Entidade JPA** | `PremiseSubmission.java` |
| **Tabela BD** | `sigevs.premise_submissions` (area_premise_id FK, submission_uuid UNIQUE, team_id FK) |
| **DTO** | `PremiseSubmissionDTO`, `SubmissionData` |
| **Controller** | `SubmissionController.POST /submission/premise` |
| **Estereótipo UFO** | `<<Event>>` — evento de coleta de dados |
| **CQs** | CQ-CAM-01, CQ-CAM-03 |

---

### F02 — Submissão de Barreira

| Campo | Valor |
|-------|-------|
| **Definição** | Formulário preenchido em barreira sanitária, com dados da fiscalção |
| **Entidade JPA** | `BarrierSubmission.java` |
| **Tabela BD** | `sigevs.barrier_submissions` (barrier_id FK, submission_uuid UNIQUE) |
| **DTO** | `BarrierSubmissionDTO` |
| **Controller** | `SubmissionController.POST /submission/barrier` |
| **Estereótipo UFO** | `<<Event>>` — evento de coleta de dados |
| **CQs** | CQ-CAM-03 |

---

### F03 — Propriedade Temporária

| Campo | Valor |
|-------|-------|
| **Definição** | Unidade não cadastrada encontrada em campo, registrada com contato, CPF/CNPJ e coordenadas |
| **Entidade JPA** | `TemporaryPremise.java` |
| **Tabela BD** | `sigevs.temporary_premises` (uuid, contact_name, cpf_cnpj, phone_number, lat/lng, premise_id FK opcional) |
| **DTO** | `TempPremiseSubmissionDTO` |
| **Controller** | `TemporaryPremiseController`, `SubmissionController.POST /submission/temporary-premise` |
| **Estereótipo UFO** | `<<Role>>` — estabelecimento não registrado formalmente |
| **CQs** | CQ-CAM-04 |

---

### F04 — Conclusão de Visita

| Campo | Valor |
|-------|-------|
| **Definição** | Status de finalização da vistoria de uma propriedade dentro de uma área operacional |
| **Entidade** | `AreaPremise.isCompleted` (Boolean) |
| **Endpoints** | `EventActionsController.POST /visit/{id}/complete`, `POST /visit/{id}/reopen` |
| **Estereótipo UFO** | `<<Phase>>` — fase binária (completa/incompleta) |
| **CQs** | CQ-CAM-01, CQ-CAM-02 |

---


