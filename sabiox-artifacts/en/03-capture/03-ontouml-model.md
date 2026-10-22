# Capture Phase — CAP-MODE (OntoUML Model)

---

## OntoUML Conceptual Model — SIGEVS-O

| Field | Value |
|-------|-------|
| Ontology: | SIGEVS-O — Ontology for Sanitary Event Management |
| Language: | OntoUML (grounded in UFO) |
| Version: | v.01 |
| Date: | 06/23/2026 |

---

## 1. Package Diagram (Subdomains)

```
┌─────────────────────────────────────────────────────────────────┐
│                        SIGEVS-O                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌───────┐ │
│  │    Core      │  │ Investigation │  │   Response   │  │ Field │ │
│  │              │  │              │  │              │  │       │ │
│  │ <<import>>   │──│ <<import>>   │──│ <<import>>   │──│«uses» │ │
│  └──────────────┘  └──────────────┘  └──────────────┘  └───────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Subdomain: Core

### Classes and UFO Stereotypes

```
┌─────────────────────────────────────────────────────────────────────────┐
│ <<Kind>>                                                               │
│ Establishment                                                          │
├─────────────────────────────────────────────────────────────────────────┤
│ - codigoSDA : String <<identifier>>                                    │
│ - nome : String                                                        │
│ - tipo : String                                                        │
│ - especies : AnimalSpecies[*]                                          │
│ - ativo : Boolean                                                      │
│ - carShape : Polygon <<Quality>>                                       │
├─────────────────────────────────────────────────────────────────────────┤
│ 1 ────────< ▶ 1 Address (<<Kind>>)                                    │
│ 1 ────────< ▶ 1 Slaughterhouse (<<Subkind>>)                          │
│ 1 ────────< ▶ 1 SwineFarm (<<Subkind>>)                               │
│ 1 ────────< ▶ 1 PoultryFarm (<<Subkind>>)                             │
│                                                                         │
│ <<Subkind>>                          <<Kind>>                           │
│ Slaughterhouse                        Address                           │
│ ├── sistemaInspecao : String          ├── logradouro : String           │
│ └── numeroInspecao : String           ├── cidade : String               │
│                                        ├── estado : String              │
│ <<Subkind>>                           ├── cep : String                  │
│ SwineFarm                             └── coordenadas : GeoCoord <<Q>> │
│ ├── finalidadeExploracao : String                                       │
│ ├── integradora : String              <<Kind>>                          │
│ └── registro : String                  Person                           │
│                                        ├── nome : String                │
│ <<Subkind>>                           ├── cpf : String                 │
│ PoultryFarm                           ├── email : String               │
│ ├── especieExploracao : String                                         │
│ ├── formaExploracao : String                                            │
│ └── finalidadeProducao : String      <<Kind>>                          │
│                                        AnimalSpecies                   │
│                                        ├── nome : String                │
│                                        └── categoria : String          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Relationships

| Source | Target | Type | Cardinality | Description |
|--------|--------|------|-------------|-------------|
| `Establishment` | `Address` | Association | 1..* → 1 | Has |
| `Establishment` | `Slaughterhouse` | Generalization (Subkind) | — | Is a type of |
| `Establishment` | `SwineFarm` | Generalization (Subkind) | — | Is a type of |
| `Establishment` | `PoultryFarm` | Generalization (Subkind) | — | Is a type of |

---

## 3. Subdomain: Sanitary Investigation

### Classes and UFO Stereotypes

