import logging
import uuid
import time
import pandas as pd
import numpy as np

class DevProdMetricsEngine:
    def __init__(self):
        self.logger = logging.getLogger("devprod-metrics-engine")

    def calculate_dora_metrics(self, deployment_data: list, incident_data: list):
        """
        Calculates core DORA metrics from deployment and incident logs.
        """
        df_deploy = pd.DataFrame(deployment_data)
        df_inc = pd.DataFrame(incident_data)
        
        freq = len(df_deploy) / 30 # Daily frequency over a month
        cfr = (len(df_inc) / len(df_deploy)) * 100 if len(df_deploy) > 0 else 0
        
        return {
            "deployment_frequency": round(freq, 2),
            "change_failure_rate": f"{round(cfr, 2)}%",
            "maturity": "ELITE" if freq > 1 and cfr < 5 else "HIGH" if freq > 0.5 else "MEDIUM"
        }

    def score_flow_efficiency(self, active_time_mins: int, wait_time_mins: int):
        """
        Calculates the ratio of active development time to total lead time.
        """
        total = active_time_mins + wait_time_mins
        if total <= 0:
            return 1.0
            
        efficiency = (active_time_mins / total) * 100
        return {
            "efficiency_percentage": round(efficiency, 2),
            "state": "FLOWING" if efficiency > 60 else "STALLED"
        }

    def predict_throughput(self, historical_throughput: list, backlog_size: int):
        """
        Predicts future delivery throughput based on historical velocity and backlog depth.
        """
        avg_vel = np.mean(historical_throughput) if len(historical_throughput) > 0 else 5
        est_weeks = backlog_size / avg_vel
        
        return {
            "avg_weekly_throughput": round(avg_vel, 2),
            "estimated_completion_weeks": round(est_weeks, 1),
            "confidence": 0.88
        }

    def detect_burnout_risk(self, survey_score: float, wip_per_dev: float, meeting_hours: int):
        """
        Identifies potential team burnout risks using sentiment and workload signals.
        """
        risk_score = (1 - survey_score) * 40 + (wip_per_dev * 10) + (meeting_hours * 5)
        
        return {
            "risk_score": round(risk_score, 2),
            "risk_level": "HIGH" if risk_score > 70 else "MEDIUM" if risk_score > 40 else "LOW",
            "primary_driver": "Workload" if wip_per_dev > 5 else "Sentiment" if survey_score < 0.5 else "None"
        }

if __name__ == "__main__":
    engine = DevProdMetricsEngine()
    
    # 1. DORA Metrics
    deploys = [{"id": 1, "status": "SUCCESS"}] * 60
    incidents = [{"id": 101, "severity": "HIGH"}] * 3
    print("DORA Metrics:", engine.calculate_dora_metrics(deploys, incidents))
    
    # 2. Flow Efficiency
    print("Flow Efficiency:", engine.score_flow_efficiency(1800, 600))
    
    # 3. Throughput Prediction
    history = [12, 14, 11, 15, 13]
    print("Throughput:", engine.predict_throughput(history, 150))
    
    # 4. Burnout Risk
    print("Burnout Risk:", engine.detect_burnout_risk(0.7, 3.5, 12))
