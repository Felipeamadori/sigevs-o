# Fase de Implementação — DOC-OPER (Documento da Ontologia Operacional)

---

## Operational Ontology Document

| Campo | Valor |
|-------|-------|
| Documento: | Operational Ontology Document |
| Ontologia: | SIGEVS-O — Ontology for Sanitary Event Management in Animal Health Defense |
| Versão: | v.02 |
| Data: | 15/07/2026 (v.01); v.02 25/11/2026 (fases de cadastro) |

---

## 1. Coded Concepts (IMP-CONC)

Os 33 conceitos de domínio do modelo OntoUML (32 classes e a enumeração `CategoriaEspecie`) foram codificados como classes OWL tipadas com os estereótipos gUFO:

| Subdomínio | Classes | Estereótipos |
|------------|---------|--------------|
| **Core** (9) | Estabelecimento, Endereco, Pessoa, EspecieAnimal, Frigorifico, GranjaAve, GranjaSuino, EstabelecimentoCadastrado, EstabelecimentoNaoCadastrado | 4 Kind, 3 Subkind, 2 Phase |
| **Investigação** (7) | AnaliseSanitaria, AlvoInvestigacao, AreaAfetada, ZonaControleInvestigacao, MovimentacaoAnimal, PropriedadeContactante, CategoriaEspecie | 2 Event, 2 Role, 1 Relator, 1 Kind, 1 Enumeration |
| **Resposta** (14) | RespostaSanitaria, CicloVigilancia, ZonaPorCiclo, EquipeCampo, MembroEquipe, Funcao, AreaOperacional, PropriedadeEmArea, BarreiraSanitaria, Veiculo, PostoComando, PessoaConvocada, RastreamentoGPS, TipoEquipe | 3 Event, 2 Relator, 1 Collective, 2 Role, 6 Kind |
| **Campo** (2) | SubmissaoPropriedade, SubmissaoBarreira | 2 Event |

Cada classe recebeu `rdf:type gufo:<Stereotype>` (ex.: `Establishment rdf:type gufo:Kind`, `InvestigationTarget rdf:type gufo:Role`, `PropertyInArea rdf:type gufo:Relator`, `PropertySubmission rdf:type gufo:Event`).

Além dos 33 conceitos de domínio, quatro classes definidas capturam estados derivados: `Closed Cycle`, `Completed Area`, `Visited Property` e `Quarantined Person` — totalizando **37 classes nomeadas**.

### Mapeamento para o Sistema SIGEVS (ODSE)

Em paralelo, o modelo conceitual foi traduzido para as estruturas do sistema desacoplado SIGEVS (backend Spring Boot):

| Estereótipo OntoUML | Estrutura no SIGEVS |
|---------------------|---------------------|
| `<<Kind>>` | Entidade JPA com tabela própria e identidade independente |
| `<<Subkind>>` | Entidade JPA com herança/relação 1:1 para o Kind |
| `<<Role>>`/`<<Phase>>` (especializam o Kind) | Entidade JPA que referencia o Kind (dispensa tabela associativa extra) |
| `<<Relator>>` | Tabela associativa com atributos próprios (ex.: `area_premises.completed`) |
| `<<Event>>` | Entidade JPA com carimbo de tempo |
| `<<Collective>>` | Entidade JPA com coleção de membros (`team_members`) |
| `<<Enumeration>>` | Enum Java (`ZoneType`, `SpeciesCategory`, etc.) |

---

## 2. Coded Relations (IMP-RELC)

As 31 relações do modelo foram codificadas como `owl:ObjectProperty` (e, no sistema, como associações JPA / FKs):

| Tipo de Relação | Codificação OWL | Codificação SIGEVS |
|-----------------|-----------------|--------------------|
| Associação simples | `owl:ObjectProperty` (ex.: `estabelecimentoHasEndereco`) | `@ManyToOne` / FK |
| Relação de mediação (`<<mediation>>`) | `owl:ObjectProperty` com domínio Relator | Tabela associativa com atributos |
| Composição (`<<memberOf>>`) | `owl:ObjectProperty` | `@OneToMany` (ex.: `EquipeCampo → MembroEquipe`) |
| Generalização (`<<Subkind>>`/`<<Role>>`/`<<Phase>>`) | `rdfs:subClassOf` | Herança JPA ou referência ao Kind |

Exemplos de propriedades de objeto codificadas: `estabelecimentoHasEndereco`, `analiseSanitariaHasAlvoInvestigacao`, `Aloca`, `CompostaPor`, `Contem`, `VinculadaA`.

---

## 3. Coded Axioms (IMP-AXIO)

Os 25 axiomas formais do modelo foram codificados em duas camadas:

### 3.1 Axiomas OWL (raciocínio lógico)

- **Axiomas de identidade** (AX-ID-*): restrições de unicidade (`owl:hasKey`; ex.: código SDA único para estabelecimentos cadastrados; GTA identificada por `(serie, numero, ufOrigem)`).
- **Axiomas de dependência** (AX-DEP-*): restrições existenciais (ex.: todo `CicloVigilancia` pertence a uma `RespostaSanitaria`).
- **Axiomas de sequência** (AX-SEQ-*): ordenação sequencial dos ciclos; fechamento de ciclo condicionado à conclusão das áreas (AX-SEQ-02, subsunção sobre a classe definida `Closed Cycle`) e conclusão de área (AX-SEQ-03, classe definida `Completed Area`).
- **Axiomas de estado** (AX-STATE-01/02): quarentena (classe definida `Quarantined Person`) e permissões independentes.
- **Axioma geográfico** (AX-GEO-01): mediação alvo→zona com cardinalidade 1..4.