```
┌──────────────────────────────────────────────────────────────────────────┐
│ <<Event>>                                                               │
│ SanitaryAnalysis                                                        │
├──────────────────────────────────────────────────────────────────────────┤
│ - dataCriacao : DateTime                                                │
│ - nome : String                                                         │
│ - ativa : Boolean                                                       │
│ - publica : Boolean                                                     │
├──────────────────────────────────────────────────────────────────────────┤
│ 1 ────────< ▶ * InvestigationTarget (<<Role>>)                         │
│ * ────────< ▶ 1 Person (userCreation)                                  │
│ 1 ────────< ▶ * AffectedArea (<<Kind>>)                                │
│ 0..1 ────< ▶ * SanitaryResponse                                        │
│                                                                          │
│ <<Role>> (generalizes: Establishment)    <<Kind>>                       │
│ InvestigationTarget                   AffectedArea                      │
│ ├── latitude : BigDecimal <<Quality>> ├── nome : String                 │
│ ├── longitude : BigDecimal <<Quality>>└── shape : Polygon               │
│ ├── zona1 : Integer (Perifoco)                                           │
│ ├── zona2 : Integer (Vigilância)         <<Relator>>                    │
│ ├── zona3 : Integer (Proteção)          InvestigationControlZone       │
│ ├── dataInicioMov : LocalDate           ├── tipo : ZoneType <<enum>>   │
│ └── dataFimMov : LocalDate              ├── raio : Integer             │
│                                         1 ──< ▶ * OperationalArea      │
│                                         (crossing: Response)            │
│                                                                          │
│ <<Event>>                                     <<Role>>                  │
│ AnimalMovement (GTA)                          ContactingProperty        │
│ ├── serie : String                            (generalizes: Establishment)│
│ ├── numero : String                          ├── tipo: Direct/Indirect  │
│ ├── ufOrigem : String                                                    │
│ ├── especie : AnimalSpecies                   <<Enumeration>>           │
│ ├── finalidade : MovementPurpose <<enum>>     SpeciesCategory           │
│ ├── dataEmissao : LocalDate                                              │
│ ├── estabelecimentoOrigem : Establishment                              │
│ └── estabelecimentoDestino : Establishment                             │
└──────────────────────────────────────────────────────────────────────────┘
```

### Relationships

| Source | Target | Type | Cardinality | Description |
|--------|--------|------|-------------|-------------|
| `SanitaryAnalysis` | `Person` | Association | * → 1 | Created by |
| `SanitaryAnalysis` | `InvestigationTarget` | Association | 1 → * | Has |
| `SanitaryAnalysis` | `AffectedArea` | Association | * → * | Covers |
| `InvestigationTarget` | `InvestigationControlZone` | Association | 1 → 1 | Defines |
| `AnimalMovement` | `Establishment` (origin) | Association | * → 1 | Origin |
| `AnimalMovement` | `Establishment` (destination) | Association | * → 1 | Destination |
| `InvestigationControlZone` | `OperationalArea` | Association | 1 → * | Delimits (crossing: Investigation → Response) |


---

## 4. Subdomain: Sanitary Response

### Classes and UFO Stereotypes

```
┌──────────────────────────────────────────────────────────────────────────┐
│ <<Event>>                                                               │
│ SanitaryResponse                                                        │
├──────────────────────────────────────────────────────────────────────────┤
│ - identificador : String                                                │
│ - dataCriacao : DateTime                                                │
│ - dataVencimento : LocalDate                                            │
│ - ativa : Boolean                                                       │
│ - concluida : Boolean                                                   │
├──────────────────────────────────────────────────────────────────────────┤
│ 1 ────────< ▶ * SurveillanceCycle (<<Event>>)                          │
│ 1 ────────< ▶ * ConvokedPerson (<<Role>>)                              │
│ 1 ────────< ▶ 0..1 CommandPost (<<Kind>>)                              │
│ * ────────< ▶ 1 SanitaryAnalysis                                       │
│                                                                          │
│ <<Event>>                              <<Relator>>                      │
│ SurveillanceCycle                      ZonePerCycle                     │
│ ├── numeroCiclo : Integer              ├── tipo : ZoneType <<enum>>   │
│ └── concluido : Boolean                ├── dataInicio : LocalDate       │
│    1 ────< ▶ * ZonePerCycle            ├── dataFim : LocalDate          │
│    1 ────< ▶ * FieldTeam              ├── fechada : Boolean            │
│                                         └── boundaryPoints : Polygon    │
│ <<Collective>>                                                          │
│ FieldTeam                              <<Kind>>                        │
│ ├── nome : String                      CommandPost                     │
│ ├── cor : String                       ├── nome : String               │
│ ├── setor : String                     ├── endereco : String           │
│ ├── ativa : Boolean                    └── coordenadas : GeoCoord      │
│ ├── 1 ──< ▶ * TeamMember (<<Role>>)                                    │
│ ├── 1 ──< ▶ * OperationalArea          <<Kind>>                        │
│ ├── 1 ──< ▶ * Vehicle (<<Kind>>)       TeamType                        │
│ ├── 1 ──< ▶ * SanitaryBarrier          ├── nome : String               │
│ ├── * ──< ▶ 1 SurveillanceCycle        ├── rotulo : String             │
│ └── * ──< ▶ 1 TeamType                 ├── setor : String              │
│                                          └── cor : String               │
│ <<Role>> (generalizes: Person)                                          │
│ TeamMember                            <<Kind>>                        │
│ ├── ativo : Boolean                   Vehicle                          │
│ └── * ──< ▶ 1 Function                ├── placa : String              │
│                                          ├── modelo : String            │
│ <<Role>> (generalizes: Person)           ├── cor : String                │
│ ConvokedPerson                         ├── marca : String              │
│ ├── sujo : Boolean (quarantine)        └── tipo : String               │
│ ├── dataExpiracaoSujo : LocalDate                                        │
│ ├── permissaoGestao : Boolean          <<Kind>>                        │
│ ├── permissaoObservacao : Boolean      SanitaryBarrier                 │
│ └── * ──< ▶ 1 Function                 ├── nome : String              │
│                                          ├── tipo : BarrierType <<e>>  │
│ <<Kind>>                               ├── funcao : BarrierRole <<e>> │
│ OperationalArea                        └── coordenadas : GeoCoord     │
│ ├── nome : String                                                       │
│ ├── cor : String                       <<Event>>                       │
│ ├── boundaryPoints : Polygon           GPSTracking                    │
│ ├── 1 ──< ▶ * PropertyInArea          ├── dataInicio : DateTime       │
│ ├── * ──< ▶ 1 ZonePerCycle            ├── dataFim : DateTime          │
│ └── * ──< ▶ 1 InvestigationControlZone└── coordenadas : GeoCoord[*]   │
│    (crossing: Investigation)                                          │
│                                         └── coordenadas : GeoCoord[*]  │
│ <<Relator>>                                                            │
│ PropertyInArea                                                       │
│ ├── concluida : Boolean                                                 │
│ └── * ──< ▶ 1 Establishment                                          │
│     * ──< ▶ 1 OperationalArea                                          │
│                                                                         │
│ (Phase as attribute:                  <<Kind>>                        │
│  PropertyInArea.concluida : Boolean)  Function                         │
│                                         ├── nome : String              │
│                                         └── rotulo : String            │
└──────────────────────────────────────────────────────────────────────────┘
```

