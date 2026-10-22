# Fase de Captura — CAP-MODE (Modelo OntoUML)

---

## Modelo Conceitual OntoUML — SIGEVS-O

| Campo | Valor |
|-------|-------|
| Ontologia: | SIGEVS-O — Ontology for Sanitary Event Management |
| Linguagem: | OntoUML (fundamentada em UFO) |
| Versão: | v.01 |
| Data: | 23/06/2026 |

---

## 1. Diagrama de Pacotes (Subdomínios)

```
┌─────────────────────────────────────────────────────────────────┐
│                        SIGEVS-O                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌───────┐ │
│  │    Core      │  │ Investigação │  │   Resposta   │  │ Campo │ │
│  │              │  │              │  │              │  │       │ │
│  │ <<import>>   │──│ <<import>>   │──│ <<import>>   │──│«uses» │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └───────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Subdomínio: Core

### Classes e Estereótipos UFO

```
┌─────────────────────────────────────────────────────────────────────────┐
│ <<Kind>>                                                               │
│ Estabelecimento                                                        │
├─────────────────────────────────────────────────────────────────────────┤
│ - codigoSDA : String <<identifier>>                                    │
│ - nome : String                                                        │
│ - tipo : String                                                        │
│ - especies : EspecieAnimal[*]                                          │
│ - ativo : Boolean                                                      │
│ - carShape : Poligono <<Quality>>                                      │
├─────────────────────────────────────────────────────────────────────────┤
│ 1 ────────< ▶ 1 Endereco (<<Kind>>)                                    │
│ 1 ────────< ▶ 1 Frigorifico (<<Subkind>>)                              │
│ 1 ────────< ▶ 1 GranjaSuino (<<Subkind>>)                              │
│ 1 ────────< ▶ 1 GranjaAve (<<Subkind>>)                                │
│                                                                         │
│ <<Subkind>>                          <<Kind>>                           │
│ Frigorifico                           Endereco                          │
│ ├── sistemaInspecao : String          ├── logradouro : String           │
│ └── numeroInspecao : String           ├── cidade : String               │
│                                        ├── estado : String              │
│ <<Subkind>>                           ├── cep : String                  │
│ GranjaSuino                           └── coordenadas : CoordGeog <<Q>> │
│ ├── finalidadeExploracao : String                                       │
│ ├── integradora : String              <<Kind>>                          │
│ └── registro : String                  Pessoa                           │
│                                        ├── nome : String                │
│ <<Subkind>>                           ├── cpf : String                 │
│ GranjaAve                             ├── email : String               │
│ ├── especieExploracao : String                                         │
│ ├── formaExploracao : String                                            │
│ └── finalidadeProducao : String      <<Kind>>                          │
│                                        EspecieAnimal                   │
│                                        ├── nome : String                │
│                                        └── categoria : String          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Relacionamentos

| Source | Target | Type | Cardinalidade | Descrição |
|--------|--------|------|---------------|-----------|
| `Estabelecimento` | `Endereco` | Association | 1..* → 1 | Possui |
| `Estabelecimento` | `Frigorifico` | Generalization (Subkind) | — | É um tipo de |
| `Estabelecimento` | `GranjaSuino` | Generalization (Subkind) | — | É um tipo de |
| `Estabelecimento` | `GranjaAve` | Generalization (Subkind) | — | É um tipo de |

---

## 3. Subdomínio: Investigação Sanitária

### Classes e Estereótipos UFO

```
┌──────────────────────────────────────────────────────────────────────────┐
│ <<Event>>                                                               │
│ AnaliseSanitaria                                                        │
├──────────────────────────────────────────────────────────────────────────┤
│ - dataCriacao : DateTime                                                │
│ - nome : String                                                         │
│ - ativa : Boolean                                                       │
│ - publica : Boolean                                                     │
├──────────────────────────────────────────────────────────────────────────┤
│ 1 ────────< ▶ * AlvoInvestigacao (<<Role>>)                            │
│ * ────────< ▶ 1 Pessoa (userCreation)                           │
│ 1 ────────< ▶ * AreaAfetada (<<Kind>>)                                 │
│ 0..1 ────< ▶ * RespostaSanitaria                                       │
│                                                                          │
│ <<Role>> (generaliza: Estabelecimento)    <<Kind>>                      │
│ AlvoInvestigacao                          AreaAfetada                   │
│ ├── latitude : BigDecimal <<Quality>>     ├── nome : String             │
│ ├── longitude : BigDecimal <<Quality>>    └── shape : Poligono          │
│ ├── zona1 : Integer (Perifoco)                                           │
│ ├── zona2 : Integer (Vigilância)          <<Relator>>                    │
│ ├── zona3 : Integer (Proteção)           ZonaControleInvestigacao      │
│ ├── dataInicioMov : LocalDate            ├── tipo : ZoneType <<enum>>  │
│ └── dataFimMov : LocalDate               ├── raio : Integer            │
│                                          1 ──< ▶ * AreaOperacional   │
│                                          (cruzamento: Resposta)        │
│                                                                          │
│ <<Event>>                                     <<Role>>                  │
│ MovimentacaoAnimal (GTA)                      PropriedadeContactante   │
│ ├── serie : String                            (generaliza: Estabelecimento)│
│ ├── numero : String                          ├── tipo: Direta/Indireta │
│ ├── ufOrigem : String                                                    │
│ ├── especie : EspecieAnimal                   <<Enumeration>>           │
│ ├── finalidade : MovementPurpose <<enum>>     CategoriaEspecie          │
│ ├── dataEmissao : LocalDate                                              │
│ ├── estabelecimentoOrigem : Estabelecimento                              │
│ └── estabelecimentoDestino : Estabelecimento                             │
└──────────────────────────────────────────────────────────────────────────┘
```