### 3.2 Restrições de Banco / Serviço (SIGEVS)

| Axioma | Codificação no SIGEVS |
|--------|-----------------------|
| AX-SEQ-01 (ciclos sequenciais) | `UNIQUE(cycle_number, response_id)` + verificação na criação de ciclos |
| AX-CARD-01 (convocação única) | `UNIQUE(user_id, response_id)` em `response_convoked_users` |
| AX-DEP-* (dependências) | `FOREIGN KEY` (ex.: `response_id` em `response_surveillance_cycle`) |
| AX-STATE-01 (quarentena) | Sinalizador + data de expiração (`isDirty`, `dirtyUntil`) |
| Estados persistidos (nível de implementação) | Colunas `NOT NULL` (`closed`, `completed`, `active`) |
| CQ-INV-01 (propriedades em zona de risco) | Consulta PostGIS `ST_DWithin` com buffers geoespaciais |

**Geolocalização:** atributos espaciais (coordenadas, polígonos) foram codificados com o tipo `geography` do PostGIS, permitindo consultas espaciais (ST_DWithin) que substituem um reasoner OWL em tempo de execução, atendendo aos requisitos de desempenho.

---

## 4. Operational Ontology Metrics

| Métrica | Valor |
|---------|-------|
| Conceitos de domínio (32 classes + 1 enumeração) | 33 |
| Classes definidas (estados derivados) | 4 |
| **Total de classes nomeadas** | **37** |
| Propriedades de objeto | 36 |
| Propriedades de dados | 113 |
| Indivíduos (enums + declarações de tipo) | 34 |
| Restrições de classe OWL | 42 |
| Chaves (`owl:hasKey`) | 7 |
| Cadeias de propriedades | 1 |
| Axiomas lógicos (script rdflib; v.01: 402 — Protégé reportou 401) | 421 |
| Declarações (script rdflib; v.01: 214) | 225 |
| Axiomas totais (script rdflib; v.01: 867) | 910 |

---

## 5. Verification (EVA-OPER)

A ontologia operacional foi verificada por duas vias:

1. **Consultas SPARQL** — as questões de competência foram respondidas sobre o modelo povoado; as consultas oficiais estão em `sparql/cq-*.rq` (executadas no Protégé e, a espacial, no Apache Jena com `jena-geosparql`). Exemplos:

```sparql
# CQ-CORE-01: Quais estabelecimentos estão cadastrados?
PREFIX sigevs: <https://sigevs.ontologies#>

SELECT ?estabelecimento ?nome WHERE {
  ?estabelecimento a sigevs:EstabelecimentoCadastrado ;
                   sigevs:nomeEstabelecimento ?nome .
}
ORDER BY ?nome
```

```sparql
# CQ-RES-03: Membros de cada equipe de campo
PREFIX sigevs: <https://sigevs.ontologies#>

SELECT ?equipe ?nomeEquipe ?membro ?nomeMembro WHERE {
  ?equipe a sigevs:EquipeCampo ;
          sigevs:nomeEquipe ?nomeEquipe ;
          sigevs:CompostaPor ?membro .
  ?membro a sigevs:MembroEquipe ;
          sigevs:nomePessoa ?nomeMembro .
}
ORDER BY ?nomeEquipe ?nomeMembro
```

2. **Raciocínio com HermiT** (via owlready2, com gUFO carregado) — após povoar a ontologia com um cenário de surto de exemplo, o reasoner confirmou a **consistência lógica** (0 classes insatisfatíveis) e inferiu as pertinências esperadas (`Visited Property` e `Closed Cycle`). As restrições de sequência AX-SEQ-02 e AX-SEQ-03 foram validadas adicionalmente com um cenário propositalmente falho (ciclo fechado com propriedade não visitada), e o reasoner detectou corretamente a inconsistência resultante. Suíte: `scripts/validate_ontology.py` e `scripts/validate_cqs.py` (36/36 CQs: 29 SPARQL, 4 estruturais, 3 na camada de aplicação).

---

## 6. Version Control

| Version | Date | Description |
|---------|------|-------------|
| v.01 | 15/07/2026 | Ontologia operacional SIGEVS-O codificada em gUFO/OWL e verificada |
| v.02 | 25/11/2026 | Fases de cadastro no lugar do papel Propriedade Temporária; AX-GEO-01 1..4; 24 axiomas; 36 classes nomeadas; 43 restrições |

---

## References

- SABiOx Guide 2024-09: Sections 7.1 (IMP-CONC), 7.2 (IMP-RELC), 7.3 (IMP-AXIO), 7.4 (DOC-OPER), 7.6 (EVA-OPER)
- Operational Ontology Premise: `../04-design/01-doc-oper.md`
- Reference Ontology Document (complete): `../03-captura/05-doc-mode.md`
- Axioms: `../03-captura/02-cap-axim.md`
- Classes e Relações: `../conceptual-model/relacoes-sigevs.md` (repositório)