### Relationships

| Source | Target | Type | Cardinality | Description |
|--------|--------|------|-------------|-------------|
| `SanitaryResponse` | `SanitaryAnalysis` | Association | * → 1 | Based on |
| `SanitaryResponse` | `SurveillanceCycle` | Association | 1 → * | Has |
| `SanitaryResponse` | `CommandPost` | Association | 0..1 → 1 | Has |
| `SanitaryResponse` | `ConvokedPerson` | Association | 1 → * | Convenes |
| `SurveillanceCycle` | `ZonePerCycle` | Association | 1 → * | Subdivides into |
| `SurveillanceCycle` | `FieldTeam` | Association | 1 → * | Allocates |
| `FieldTeam` | `TeamType` | Association | * → 1 | Classified as |
| `FieldTeam` | `TeamMember` | memberOf | 1 → * | Composed of |
| `FieldTeam` | `OperationalArea` | Association | 1 → * | Acts in |
| `FieldTeam` | `Vehicle` | Association | 1 → * | Uses |
| `FieldTeam` | `SanitaryBarrier` | Association | 1 → * | Operates |
| `TeamMember` | `Function` | Association | * → 1 | Performs |
| `OperationalArea` | `ZonePerCycle` | Association | * → 1 | Belongs to |
| `OperationalArea` | `PropertyInArea` | Association | 1 → * | Contains |
| `PropertyInArea` | `Establishment` | Association | * → 1 | Refers to |
| `ConvokedPerson` | `Function` | Association | * → 1 | Performs |
| `ConvokedPerson` | `TeamMember` | Association | 0..1 → 1 | Allocated as |
| `GPSTracking` | `Vehicle` | Association | * → 1 | Tracks |

---

## 5. Subdomain: Field Actions

### Classes and UFO Stereotypes

```
┌──────────────────────────────────────────────────────────────────────────┐
│ <<Event>>                                                               │
│ PropertySubmission                                                      │
├──────────────────────────────────────────────────────────────────────────┤
│ - uuid : UUID                                                           │
│ - dataHora : DateTime                                                   │
├──────────────────────────────────────────────────────────────────────────┤
│ * ────────< ▶ 1 PropertyInArea                                         │
│ * ────────< ▶ 1 FieldTeam                                              │
│                                                                          │
│ <<Event>>                                                               │
│ BarrierSubmission                                                       │
├──────────────────────────────────────────────────────────────────────────┤
│ - uuid : UUID                                                           │
│ - dataHora : DateTime                                                   │
├──────────────────────────────────────────────────────────────────────────┤
│ * ────────< ▶ 1 SanitaryBarrier                                         │
│                                                                          │
│ <<Role>> (generalizes: Establishment)                                   │
│ TemporaryProperty                                                       │
│ ├── nomeContato : String                                                │
│ ├── cpfCnpj : String                                                    │
│ ├── telefone : String                                                   │
│ └── coordenadas : GeoCoord                                              │
│ (Phase as attribute:                                                    │
│  PropertyInArea.concluida : Boolean)                                    │
└──────────────────────────────────────────────────────────────────────────┘
```

