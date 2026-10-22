# Fase de Captura — DOC-MODE (Documento da Ontologia de Referência)

---

## Reference Ontology Document — SIGEVS-O

| Campo | Valor |
|-------|-------|
| Documento: | Reference Ontology Document |
| Ontologia: | SIGEVS-O — Ontology for Sanitary Event Management in Animal Health Defense |
| Versão: | v.01 |
| Data: | 24/06/2026 |

---

## 1. Modeling Language

**OntoUML** — Language for Ontology-Driven Conceptual Modeling based on UFO. Used for constructing the reference ontology with formally defined stereotypes (`<<Kind>>`, `<<Subkind>>`, `<<Role>>`, `<<Event>>`, `<<Relator>>`, `<<Collective>>`, `<<Phase>>`).

---

## 2. Foundational Ontology

**UFO (Unified Foundational Ontology)** — provides the semantic foundation for all concepts, relations, and axioms. UFO's ontological categories guide the classification of each domain concept:

| UFO Category | SIGEVS-O Application |
|--------------|---------------------|
| **Endurant** | Estabelecimento, Pessoa, Endereço, Barreira, Veículo, Posto de Comando |
| **Event** | Análise Sanitária, Ciclo de Vigilância, Movimentação Animal, Submissão, Rastreamento GPS |
| **Relator** | CAR, Zona de Controle, Zona por Ciclo, Propriedade em Área |
| **Collective** | Equipe de Campo |
| **Role** | Alvo de Investigação, Membro de Equipe, Usuário Convocado, Propriedade Contactante |
| **Subkind** | Frigorífico, Granja Suína, Granja Avícola |
| **Phase** | Conclusão de Visita (Pendente/Completa) |

---

## 3. Concept Criteria

| ID | Criterion | Type |
|----|-----------|------|
| CR-01 | Domain Relevance — concept belongs to animal health defense within SVO scope | Subjective |
| CR-02 | SIGEVS Presence — concept represented in at least one SIGEVS functionality | Objective |
| CR-03 | Subdomain Coverage — concept fits within Core, Investigação, Resposta, or Campo | Objective |
| CR-04 | UFO Classifiable — concept can be mapped to a UFO stereotype | Subjective |
| CR-05 | Domain Recognition — concept defined in recognized sources (SIGEVS, FAO GEMP, legislation) | Objective |

---

## 4. Ontologies to Reuse

*Evaluated during Capture Phase. Pending integration:*

| Ontology | Domain | Analysis | Status |
|----------|--------|----------|--------|
| FAO GEMP | Animal health emergency management | Concepts partially overlap with Resposta Sanitária subdomain | Pending (see `gemp.md`) |
| AGROVOC | Agriculture/livestock/veterinary thesaurus | Useful for species taxonomy and establishment types | To be evaluated |
| IDO | Infectious disease ontology | Potential alignment for disease-related concepts | To be evaluated |

---

## 5. Modularization

```
┌─────────────────────────────────────────────────────────────┐
│                     SIGEVS-O                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐  ┌─────┐  │
│  │    Core      │  │ Investigação │  │ Resposta │  │Campo│  │
│  │              │  │              │  │          │  │     │  │
│  │ 4 Kinds      │  │ 2 Events     │  │ 6 Kinds  │  │ 1   │  │
│  │ 3 Subkinds   │  │ 2 Roles      │  │ 3 Events │  │Role │  │
│  │ 1 Relator    │  │ 2 Relators   │  │ 1 Collect│  │ 2   │  │
│  └──────────────┘  │ 1 Kind       │  │ 3 Relat. │  │Events│  │
│                    │ 1 Enum       │  │ 2 Roles  │  └─────┘  │
│                    └──────────────┘  └──────────┘           │
└─────────────────────────────────────────────────────────────┘
```

### Subdomain: Core (8 classes)

