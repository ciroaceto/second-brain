import time
from typing import Dict, List
from dataclasses import dataclass, field

@dataclass
class Metric:
    name: str
    value: float
    timestamp: float = field(default_factory=time.time)

class MetricsCollector:
    def __init__(self):
        self.metrics: List[Metric] = []
    
    def record(self, name: str, value: float):
        """Record a metric."""
        self.metrics.append(Metric(name, value))
    
    def get_metrics(self, name: str = None) -> List[Metric]:
        """Get metrics, optionally filtered by name."""
        if name:
            return [m for m in self.metrics if m.name == name]
        return self.metrics
    
    def get_stats(self, name: str) -> Dict:
        """Get statistics for a metric."""
        metrics = self.get_metrics(name)
        if not metrics:
            return {}
        values = [m.value for m in metrics]
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
        }

collector = MetricsCollector()

