import os
from pdf_query_tool import PDFQueryTool

def main():
    # Load OpenAI API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        raise ValueError("API key not found. Set the OPENAI_API_KEY environment variable.")

    # pdf_file = 'docs/2301.02111v1.pdf'  # Path to the PDF file
    pdf_file = 'docs/KPI Update.pdf'
    tool = PDFQueryTool(api_key)

    # Extract text and initialize context once
    pdf_text = tool.extract_text_from_pdf(pdf_file)
    tool.initialize_conversation_context(pdf_text)

    print("Ask me any questions about the document. Type 'exit' to quit.")

    while True:
        question = input("You: ")
        if question.lower() == 'exit':
            print("Exiting the program. Goodbye!")
            break
        
        # Ask the question using the existing context
        answer = tool.ask_question_with_context(question)  # Use the updated method

        print(f"AI: {answer}")

if __name__ == "__main__":
    main()
