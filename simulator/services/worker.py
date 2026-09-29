from dataclasses import dataclass


@dataclass
class WorkerService:
    name: str = "worker"
    version: str = "v1.5.0"

    queue_depth: int = 42
    processing_latency_ms: float = 180.0
    error_rate: float = 0.3

    healthy: bool = True

    def apply_bad_deployment(self) -> None:
        self.queue_depth = 1840
        self.processing_latency_ms = 4200.0
        self.error_rate = 8.7
        self.healthy = False

    def recover(self) -> None:
        self.queue_depth = 35
        self.processing_latency_ms = 170.0
        self.error_rate = 0.2
        self.healthy = True

    def metrics(self) -> dict:
        return {
            "service": self.name,
            "version": self.version,
            "queue_depth": self.queue_depth,
            "processing_latency_ms": (
                self.processing_latency_ms
            ),
            "error_rate_percent": self.error_rate,
            "healthy": self.healthy,
        }