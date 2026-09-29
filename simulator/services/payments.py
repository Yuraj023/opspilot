from dataclasses import dataclass


@dataclass
class PaymentsService:
    name: str = "payments-api"
    version: str = "v1.8.2"

    latency_ms: float = 220.0
    error_rate: float = 0.4
    cpu_percent: float = 45.0
    memory_percent: float = 55.0
    db_pool_percent: float = 48.0

    healthy: bool = True

    def apply_slow_query(self) -> None:
        self.latency_ms = 2800.0
        self.error_rate = 7.2
        self.cpu_percent = 61.0
        self.memory_percent = 68.0
        self.db_pool_percent = 98.0
        self.healthy = False

    def apply_high_cpu(self) -> None:
        self.latency_ms = 1250.0
        self.error_rate = 2.8
        self.cpu_percent = 97.0
        self.memory_percent = 72.0
        self.db_pool_percent = 62.0
        self.healthy = False

    def apply_memory_leak(self) -> None:
        self.latency_ms = 1100.0
        self.error_rate = 3.1
        self.cpu_percent = 70.0
        self.memory_percent = 96.0
        self.db_pool_percent = 66.0
        self.healthy = False

    def apply_database_exhaustion(self) -> None:
        self.latency_ms = 2200.0
        self.error_rate = 6.4
        self.cpu_percent = 58.0
        self.memory_percent = 64.0
        self.db_pool_percent = 99.0
        self.healthy = False

    def recover(self) -> None:
        self.latency_ms = 210.0
        self.error_rate = 0.3
        self.cpu_percent = 43.0
        self.memory_percent = 53.0
        self.db_pool_percent = 42.0
        self.healthy = True

    def metrics(self) -> dict:
        return {
            "service": self.name,
            "version": self.version,
            "p95_latency_ms": self.latency_ms,
            "error_rate_percent": self.error_rate,
            "cpu_percent": self.cpu_percent,
            "memory_percent": self.memory_percent,
            "db_pool_percent": self.db_pool_percent,
            "healthy": self.healthy,
        }