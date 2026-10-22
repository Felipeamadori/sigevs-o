# Classes (31)

| # | Nome | Estereótipo |
|---|------|------------|
| 1 | Estabelecimento | «kind» |
| 2 | Endereco | «kind» |
| 3 | Pessoa | «kind» |
| 4 | EspecieAnimal | «kind» |
| 5 | Frigorifico | «subkind» |
| 6 | GranjaAve | «subkind» |
| 7 | GranjaSuino | «subkind» |
| 8 | AnaliseSanitaria | «event» |
| 9 | AlvoInvestigacao | «role» |
| 10 | AreaAfetada | «kind» |
| 11 | ZonaControleInvestigacao | «relator» |
| 12 | MovimentacaoAnimal | «event» |
| 13 | PropriedadeContactante | «role» |
| 14 | CategoriaEspecie | «enumeration» |
| 15 | RespostaSanitaria | «event» |
| 16 | CicloVigilancia | «event» |
| 17 | ZonaPorCiclo | «relator» |
| 18 | EquipeCampo | «collective» |
| 19 | MembroEquipe | «role» |
| 20 | Funcao | «kind» |
| 21 | AreaOperacional | «kind» |
| 22 | PropriedadeEmArea | «relator» |
| 23 | BarreiraSanitaria | «kind» |
| 24 | Veiculo | «kind» |
| 25 | PostoComando | «kind» |
| 26 | PessoaConvocada | «role» |
| 27 | RastreamentoGPS | «event» |
| 28 | TipoEquipe | «kind» |
| 29 | SubmissaoPropriedade | «event» |
| 30 | SubmissaoBarreira | «event» |
| 31 | PropriedadeTemporaria | «role» |

# Generalizações (8)

- Frigorifico → Estabelecimento
- GranjaAve → Estabelecimento
- GranjaSuino → Estabelecimento
- AlvoInvestigacao → Estabelecimento (restrictedTo = kind)
- PropriedadeContactante → Estabelecimento (restrictedTo = kind)
- MembroEquipe → Pessoa (restrictedTo = kind)
- PessoaConvocada → Pessoa (restrictedTo = kind)
- PropriedadeTemporaria → Estabelecimento (restrictedTo = kind)

# Relacionamentos (31)

| # | Source | Target | Estereótipo | Source Card | Target Card | Nome |
|---|--------|--------|------------|-------------|-------------|------|
| R01 | Estabelecimento | Endereco | — | 1..* | 1 | |
| R03 | AnaliseSanitaria | Pessoa | — | * | 1 | Criada por |
| R04 | AnaliseSanitaria | AlvoInvestigacao | — | 1 | * | |
| R05 | AnaliseSanitaria | AreaAfetada | — | * | * | |
| — | ~~R06~~ | ~~AlvoInvestigacao → Estabelecimento~~ | ~~«material»~~ | ~~0..*~~ | ~~1~~ | ~~substituído por generalização~~ |
| R06 | AlvoInvestigacao | ZonaControleInvestigacao | «mediation» | 1 | 1 | |
| R07 | MovimentacaoAnimal | Estabelecimento | — | * | 1 | Origem |
| R08 | MovimentacaoAnimal | Estabelecimento | — | * | 1 | Destino |
| — | ~~R09~~ | ~~PropriedadeContactante → Estabelecimento~~ | ~~«material»~~ | ~~0..*~~ | ~~1~~ | ~~substituído por generalização~~ |
| R09 | RespostaSanitaria | AnaliseSanitaria | — | * | 1 | Baseada em |
| R10 | RespostaSanitaria | CicloVigilancia | — | 1 | * | Possui |
| R11 | RespostaSanitaria | PostoComando | — | 0..1 | 1 | Tem |
| R12 | RespostaSanitaria | PessoaConvocada | — | 1 | * | Convoca |
| R13 | CicloVigilancia | ZonaPorCiclo | «mediation» | 1 | * | Subdivide-se |
| R14 | CicloVigilancia | EquipeCampo | — | 1 | * | Aloca |
| R15 | EquipeCampo | TipoEquipe | — | * | 1 | Classifica-se |
| R16 | EquipeCampo | MembroEquipe | «memberOf» | 1 | * | Composta por |
| R17 | EquipeCampo | AreaOperacional | — | 1 | * | Atua em |
| R18 | EquipeCampo | Veiculo | — | 1 | * | Utiliza |
| R19 | EquipeCampo | BarreiraSanitaria | — | 1 | * | Opera |
| — | ~~R20~~ | ~~MembroEquipe → Pessoa~~ | ~~«material»~~ | ~~*~~ | ~~1~~ | ~~substituído por generalização~~ |
| R20 | MembroEquipe | Funcao | — | * | 1 | Desempenha |
| R21 | AreaOperacional | ZonaPorCiclo | «mediation» | * | 1 | Pertence a |
| R22 | AreaOperacional | PropriedadeEmArea | «mediation» | 1 | * | Contém |
| R23 | PropriedadeEmArea | Estabelecimento | «mediation» | * | 1 | Refere-se a |
| — | ~~R24~~ | ~~PropriedadeEmArea → AreaOperacional~~ | ~~—~~ | ~~*~~ | ~~1~~ | ~~Está em (duplicata de R22)~~ |
| — | ~~R25~~ | ~~PessoaConvocada → Pessoa~~ | ~~«material»~~ | ~~*~~ | ~~1~~ | ~~substituído por generalização~~ |
| R24 | PessoaConvocada | Funcao | — | * | 1 | Desempenha |
| R25 | SubmissaoPropriedade | PropriedadeEmArea | — | * | 1 | Vinculada a |
| R26 | SubmissaoPropriedade | EquipeCampo | — | * | 1 | Realizada por |
| R27 | SubmissaoBarreira | BarreiraSanitaria | — | * | 1 | Vinculada a |
| — | ~~R28~~ | ~~PropriedadeTemporaria → Estabelecimento~~ | ~~«material»~~ | ~~0..1~~ | ~~1~~ | ~~substituído por generalização~~ |
| R28 | PessoaConvocada | MembroEquipe | — | 0..1 | 1 | Alocado como |
| R29 | Estabelecimento | EspecieAnimal | — | * | * | |
| R30 | EspecieAnimal | CategoriaEspecie | — | * | 1 | |
| R31 | RastreamentoGPS | Veiculo | — | * | 1 | |
| R32 | ZonaControleInvestigacao | AreaOperacional | «mediation» | 1 | * | Delimita |
