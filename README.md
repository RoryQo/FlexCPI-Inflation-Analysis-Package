# FlexCPI
Python package for building and analyzing custom Consumer Price Indexes (CPI). FlexCPI lets users define their own consumption baskets and compute inflation measures tailored to specific populations, regions, or use cases.

```
flexcpi/
├── flexcpi/                    # Core package source
│   ├── __init__.py
│   ├── calculator.py           # Main CPI computation engine
│   ├── baskets.py              # Predefined and user-defined basket utilities
│   ├── data_loader.py          # Functions to load price data from local/API
│   ├── visualizer.py           # Plotting utilities for CPI trends
│   └── utils.py                # Helpers: deflators, weight normalization, etc.
│
├── examples/                   # Jupyter notebooks or scripts
│   └── example_custom_cpi.ipynb
│
├── tests/                      # Unit and integration tests
│   ├── test_calculator.py
│   └── test_baskets.py
│
├── pyproject.toml              # Package metadata & build system
├── README.md                   # Project overview and usage instructions
├── LICENSE                     # Licensing file (e.g., MIT)
├── .gitignore
└── .github/                    # GitHub Actions/issue templates (optional)
    └── workflows/
        └── test.yml           # CI pipeline (e.g., pytest on push)
```