| Class | Stereotype | Description |
|-------|------------|-------------|
| Estabelecimento | `<<Kind>>` | Rural productive unit registered in the veterinary service |
| Endereco | `<<Kind>>` | Geographic address of an establishment |
| Pessoa | `<<Kind>>` | Person registered in the official veterinary service |
| EspecieAnimal | `<<Kind>>` | Animal species classification |
| Frigorifico | `<<Subkind>>` | Slaughterhouse (specialization of Estabelecimento) |
| GranjaSuino | `<<Subkind>>` | Swine farm (specialization of Estabelecimento) |
| GranjaAve | `<<Subkind>>` | Poultry farm (specialization of Estabelecimento) |
| CAR | `<<Relator>>` | Rural Environmental Registry connecting establishment to geospatial perimeter |

### Subdomain: Investigação Sanitária (7 classes)

| Class | Stereotype | Description |
|-------|------------|-------------|
| AnaliseSanitaria | `<<Event>>` | Investigation record for disease suspicion |
| AlvoInvestigacao | `<<Role>>` | Property designated as investigation target |
| AreaAfetada | `<<Kind>>` | Geographic region under investigation |
| ZonaControleInvestigacao | `<<Relator>>` | Perimeter zone connecting target to radius/type |
| MovimentacaoAnimal | `<<Event>>` | Animal transit record (GTA) between properties |
| PropriedadeContactante | `<<Role>>` | Property with direct/indirect contact to investigated premise |
| CategoriaEspecie | `<<Enumeration>>` | Fixed species categories for sanitary filtering |

### Subdomain: Resposta Sanitária (14 classes)

| Class | Stereotype | Description |
|-------|------------|-------------|
| RespostaSanitaria | `<<Event>>` | Central record of outbreak containment coordination |
| CicloVigilancia | `<<Event>>` | Numbered round of surveillance in a control zone |
| ZonaPorCiclo | `<<Relator>>` | Zone delimitation within a specific cycle |
| EquipeCampo | `<<Collective>>` | Team of professionals for field operations |
| MembroEquipe | `<<Role>>` | Person assigned to a field team |
| Funcao | `<<Kind>>` | Predefined role for team allocation |
| AreaOperacional | `<<Kind>>` | Geographic sector assigned to a team within a zone |
| PropriedadeEmArea | `<<Relator>>` | Link between property and operational area with completion status |
| BarreiraSanitaria | `<<Kind>>` | Fixed or mobile checkpoint for animal transit control |
| Veiculo | `<<Kind>>` | Vehicle assigned to field teams |
| PostoComando | `<<Kind>>` | Command HQ for the sanitary response operation |
| UsuarioConvocado | `<<Role>>` | Person mobilized for a sanitary response |
| RastreamentoGPS | `<<Event>>` | GPS tracking record of team displacement |
| TipoEquipe | `<<Kind>>` | Functional classification of field teams |

### Subdomain: Ações em Campo (3 classes)

| Class | Stereotype | Description |
|-------|------------|-------------|
| SubmissaoPropriedade | `<<Event>>` | Form submitted during property visit |
| SubmissaoBarreira | `<<Event>>` | Form submitted at sanitary barrier |
| PropriedadeTemporaria | `<<Role>>` | Unregistered property found in the field |

---

## 6. Conceptual Model

### 6.1 Generalization Hierarchy

```
<<Kind>> Estabelecimento
    ├── <<Subkind>> Frigorifico
    ├── <<Subkind>> GranjaSuino
    └── <<Subkind>> GranjaAve

<<Kind>> Pessoa
    ├── <<Role>> MembroEquipe        (assumed within EquipeCampo)
    └── <<Role>> UsuarioConvocado     (assumed within RespostaSanitaria)

<<Kind>> Estabelecimento
    ├── <<Role>> AlvoInvestigacao       (during investigation)
    ├── <<Role>> PropriedadeContactante (when identified via movements)
    └── <<Role>> PropriedadeTemporaria  (when found unregistered)
```

### 6.2 Core Subdomain

