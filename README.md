# HTML Data Extraction Pipeline

A Nextflow pipeline for extracting tabular data from HTML reports and consolidating them into Excel files.

## Overview

This pipeline processes HTML reports (typically from Rhapsody primary pipelines), extracts tables and metadata, and outputs individual Excel files for each input. It then merges all Excel files into a consolidated workbook for downstream analysis.

## Features

- Extract tables from HTML reports with automatic title detection
- Add metadata columns (source, assay type, run name, pipeline version)
- Filter out empty rows from extracted data
- Generate individual Excel files per HTML input
- Merge all Excel files into a single consolidated workbook
- Containerized execution for reproducibility

## Requirements

- [Nextflow](https://www.nextflow.io/) (>= 21.04)
- [Docker](https://www.docker.com/) or [Singularity](https://sylabs.io/singularity/)

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd htmlExt_nextflow
   ```

2. **Prepare your input CSV file:**
   Create an `input.csv` file with semicolon-separated values:
   ```csv
   ./input_html/report1.html;assay_type1;source1
   ./input_html/report2.html;assay_type2;source2
   ```

3. **Run the pipeline:**
   ```bash
   nextflow run htmlExt.nf
   ```

   **With custom input file:**
   ```bash
   nextflow run htmlExt.nf --input my_samples.csv
   ```

## Input Format

The pipeline expects a CSV file (default: `input.csv`) with three columns separated by semicolons:
- **Column 1**: Path to HTML file
- **Column 2**: Assay type identifier
- **Column 3**: Source identifier

Example:
```csv
./input_html/AT206-multiomic_Pipeline_Report.html;multiome;demo
./input_html/AT209-atacOnly_Pipeline_Report.html;atac;demo
./input_html/Targeted-AbSeq_Pipeline_Report.html;targeted+abseq;demo
./input_html/WTA-AbSeq-SMK_Pipeline_Report.html;wta+abseq+smk;demo
./input_html/WTA-VDJ_Pipeline_Report.html;wta+vdj;demo
```

## Output

The pipeline generates:

### Individual Excel Files
- **Location**: `results/extracted_html/`
- **Format**: One Excel file per HTML input
- **Naming**: `{input_basename}.xlsx`
- **Content**: Multiple sheets with extracted tables, each with added metadata columns:
  - `source`: Source identifier from input CSV
  - `assayType`: Assay type from input CSV
  - `runName`: Extracted from HTML content
  - `pipelineVersion`: Extracted from HTML content

### Merged Excel File
- **Location**: `results/merged_results.xlsx`
- **Content**: All individual Excel files consolidated into one workbook
- **Merging**: Sheets with the same name are combined; unique sheets are preserved

## Configuration

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `params.input` | `'input.csv'` | Path to input CSV file |

### Container

The pipeline uses the Docker image `yujuanguibdgh/html_ext:latest`. To use a different container, change in `nextflow.config` file:

```nextflow
process.container = 'yujuanguibdgh/html_ext:latest'
docker.enabled = true
```

## Pipeline Structure

```
htmlExt_nextflow/
├── htmlExt.nf              # Main pipeline script
├── modules/
│   ├── extract_html.nf     # HTML extraction process
│   └── merge_excel.nf      # Excel merging process
├── extract_html.py         # Python script for HTML parsing
├── merge_excel.py          # Python script for Excel merging
├── input.csv              # Input file specification
├── input_html/            # Directory containing HTML files
│   ├── AT206-multiomic_Pipeline_Report.html
│   ├── AT209-atacOnly_Pipeline_Report.html
│   └── ...
├── results/               # Output directory (created by pipeline)
│   ├── extracted_html/    # Individual Excel files
│   └── merged_results.xlsx # Consolidated Excel file
├── nextflow.config        # Pipeline configuration (optional)
└── README.md              # This file
```

## Processes

### extract_html
- **Input**: HTML file, assay type, source identifier
- **Function**: 
  - Extracts tables from HTML using BeautifulSoup and pandas
  - Automatically detects table titles from preceding `<h3>` tags or `<caption>` elements
  - Extracts run name from JavaScript variables in HTML
  - Extracts pipeline version from HTML content
  - Adds metadata columns to each table
  - Filters out rows with empty data columns
- **Output**: Individual Excel files with multiple sheets

### merge_excel
- **Input**: Collection of Excel files
- **Function**:
  - Combines all individual Excel files into one workbook
  - Merges sheets with identical names by concatenating data
  - Preserves all unique sheets across files
  - Handles column alignment automatically
- **Output**: Single consolidated Excel workbook

## Data Processing Details

### Metadata Extraction
The pipeline automatically extracts:
- **Run Name**: From JavaScript variables (`run_name = ['value']`)
- **Pipeline Version**: From text patterns matching version numbers
- **Table Titles**: From HTML structure (h3 headers or table captions)

### Data Filtering
- Removes rows where all data columns (excluding metadata) are empty
- Preserves rows with at least one non-empty data value
- Handles both NaN values and empty strings

## Customization

### Adding New Metadata Fields
To extract additional metadata from HTML files, modify `extract_html.py`:

```python
# Add new metadata extraction logic
new_metadata = extract_custom_field(soup)
df.insert(4, "newField", new_metadata)
```

### Changing Table Detection
To modify how tables are identified and titled, update the `extract_tables_with_titles()` function in `extract_html.py`.

### Custom Filtering Rules
Modify the filtering logic in `extract_html.py` to change which rows are kept or removed.

## Troubleshooting

### Common Issues

1. **File not found errors**
   - Ensure HTML file paths in `input.csv` are correct and files exist
   - Use absolute paths if relative paths cause issues

2. **Container platform warnings**
   - Add platform specification to your Docker command or nextflow.config
   - Use `--platform linux/amd64` for compatibility

3. **Empty Excel output**
   - Check that HTML files contain valid `<table>` structures
   - Verify tables have actual data content
   - Review debug output for parsing issues

4. **Merge failures**
   - Ensure all individual Excel files are generated successfully
   - Check for file permission issues in output directories

### Debug Mode
Enable debugging by adding debug output to `extract_html.py`:

```python
# Add to the process loop
with open("debug_output.txt", "w") as debug_file:
    debug_file.write(f"Processing: {html_path}\n")
    debug_file.write(f"Tables found: {len(tables_with_titles)}\n")
    debug_file.write(f"DataFrame shape: {df.shape}\n")
```

## Example Use Cases

- **Bioinformatics Pipeline Reports**: Process output from single-cell analysis pipelines
- **Quality Control Dashboards**: Extract metrics from HTML QC reports
- **Multi-Sample Analysis**: Consolidate results across multiple experimental conditions


## License

Place holder for license information.


## Changelog

### v1.0.0
- Initial release
- HTML table extraction with metadata
- Excel consolidation functionality