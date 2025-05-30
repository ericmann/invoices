import markdown
import weasyprint
import yaml
import os
import glob
from datetime import datetime

def load_invoice_data(yaml_file):
    """Load invoice data from a YAML file."""
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)

def load_css(css_file="includes/style.css"):
    """Load CSS from external file."""
    try:
        with open(css_file, 'r') as file:
            return f"<style>\n{file.read()}\n</style>"
    except FileNotFoundError:
        print(f"Warning: CSS file {css_file} not found. Using minimal styling.")
        return "<style>body { font-family: Arial, sans-serif; margin: 40px; }</style>"

def get_invoice_files():
    """Get all invoice YAML files except the template."""
    invoice_files = glob.glob("invoices/*.yaml")
    # Filter out the template file
    return [f for f in invoice_files if not os.path.basename(f).startswith('_')]

def check_existing_pdf(invoice_number, output_dir="output"):
    """Check if a PDF for this invoice already exists."""
    pattern = os.path.join(output_dir, f"invoice_{invoice_number}_*.pdf")
    existing_pdfs = glob.glob(pattern)
    return len(existing_pdfs) > 0

# Markdown template for the invoice
def create_markdown_invoice(data):
    total_hours = sum(item["hours"] for item in data["services"])
    markdown_content = f"""
# INVOICE

**Invoice Number:** {data["invoice_number"]}  
**Invoice Date:** {data["invoice_date"]}  
**Due Date:** {data["due_date"]}  

## From
{data["from_name"]}  
Email: {data["from_email"]}  

## To
{data["to_name"]}  

## Description of Services
For professional services rendered:

| Description                  | Hours | Rate    | Amount    |
|------------------------------|-------|---------|-----------|
"""
    for service in data["services"]:
        markdown_content += f"| {service['description']:<28} | {service['hours']:>5.1f} | ${service['rate']:>6.2f}/hr | ${service['amount']:>8.2f} |\n"

    markdown_content += f"""
**Total Hours:** {total_hours:.1f}  
**Total Amount Due:** ${data["total_amount"]:,.2f}

## Payment Instructions
{data["payment_instructions"]}

## Terms
{data["terms"]}
"""
    return markdown_content

# Generate the PDF
def generate_pdf(markdown_content, output_filename):
    """Generate PDF from markdown content."""
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)
    
    # Load CSS from external file
    css = load_css()
    
    # Convert Markdown to HTML
    html_content = markdown.markdown(markdown_content, extensions=['tables'])
    # Combine HTML with CSS
    full_html = f"<html><head>{css}</head><body>{html_content}</body></html>"
    # Generate PDF using WeasyPrint
    weasyprint.HTML(string=full_html).write_pdf(output_filename)
    print(f"PDF generated: {output_filename}")

# Main function
def main():
    """Process all invoice YAML files and generate PDFs."""
    # Ensure directories exist
    os.makedirs("invoices", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    os.makedirs("includes", exist_ok=True)
    
    # Get all invoice files
    invoice_files = get_invoice_files()
    
    if not invoice_files:
        print("No invoice files found in the invoices directory.")
        print("Create a YAML file based on _template.yaml in the invoices directory.")
        return
    
    print(f"Found {len(invoice_files)} invoice(s) to process...")
    
    processed_count = 0
    skipped_count = 0
    
    for invoice_file in invoice_files:
        try:
            # Load invoice data
            invoice_data = load_invoice_data(invoice_file)
            invoice_number = invoice_data["invoice_number"]
            
            # Check if PDF already exists
            if check_existing_pdf(invoice_number):
                print(f"Skipping invoice {invoice_number} - PDF already exists")
                skipped_count += 1
                continue
            
            # Create Markdown content
            markdown_content = create_markdown_invoice(invoice_data)
            
            # Generate PDF
            output_filename = f"output/invoice_{invoice_number}_{datetime.now().strftime('%Y%m%d')}.pdf"
            generate_pdf(markdown_content, output_filename)
            processed_count += 1
            
        except Exception as e:
            print(f"Error processing {invoice_file}: {str(e)}")
    
    print(f"\nProcessing complete!")
    print(f"Generated: {processed_count} invoice(s)")
    print(f"Skipped: {skipped_count} invoice(s)")

if __name__ == "__main__":
    main()