### Relacionamentos

| Source | Target | Type | Cardinalidade | Descrição |
|--------|--------|------|---------------|-----------|
| `AnaliseSanitaria` | `Pessoa` | Association | * → 1 | Criada por |
| `AnaliseSanitaria` | `AlvoInvestigacao` | Association | 1 → * | Possui |
| `AnaliseSanitaria` | `AreaAfetada` | Association | * → * | Abrange |
| `AlvoInvestigacao` | `ZonaControleInvestigacao` | Association | 1 → 1 | Define |
| `MovimentacaoAnimal` | `Estabelecimento` (origem) | Association | * → 1 | Origem |
| `MovimentacaoAnimal` | `Estabelecimento` (destino) | Association | * → 1 | Destino |
| `ZonaControleInvestigacao` | `AreaOperacional` | Association | 1 → * | Delimita (cruzamento: Investigação → Resposta) |


---

## 4. Subdomínio: Resposta Sanitária

### Classes e Estereótipos UFO

```
┌──────────────────────────────────────────────────────────────────────────┐
│ <<Event>>                                                               │
│ RespostaSanitaria                                                       │
├──────────────────────────────────────────────────────────────────────────┤
│ - identificador : String                                                │
│ - dataCriacao : DateTime                                                │
│ - dataVencimento : LocalDate                                            │
│ - ativa : Boolean                                                       │
│ - concluida : Boolean                                                   │
├──────────────────────────────────────────────────────────────────────────┤
│ 1 ────────< ▶ * CicloVigilancia (<<Event>>)                            │
│ 1 ────────< ▶ * PessoaConvocada (<<Role>>)                            │
│ 1 ────────< ▶ 0..1 PostoComando (<<Kind>>)                             │
│ * ────────< ▶ 1 AnaliseSanitaria                                       │
│                                                                          │
│ <<Event>>                              <<Relator>>                      │
│ CicloVigilancia                        ZonaPorCiclo                     │
│ ├── numeroCiclo : Integer              ├── tipo : ZoneType <<enum>>   │
│ └── concluido : Boolean                ├── dataInicio : LocalDate       │
│    1 ────< ▶ * ZonaPorCiclo            ├── dataFim : LocalDate          │
│    1 ────< ▶ * EquipeCampo             ├── fechada : Boolean            │
│                                         └── boundaryPoints : Poligono    │
│ <<Collective>>                                                          │
│ EquipeCampo                             <<Kind>>                        │
│ ├── nome : String                      PostoComando                    │
│ ├── cor : String                       ├── nome : String               │
│ ├── setor : String                     ├── endereco : String           │
│ ├── ativa : Boolean                    └── coordenadas : CoordGeog     │
│ ├── 1 ──< ▶ * MembroEquipe (<<Role>>)                                   │
│ ├── 1 ──< ▶ * AreaOperacional           <<Kind>>                        │
│ ├── 1 ──< ▶ * Veiculo (<<Kind>>)       TipoEquipe                      │
│ ├── 1 ──< ▶ * BarreiraSanitaria        ├── nome : String               │
│ ├── * ──< ▶ 1 CicloVigilancia          ├── rotulo : String             │
│ └── * ──< ▶ 1 TipoEquipe               ├── setor : String              │
│                                          └── cor : String               │
│ <<Role>> (generaliza: Pessoa)                                             │
│ MembroEquipe                           <<Kind>>                        │
│ ├── ativo : Boolean                    Veiculo                          │
│ └── * ──< ▶ 1 Funcao                   ├── placa : String              │
│                                          ├── modelo : String            │
│ <<Role>> (generaliza: Pessoa)            ├── cor : String                │
│ PessoaConvocada                         ├── marca : String              │
│ ├── sujo : Boolean (quarentena)         └── tipo : String               │
│ ├── dataExpiracaoSujo : LocalDate                                        │
│ ├── permissaoGestao : Boolean           <<Kind>>                        │
│ ├── permissaoObservacao : Boolean       BarreiraSanitaria               │
│ └── * ──< ▶ 1 Funcao                    ├── nome : String              │
│                                          ├── tipo : BarreiraType <<e>> │
│ <<Kind>>                                ├── funcao : BarrierRole <<e>>│
│ AreaOperacional                         └── coordenadas : CoordGeog    │
│ ├── nome : String                                                        │
│ ├── cor : String                        <<Event>>                       │
│ ├── boundaryPoints : Poligono           RastreamentoGPS                │
│ ├── 1 ──< ▶ * PropriedadeEmArea        ├── dataInicio : DateTime       │
│ ├── * ──< ▶ 1 ZonaPorCiclo             ├── dataFim : DateTime          │
│ └── * ──< ▶ 1 ZonaControleInvestigacao └── coordenadas : CoordGeog[*] │
│    (cruzamento: Investigação)                                          │
│                                          └── coordenadas : CoordGeog[*] │
│ <<Relator>>                                                             │
│ PropriedadeEmArea                                                        │
│ ├── concluida : Boolean                                                  │
│ └── * ──< ▶ 1 Estabelecimento                                           │
│     * ──< ▶ 1 AreaOperacional                                            │
│                                                                          │
│ (Phase como atributo:                   <<Kind>>                        │
│  PropriedadeEmArea.concluida : Boolean)  Funcao                          │
│                                          ├── nome : String              │
│                                          └── rotulo : String            │
└──────────────────────────────────────────────────────────────────────────┘
```

