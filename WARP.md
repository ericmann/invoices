# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Python-based invoice generator that creates professional PDF invoices from YAML data files. The system uses WeasyPrint for PDF generation, Markdown for content formatting, and external CSS for styling.

## Key Development Commands

### Setup and Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Invoice Generation
```bash
# Generate all new invoices (skips existing PDFs)
python main.py

# Force regenerate all invoices (overwrites existing PDFs)
python main.py --regenerate

# Debug mode - saves HTML output for inspection
python main.py --debug

# Combined: regenerate with debug output
python main.py --regenerate --debug
```

### Creating New Invoices
```bash
# Copy template for new invoice
cp invoices/_template.yaml invoices/INVOICE_NUMBER.yaml
```

## Architecture

### Core Components

- **main.py**: Single-file application containing all logic
  - `load_invoice_data()`: YAML file parsing
  - `create_markdown_invoice()`: Converts YAML data to Markdown
  - `generate_pdf()`: Markdown → HTML → PDF pipeline
  - `get_invoice_files()`: File discovery (excludes _template.yaml)
  - `check_existing_pdf()`: Duplicate prevention logic

### Data Flow
1. Scan `invoices/*.yaml` (excluding `_template.yaml`)
2. Load YAML data and validate structure
3. Convert to Markdown using template
4. Apply CSS styling from `includes/style.css`
5. Generate PDF using WeasyPrint
6. Save to `output/invoice_{number}_{YYYYMMDD}.pdf`

### Directory Structure
```
├── main.py              # Single-file application
├── requirements.txt     # Python dependencies
├── invoices/           # YAML invoice data
│   ├── _template.yaml  # Template file (ignored by processor)
│   └── *.yaml          # Individual invoice files
├── includes/           # Assets and styling
│   └── style.css      # PDF styling (Google Fonts + custom CSS)
└── output/            # Generated PDF files
```

## Key Technical Details

### YAML Invoice Structure
- Required fields: `invoice_number`, `invoice_date`, `due_date`, `from_name`, `from_email`, `to_name`, `services` (array), `total_amount`, `payment_instructions`, `terms`
- Optional fields: `to_email` (displays under client name if provided)
- Services array: each item has `description`, `hours`, `rate`, `amount`

### PDF Generation Pipeline
1. YAML → Python dict
2. Python dict → Markdown (using string templates)
3. Markdown → HTML (using `markdown` library with tables extension)
4. HTML + CSS → PDF (using WeasyPrint)

### Styling System
- External CSS file: `includes/style.css`
- Google Fonts: Funnel Display (headers), Geist (body), Geist Mono (code)
- Color scheme: Blue (#168FD8), Red (#E25041), Dark gray (#030303)
- Fallback styling if CSS file missing

### File Naming Convention
- Input: `invoices/{invoice_number}.yaml`
- Output: `output/invoice_{invoice_number}_{YYYYMMDD}.pdf`
- Debug: `debug.html` (root directory)

### Duplicate Prevention
- Checks for existing PDFs matching pattern before generation
- `--regenerate` flag bypasses this check
- Uses glob patterns to find existing files

## Working with the Codebase

### Adding New Features
- All logic is in single `main.py` file
- CSS customizations go in `includes/style.css`
- Template modifications in `invoices/_template.yaml`

### Debugging Invoice Layout
- Use `--debug` flag to save HTML output
- Open `debug.html` in browser to inspect styling
- CSS changes require regeneration to see effects

### Dependencies
- `weasyprint==59.0`: PDF generation engine
- `markdown==3.4.4`: Markdown to HTML conversion
- `PyYAML==6.0.1`: YAML file parsing
- `pydyf==0.10.0`: WeasyPrint dependency

### Git Ignore Patterns
- `.venv/`: Virtual environment
- `output/`: Generated PDFs (not version controlled)
- `invoices/`: Invoice data (not version controlled for privacy)
- `debug.html`: Debug output

## Command Line Interface

The application uses `argparse` with two optional flags:
- `--regenerate`: Force overwrite existing PDFs
- `--debug`: Save HTML output for inspection

Both flags can be combined and the application provides clear feedback about processing mode and results.
