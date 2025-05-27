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

FlexCPI is a Python package that allows users to build and analyze custom price indices using Bureau of Labor Statistics (BLS) data. It enables the construction of custom price indices by offering keyword-based series search, series data extraction via the BLS API, series matching to official expenditure weights or manual weight assignment, along with index and year-over-year inflation computation over any period for maximum flexibility. To ensure index validity, the package includes a function to normalize the weights to sum to one.

FlexCPI also includes functions that support the analysis of the computed price indices for easy plotting price indices trends, integrated options to compare with official benchmarks, and simple forecasting using ARIMA models.

Additionally, the package includes several predefined consumption baskets built from simple approximations of weights and series from the BLS Consumer Expenditure Survey (full predefined baskets are viewable in the GitHub repository). These predefined baskets are designed to be directly compatible with all the analysis functions included in the package and ready for comparative analysis.


# Statement of need

Time-series analyses are fundamental to macroeconomic research. FRED provides publicly available macroeconomic indicator data. While current packages, such as StatsModels, contain time-series analysis functions, and the Fredapi package allows users to download and import data from FRED easily, the FredQuincast package goes a step further by integrating and automating the two components. By streamlining exploratory time-series tasks, such as stationarity testing, model selection, and basic forecasting, this package helps macroeconomic researchers save time on routine tasks and enhance workflow reproducibility.

# Acknowledgments

We gratefully acknowledge the Bureau of Labor Statistics's commitment to providing credible and publicly accessible data. We also thank the developers of Statsmodels, Pandas, and Matplotlib, as these packages form the foundation of FlexCPI. Finally, we thank Editage for English language editing support.
\clearpage

# References
::: {#refs}
:::

