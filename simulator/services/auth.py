from dataclasses import dataclass


@dataclass
class AuthService:
    name: str = "auth-api"
    version: str = "v2.4.1"

    latency_ms: float = 180.0
    error_rate: float = 0.2
    cpu_percent: float = 39.0
    memory_percent: float = 51.0

    healthy: bool = True

    def apply_high_cpu(self) -> None:
        self.latency_ms = 1450.0
        self.error_rate = 4.5
        self.cpu_percent = 98.0
        self.memory_percent = 70.0
        self.healthy = False

    def recover(self) -> None:
        self.latency_ms = 170.0
        self.error_rate = 0.2
        self.cpu_percent = 37.0
        self.memory_percent = 50.0
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