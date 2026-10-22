# Fase de Requisitos — REQ-ELIC (Elicitação de Requisitos)

---

## Requisitos Funcionais — Questões de Competência (CQs)

### Subdomínio: Core (Cadastro e Geolocalização)

| ID | Questão de Competência |
|----|------------------------|
| CQ-CORE-01 | Quais estabelecimentos rurais estão cadastrados no SVO? |
| CQ-CORE-02 | Quais espécies animais são exploradas em um estabelecimento? |
| CQ-CORE-03 | Qual a localização geográfica (coordenadas) de um estabelecimento? |
| CQ-CORE-04 | Quais usuários estão vinculados a uma determinada região/inspetoria? |
| CQ-CORE-05 | Quais estabelecimentos possuem CAR (Cadastro Ambiental Rural)? |
| CQ-CORE-06 | Quais estabelecimentos são frigoríficos e qual o tipo de inspeção sanitária? |
| CQ-CORE-07 | Quais perfis e permissões um usuário possui no sistema? |

---

### Subdomínio: Investigação (Análise Sanitária)

| ID | Questão de Competência |
|----|------------------------|
| CQ-INV-01 | Quais propriedades estão dentro do raio de vigilância de um foco ativo? |
| CQ-INV-02 | Uma propriedade pode ser alvo de mais de uma investigação ao mesmo tempo? |
| CQ-INV-03 | Qual o histórico de movimentação animal (GTAs) de uma propriedade durante o período de investigação? |
| CQ-INV-04 | Quais são as propriedades contactantes diretas de uma propriedade investigada? |
| CQ-INV-05 | Quais são as propriedades contactantes indiretas de uma propriedade investigada? |
| CQ-INV-06 | Quais zonas de controle foram definidas para uma investigação? |
| CQ-INV-07 | Qual o status atual de uma investigação sanitária? |
| CQ-INV-08 | Quais áreas geográficas (municípios) são afetadas por uma investigação? |
| CQ-INV-09 | Quais categorias de espécies estão envolvidas em uma investigação? |

---

### Subdomínio: Resposta (Gestão da Contenção)

| ID | Questão de Competência |
|----|------------------------|
| CQ-RES-01 | Quais ciclos de vigilância pertencem a uma resposta sanitária? |
| CQ-RES-02 | Quais equipes estão alocadas a um determinado ciclo de vigilância? |
| CQ-RES-03 | Quais profissionais (membros) compõem uma equipe de campo? |
| CQ-RES-04 | Uma barreira sanitária pode estar ativa em múltiplos ciclos simultaneamente? |
| CQ-RES-05 | Uma zona de controle pode ser redefinida entre ciclos? |
| CQ-RES-06 | Quais profissionais estiveram em campo em uma determinada data? |
| CQ-RES-07 | Uma equipe pode estar alocada a mais de um ciclo simultaneamente? |
| CQ-RES-08 | Qual área operacional está atribuída a cada equipe em um ciclo? |
| CQ-RES-09 | Quais barreiras sanitárias estão ativas em uma resposta? |
| CQ-RES-10 | Quais propriedades estão dentro de uma área operacional? |
| CQ-RES-11 | Qual o tipo de uma barreira sanitária (fixa/volante) e sua função (sanitária/desvio)? |
| CQ-RES-12 | Quais veículos estão vinculados a uma equipe? |
| CQ-RES-13 | Qual o posto de comando associado a uma resposta sanitária? |
| CQ-RES-14 | Quais usuários foram convocados para uma resposta e qual seu status de quarentena? |

---

### Subdomínio: Campo (Coleta e Monitoramento)

| ID | Questão de Competência |
|----|------------------------|
| CQ-CAM-01 | Quais propriedades foram visitadas (submetidas) em um ciclo? |
| CQ-CAM-02 | Qual o status de conclusão de uma propriedade em área operacional? |
| CQ-CAM-03 | Quais submissões foram realizadas por uma equipe em um período? |
| CQ-CAM-04 | Quais propriedades temporárias foram registradas durante a operação? |
| CQ-CAM-05 | Qual o histórico de auditoria de uma submissão ou operação? |
| CQ-CAM-06 | Quais arquivos foram anexados a uma submissão? |

---

## Requisitos Não-Funcionais (RNFs)

| ID | Requisito Não-Funcional |
|----|------------------------|
| RNF-01 | A ontologia deve ser modular para facilitar reuso por outras ontologias |
| RNF-02 | A ontologia deve ser fundamentada em uma ontologia de fundação (UFO) |
| RNF-03 | A ontologia deve ser expressa em OntoUML como ontologia de referência |
| RNF-04 | A ontologia deve ser codificável em OWL/gUFO como ontologia operacional |
| RNF-05 | A ontologia deve ser definida a partir de fontes de conhecimento reconhecidas (SIGEVS, FAO GEMP, legislação SVO) |
| RNF-06 | A ontologia deve representar conhecimento consensual do domínio (validação com especialistas) |
| RNF-07 | A ontologia deve suportar raciocínio sobre zonas de controle e relações geoespaciais |
| RNF-08 | A ontologia deve ser extensível para novos tipos de doenças e medidas de controle |
| RNF-09 | O vocabulário da ontologia deve ser alinhado com a terminologia do domínio de defesa sanitária animal brasileiro |
