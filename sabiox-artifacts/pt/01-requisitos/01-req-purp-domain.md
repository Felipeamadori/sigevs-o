# Fase de Requisitos — REQ-PURP (Propósito) e REQ-DOMN (Domínio)

---

## Documento de Especificação da Ontologia — v.01

| Campo | Valor |
|-------|-------|
| Ontologia | SIGEVS-O — Ontologia de Gestão de Eventos Sanitários Veterinários |
| Data | 23/06/2026 |
| Versão | v.01 |
| Responsável | Ontology Engineer |
| Participante | Ontology Owner (PO SIGEVS) |

---

## 1. Propósito da Ontologia (REQ-PURP)

### 1.1. What (o que a ontologia representa)

A ontologia representa os conceitos do domínio de **defesa sanitária animal** no âmbito dos **Serviços Veterinários Oficiais (SVO)**, abrangendo:

- Investigação epidemiológica de suspeitas de doenças
- Gestão operacional da contenção de focos sanitários
- Coordenação de ciclos de vigilância, equipes de campo, barreiras sanitárias e áreas operacionais
- Coleta e monitoramento de dados em campo

### 1.2. For What (para que a ontologia será útil)

Para que o conhecimento implícito do domínio embutido na plataforma SIGEVS seja explicitamente documentado, compreendido, integrado e passível de raciocínio formal, servindo como:

- Documentação conceitual oficial do domínio de defesa sanitária animal
- Base para Domain-Driven Design na evolução do SIGEVS
- Referência para integração com outros sistemas (SVO, MAPA)
- Material de onboarding para novos desenvolvedores
- Base para Knowledge Graphs do domínio sanitário
- Fonte de verdade independente da implementação

### 1.3. Why (por que a ontologia deve ser construída)

O Módulo de Geoanálise, do qual o SIGEVS derivou, evoluiu sem uma modelagem conceitual formal, resultando em problemas de semântica do domínio que motivaram a construção da ontologia. O SIGEVS, por sua vez, foi desacoplado já tendo essa modelagem como base conceitual, de modo que esses problemas serviram de justificativa para o desenvolvimento da SIGEVS-O:

- Conceitos de domínio ambíguos (ex.: o que distingue "foco" de "suspeita"?)
- Regras de negócio escondidas no código
- APIs que refletem decisões técnicas, não conceitos de negócio
- Banco de dados que mistura persistência com semântica do domínio
- Dificuldade de integração com outros sistemas
- Curva de aprendizado elevada para novos desenvolvedores
- Ausência de uma fonte de verdade conceitual independente da implementação

---

## 2. Domínio da Ontologia (REQ-DOMN)

### 2.1. Definição do Domínio

Defesa sanitária animal no âmbito dos Serviços Veterinários Oficiais (SVO), compreendendo o ciclo completo de gestão de eventos sanitários:

1. **Cadastro e Geolocalização** — base cadastral de estabelecimentos rurais, endereços, espécies exploradas e usuários do SVO
2. **Investigação Epidemiológica** — registro e acompanhamento de suspeitas de doenças, definição de zonas de controle, rastreamento de movimentação animal e identificação de propriedades contactantes
3. **Resposta ao Foco** — coordenação da contenção sanitária por meio de ciclos de vigilância, alocação de equipes, implantação de barreiras, definição de áreas operacionais e posto de comando
4. **Ações em Campo** — coleta de dados nas propriedades e barreiras, submissão de formulários, controle de conclusão de visitas e auditoria

### 2.2. Dimensão Horizontal (fronteiras externas)

**Dentro do escopo:**
- Cadastro e georreferenciamento de estabelecimentos rurais
- Gestão de espécies animais e segmentos produtivos
- Investigação de suspeitas de doenças alvo
- Definição e gerenciamento de zonas de controle (Perifoco, Vigilância, Proteção)
- Rastreamento de movimentação animal (GTAs) e contactantes
- Coordenação de ciclos de vigilância
- Alocação e gestão de equipes de campo
- Implantação e operação de barreiras sanitárias
- Coleta de dados em campo (submissões)
- Controle de usuários, perfis e permissões

**Fora do escopo:**
- Processamento laboratorial de amostras biológicas
- Logística de produção e distribuição de vacinas
- Saúde humana (exceto onde intersecta a defesa animal via notificação)
- Gestão de fauna silvestre não-doméstica
- Aspectos financeiros, orçamentários ou indenizatórios
- Comércio internacional e certificação de produtos de origem animal
- Bem-estar animal (exceto quando diretamente relacionado ao controle sanitário)
- Simulação epidemiológica preditiva (SEIR-VD) e modelagem de propagação de doenças

### 2.3. Dimensão Vertical (nível de detalhamento)

**Dentro do escopo:**
- Nível conceitual do domínio de negócio da defesa sanitária
- Entidades estruturais (estabelecimentos, animais, equipamentos)
- Eventos de negócio (notificação, confirmação, conclusão de ciclo)
- Papéis que as entidades assumem (propriedade investigada, infectada)
- Relacionamentos e regras do domínio
- Ciclos de vida dos conceitos (suspeito → investigado → confirmado → saneado → encerrado)

**Fora do escopo:**
- Detalhes de implementação (APIs REST, tabelas de banco, DTOs, classes Java)
- Rastreamento individual de animais (opera no nível de propriedade/rebanho)
- Interface de usuário e experiência do usuário (UX/UI)
- Detalhes de infraestrutura de TI
- Algoritmos de roteamento e otimização logística

---

## 3. Glossário Inicial

| Termo | Definição |
|-------|-----------|
| Estabelecimento | Unidade produtiva rural cadastrada no serviço veterinário, com código SDA, coordenadas geográficas e espécies exploradas |
| Propriedade | Sinônimo de Estabelecimento no contexto operacional |
| Foco Sanitário | Propriedade onde foi confirmada a ocorrência de uma doença alvo |
| Zona de Controle | Perímetro geográfico definido ao redor de um foco |
| Perifoco | Zona mais interna ao redor do foco (infectada) |
| Vigilância | Zona intermediária de buffer |
| Proteção | Zona externa de vigilância ampliada |
| Ciclo de Vigilância | Rodada numerada de varredura em zona de controle |
| GTA | Guia de Trânsito Animal — documento de movimentação de animais |
| Equipe de Campo | Grupo de profissionais alocados a operações de vigilância |
| Barreira Sanitária | Posto de fiscalização de trânsito animal |
| Área Operacional | Setor geográfico atribuído a uma equipe dentro de uma zona |
| Análise Sanitária | Registro de investigação de suspeita de doença |
| Resposta Sanitária | Registro central da coordenação de contenção de um foco |
| Submissão | Formulário preenchido em visita a propriedade ou barreira |

---

## 4. Referências

- Documento: "Iniciativa - Modelagem Ontológica SIGEVS.md"
- Documento: "Funcionalidades SIGEVS.md"
- Guia SABiOx (v.2024-09): Seções 3.1 (REQ-PURP) e 3.2 (REQ-DOMN)