```
 ┌───────────────┐         ┌─────────────────┐
 │  Estabelecimento│──1..*──│    Endereco      │
 │   <<Kind>>     │    1    │   <<Kind>>      │
 ├────────────────┤         ├─────────────────┤
 │ -codigoSDA:Str │         │ -logradouro:Str │
 │ -nome:String   │         │ -cidade:String  │
 │ -especies:List │         │ -uf:String      │
 │ -ativo:Boolean │         │ -coord:Geog     │
 └───────┬────────┘         └─────────────────┘
         │
    ┌────┼──────────────────────┐
    │    │                      │
 ┌──▼──────┐ ┌──────▼─────┐ ┌──▼──────┐
 │Frigorif.│ │GranjaSuino │ │GranjaAve│
 │<<Subk.>>│ │<<Subk.>>   │ │<<Subk.>>│
 └─────────┘ └────────────┘ └─────────┘

 ┌────────────────┐
 │   Pessoa        │
 │   <<Kind>>      │
 └────────────────┘

 ┌──────────────────────────┐
 │         CAR              │
 │       <<Relator>>        │
 │ ┌──────────────────────┐ │
 │ │conecta Estabelecimento│ │
 │ │a seu perímetro        │ │
 │ └──────────────────────┘ │
 └──────────────────────────┘
```

### 6.3 Investigação Sanitária Subdomain

```
 ┌───────────────────┐         ┌─────────────────────┐
 │  AnaliseSanitaria  │────*────│   Pessoa            │
 │    <<Event>>       │    1    │   <<Kind>>          │
 ├───────────────────┤         └─────────────────────┘
 │ -nome:String      │
 │ -ativa:Boolean    │──1────*──┌─────────────────────┐
 │ -criadaEm:DateTime│         │  AlvoInvestigacao   │
 └───────────────────┘         │    <<Role>>         │
                               ├─────────────────────┤
 ┌──────────────────┐          │ -lat/lng:BigDecimal │
 │  AreaAfetada     │──*──*──│ -zone1/2/3:Integer  │
 │   <<Kind>>       │         │ -dataMov:LocalDate  │
 └──────────────────┘         └──────────┬──────────┘
                                         │*        1
                                   ┌─────▼──────────┐
                                   │ Estabelecimento │
                                   │   <<Kind>>      │
                                   └─────────────────┘

 ┌─────────────────────────┐
 │ ZonaControleInvestigacao│
 │      <<Relator>>        │
 ├─────────────────────────┤
 │ -tipo:ZoneType          │
 │ -raio:Integer           │
 └─────────────────────────┘

 ┌──────────────────────┐       ┌──────────────────────┐
 │ MovimentacaoAnimal    │──*──1│ Estabelecimento      │
 │    <<Event>>          │ (origem e destino)         │
 ├──────────────────────┤       └──────────────────────┘
 │ -serie,numero,uf:PK  │
 │ -especie,quantidade  │
 │ -finalidade:enum     │
 └──────────────────────┘

 ┌────────────────────────┐
 │ PropriedadeContactante  │
 │      <<Role>>          │
 ├────────────────────────┤
 │ -tipo:Direta/Indireta  │
 │ (materia: Estabeleci.) │
 └────────────────────────┘
```

### 6.4 Resposta Sanitária Subdomain

