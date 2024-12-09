# Wikipedia Music Project Context

## Project Overview
I'm working on a Python project that scrapes Wikipedia articles looking for music-related content. The code currently lives in a flat directory structure with separate folders for utilities, analysis, etc. I want to transition this into a proper Python package structure.

## Agreed Structure
```
wikipedia_random_music/
├── src/
│   └── wiki_music/
│       ├── __init__.py
│       ├── data_collection/
│       │   ├── __init__.py
│       │   └── wiki_scraper.py
│       ├── utilities/
│       │   ├── __init__.py
│       │   └── helpers.py
│       └── analysis/
│           ├── __init__.py
│           └── metrics.py
├── tests/
├── data/
│   ├── raw/         # Original Wikipedia descriptions
│   ├── processed/   # Classified data
│   └── models/      # Any trained models
├── requirements.txt
├── setup.py
└── README.md
```

## Key Points Discussed
1. Version control (.git) and virtual environment (.venv) stay at root level
2. Empty __init__.py files are needed to mark directories as Python packages
3. setup.py enables development installation with `pip install -e .`
4. Data organization separates raw data from processed data
5. Project should be structured as a single Python package with logical components

## Current Status
We've outlined the structure and discussed migration strategy. The next step is implementing the transition of existing code into this new structure.

## Previous Files Referenced
- get_urls.py (Wikipedia API interaction)
- data_harness.py (Data processing)
- Various analysis scripts

I'm now working on migrating the existing codebase to this structure and have questions about the specific implementation details.
