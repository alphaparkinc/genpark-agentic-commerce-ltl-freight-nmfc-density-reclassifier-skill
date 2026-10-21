# LTL Freight NMFC Density & Reclassification Dispute Arbiter Skill

[![GenPark Official](https://img.shields.io/badge/GenPark-Official%20Skill-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green)](https://modelcontextprotocol.io/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20Stdlib-brightgreen)](https://python.org)

NMFC (National Motor Freight Classification) density rating calculator, dimensional weight vs actual weight re-class, and LTL freight overcharge dispute generator. Built for GenPark (https://www.genpark.ai).

## 🌐 Official Channels
- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## 🛠️ MCP Tools Exposed
- `calculate_freight_density_and_nmfc_class`: Calculate shipment cubic feet, density (PCF), and mapped National Motor Freight Classification (NMFC) tier.
- `audit_carrier_w_and_r_chargeback`: Audit carrier Weight & Inspection (W&R) re-classification fee chargeback against verified packaging spec.

## 🚀 Installation & Usage
```bash
python -m genpark_agentic_commerce_ltl_freight_nmfc_density_reclassifier_skill.server --test
```