```
 ┌──────────────────────┐         ┌───────────────────────┐
 │   RespostaSanitaria   │────1───│   AnaliseSanitaria    │
 │     <<Event>>         │    *   │     <<Event>>         │
 ├──────────────────────┤         └───────────────────────┘
 │ -identificador:String│
 │ -dataVencimento:Date │──1──*──┌────────────────────────┐
 │ -ativa,concluida:Bool│        │    CicloVigilancia     │
 └──────────┬───────────┘        │      <<Event>>         │
            │                    ├────────────────────────┤
       ┌────┴────┐               │ -numeroCiclo:Integer   │
       │         │               │ -concluido:Boolean     │
 ┌─────▼────┐ ┌──▼────────┐     └───────────┬────────────┘
 │PostoCom.│ │Usuário     │                 │
 │<<Kind>> │ │Convocado   │            ┌────┴────┐
 └─────────┘ │ <<Role>>   │            │         │
             └────────────┘      ┌─────▼──┐ ┌───▼────────┐
                                 │ZonaPor │ │EquipeCampo │
                                 │ Ciclo  │ │<<Collect.>>│
 ┌──────────────────────┐        │<<Relat>>│ └──┬──┬──┬──┘
 │   AreaOperacional     │        └────────┘    │  │  │
 │     <<Kind>>          │          ↑           │  │  │
 ├──────────────────────┤          │*           │  │  │
 │ -nome,cor,String     │──────────┘           │  │  │
 │ -boundary:Poligono   │                      │  │  │
 └──────────┬───────────┘            ┌─────────┘  │  │
            │                       │            │  │
       ┌────┴────┐            ┌─────▼──┐  ┌──────┘  │
       │         │            │Membro  │  │         │
 ┌─────▼────┐    │            │Equipe  │  │         │
 │Propried. │    │            │<<Role>>│  │         │
 │Em Área   │    │            └──┬──────┘  │         │
 │<<Relator>>│   │               │         │         │
 ├──────────┤    │               │*        │         │
 │-concluída│    │          ┌────▼──┐  ┌──┴───┐  ┌──┴────┐
 │:Boolean  │    │          │Função │  │Veículo│  │Barreir│
 └────┬─────┘    │          │<<Kind>>│  │<<Kind>>│ │<<Kind>>│
      │*         │          └───────┘  └───────┘  └───────┘
 ┌────▼──────┐   │
 │Estabeleci.│   │
 │<<Kind>>   │   │
 └───────────┘   │
                 │
 ┌───────────────┴────────────────────────────────────────┐
 │                  RastreamentoGPS                        │
 │                    <<Event>>                            │
 ├────────────────────────────────────────────────────────┤
 │ -dataInicio,fim:DateTime                                │
 │ -coordenadas:LatLng[*]                                  │
 └────────────────────────────────────────────────────────┘
```

### 6.5 Ações em Campo Subdomain

```
 ┌──────────────────────┐        ┌──────────────────────┐
 │ SubmissaoPropriedade  │──*──1─│ PropriedadeEmArea    │
 │     <<Event>>         │        │    <<Relator>>       │
 ├──────────────────────┤        └──────────────────────┘
 │ -uuid:UUID           │
 │ -dataHora:DateTime   │──*──1─┌──────────────────────┐
 └──────────────────────┘        │   EquipeCampo        │
                                 │  <<Collective>>      │
 ┌──────────────────────┐        └──────────────────────┘
 │  SubmissaoBarreira    │──*──1─┌──────────────────────┐
 │     <<Event>>         │        │  BarreiraSanitaria  │
 ├──────────────────────┤        │    <<Kind>>         │
 │ -uuid:UUID           │        └──────────────────────┘
 │ -dataHora:DateTime   │
 └──────────────────────┘        ┌──────────────────────┐
                                  │ PropriedadeTemporaria│
                                  │     <<Role>>         │
                                  ├──────────────────────┤
                                  │ -contato,cpf,tel    │
                                  │ -lat/lng            │
                                  │ (materia:Estab.)    │
                                  └──────────────────────┘
```

---

## 7. Model Axioms

### Identity Axioms

| ID | Axiom |
|----|-------|
| AX-ID-01 | Each `Estabelecimento` has a unique `codigoSDA` |
| AX-ID-02 | Each `Pessoa` is uniquely identified by `keycloak_subject_id`, `cpf`, and `email` |
| AX-ID-03 | Each `MovimentacaoAnimal` is identified by the triple `(serie, numero, ufOrigem)` |
| AX-ID-04 | Each `SubmissaoPropriedade` and `SubmissaoBarreira` is identified by a unique `uuid` |
| AX-ID-05 | A `CicloVigilancia` is uniquely identified by `(numeroCiclo, RespostaSanitaria)` |

