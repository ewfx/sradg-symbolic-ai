#!/usr/bin/env python

from typing import Optional
import pandas as pd
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start, router, or_

from reconciliationflow.crews.anomaly_detection.anomaly_detection import AnomalyDetection
from reconciliationflow.crews.anomaly_review.anomaly_review import AnomalyReview
from reconciliationflow.crews.report_summary.report_summary import ReportSummary


class ReconciliationState(BaseModel):
    metadata: str = ""
    historicalData: str = ""
    realtimeData: str = ""
    report: str = ""
    valid: bool = False
    feedback: Optional[str] = None
    retryCount: int = 0


class ReconciliatonFlow(Flow[ReconciliationState]):
    """Flow for analysis & classification"""

    @start()
    def generate_input(self):
        #Generate the reconciliation input
        historical_df = pd.read_excel("Reconciliation.xlsx", sheet_name="Historical")
        self.state.historicalData = historical_df.to_json(orient = 'records')

        realtime_df = pd.read_excel("Reconciliation.xlsx", sheet_name="Real Time")
        self.state.realtimeData = realtime_df.to_json(orient = 'records')

        with (open("metadata.txt", "r") as f):
            self.state.metadata = f.read()


    @listen(or_(generate_input, "retry"))
    def generate_analysis(self):
        print("Analysing the data provided & generating analysis report")
        result = (
            AnomalyDetection().crew().kickoff(inputs={
                "metadata": self.state.metadata,
                "historicalData": self.state.historicalData,
                "realtimeData": self.state.realtimeData,
                "feedback": self.state.feedback
            })
        )

        #Store the content
        self.state.report = result.raw

    @router(generate_analysis)
    def evaluate_analysis(self):
        if self.state.retryCount > 1:

            return "completed"

        result = AnomalyReview().crew().kickoff(inputs={
            "report": self.state.report
        })

        self.state.valid = result["valid"]
        self.state.feedback = result["feedback"]
        self.state.retryCount += 1

        if self.state.valid:
            return "completed"

        print("RETRY")
        return "retry"

    @listen("completed")
    def save_result(self):
        if self.state.valid:
            feedbackResult = "The report generated by the anomaly detector was successfully validated.\n"
        else:
            feedbackResult = "The report generated by the anomaly detector was not validated & needs expert review.\n"

        feedbackResult += self.state.feedback
        with open("output/reviewComments.md", "w") as f:
            f.write(feedbackResult)

        result = ReportSummary().crew().kickoff(inputs={
            "report": self.state.report
        })
        summary = result.raw

        with open("output/finalReport.md", "w") as f:
            f.write(summary)


def kickoff():
    ReconciliatonFlow().kickoff()

def plot():
    """Generate a visualization of the flow"""
    flow = ReconciliatonFlow()
    flow.plot("reconciliation_flow")
    print("Flow visualization saved to reconciliation_flow.html")


if __name__ == "__main__":
    #kickoff()
    plot()
