# Questões de Competência — Subdomínio Investigação Sanitária

| ID | Questão de Competência | Caminho no Modelo | Implementação |
|----|----------------------|--------------------|---------------|
| CQ-INV-01 | Quais propriedades estão dentro de cada zona de risco (Perifoco, Vigilância, Proteção)? | `InvestigationTarget` → `ControlZone.radius` → establishments in buffer | PostGIS/GeoSPARQL |
| CQ-INV-02 | Uma mesma propriedade pode ser alvo de múltiplas investigações simultâneas? | `InvestigationTarget` (sem UNIQUE constraint em analysis_id + premise_id) | Análise estrutural |
| CQ-INV-03 | Quais movimentações de animais ocorreram entre propriedades em um período? | `AnimalMovement` (origin/destination = `Establishment`) | JPA/SPARQL |
| CQ-INV-04 | Quais propriedades tiveram contato direto com uma propriedade investigada? | `InvestigationTarget` → `ContactingProperty` (direto) | JPA query |
| CQ-INV-05 | Quais propriedades tiveram contato indireto (cadeia de movimentações)? | `InvestigationTarget` → `IndirectContactProperty` | JPA query |
| CQ-INV-06 | Qual o raio de cada zona de controle definida em uma investigação? | `InvestigationTarget` → `ControlZone` | JPA/SPARQL |
| CQ-INV-07 | Quais análises sanitárias estão ativas? | `SanitaryAnalysis` → `isActive` | JPA query |
| CQ-INV-08 | Quais municípios estão na área afetada de uma investigação? | `InvestigationTarget` → `Address` → municipality | JPA query |
| CQ-INV-09 | Quais categorias de espécie estão sendo investigadas? | `InvestigationTarget` → `AnimalSpecies` | JPA query |
