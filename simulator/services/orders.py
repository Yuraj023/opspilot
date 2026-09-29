from dataclasses import dataclass


@dataclass
class OrdersService:
    name: str = "orders-api"
    version: str = "v3.2.0"

    latency_ms: float = 240.0
    error_rate: float = 0.5
    cpu_percent: float = 47.0
    memory_percent: float = 57.0

    healthy: bool = True

    def apply_redis_failure(self) -> None:
        self.latency_ms = 1750.0
        self.error_rate = 12.5
        self.cpu_percent = 74.0
        self.memory_percent = 63.0
        self.healthy = False

    def recover(self) -> None:
        self.latency_ms = 230.0
        self.error_rate = 0.4
        self.cpu_percent = 45.0
        self.memory_percent = 55.0
        self.healthy = True

    def metrics(self) -> dict:
        return {
            "service": self.name,
            "version": self.version,
            "p95_latency_ms": self.latency_ms,
            "error_rate_percent": self.error_rate,
            "cpu_percent": self.cpu_percent,
            "memory_percent": self.memory_percent,
            "healthy": self.healthy,
        }