# Axiomas — Identidade

| ID | Axioma | Descrição | Fonte |
|----|--------|-----------|-------|
| AX-ID-01 | `codigoEstabelecimento` é único globalmente | Todo Estabelecimento cadastrado (fase EstabelecimentoCadastrado) possui um código SDA único; unidades não cadastradas (fase EstabelecimentoNaoCadastrado) não possuem código SDA e são identificadas pelo registro de campo | `UNIQUE(codigo_estabelecimento)` em `cadastros.estabelecimento` |
| AX-ID-04 | Todo estabelecimento com `tipo = "Frigorífico"` possui um registro em `Frigorifico` | A existência de Frigorifico depende da existência de um Estabelecimento com essa classificação | `Frigorifico.id_estabelecimento FK` |
| AX-ID-02 | Uma Pessoa é identificada por `keycloak_subject_id` e alternativamente por `cpf` e `email` | Identidades únicas nas três dimensões (Keycloak, CPF, email) | `UNIQUE(keycloak_subject_id, cpf, email)` em `cadastros.usuario` |
| AX-ID-03 | Uma movimentação animal é identificada pela tripla `(serie, numero, uf_origem)` | Cada GTA é única por série-número-UF de origem | `PK(serie, numero, uf_origem)` nas tabelas `movimentacao.*` |
