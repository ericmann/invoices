# Invoice Generator

A Python script that generates professional PDF invoices from YAML data files.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Directory structure:
   ```
   .
   ├── main.py              # Main script
   ├── requirements.txt     # Python dependencies
   ├── invoices/           # YAML invoice data files
   │   ├── _template.yaml  # Template for new invoices
   │   └── 1001.yaml       # Example invoice
   ├── includes/           # Styling and assets
   │   └── style.css       # PDF styling
   └── output/             # Generated PDF files
   ```

## Usage

### Creating a New Invoice

1. Copy the template file:
   ```bash
   cp invoices/_template.yaml invoices/YOUR_INVOICE_NUMBER.yaml
   ```

2. Edit the new YAML file with your invoice details:
   - Replace placeholders with actual values
   - Update services, rates, and amounts
   - Modify payment instructions and terms

3. Run the script to generate all pending invoices:
   ```bash
   python main.py
   ```

### Command Line Options

The script supports the following command line options:

- **Standard generation**: `python main.py`
  - Processes all invoices and skips any that already have PDFs generated

- **Force regeneration**: `python main.py --regenerate`
  - Forces regeneration of all invoices, overwriting existing PDFs
  - Useful when you've updated styling or invoice data and want fresh PDFs

- **Debug mode**: `python main.py --debug`
  - Saves the generated HTML to `debug.html` for browser inspection
  - Useful for testing CSS changes and troubleshooting layout issues
  - Opens in your browser to see exactly how the invoice will look

- **Combined flags**: `python main.py --regenerate --debug`
  - You can combine flags to regenerate all invoices AND save debug output

### Customizing Invoice Styling

You can customize the appearance of your invoices by editing `includes/style.css`. The CSS file contains styling for:

- Typography and fonts (Google Fonts: Funnel Display, Geist, Geist Mono)
- Colors and spacing
- Table formatting
- Layout and margins

If the CSS file is missing, the script will fall back to minimal default styling.

### How It Works

- The script scans the `invoices/` directory for all `.yaml` files (except `_template.yaml`)
- For each invoice file, it checks if a PDF already exists in the `output/` directory
- If no PDF exists (or `--regenerate` is used), it generates a new one with the current date
- If a PDF already exists and `--regenerate` is not used, it skips generation to avoid duplicates
- CSS styling is loaded from `includes/style.css` at runtime

### Example Invoice YAML Structure

```yaml
invoice_number: "1001"
invoice_date: "May 31, 2025"
due_date: "Upon receipt"

from_name: "Your Name"
from_email: "your.email@domain.com"

to_name: "Client Name"
# to_email: "client@example.com"  # Optional field

services:
  - description: "Service Description"
    hours: 10.0
    rate: 100.00
    amount: 1000.00

total_amount: 1000.00

payment_instructions: |
  Payment instructions here

terms: "Payment terms here"
```

**Optional Fields:**
- `to_email`: If provided, the client's email will be displayed under their name in the "To" section. If omitted or empty, only the client name is shown.

## Features

- **YAML-based data storage**: Easy to edit and version control
- **Template system**: Reusable template for consistency
- **Duplicate prevention**: Automatically skips invoices that have already been generated
- **Force regeneration**: `--regenerate` flag to overwrite existing PDFs
- **Debug mode**: `--debug` flag to save HTML output for browser inspection
- **Professional styling**: Clean, modern PDF output with customizable CSS and Google Fonts
- **Batch processing**: Processes multiple invoices in one run
- **Flexible styling**: External CSS file for easy customization 