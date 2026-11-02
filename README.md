# Cloud Logistics Platform

An automated logistics document processing and shipment tracking platform built using Python, Playwright, FastAPI, and OCR technologies.

## Overview

The Cloud Logistics Platform automates shipment tracking and logistics document collection across multiple carrier websites.

In traditional logistics workflows, tracking information and shipment documents must be collected manually from different websites. This process is time-consuming, repetitive, and prone to errors.

This project streamlines the process by automating shipment tracking, extracting container information, retrieving carrier-specific documents, merging PDFs, and generating OCR-based text outputs.

## Key Features

- **Automated Shipment Tracking:** Extracts container information from Vanguard Logistics.
- **Multi-Carrier Integration:** Supports carrier-specific tracking workflows for platforms such as ONE, Maersk, Hapag-Lloyd, HMM, Yang Ming, Wan Hai, and ShipmentLink.
- **Dynamic Carrier Routing:** Uses container prefixes and database mappings to identify the appropriate carrier website.
- **Browser Automation:** Uses Playwright to interact with tracking websites and retrieve shipment documents.
- **Dual Processing Modes:**
  - Normal Mode: Retrieves carrier information using direct database mapping.
  - LCL Mode: Extracts container numbers from Vanguard Logistics and dynamically routes them to the respective carrier.
- **PDF Processing:** Downloads and combines Vanguard and carrier-generated shipment documents.
- **OCR Integration:** Extracts text from merged PDF documents and generates searchable text outputs.
- **API Integration:** Uses FastAPI for backend service development.

## System Workflow

1. Receive shipment tracking input.
2. Extract container numbers where required.
3. Identify the shipping carrier using container prefix mapping.
4. Navigate to the corresponding carrier tracking website.
5. Automate the tracking process using Playwright.
6. Retrieve available shipment documents.
7. Save and merge the collected PDF files.
8. Perform OCR on the merged documents.
9. Generate structured text outputs for further processing.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend Framework | FastAPI |
| Browser Automation | Playwright |
| Database | SQL |
| Web Scraping | Playwright, BeautifulSoup |
| Document Processing | PyPDF2 |
| OCR | OCR API |
| API Server | Uvicorn |
| Containerization | Docker |
| Version Control | Git, GitHub |

## Project Structure

```text
cloud_logistics_platform/
│
├── app/
│   └── Application source code
│
├── carotrans_outputs/
│   └── Generated processing outputs
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Nitisha-27/cloud_logistics_platform.git
cd cloud_logistics_platform
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**Linux / macOS**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

```bash
playwright install
```

### 5. Run the Application

Refer to the application entry point and configuration inside the `app/` directory to start the backend service.

## Docker Support

The project includes a Dockerfile for containerized deployment.

Build the Docker image:

```bash
docker build -t cloud-logistics-platform .
```

Run the container:

```bash
docker run -p 8000:8000 cloud-logistics-platform
```

Adjust the port mapping and runtime configuration if required by the application.

## Applications

- Automated logistics documentation.
- Multi-carrier shipment tracking.
- Container information extraction.
- PDF consolidation and document processing.
- OCR-based logistics data extraction.

## Future Enhancements

- Cloud-based deployment and scalability.
- Improved exception handling and retry mechanisms.
- Centralized shipment tracking dashboard.
- Advanced document classification and information extraction.
- Automated monitoring and processing logs.

## Author

**Nitisha Mishra**

B.Tech – Electronics and Communication Engineering (Biomedical Specialization)

GitHub: [Nitisha-27](https://github.com/Nitisha-27)

---

*This project demonstrates the application of browser automation, backend development, database-driven routing, and document processing to real-world logistics workflows.*
