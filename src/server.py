# main.py

import os
import uuid
import requests
from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List
from pathlib import Path
from report_generator import ReportGenerator

app = FastAPI()

class ReportRequest(BaseModel):
    file_urls: List[str]
    template_html_url: str

def download_file(url: str, save_path: str):
    """
    Downloads a file from a URL and saves it to the specified path.
    """
    print(f"Downloading file from {url} to {save_path}")
    response = requests.get(url)
    response.raise_for_status()
    with open(save_path, 'wb') as f:
        f.write(response.content)

def generate_report_task(file_urls, template_html_url, request_id):
    """
    Background task to generate a report based on provided file URLs and a template URL.
    """
    # Create a unique directory for this request using UUID
    results_folder = Path(f"results/{request_id}")
    results_folder.mkdir(parents=True, exist_ok=True)

    # Define paths for temporary files
    template_path = results_folder / "template.html"
    output_path = results_folder / "output_report.html"

    # Download the HTML template
    try:
        download_file(template_html_url, str(template_path))
    except Exception as e:
        error_data = {"request_id": request_id, "error": f"Failed to fetch template HTML: {str(e)}"}
        print(f"Error: {error_data}")
        return

    # Download PDF files
    file_paths = []
    try:
        for index, file_url in enumerate(file_urls):
            file_path = results_folder / f"File{index + 1}.pdf"
            file_paths.append(str(file_path))
            download_file(file_url, str(file_path))
    except Exception as e:
        error_data = {"request_id": request_id, "error": f"Failed to download files: {str(e)}"}
        print(f"Error: {error_data}")
        return

    # Run ReportGenerator
    print("Running ReportGenerator...")
    report_generator = ReportGenerator(file_paths, str(template_path))
    try:
        report_generator.save_summary_to_file(output_path)
    except Exception as e:
        error_data = {"request_id": request_id, "error": f"Report generation failed: {str(e)}"}
        print(f"Error: {error_data}")
        return


@app.post("/generate-report/")
def generate_report(request: ReportRequest, background_tasks: BackgroundTasks):
    """
    Endpoint to initiate report generation based on provided file URLs and a template URL.
    """
    # Generate a unique request ID and create a results folder
    request_id = str(uuid.uuid4())

    print(f"Received a new report generation request with ID: {request_id}")
    print(f"Files: {request.file_urls}")
    print(f"Template: {request.template_html_url}")

    results_folder = Path(f"results/{request_id}")

    # Launch the background task
    background_tasks.add_task(
        generate_report_task,
        request.file_urls,
        request.template_html_url,
        request_id
    )

    # Return immediately to the client with the request ID
    return {"message": "Report generation started", "request_id": request_id, "folder_path": str(results_folder.resolve())}
