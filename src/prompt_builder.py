# PromptBuilder.py

import fitz  # PyMuPDF

class PromptBuilder:
    def __init__(self, investor_pdf, kpi_pdf, portfolio_pdf, template_html):
        """
        Initialize the PromptBuilder with paths to input files.

        :param investor_pdf: Path to the Investor Presentation PDF file.
        :param kpi_pdf: Path to the KPI PDF file.
        :param portfolio_pdf: Path to the Portfolio Investments PDF file.
        :param template_html: Path to the HTML template file.
        """
        self.investor_pdf = investor_pdf
        self.kpi_pdf = kpi_pdf
        self.portfolio_pdf = portfolio_pdf
        self.template_html = template_html

    def extract_text_from_pdf(self, pdf_file: str) -> str:
        """
        Extracts text from the provided PDF file.
        """
        doc = fitz.open(pdf_file)
        pdf_text = ""

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pdf_text += page.get_text("text")  # Extract text from each page

        return pdf_text

    def read_kpi_file(self):
        """Reads key financial metrics from the KPI PDF."""
        kpi_text = self.extract_text_from_pdf(self.kpi_pdf)
        return f"<KPI File Start>{kpi_text}<KPI File End>"

    def read_investor_presentation(self):
        """Reads company overview and other details from the Investor Presentation."""
        investor_text = self.extract_text_from_pdf(self.investor_pdf)
        return f"<Investor Presentation Start>{investor_text}<Investor Presentation End>"

    def read_portfolio_investments(self):
        """Reads investment details from the Portfolio Investments file."""
        portfolio_text = self.extract_text_from_pdf(self.portfolio_pdf)
        return f"<Portfolio Investments Start>{portfolio_text}<Portfolio Investments End>"

    def read_html_template(self):
        """
        Reads the contents of the HTML template file and returns it as a string.
        """
        with open(self.template_html, 'r', encoding='utf-8') as file:
            html_content = file.read()
        return f"<Report Template Start>{html_content}<Report Template End>"

    def build_prompt(self):
        """
        Builds the prompt by combining the extracted text from the PDFs and the HTML template.
        """
        company_overview = self.read_investor_presentation()
        financial_metrics = self.read_kpi_file()
        investment_details = self.read_portfolio_investments()
        template = self.read_html_template()

        # Combine all parts into the prompt
        return company_overview + financial_metrics + investment_details + template
