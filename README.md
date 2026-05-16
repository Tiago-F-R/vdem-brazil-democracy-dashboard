# Brazilian Democracy Dashboard — V-Dem Analysis

Interactive dashboard built with Python and Streamlit to visualize and compare 
Brazilian democratic quality indicators against a global sample, using data from 
the V-Dem Project (v16, 2026).

Developed as a project for the *Data Science with Python* course at 
FGV EPGE — Escola Brasileira de Economia e Finanças.

---

## Features

- **Time-series analysis** of 14 democratic indicators for Brazil (1789–2024), 
  with toggleable historical event markers (1964 coup, 1985 redemocratization, etc.)
- **World choropleth map** for any indicator and year across all V-Dem countries
- **Radar chart** of Brazil's full democratic profile for any selected year
- **Cross-country bar chart** comparing Brazil to Latin American and OECD countries
- **Summary metrics** with 5-year delta for key indices
- **Data table** with full indicator history, filterable by period

---

## Indicators

| Index | V-Dem variable |
|---|---|
| Liberal Democracy | `v2x_libdem` |
| Electoral Democracy | `v2x_polyarchy` |
| Participatory Democracy | `v2x_partipdem` |
| Egalitarian Democracy | `v2x_egaldem` |
| Deliberative Democracy | `v2x_delibdem` |
| Freedom of Expression | `v2x_freexp_altinf` |
| Freedom of Association | `v2x_frassoc_thick` |
| Free & Fair Elections | `v2xel_frefair` |
| Rule of Law | `v2xcl_rol` |
| Control of Corruption | `v2x_accountability` |
| Judicial Constraints | `v2x_jucon` |
| Legislative Constraints | `v2xlg_legcon` |
| Women's Empowerment | `v2x_gender` |
| Civil Society | `v2xcs_ccsi` |

---

## Requirements
