# Questões de Competência — Subdomínio Core

| ID | Questão de Competência | Caminho no Modelo | Implementação |
|----|----------------------|--------------------|---------------|
| CQ-CORE-01 | Quais estabelecimentos rurais estão cadastrados no sistema? | Instâncias de `Establishment` | JPA/SPARQL |
| CQ-CORE-02 | Quais espécies animais são exploradas em cada estabelecimento? | `Establishment` → `AnimalSpecies` | JPA query |
| CQ-CORE-03 | Qual a localização geográfica de um estabelecimento? | `Establishment` → `Address.coordinates` | JPA query |
| CQ-CORE-04 | Quais profissionais estão cadastrados no serviço veterinário? | `Person` → `region` | JPA query |
| CQ-CORE-05 | Qual o perímetro geográfico (CAR) de uma propriedade? | `Establishment` → `carPerimeter` (NOT NULL) | JPA query |
| CQ-CORE-06 | Quais estabelecimentos possuem inspeção federal (SIF)? | `Slaughterhouse` (subkind of `Establishment`) → `inspectionType` | JPA/SPARQL |
| CQ-CORE-07 | Quais módulos do sistema cada profissional pode acessar? | `Person` → `profile` | JPA query |
