# Bachelor’s Thesis Project (BTP) - IIT Kharagpur

This repository contains the complete work for my **final year Bachelor’s Thesis Project (BTP)** at the **Indian Institute of Technology Kharagpur (IIT KGP)**. The research focuses on the **Computation of Conformal Mappings**, specifically looking at the Schwarz-Christoffel transformation and related numerical methods.

The project was carried out over two semesters:

### Part 1 (Autumn 2025) - Theoretical Foundations
The first half of the project involved establishing the mathematical bedrock for conformal mapping and polygon transformations.
*   **Key Topics**: Analytic functions, Cauchy-Riemann equations, Riemann Mapping Theorem, and the derivation of the Schwarz-Christoffel formula.
*   **Case Studies**: Explicit mapping constructions for standard geometries like rectangles (elliptic integrals), semi-infinite strips, and triangles.
*   **Deliverables**: [Mid-term Report](BTP-1/report.tex) and evaluation slides.

### Part 2 (Spring 2026) - Numerical Methods & Extremal Principles
The final phase shifted focus from theoretical derivation to the practical challenges of numerical construction.
*   **Key Topics**: 
    *   **Numerical Parameter Problem**: Implementing Newton-Raphson iteration to determine prevertex locations from polygon side-length ratios.
    *   **Singularity Removal**: Handling algebraic singularities in SC integrals using Kantorovich-type subtraction techniques.
    *   **Extremal Principles**: Variational approaches to mapping, including Bieberbach's area-minimizing principle and the Bergman kernel.
*   **Deliverables**: [Final Thesis Report](BTP-2/final_report.tex) and original TikZ-based mathematical illustrations.

## Compile

To generate the PDF from LaTex on Linux:

```bash
pdflatex -interaction=nonstopmode final_report.tex 2>&1 | tail -20
```

---
*Submitted for the degree of Bachelor of Science (Honours) in Mathematics and Computing, Department of Mathematics, IIT Kharagpur (2025--2026).*