### Dependency Axioms

| ID | Axiom |
|----|-------|
| AX-DEP-01 | Every `CicloVigilancia` belongs exclusively to one `RespostaSanitaria` |
| AX-DEP-02 | Every `EquipeCampo` belongs exclusively to one `CicloVigilancia` |
| AX-DEP-03 | Every `AreaOperacional` belongs to one `EquipeCampo` and one `ZonaPorCiclo` |
| AX-DEP-04 | Every `PropriedadeEmArea` belongs to exactly one `AreaOperacional` |
| AX-DEP-05 | Every `SubmissaoPropriedade` is linked to one `PropriedadeEmArea` and one `EquipeCampo` |
| AX-DEP-06 | Every `SubmissaoBarreira` is linked to one `BarreiraSanitaria` |
| AX-DEP-07 | Every `AlvoInvestigacao` depends on exactly one `AnaliseSanitaria` |
| AX-DEP-08 | Every `RespostaSanitaria` depends on exactly one `AnaliseSanitaria` |

### Sequence & Temporal Axioms

| ID | Axiom |
|----|-------|
| AX-SEQ-01 | Surveillance cycles are numbered sequentially within a response: `UNIQUE(numeroCiclo, response_id)` |
| AX-SEQ-02 | A cycle can only be closed when all its operational areas are completed |
| AX-SEQ-03 | An operational area is completed when all its properties have been visited |

### Cardinality & Uniqueness Axioms

| ID | Axiom |
|----|-------|
| AX-CARD-01 | A professional can only be convoked once per response: `UNIQUE(user_id, response_id)` |
| AX-CARD-02 | An establishment can be the target of multiple simultaneous investigations (no uniqueness constraint) |
| AX-CARD-03 | A team can have multiple members (1:N) |
| AX-CARD-04 | A response can have at most one Command Post (1:1) |

### State Axioms

| ID | Axiom | States |
|----|-------|--------|
| AX-STATE-01 | `AnaliseSanitaria` can be active or inactive | `{ativa, inativa}` |
| AX-STATE-02 | `RespostaSanitaria` can be active, completed, or soft-deleted | `{ativa, concluida}` |
| AX-STATE-03 | `ZonaPorCiclo` can be open or closed | `{aberta, fechada}` |
| AX-STATE-04 | `PropriedadeEmArea` can be complete or pending (`isCompleted`) | `{pendente, completa}` |

---

## 8. Model Dictionary

### Core

| Concept | Definition |
|---------|-----------|
| **Estabelecimento** | Unidade produtiva rural cadastrada no serviço veterinário, com código SDA único |
| **Endereço** | Dados de localização de um estabelecimento (logradouro, município, UF, coordenadas) |
| **Pessoa** | Pessoa física cadastrada no Serviço Veterinário Oficial (SVO) com credenciais de acesso |
| **Espécie Animal** | Classificação das espécies animais exploradas (bovinos, suínos, aves, ovinos, caprinos) |
| **Frigorífico** | Estabelecimento de abate com tipo de inspeção sanitária (SIF, SIE, SIM) |
| **Granja Suína** | Estabelecimento especializado em produção suína |
| **Granja Avícola** | Estabelecimento especializado em produção avícola |
| **CAR** | Registro público do perímetro geoespacial da propriedade rural |

### Investigação Sanitária

| Concept | Definition |
|---------|-----------|
| **Análise Sanitária** | Registro de abertura de investigação epidemiológica sobre suspeita de doença |
| **Alvo de Investigação** | Propriedade delimitada como foco da investigação, com coordenadas e raios de zona |
| **Área Afetada** | Região geográfica (municípios, polígonos) sob investigação |
| **Zona de Controle** | Perímetro geográfico ao redor de um alvo (Perifoco, Vigilância, Proteção, Investigação) |
| **Movimentação Animal** | Registro de trânsito animal (GTA) entre propriedades, por espécie |
| **Propriedade Contactante** | Propriedade com contato direto ou indireto com uma propriedade investigada |
| **Categoria de Espécie** | Classificação sanitária das espécies (aves, suínos, ovinos, bovinos, outros) |