### Relacionamentos

| Source | Target | Type | Cardinalidade | Descrição |
|--------|--------|------|---------------|-----------|
| `RespostaSanitaria` | `AnaliseSanitaria` | Association | * → 1 | Baseada em |
| `RespostaSanitaria` | `CicloVigilancia` | Association | 1 → * | Possui |
| `RespostaSanitaria` | `PostoComando` | Association | 0..1 → 1 | Tem |
| `RespostaSanitaria` | `PessoaConvocada` | Association | 1 → * | Convoca |
| `CicloVigilancia` | `ZonaPorCiclo` | Association | 1 → * | Subdivide-se |
| `CicloVigilancia` | `EquipeCampo` | Association | 1 → * | Aloca |
| `EquipeCampo` | `TipoEquipe` | Association | * → 1 | Classifica-se |
| `EquipeCampo` | `MembroEquipe` | memberOf | 1 → * | Composta por |
| `EquipeCampo` | `AreaOperacional` | Association | 1 → * | Atua em |
| `EquipeCampo` | `Veiculo` | Association | 1 → * | Utiliza |
| `EquipeCampo` | `BarreiraSanitaria` | Association | 1 → * | Opera |
| `MembroEquipe` | `Funcao` | Association | * → 1 | Desempenha |
| `AreaOperacional` | `ZonaPorCiclo` | Association | * → 1 | Pertence a |
| `AreaOperacional` | `PropriedadeEmArea` | Association | 1 → * | Contém |
| `PropriedadeEmArea` | `Estabelecimento` | Association | * → 1 | Refere-se a |
| `PessoaConvocada` | `Funcao` | Association | * → 1 | Desempenha |
| `PessoaConvocada` | `MembroEquipe` | Association | 0..1 → 1 | Alocado como |
| `RastreamentoGPS` | `Veiculo` | Association | * → 1 | Rastreia |

---

## 5. Subdomínio: Ações em Campo

### Classes e Estereótipos UFO

```
┌──────────────────────────────────────────────────────────────────────────┐
│ <<Event>>                                                               │
│ SubmissaoPropriedade                                                    │
├──────────────────────────────────────────────────────────────────────────┤
│ - uuid : UUID                                                           │
│ - dataHora : DateTime                                                   │
├──────────────────────────────────────────────────────────────────────────┤
│ * ────────< ▶ 1 PropriedadeEmArea                                      │
│ * ────────< ▶ 1 EquipeCampo                                            │
│                                                                          │
│ <<Event>>                                                               │
│ SubmissaoBarreira                                                       │
├──────────────────────────────────────────────────────────────────────────┤
│ - uuid : UUID                                                           │
│ - dataHora : DateTime                                                   │
├──────────────────────────────────────────────────────────────────────────┤
│ * ────────< ▶ 1 BarreiraSanitaria                                       │
│                                                                          │
│ <<Role>> (generaliza: Estabelecimento)                                   │
│ PropriedadeTemporaria                                                     │
│ ├── nomeContato : String                                                 │
│ ├── cpfCnpj : String                                                     │
│ ├── telefone : String                                                    │
│ └── coordenadas : CoordGeog                                              │
│ (Phase como atributo:                                                    │
│  PropriedadeEmArea.concluida : Boolean)                                  │
└──────────────────────────────────────────────────────────────────────────┘
```

