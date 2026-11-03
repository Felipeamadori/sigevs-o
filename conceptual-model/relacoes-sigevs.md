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

# Relacionamentos (29)

| # | Source | Target | Estereótipo | Source Card | Target Card | Nome |
|---|--------|--------|------------|-------------|-------------|------|
| R01 | Estabelecimento | Endereco | — | 1..* | 1 | |
| R02 | Estabelecimento | EspecieAnimal | — | * | * | |
| R03 | AnaliseSanitaria | Pessoa | — | * | 1 | Criada por |
| R04 | AnaliseSanitaria | AlvoInvestigacao | — | 1 | * | |
| R05 | AnaliseSanitaria | AreaAfetada | — | * | * | |
| R06 | AlvoInvestigacao | ZonaControleInvestigacao | «mediation» | 1 | 1 | |
| R07 | MovimentacaoAnimal | Estabelecimento | — | * | 1 | Origem |
| R08 | MovimentacaoAnimal | Estabelecimento | — | * | 1 | Destino |
| R09 | EspecieAnimal | CategoriaEspecie | — | * | 1 | |
| R10 | RespostaSanitaria | AnaliseSanitaria | — | * | 1 | Baseada em |
| R11 | RespostaSanitaria | CicloVigilancia | — | 1 | * | Possui |
| R12 | RespostaSanitaria | PostoComando | — | 0..1 | 1 | Tem |
| R13 | PessoaConvocada | RespostaSanitaria | — | * | 1 | Convoca |
| R14 | CicloVigilancia | ZonaPorCiclo | «mediation» | 1 | * | Subdivide-se |
| R15 | CicloVigilancia | EquipeCampo | — | 1 | * | Aloca |
| R16 | EquipeCampo | MembroEquipe | «memberOf» | 1 | * | Composta por |
| R17 | EquipeCampo | TipoEquipe | — | * | 1 | Classifica-se |
| R18 | EquipeCampo | AreaOperacional | — | 1 | * | Atua em |
| R19 | EquipeCampo | BarreiraSanitaria | — | 1 | * | Opera |
| R20 | EquipeCampo | Veiculo | — | 1 | * | Utiliza |
| R21 | MembroEquipe | Funcao | — | * | 1 | Desempenha |
| R22 | AreaOperacional | ZonaPorCiclo | «mediation» | * | 1 | Pertence a |
| R23 | AreaOperacional | PropriedadeEmArea | «mediation» | 1 | * | Contém |
| R24 | PropriedadeEmArea | Estabelecimento | «mediation» | * | 1 | Refere-se a |
| R25 | RastreamentoGPS | Veiculo | — | * | 1 | |
| R26 | ZonaControleInvestigacao | AreaOperacional | «mediation» | 1 | * | Delimita |
| R27 | SubmissaoPropriedade | PropriedadeEmArea | — | * | 1 | Vinculada a |
| R28 | SubmissaoPropriedade | EquipeCampo | — | * | 1 | Realizada por |
| R29 | SubmissaoBarreira | BarreiraSanitaria | — | * | 1 | Vinculada a |

# Relações descontinuadas

As relações abaixo foram removidas do modelo final:

- `AlvoInvestigacao → Estabelecimento` («material»): substituída pela generalização `AlvoInvestigacao → Estabelecimento`.
- `PropriedadeContactante → Estabelecimento` («material»): substituída pela generalização `PropriedadeContactante → Estabelecimento`.
- `MembroEquipe → Pessoa` («material»): substituída pela generalização `MembroEquipe → Pessoa`.
- `PessoaConvocada → Pessoa` («material»): substituída pela generalização `PessoaConvocada → Pessoa`.
- `PropriedadeTemporaria → Estabelecimento` («material»): substituída pela generalização `PropriedadeTemporaria → Estabelecimento`.
- `PropriedadeEmArea → AreaOperacional`: relação inversa redundante de R23 (`AreaOperacional → PropriedadeEmArea`).
- `PessoaConvocada → Funcao`: removida; a função é desempenhada por `MembroEquipe` (R21).
- `PessoaConvocada → MembroEquipe`: removida; não integra o modelo final.

A relação `PessoaConvocada → RespostaSanitaria` (R13) segue a direção do modelo final; a versão anterior (`RespostaSanitaria → PessoaConvocada`) foi descontinuada.
