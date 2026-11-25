# Fase de Design — DOC-OPER (Documento de Premissas da Ontologia Operacional)

---

## Operational Ontology Document (Premise)

| Campo | Valor |
|-------|-------|
| Documento: | Operational Ontology Document (Premise) |
| Ontologia: | SIGEVS-O — Ontology for Sanitary Event Management in Animal Health Defense |
| Versão: | v.02 |
| Data: | 08/07/2026 (v.01); v.02 25/11/2026 (fases de cadastro) |

---

## 1. Encoding Language (DES-LANG)

**OWL 2** codificada por meio da **gUFO** — uma implementação leve da Unified Foundational Ontology (UFO) [Almeida et al. 2019].

A gUFO foi escolhida por preservar, em uma ontologia OWL praticável, as distinções ontológicas centrais de UFO (Kind, Subkind, Role, Phase, Relator, Event, Collective, etc.), permitindo:

- **Raciocínio automatizado** com reasoners como HermiT;
- **Resposta a consultas SPARQL** diretamente sobre o modelo importado (Protégé);
- **Consistência semântica** em cenários de aplicação real, sem exigir a formalização completa de todos os axiomas da teoria de fundação.

Diferentemente de uma ontologia OWL "pura" (sem fundamentação), a adoção da gUFO garante que as distinções ontológicas capturadas no modelo conceitual OntoUML (Kind, Role, Phase, Relator, Event) sejam preservadas na codificação operacional.

---

## 2. Vocabularies (DES-VOCA)

Os seguintes vocabulários/recursos foram adotados na codificação operacional:

| Vocabulário / Recurso | Papel |
|-----------------------|-------|
| **gUFO** (`http://purl.org/nemo/gufo`) | Fornece as classes de estereótipos UFO (`gufo:Kind`, `gufo:Role`, `gufo:Phase`, `gufo:Relator`, `gufo:Event`, etc.) para tipagem das classes de domínio |
| **OWL 2 / RDF / RDFS** | Linguagem de codificação e primitivas de modelagem (`owl:Class`, `rdfs:subClassOf`, `owl:ObjectProperty`, `owl:DatatypeProperty`) |
| **ontouml-schema** (`https://github.com/tgoprince/ontouml-schema`) | Formato JSON de serialização do modelo OntoUML para intercâmbio com ferramentas (Visual Paradigm, ontouml-js) |

**IRIs:** a ontologia implementa os conceitos do domínio com **IRIs em português** e **rótulos (`rdfs:label`) em inglês** (ex.: `sigevs:Estabelecimento` com `rdfs:label "Establishment"`). O prefixo `sigevs:` aponta para `https://sigevs.ontologies#`.

Nenhum vocabulário de domínio externo (ex.: AGROVOC, IDO) foi importado nesta versão — o reuso de ontologias de domínio permanece como trabalho futuro (ver `../02-configuracao/01-doc-refe.md`, Seção 4).

---

## 3. Ontology Encoding (DES-CODE)

### 3.1 Mapeamento OntoUML → OWL/gUFO

| OntoUML | OWL/gUFO | Exemplo |
|---------|----------|---------|
| `<<Kind>>` | `owl:Class` tipada com `gufo:Kind` | `Establishment rdf:type gufo:Kind` |
| `<<Subkind>>` | `rdfs:subClassOf` (especialização do Kind) | `Slaughterhouse rdfs:subClassOf Establishment` |
| `<<Role>>` | `owl:Class` tipada com `gufo:Role` | `InvestigationTarget rdf:type gufo:Role` |
| `<<Phase>>` | `owl:Class` tipada com `gufo:Phase` (+ `owl:disjointWith` entre fases da mesma partição) | `RegisteredEstablishment rdf:type gufo:Phase` |
| `<<Relator>>` | `owl:Class` tipada com `gufo:Relator` | `PropertyInArea rdf:type gufo:Relator` |
| `<<Event>>` | `owl:Class` tipada com `gufo:EventType` | `PropertySubmission rdf:type gufo:EventType` |
| `<<Collective>>` | `owl:Class` tipada com `gufo:Collective`/`VariableCollection` | `FieldTeam rdf:type gufo:Collective` |
| Associação | `owl:ObjectProperty` | `establishmentHasAddress` |
| Atributo | `owl:DatatypeProperty` | `establishmentName` |
| Generalização (Role/Phase de Kind) | `rdfs:subClassOf` | `InvestigationTarget rdfs:subClassOf Establishment` |

### 3.2 Regras de Codificação

1. **Roles e Phases especializam seu Kind** (`rdfs:subClassOf`), dispensando associações `material` ontologicamente redundantes — os papéis `AlvoInvestigacao` e `PropriedadeContactante` especializam `Estabelecimento`; `MembroEquipe` e `PessoaConvocada` especializam `Pessoa`; as fases `EstabelecimentoCadastrado` e `EstabelecimentoNaoCadastrado` também especializam `Estabelecimento` (condição intrínseca e contingente, modelada como Phase — e não como Role — por não ser relacional).
2. **Relators** mediam ao menos duas entidades (ex.: `PropertyInArea` medeia `AreaOperacional` e `PropriedadeInspecionada` (papel de `Estabelecimento`), carregando a qualidade `visitaConcluida`); `ZonaControleInvestigacao` medeia `AlvoInvestigacao` e delimita `AreaOperacional`.
3. **Events** recebem carimbo de tempo e participam de relações de composição hierárquica (ex.: `RespostaSanitaria` possui `CicloVigilancia`).
4. **Enums** (ZoneType, BarrierType, BarrierRole, MovementPurpose, além da enumeração `CategoriaEspecie`) são codificados como indivíduos de uma classe `Enumeration`.

---

## 4. Classes Definidas (Estados Derivados)

Além dos 33 conceitos de domínio, quatro classes definidas capturam estados derivados por inferência lógica:

| Classe Definida | Definição |
|-----------------|-----------|
| `Closed Cycle` | `CicloVigilancia` marcado como fechado (`cicloFechado = true`), definida por equivalência e com a restrição de fechamento como subsunção adicional (todas as áreas concluídas) |
| `Completed Area` | `AreaOperacional` cujas propriedades foram todas visitadas |
| `Visited Property` | `PropriedadeEmArea` com `visitaConcluida = true` |
| `Quarantined Person` | `PessoaConvocada` com status de quarentena ativo |

---

## 5. Version Control

| Version | Date | Description |
|---------|------|-------------|
| v.01 | 08/07/2026 | Premissas da ontologia operacional SIGEVS-O (gUFO/OWL) |
| v.02 | 25/11/2026 | Substituição do papel Propriedade Temporária pelas fases de cadastro; AX-GEO-01 (zonas: máx. 3 concêntricas; `INVESTIGATION` da API fora do modelo); renumeração dos axiomas (24) |

---

## References

- SABiOx Guide 2024-09: Sections 6.1 (DES-LANG), 6.2 (DES-VOCA), 6.3 (DES-CODE), 6.4 (DOC-OPER)
- Reference Ontology Document (complete): `../03-captura/05-doc-mode.md`
- OntoUML Model: `../03-captura/03-cap-mode-ontouml.md`
- gUFO: [Almeida et al. 2019] — A Lightweight Implementation of the Unified Foundational Ontology (UFO)