### Relacionamentos

| Source | Target | Type | Cardinalidade | Descrição |
|--------|--------|------|---------------|-----------|
| `SubmissaoPropriedade` | `PropriedadeEmArea` | Association | * → 1 | Vinculada a |
| `SubmissaoPropriedade` | `EquipeCampo` | Association | * → 1 | Realizada por |
| `SubmissaoBarreira` | `BarreiraSanitaria` | Association | * → 1 | Vinculada a |
| `Estabelecimento` | `EspecieAnimal` | Association | * → * | Possui |
| `EspecieAnimal` | `CategoriaEspecie` | Association | * → 1 | Categoriza-se |

---

## 6. Mapa de Generalizações

```
<<Kind>> Estabelecimento
    ├── <<Subkind>> Frigorifico
    ├── <<Subkind>> GranjaSuino
    ├── <<Subkind>> GranjaAve
    ├── <<Role>> AlvoInvestigacao (restrictedTo = kind)
    ├── <<Role>> PropriedadeContactante (restrictedTo = kind)
    └── <<Role>> PropriedadeTemporaria (restrictedTo = kind)

<<Kind>> Pessoa
    ├── <<Role>> MembroEquipe (restrictedTo = kind)
    └── <<Role>> PessoaConvocada (restrictedTo = kind)
```

---

## 7. Mapa de Enums

| Enum | Tipo | Valores | Uso |
|------|------|---------|-----|
| `ZoneType` | `<<Enum>>` | INFECTED, BUFFER, SURVEILLANCE, INVESTIGATION | ZonaControle, ZonaPorCiclo |
| `BarreiraType` | `<<Enum>>` | FIXED, MOBILE | BarreiraSanitaria.tipo |
| `BarreiraRole` | `<<Enum>>` | SANITARY, DIVERSION | BarreiraSanitaria.funcao |
| `MovimentoPurpose` | `<<Enum>>` | ABATE, ENGORDA, OUTROS | MovimentacaoAnimal.finalidade |
| `EspecieCategoria` | `<<Enum>>` | AVES, SUINOS, OVINOS, BOVINOS, OUTROS | CategoriaEspecie |

---

## 8. Verificação de Questões de Competência

| CQ | Resposta no Modelo |
|----|--------------------|
| CQ-CORE-01 | `Estabelecimento>> todas as instâncias` |
| CQ-CORE-02 | `Estabelecimento.especies` |
| CQ-CORE-03 | `Endereco.coordenadas` via `Estabelecimento > Endereco` |
| CQ-CORE-04 | `Pessoa` filtrado por região |
| CQ-INV-01 | `AlvoInvestigacao > ZonaControle(raio) > Estabelecimento` |
| CQ-INV-02 | `AlvoInvestigacao` múltiplos para mesmo `Estabelecimento` |
| CQ-INV-03 | `MovimentacaoAnimal(origem/destino = Estabelecimento)` |
| CQ-INV-04 | `MovimentacaoAnimal > EstabelecimentoContactante(direta)` |
| CQ-INV-06 | `AlvoInvestigacao > ZonaControle` |
| CQ-RES-01 | `RespostaSanitaria > CicloVigilancia` |
| CQ-RES-02 | `CicloVigilancia > EquipeCampo` |
| CQ-RES-03 | `EquipeCampo > MembroEquipe > Pessoa` |
| CQ-RES-04 | `BarreiraSanitaria` via `EquipeCampo > CicloVigilancia` |
| CQ-RES-06 | `RastreamentoGPS(equipe, data)` |
| CQ-RES-08 | `EquipeCampo > AreaOperacional` |
| CQ-RES-09 | `RespostaSanitaria > CicloVigilancia > EquipeCampo > Barreira` |
| CQ-RES-10 | `AreaOperacional > PropriedadeEmArea > Estabelecimento` |
| CQ-RES-12 | `EquipeCampo > Veiculo` |
| CQ-CAM-01 | `AreaOperacional > PropriedadeEmArea > SubmissaoPropriedade` |
| CQ-CAM-02 | `PropriedadeEmArea.concluida` |
| CQ-CAM-03 | `EquipeCampo > SubmissaoPropriedade` |

---

## 9. Referências

- Catálogo de Conceitos: `01-cap-cata.md`
- Axiomas: `02-cap-axim.md`
- Guia de Captura: `00-guia-captura.md`
- Ontology Specification Document: `../1-requirements/04-doc-spec.md`
