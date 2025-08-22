---
id: natural_language_test
title: Create a simple python script that reads a csv file and prints a summary of t...
type: atomic
source: natural_language
acceptance:
  - should count the number of rows and columns, and show the first 5 rows.
  - should handle cases where the CSV file doesn't exist and show a helpful error message.
  - should be named data_summary.
  - should be easy to use from the command line.
policy:
  max_attempts: 3
  max_depth: 3
  timeout_seconds: 300
priority: 5
estimated_effort: low
---

# Create a simple python script that reads a csv file and prints a summary of t...

I need to create a simple Python script that reads a CSV file and prints a summary of the data. The script should count the number of rows and columns, and show the first 5 rows. It should handle cases where the CSV file doesn't exist and show a helpful error message. The script should be named data_summary.py and should be easy to use from the command line. Please make sure it works with Python 3 and uses only standard library modules.

## Requirements

- need to create a simple Python script that reads a CSV file and prints a summary of the data.
- should count the number of rows and columns, and show the first 5 rows.
- should handle cases where the CSV file doesn't exist and show a helpful error message.
- should be named data_summary.
- should be easy to use from the command line.

## Identified Domains

- maintenance
- data

## Technologies Mentioned

- python

## Dependencies

- 5 rows