### Relationships

| Source | Target | Type | Cardinality | Description |
|--------|--------|------|-------------|-------------|
| `PropertySubmission` | `PropertyInArea` | Association | * → 1 | Linked to |
| `PropertySubmission` | `FieldTeam` | Association | * → 1 | Performed by |
| `BarrierSubmission` | `SanitaryBarrier` | Association | * → 1 | Linked to |
| `Establishment` | `AnimalSpecies` | Association | * → * | Has |
| `AnimalSpecies` | `SpeciesCategory` | Association | * → 1 | Classified as |

---

## 6. Generalization Map

```
<<Kind>> Establishment
    ├── <<Subkind>> Slaughterhouse
    ├── <<Subkind>> SwineFarm
    ├── <<Subkind>> PoultryFarm
    ├── <<Role>> InvestigationTarget (restrictedTo = kind)
    ├── <<Role>> ContactingProperty (restrictedTo = kind)
    └── <<Role>> TemporaryProperty (restrictedTo = kind)

<<Kind>> Person
    ├── <<Role>> TeamMember (restrictedTo = kind)
    └── <<Role>> ConvokedPerson (restrictedTo = kind)
```

---

## 7. Enum Map

| Enum | Type | Values | Usage |
|------|------|--------|-------|
| `ZoneType` | `<<Enum>>` | INFECTED, BUFFER, SURVEILLANCE, INVESTIGATION | ControlZone, ZonePerCycle |
| `BarrierType` | `<<Enum>>` | FIXED, MOBILE | SanitaryBarrier.tipo |
| `BarrierRole` | `<<Enum>>` | SANITARY, DIVERSION | SanitaryBarrier.funcao |
| `MovementPurpose` | `<<Enum>>` | ABATE, ENGORDA, OUTROS | AnimalMovement.finalidade |
| `SpeciesCategory` | `<<Enum>>` | AVES, SUINOS, OVINOS, BOVINOS, OUTROS | SpeciesCategory |

---

## 8. Competency Question Verification

| CQ | Model Answer |
|----|--------------|
| CQ-CORE-01 | `Establishment>> all instances` |
| CQ-CORE-02 | `Establishment.especies` |
| CQ-CORE-03 | `Address.coordenadas` via `Establishment > Address` |
| CQ-CORE-04 | `Person` filtered by region |
| CQ-INV-01 | `InvestigationTarget > ControlZone(radius) > Establishment` |
| CQ-INV-02 | `InvestigationTarget` multiple for same `Establishment` |
| CQ-INV-03 | `AnimalMovement(origin/destination = Establishment)` |
| CQ-INV-04 | `AnimalMovement > ContactingEstablishment(direct)` |
| CQ-INV-06 | `InvestigationTarget > ControlZone` |
| CQ-RES-01 | `SanitaryResponse > SurveillanceCycle` |
| CQ-RES-02 | `SurveillanceCycle > FieldTeam` |
| CQ-RES-03 | `FieldTeam > TeamMember > Person` |
| CQ-RES-04 | `SanitaryBarrier` via `FieldTeam > SurveillanceCycle` |
| CQ-RES-06 | `GPSTracking(team, date)` |
| CQ-RES-08 | `FieldTeam > OperationalArea` |
| CQ-RES-09 | `SanitaryResponse > SurveillanceCycle > FieldTeam > Barrier` |
| CQ-RES-10 | `OperationalArea > PropertyInArea > Establishment` |
| CQ-RES-12 | `FieldTeam > Vehicle` |
| CQ-CAM-01 | `OperationalArea > PropertyInArea > PropertySubmission` |
| CQ-CAM-02 | `PropertyInArea.concluida` |
| CQ-CAM-03 | `FieldTeam > PropertySubmission` |

---

## 9. References

- Concept Catalog: `01-cap-cata.md`
- Axioms: `02-cap-axim.md`
- Capture Guide: `00-capture-guide.md`
- Ontology Specification Document: `../1-requirements/04-doc-spec.md`
