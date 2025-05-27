# Carbon Intensity Data Import Tool

This document describes how to use the carbon intensity import tool in the GAISSALabel platform.

## Overview

The `import_carbon_intensity` management command allows you to import carbon intensity data (measured in kgCO2/kWh) for different countries from various sources. This data is essential for calculating the environmental impact of ML models when deployed in different regions.

## Quick Start
To quickly start using the carbon intensity import feature, execute the following command in your terminal:

```bash
python manage.py import_carbon_intensity
```

## Available Data Sources

The command can import data from:

1. **CSV files** on your local filesystem
2. **URLs** (default set to: https://ourworldindata.org/grapher/carbon-intensity-electricity.csv?v=1&csvType=full&useColumnShortNames=true)

## Command Usage

### Basic Command

```bash
python manage.py import_carbon_intensity [options]
```

### Options

| Option | Description |
|--------|-------------|
| `--file PATH` | Path to a CSV file containing carbon intensity data |
| `--url URL` | URL to download carbon intensity data from |
| `--verbose` | Enable more detailed output during import |

### Examples

**Import from default URL (Our World In Data):**
```bash
python manage.py import_carbon_intensity
```

**Import from a local CSV file:**
```bash
python manage.py import_carbon_intensity --file path/to/carbon_intensity_data.csv
```

**Import from a specific URL:**
```bash
python manage.py import_carbon_intensity --url https://example.com/carbon_intensity.csv
```

## CSV Data Format

The CSV file should contain the following columns (case insensitive):

| Column Name | Value | Description |
|-------------|-------------|-------------|
| Entity | country (string) | Country name |
| Code | code (string: max 5 chars) | ISO country code |
| Year | year (int) | Year of the carbon intensity value |
| co2_intensity__gco2_kwh (float) | carbon_intensity | Carbon intensity value in kgCO2/kWh |
