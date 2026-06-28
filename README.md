# AI-Powered Intelligent Pavement Asset Management System

![Project Banner](https://img.shields.io/badge/Status-Production_Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-YOLOv8-EE4C2C.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B.svg)

## Project Overview
This project is an end-to-end, production-ready **Pavement Asset Management System**. It leverages cutting-edge Deep Learning (YOLOv8) to automate the detection of road defects (potholes, cracks, etc.) and integrates a robust civil engineering rules-engine to compute severity, recommend maintenance actions, calculate a Road Health Index (RHI), and estimate repair costs.

## Key Features
- **Automated Defect Detection**: Detects 7 classes of pavement damage (Pothole, Longitudinal Crack, Transverse Crack, Alligator Crack, Rutting, Manhole Damage, Road Marking Damage).
- **Engineering Logic Engine**: Translates AI bounding boxes into quantitative severity levels (Low, Medium, High, Critical) based on relative surface area.
- **Maintenance Recommendations**: Automates decision-making by mapping defect severity to actionable repair methods (e.g., Crack Sealing, Full Depth Patching).
- **Interactive Dashboard**: A beautiful, responsive Streamlit web application for real-time inference and analytics.
- **Automated PDF Reporting**: Generates professional, downloadable inspection reports using ReportLab.
- **Road Health Index (RHI)**: A custom algorithm scoring the pavement condition from 0-100 based on weighted deductions.

## Architecture & Folder Structure

```text
AI-Pavement-Inspection-System/
├── app/
│   └── main.py                 # Streamlit dashboard entry point
├── config/
│   └── parameters.yaml         # Configuration for thresholds, costs, maintenance logic
├── data/
│   └── sample_images/          # Demo images for the dashboard testing
├── docs/
│   └── Technical_Report.md     # Full academic/technical project report
├── src/
│   ├── data_processing/        # Scripts to format RDD2022 to YOLO format
│   ├── model/                  # YOLO training pipeline, evaluation, inference
│   ├── engineering/            # Civil engineering logic (severity, cost, RHI)
│   └── reporting/              # ReportLab PDF generation
├── tests/
│   └── test_engineering.py     # PyTest unit tests for civil engineering logic
├── requirements.txt            # Python dependencies
└── README.md                   # This file

- **AI Pavement Asset Management System**: Architected and developed an end-to-end intelligent infrastructure inspection system utilizing Python, PyTorch, and YOLOv8 to automate road defect detection with real-time inference capabilities.
- **Civil Engineering Integration**: Engineered a robust business-logic engine mapping raw AI object detection outputs to quantitative severity metrics, calculating a 0-100 Road Health Index (RHI) and automated repair cost estimates based on industry-standard unit rates.
- **Data Pipeline & MLOps**: Developed data processing pipelines to convert Pascal VOC XML annotations to YOLO format, utilizing 70/10/20 splits and data augmentation to train a highly robust object detection model.
- **Full-Stack Deployment**: Deployed a responsive Streamlit web dashboard for interactive visual inspection, featuring automated PDF report generation (ReportLab) and dynamic data visualization (Plotly).
- **Software Engineering Best Practices**: Built a modular, production-ready codebase featuring configuration-driven parameters (YAML), comprehensive Pytest unit coverage for engineering logic, and clean MVC architecture.

## License
This project is licensed under the MIT License.
