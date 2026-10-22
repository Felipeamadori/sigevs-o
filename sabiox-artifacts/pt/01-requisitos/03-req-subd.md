# Fase de Requisitos — REQ-SUBD (Identificação de Subdomínios)

---

## Subdomínios da Ontologia SIGEVS-O

Os subdomínios foram identificados a partir da análise das 5 áreas funcionais do SIGEVS (documento `Funcionalidades SIGEVS.md`) e do agrupamento das Questões de Competência (REQ-ELIC). Cada subdomínio representa um módulo coeso da ontologia, permitindo desenvolvimento distribuído e reuso seletivo.

---

### 1. Subdomínio: **Core**

**Definição:** Entidades fundamentais e transversais do domínio de defesa sanitária animal. Serve como âncora para todos os demais subdomínios.

**Conceitos principais:**
- Estabelecimento (Kind)
- Animal / Espécie / Segmento Produtivo
- Usuário / Profissional
- Endereço / Município / Estado
- Coordenadas Geográficas
- CAR (Cadastro Ambiental Rural)
- Frigorífico

**CQs associadas:** CQ-CORE-01 a CQ-CORE-07

**Dependências:** Nenhuma (módulo raiz)

---

### 2. Subdomínio: **Investigação Sanitária**

**Definição:** Processo de investigação epidemiológica de suspeitas de doenças, incluindo definição de alvos, zonas de controle, rastreamento de movimentação animal e identificação de contactantes.

**Conceitos principais:**
- Análise Sanitária (Event)
- Alvo de Investigação (Role)
- Zona de Controle (Relator) — Perifoco, Vigilância, Proteção, Investigação
- Movimentação Animal / GTA (Event)
- Propriedade Contactante Direta / Indireta
- Área Afetada
- Categoria de Espécie

**CQs associadas:** CQ-INV-01 a CQ-INV-09

**Dependências:** Core

---

### 3. Subdomínio: **Resposta Sanitária**

**Definição:** Coordenação operacional da contenção de focos, incluindo ciclos de vigilância, alocação de equipes, implantação de barreiras, áreas operacionais, veículos e posto de comando.

**Conceitos principais:**
- Resposta Sanitária (Event)
- Ciclo de Vigilância (Event)
- Zona por Ciclo
- Equipe de Campo (Collective)
- Membro de Equipe (Role)
- Função (veterinário, auxiliar, técnico)
- Área Operacional
- Propriedade em Área
- Barreira Sanitária (Kind) — fixa/volante, sanitária/desvio
- Veículo / Viatura
- Posto de Comando
- Usuário Convocado
- Rastreamento GPS

**CQs associadas:** CQ-RES-01 a CQ-RES-14

**Dependências:** Core, Investigação Sanitária

---

### 4. Subdomínio: **Ações em Campo**

**Definição:** Coleta operacional de dados nas propriedades e barreiras, incluindo submissão de formulários, controle de conclusão de visitas, registro de propriedades temporárias e auditoria.

**Conceitos principais:**
- Submissão de Propriedade (Event)
- Submissão de Barreira (Event)
- Propriedade Temporária
- Conclusão de Visita (Phase)
- Log de Auditoria

**CQs associadas:** CQ-CAM-01 a CQ-CAM-06

**Dependências:** Core, Resposta Sanitária

---

## Diagrama de Dependências entre Subdomínios

```
     ┌─────────────┐
     │    Core      │ (raiz)
     └──────┬───────┘
            │
     ┌──────▼───────┐
     │ Investigação │
     └──────┬───────┘
            │
     ┌──────▼───────┐     ┌──────────────────┐
     │   Resposta   │────▶│   Ações em Campo │
     └──────────────┘     └──────────────────┘
```

---

## Estratégia de Modularização

Adotar estratégia de **particionamento** (partitioning), onde cada subdomínio é tratado como um módulo independente com suas próprias classes e relações, mantendo interfaces mínimas de dependência. A integração entre módulos ocorrerá por associação e especialização dos conceitos do Core.

Na fase de **Setup**, decidiremos sobre ontologias a reutilizar (ex.: FAO GEMP, AGROVOC) que possam ancorar conceitos específicos do domínio.
