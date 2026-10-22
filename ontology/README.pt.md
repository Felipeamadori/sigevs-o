# Ontology

Este diretório contém a formalização gUFO/OWL do SIGEVS-O.

## Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `SIGEVS-O.ttl` | Export bruto do modelo OntoUML pelo plugin OntoUML do Visual Paradigm (classes e object properties) |
| `SIGEVS-O-complete.ttl` | Formalização completa: datatype properties (atributos), relações inversas, axiomas `owl:hasKey` e os 31 axiomas formais — artefato canônico |
| `sigevs-o.owx` | Serialização OWL/XML do Protégé da formalização completa (usada para obter as métricas do Protégé) |

## Como Carregar

1. Abrir Protégé (≥ 5.6.0)
2. File → Open → selecionar `SIGEVS-O-complete.ttl`
3. Carregar vocabulário gUFO: [https://purl.org/nemo/gufo](https://purl.org/nemo/gufo)
4. Executar o reasoner HermiT para verificar consistência

Para validar a ontologia automaticamente (popular → reasoner → SPARQL), execute:

```bash
python ../scripts/validate_ontology.py
```

## Dependências

- [gUFO](https://purl.org/nemo/gufo) — Implementação OWL leve de UFO
- `rdflib` e `owlready2` (para o script de validação)
