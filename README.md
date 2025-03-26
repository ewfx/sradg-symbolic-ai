# ReconciliationFlow: Anomaly Detection System

## Overview

ReconciliationFlow is an advanced anomaly detection system designed to streamline financial reconciliation by automating the detection of inconsistencies across multiple data sources. This system leverages machine learning and large language models (LLMs) to enhance accuracy, reduce manual efforts, and provide meaningful insights.

## Technical Approach

The system follows a modular and scalable architecture that allows seamless integration with existing reconciliation processes.

### 1. Data Ingestion & Preprocessing

- **Sources**: Historical and real-time data are ingested from Excel files and metadata files.
- **Processing**:
  - Converts data into JSON format.
  - Extracts key, criteria, derived, historical, date, and comment columns for reconciliation.

### 2. Anomaly Detection Pipeline

- **Core Model**: The anomaly detection engine is powered by **GPT-4o-mini** for recognizing historical patterns and deviations.
- **Processing Flow**:
  1. The `AnomalyDetection` agent analyzes discrepancies between historical and real-time data.
  2. It classifies breaks as either anomalies or expected variations based on historical trends.
  3. A structured Markdown report is generated with explanations and classifications.

### 3. Review & Validation

- **Review Agent**: The `AnomalyReview` agent cross-validates flagged anomalies to minimize false positives and negatives.
- **Rules Applied**:
  - Only significant breaks violating historical trends are anomalies.
  - Uniform deviations across time do not qualify as anomalies.
  - Outlier detection is based on predefined reconciliation rules.
- **Feedback Loop**: If necessary, the system retries detection and refinement up to three times.

### 4. Reporting & Summarization

- **Summary Generation**:
  - The `ReportSummary` agent generates a structured, easy-to-understand summary for business stakeholders.
  - Each data point includes:
    - **Break status**
    - **Resolution details**
    - **Anomaly classification**
- **Output Formats**:
  - Reports are stored in Markdown (`finalReport.md`).
  - Reviewer feedback is logged in (`reviewComments.md`).

## Workflow

1. **Load Data**: Historical and real-time datasets are extracted and converted into JSON.
2. **Anomaly Detection**: Discrepancies are analyzed based on past trends.
3. **Validation**: A review agent ensures accuracy and classifies anomalies.
4. **Report Generation**: Structured insights are compiled for business review.

## Configuration & Agents

The system utilizes specialized agents for different tasks:

### Agents

- **Anomaly Detector** (`anomaly_detector`):
  - Identifies and classifies anomalies based on reconciliation data.
- **Anomaly Reviewer** (`anomaly_reviewer`):
  - Validates anomaly classification against strict reconciliation rules.
- **Report Summary Agent** (`report_summary`):
  - Converts analysis into a readable format for stakeholders.

### Tasks

- **Analysis Task** (`analysis_task`):
  - Evaluates data discrepancies and applies anomaly detection rules.
- **Review Task** (`review_task`):
  - Ensures detected anomalies conform to predefined business logic.
- **Reporting Task** (`reporting_task`):
  - Generates structured summaries for easy interpretation.

## Installation & Execution

### Prerequisites

- Python 3.10+
- CrewAI

### Running the Application

```bash
crewai flow kickoff
```

### Output Files

- `output/finalReport.md`: Final reconciliation summary.
- `output/reviewComments.md`: Review and validation logs.

## Next Steps: Actionable API Integration

To enhance anomaly resolution, the next phase involves integrating APIs that trigger automated actions when anomalies are detected. These may include:

- **Operator Assistance**: Generating resolution tasks for manual review.
- **Automated Actions**:
  - Calling external APIs to rectify detected issues.
  - Sending notifications or emails to relevant stakeholders.
  - Creating tickets in incident management systems.

This enhancement will ensure that anomalies are not just identified but also efficiently resolved through an automated workflow.

## Benefits

- **Enhanced Accuracy**: AI-powered detection minimizes human errors.
- **Time Efficiency**: Reduces manual effort in identifying anomalies.
- **Scalability**: Designed to handle large datasets effectively.
- **Actionable Insights**: Provides clear explanations for detected anomalies.
