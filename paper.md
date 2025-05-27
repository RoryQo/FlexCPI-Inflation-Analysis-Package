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
date: 27 May 2025
bibliography: paper.bib
nocite: |
  @*
---


## Summary


FlexCPI is a Python package that enables users to construct and analyze custom price indices utilizing Bureau of Labor Statistics (BLS) data. It enables the construction of custom price indices by offering keyword-based series search, series data extraction via the BLS API, series matching to official expenditure weights or manual weight assignment, along with index and year-over-year inflation computation over any period for maximum flexibility. To ensure index validity, the package includes a function to normalize the weights so that they sum to one.

FlexCPI also includes functions that support the analysis of the computed price indices, allowing for easy plotting of price index trends. It also features integrated options for comparison with the official CPI series and simple forecasting using ARIMA models.

Additionally, the package includes several predefined consumption baskets built from simple approximations of weights and series from the BLS Consumer Expenditure Survey (full predefined baskets are viewable in the GitHub repository). These predefined baskets are designed to be directly compatible with all the analysis functions included in the package and ready for comparative analysis.


## Statement of Need

Economists and researchers can tailor CPI baskets for specific populations or geographies and use these baskets to inform policy decisions, conduct specialized economic analyses, and evaluate marginal effects. While CPI is a widely used macroeconomic indicator, current tools for CPI analysis are limited to fetching national-level inflation indices or require extensive manual effort to compile custom indices via available APIs. 

FlexCPI offers a dedicated Python package for constructing and analyzing custom CPI indexes. It simplifies the process of selecting series and weights, computing custom indices and inflation, and comparing these inflation trends to official CPI series. Built-in predefined baskets, including student, senior, low-income, and young professional, make it easy to start comparing inflation effects across different demographics. 

Currently, there is no open-source software with this level of price index computation flexibility using the BLS API; therefore, FlexCPI is a critical resource for those seeking greater control and transparency in inflation measurement.




# Acknowledgments

We gratefully acknowledge the Bureau of Labor Statistics's commitment to providing credible and publicly accessible data. We also thank the developers of Statsmodels, Pandas, and Matplotlib, as these packages form the foundation of FlexCPI. Finally, we thank Editage for English language editing support.
\clearpage

# References
::: {#refs}
:::

