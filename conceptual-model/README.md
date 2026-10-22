# Conceptual Model

OntoUML conceptual model of SIGEVS-O, expressed as Mermaid class diagrams.

## Files

| File | Description |
|------|-------------|
| `sigevs-o-complete.mmd` | Complete model (31 classes, all subdomains) |
| `sigevs-o-core.mmd` | Core subdomain |
| `sigevs-o-investigation.mmd` | Sanitary Investigation subdomain |
| `sigevs-o-response.mmd` | Sanitary Response subdomain |
| `sigevs-o-field.mmd` | Field Actions subdomain |
| `architecture.mmd` | PDSA-RS platform architecture |

## Colour Scheme

| Subdomain | Fill | Stroke |
|-----------|------|--------|
| Core | `#e8f5e9` (green) | `#2e7d32` |
| Investigation | `#fff3e0` (orange) | `#ef6c00` |
| Response | `#e3f2fd` (blue) | `#1565c0` |
| Field Actions | `#fce4ec` (pink) | `#c62828` |

## Regenerate PNGs

```bash
npx @mermaid-js/mermaid-cli -i sigevs-o-complete.mmd -o sigevs-o-complete.png -w 2400 -s 3 -b white
```
