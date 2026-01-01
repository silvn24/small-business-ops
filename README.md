## Purpose
This repository contains exploratory Python scripts used to analyze operational service data in a small service business context.

## Context
These scripts were written to answer operational questions that were not easily addressed using built-in ERP reporting, including:
- comparing actual service time to pricing assumptions (MaintAveTimeCalc-github.py)
- examining technician assignment patterns by property (Day_Partner_change_review-github.py)
- understanding seasonal service-day changes (Day_Partner_change_review-github.py)

## Notes
- The scripts were used as decision-support tools, not production systems.
- The scripts are provided as-is to illustrate applied analysis, not as reusable tools.
- The scripts reference customer and technician identifier column names expected in ERP export files.
- No data files are included, and no identifiers exist in this repository.
- Developed with AI support as a learning and debugging aid. The goal was to have a working analysis, not a perfect script.

## How to Run
- Export the relevant ERP reports to Excel or CSV and place the files locally.
- Update all case-specific input and output filenames in the script to match your environment.
- Input files must use the same column names referenced in the script.
- Run python <script>.py
