# Figures

Generated diagrams from Mermaid source files.

## Files

| File | Description |
|------|-------------|
| `onto-complete.png` | Complete ontology model (colour-coded) |
| `onto-core.png` | Core subdomain (green) |
| `onto-investigation.png` | Investigation subdomain (orange) |
| `onto-response.png` | Response subdomain (blue) |
| `onto-field.png` | Field Actions subdomain (pink) |
| `architecture.png` | PDSA-RS platform architecture |

## Regeneration

PNGs are generated from `.mmd` files in `conceptual-model/`. Run from the `sigevs-o/` directory:

```bash
npx @mermaid-js/mermaid-cli -i conceptual-model/onto-complete.mmd -o figures/onto-complete.png -w 2400 -s 3 -b white
```
