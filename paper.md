---
title: 'FlexCPI: A Python Package to Build and Analyze Custom CPIs with BLS Data'
tags:
  - Python 
  - Inflation
  - Macroeconomics
  - Price index modeling
  - Economic research tool

  - BLS data
authors:
  - name: Rory G. Quinlan
    orcid: 0009-0006-7483-6769
    equal-contrib: true
    affiliation: "1"
affiliations:
  - name: University of Pittsburgh
    index: 1
    ror: 00hx57361
date: 15 May 2025
bibliography: paper.bib
nocite: |
  @*
---


# Summary

FlexCPI is a Python package available on PyPI that analyzes time-series data and streamlines exploratory time-series analysis with The Federal Reserve Economic Data (FRED) by automating routine tasks, including stationarity testing, grid searching for optimal ARIMA and SARIMA models, assessing the ARIMA and SARIMA model fit, and quick forecasting. This package includes automated model stability checks and model selection, along with Jupyter-optimized outputs, ensuring its rigor and efficiency for exploratory analyses in macroeconomic research.

# Statement of need

Time-series analyses are fundamental to macroeconomic research. FRED provides publicly available macroeconomic indicator data. While current packages, such as StatsModels, contain time-series analysis functions, and the Fredapi package allows users to download and import data from FRED easily, the FredQuincast package goes a step further by integrating and automating the two components. By streamlining exploratory time-series tasks, such as stationarity testing, model selection, and basic forecasting, this package helps macroeconomic researchers save time on routine tasks and enhance workflow reproducibility.

# Acknowledgments

We gratefully acknowledge the Bureau of Labor Statistics's commitment to providing credible and publicly accessible data. We also thank the developers of Statsmodels, Pandas, and Matplotlib, as these packages form the foundation of FlexCPI. Finally, we thank Editage for English language editing support.
\clearpage

# References
::: {#refs}
:::