### Resposta Sanitária

| Concept | Definition |
|---------|-----------|
| **Resposta Sanitária** | Registro central da coordenação de contenção de um foco sanitário |
| **Ciclo de Vigilância** | Rodada numerada de varredura em zona de controle |
| **Zona por Ciclo** | Delimitação geoespacial de cada zona dentro de um ciclo específico |
| **Equipe de Campo** | Grupo de profissionais alocados a operações de vigilância |
| **Membro de Equipe** | Pessoa vinculada a uma equipe com função específica |
| **Função** | Papel predefinido (membro, modelagem de barreira, modelagem de vigilância) |
| **Área Operacional** | Setor geográfico atribuído a uma equipe dentro de uma zona |
| **Propriedade em Área** | Vínculo entre propriedade e área operacional com controle de conclusão |
| **Barreira Sanitária** | Posto fixo ou volante para fiscalização de trânsito animal |
| **Veículo** | Viatura vinculada às equipes de campo |
| **Posto de Comando** | QG da operação de resposta, com endereço e coordenadas |
| **Usuário Convocado** | Pessoa mobilizada para uma resposta com permissões específicas |
| **Rastreamento GPS** | Registro do deslocamento de equipes em campo |
| **Tipo de Equipe** | Classificação funcional (vigilância, barreira, vacinação, etc.) |

### Ações em Campo

| Concept | Definition |
|---------|-----------|
| **Submissão de Propriedade** | Formulário preenchido na visita a uma propriedade |
| **Submissão de Barreira** | Formulário preenchido em barreira sanitária |
| **Propriedade Temporária** | Unidade não cadastrada encontrada em campo |

---

## 9. Verification (Competency Question × Model)

| CQ | Answer Path |
|----|-------------|
| CQ-CORE-01 | `Estabelecimento` instances |
| CQ-CORE-02 | `Estabelecimento.especies` |
| CQ-CORE-03 | `Estabelecimento → Endereço.coordenadas` |
| CQ-INV-01 | `AlvoInvestigacao → Estabelecimento` filtered by zone radius |
| CQ-INV-03 | `MovimentacaoAnimal(origem/destino = Estabelecimento)` |
| CQ-RES-01 | `RespostaSanitaria → CicloVigilancia` |
| CQ-RES-02 | `CicloVigilancia → EquipeCampo` |
| CQ-RES-03 | `EquipeCampo → MembroEquipe → Pessoa` |
| CQ-RES-09 | `RespostaSanitaria → CicloVigilancia → EquipeCampo → Barreira` |
| CQ-CAM-01 | `AreaOperacional → PropriedadeEmArea → SubmissaoPropriedade` |
| CQ-CAM-02 | `PropriedadeEmArea.concluida` |

*Complete verification table in `03-cap-mode-ontouml.md` Section 8.*

---

## 10. Version Control

| Version | Date | Description |
|---------|------|-------------|
| v.01 | 24/06/2026 | Versão completa da ontologia de referência SIGEVS-O |
| v.02 | 04/07/2026 | Renomeado Profissional→Pessoa; removido ModuloAcesso e LogAuditoria; CategoriaEspecie como Enumeration; total 32 classes |

---

## 11. References

- Ontology Specification Document: `../1-requirements/04-doc-spec.md`
- Reference Ontology Premises: `../2-setup/01-doc-refe.md`
- Concept Catalog: `01-cap-cata.md`
- Axioms: `02-cap-axim.md`
- OntoUML Model: `03-cap-mode-ontouml.md`
- OntoUML JSON (ontouml-schema): `04-sigevs-o.ontouml.json`
- Guia de Captura: `00-guia-captura.md`
- Código Fonte: `C:\LUMAC\sigevs-api\`
