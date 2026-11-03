# Conceptual Model

OntoUML conceptual model of SIGEVS-O, expressed as Mermaid class diagrams.

## Files

| File | Description |
|------|-------------|
| `onto-complete.mmd` | Complete model (31 classes, all subdomains) |
| `onto-core.mmd` | Core subdomain |
| `onto-investigation.mmd` | Sanitary Investigation subdomain |
| `onto-response.mmd` | Sanitary Response subdomain |
| `onto-field.mmd` | Field Actions subdomain |
| `architecture.mmd` | PDSA-RS platform architecture |

## Colour Scheme

| Subdomain | Fill | Stroke |
|-----------|------|--------|
| Core | `#e8f5e9` (green) | `#2e7d32` |
| Investigation | `#fff3e0` (orange) | `#ef6c00` |
| Response | `#e3f2fd` (blue) | `#1565c0` |
| Field Actions | `#fce4ec` (pink) | `#c62828` |

## Regenerate PNGs

Run from the `sigevs-o/` directory:

```bash
npx @mermaid-js/mermaid-cli -i conceptual-model/onto-complete.mmd -o figures/onto-complete.png -w 2400 -s 3 -b white
```
