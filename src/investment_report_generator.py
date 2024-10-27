# ReportGenerator.py

import os
from openai import OpenAI
from htmldocx import HtmlToDocx
from prompt_builder import PromptBuilder

class ReportGenerator:
    def __init__(self, api_key, investor_pdf, kpi_pdf, portfolio_pdf, template_html):
        """
        Initialize the ReportGenerator with paths to input files and the API key.

        :param api_key: OpenAI API key.
        :param investor_pdf: Path to the Investor Presentation PDF file.
        :param kpi_pdf: Path to the KPI PDF file.
        :param portfolio_pdf: Path to the Portfolio Investments PDF file.
        :param template_html: Path to the HTML template file.
        """
        self.api_key = api_key
        self.prompt_builder = PromptBuilder(investor_pdf, kpi_pdf, portfolio_pdf, template_html)

        self.context = [
            {"role": "system", "content": "You are an assistant that answers questions based on the provided documents. The documents are attached with <Filename Start> and <Filename End> tags. Your role is to generate a summary based on the extracted information and put it into the report template format supplied in the <Report Template Start> <Report Template End> tags. Retain the css."}
        ]

    def initialize_conversation_context(self):
        """
        Initializes the conversation context with the generated prompt.
        """
        prompt = self.prompt_builder.build_prompt()
        self.context.append({"role": "user", "content": prompt})

    def generate_summary(self):
        """
        Generates a report summary using the AI service.
        """
        self.initialize_conversation_context()

        client = OpenAI(api_key=self.api_key)

        response = client.chat.completions.create(
            messages=self.context,
            model="gpt-4o",
        )

        answer = response.choices[0].message.content
        return answer

    def save_summary_to_file(self, output_path="template/output_report.html"):
        """
        Generates the report and saves it to a file.
        
        :param output_path: Path to save the output report file.
        """
        summary = self.generate_summary()
        with open(output_path, "w") as f:
            f.write(summary)

        # Convert the HTML report to DOCX
        new_parser = HtmlToDocx()
        new_parser.parse_html_file(output_path, f"{output_path}.docx")

        print(f"Summary has been generated and saved to '{output_path}'.")

# Example usage
if __name__ == "__main__":
    # Load OpenAI API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        raise ValueError("API key not found. Set the OPENAI_API_KEY environment variable.")

    investor_pdf = "docs/report_data/Investor presentation.pdf"
    kpi_pdf = "docs/report_data/KPI.pdf"
    portfolio_pdf = "docs/report_data/portfolio_investments.pdf"
    template_html = "template/report2.html"

    report_generator = ReportGenerator(api_key, investor_pdf, kpi_pdf, portfolio_pdf, template_html)
    report_generator.save_summary_to_file(output_path="template/output_report.html")
