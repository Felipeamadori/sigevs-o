# Scripts de Validação

Scripts Python para validar a ontologia SIGEVS-O e as 36 questões de
competência (CQs). Requisitos: `pip install rdflib owlready2` (HermiT exige
Java; os demais scripts usam apenas rdflib).

## validate_ontology.py

Validação ponta a ponta do artefato gUFO/OWL:

1. Carrega `ontology/SIGEVS-O-complete.ttl` e povoa com um cenário de surto;
2. Executa o reasoner **HermiT** (via owlready2): consistência lógica,
   inferência das classes definidas (`PropriedadeVisitada`, `CicloFechado`) e
   detecção da violação do AX-SEQ-02/03 num cenário propositalmente falho;
3. Executa 4 CQs representativas via SPARQL (CQ-CORE-01, CQ-INV-01,
   CQ-RES-03, CQ-CAM-04).

```bash
python scripts/validate_ontology.py
python scripts/validate_ontology.py --save-populated ontology/SIGEVS-O-populated.ttl
```

## validate_cqs.py

Valida **as 36 questões de competência** contra a ontologia povoada com um
cenário de exemplo cobrindo os quatro subdomínios:

- **SPARQL (29 CQs)**: consulta executada sobre o grafo populado deve
  retornar as instâncias esperadas do cenário;
- **Estrutural (4 CQs)**: a resposta é uma propriedade do modelo verificada
  diretamente no TBox (ex.: ausência de restrição de unicidade — CQ-INV-02,
  CQ-RES-04/05/07);
- **Camada de implementação (3 CQs)**: CQ-CORE-04 (região/inspetoria),
  CQ-CAM-05 (log de auditoria) e CQ-CAM-06 (anexos) são respondidos na
  camada JPA/serviço e não foram materializados em OWL; o script apenas
  reporta a camada responsável.

```bash
python scripts/validate_cqs.py
```

## validate_ontology_structure.py

Validação estrutural do TBox (sem ABox, sem Java):

- Métricas do inventário: 33 conceitos de domínio (32 classes + a enumeração
  `CategoriaEspecie`), 4 classes definidas (37 nomeadas), 36 object
  properties, 113 datatype properties;
- Conformidade gUFO: cada classe com o estereótipo documentado (Kind,
  SubKind, Role, EventType, Relator, Collective, AbstractIndividualType);
  valores da enumeração SpeciesCategory presentes;
- Taxonomia: as 10 generalizações via `rdfs:subClassOf`;
- Sanidade das propriedades: domínios/ranges declarados.

```bash
python scripts/validate_ontology_structure.py
```

## validate_model_sync.py

Cruzamento entre o modelo conceitual (`conceptual-model/onto-complete.mmd`,
fonte da verdade) e a ontologia OWL, detectando desvios:

- mesmos 33 conceitos nos dois lados (mapeamento nomes em inglês do modelo →
  nomes em português da OWL);
- estereótipos do modelo correspondem aos tipos gUFO;
- as 10 generalizações do modelo correspondem aos pares `rdfs:subClassOf`;
- as 31 relações do modelo presentes, 36 object properties na OWL;
- `visitaConcluida` é datatype property de `PropriedadeEmArea`;
- classes definidas existem apenas na OWL (não no modelo conceitual).

```bash
python scripts/validate_model_sync.py
```

## validate_time_window.py

Verifica o axioma **AX-SEQ-06** (janela temporal de coleta): a
`dataHoraColeta` de cada submissão de propriedade deve estar dentro de
[`dataInicioZona`, `dataFimZona`] da zona por ciclo que contém a área da
propriedade (zona sem data de fim está aberta). Como a comparação de datas
está fora do OWL 2 DL, a regra é imposta pelo serviço do SIGEVS
(`SubmissionService.validateZoneStatus`) e verificada aqui por SPARQL sobre o
cenário das CQs, com um teste negativo (submissão após o fim da janela).

O mesmo script confere que o estado dos eventos é derivável da sua extensão
temporal: ciclo fechado ⇔ possui `fimCiclo`; análise ativa ⇔ sem
`encerradaEm`; resposta ativa ⇔ sem `fimResposta`. As flags booleanas
(`cicloFechado`, `analiseAtiva`, `respostaAtiva`) espelham a implementação.

```bash
python scripts/validate_time_window.py
```

## Suíte completa

```bash
python scripts/validate_ontology_structure.py
python scripts/validate_model_sync.py
python scripts/validate_cqs.py
python scripts/validate_time_window.py
python scripts/validate_ontology.py   # requer Java (HermiT)
```

Todos os scripts devolvem código de saída 0 quando todas as verificações
passam e 1 em caso de falha.
