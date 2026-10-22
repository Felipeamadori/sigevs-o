# Questões de Competência — Subdomínio Ações em Campo

| ID | Questão de Competência | Caminho no Modelo | Implementação |
|----|----------------------|--------------------|---------------|
| CQ-CAM-01 | Quais propriedades em uma área já foram visitadas e qual está pendente? | `PropertyInArea` → `PropertySubmission` | JPA/SPARQL FILTER |
| CQ-CAM-02 | Qual o status de conclusão da visita a cada propriedade? | `PropertyInArea.isCompleted` | JPA query |
| CQ-CAM-03 | Quais submissões (formulários) foram realizadas por cada equipe? | `PropertySubmission` → `FieldTeam` + faixa de datas | JPA query |
| CQ-CAM-04 | Quais propriedades temporárias (não cadastradas) foram identificadas em campo? | Instâncias de `TemporaryProperty` | JPA/SPARQL |
| CQ-CAM-05 | Qual o histórico de auditoria das operações no sistema? | `PropertySubmission` → audit log | JPA query |
| CQ-CAM-06 | Quais arquivos foram anexados a uma submissão? | `PropertySubmission` → `file` (bytea) | JPA query |
