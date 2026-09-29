import json
from pathlib import Path

import yaml

from simulator.generators.events import (
    generate_code_change_event,
    generate_deployment_events,
)
from simulator.generators.logs import (
    generate_logs,
)
from simulator.generators.metrics import (
    generate_metrics,
)
from simulator.services.auth import AuthService
from simulator.services.orders import OrdersService
from simulator.services.payments import PaymentsService
from simulator.services.worker import WorkerService


PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)

SCENARIO_DIR = (
    PROJECT_ROOT
    / "simulator"
    / "scenarios"
)

DATA_DIR = (
    PROJECT_ROOT
    / "simulator"
    / "data"
)


class IncidentSimulator:
    def __init__(self):
        self.services = {
            "payments-api": PaymentsService(),
            "auth-api": AuthService(),
            "orders-api": OrdersService(),
            "worker": WorkerService(),
        }

    def load_scenario(
        self,
        scenario_name: str,
    ) -> dict:
        path = (
            SCENARIO_DIR
            / f"{scenario_name}.yaml"
        )

        if not path.exists():
            raise FileNotFoundError(
                f"Scenario not found: {scenario_name}"
            )

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            return yaml.safe_load(file)

    def apply_failure(
        self,
        scenario: dict,
    ) -> None:
        service_name = scenario["service"]
        failure_type = scenario["failure_type"]

        service = self.services.get(
            service_name
        )

        if service is None:
            raise ValueError(
                f"Unknown service: {service_name}"
            )

        failure_methods = {
            "slow_query": "apply_slow_query",
            "high_cpu": "apply_high_cpu",
            "memory_leak": "apply_memory_leak",
            "redis_failure": "apply_redis_failure",
            "database_exhaustion": (
                "apply_database_exhaustion"
            ),
            "bad_deployment": "apply_bad_deployment",
        }

        method_name = failure_methods.get(
            failure_type
        )

        if method_name is None:
            raise ValueError(
                f"Unsupported failure type: "
                f"{failure_type}"
            )

        method = getattr(
            service,
            method_name,
            None,
        )

        if method is None:
            raise ValueError(
                f"Service '{service_name}' does not "
                f"support failure '{failure_type}'."
            )

        method()

    def build_evidence(
        self,
        scenario: dict,
    ) -> dict:
        service_name = scenario["service"]
        failure_type = scenario["failure_type"]

        service = self.services[
            service_name
        ]

        service_metrics = generate_metrics(
            service
        )

        logs = generate_logs(
            service=service_name,
            failure_type=failure_type,
        )

        deployment_events = (
            generate_deployment_events(
                current_version=service.version,
                previous_version=self._previous_version(
                    scenario
                ),
            )
        )

        code_change = (
            generate_code_change_event(
                version=service.version,
                failure_type=failure_type,
            )
        )

        return {
            "scenario": {
                "id": scenario["id"],
                "title": scenario["title"],
                "description": scenario[
                    "description"
                ],
                "service": service_name,
                "severity": scenario["severity"],
                "failure_type": failure_type,
                "environment": scenario[
                    "environment"
                ],
            },
            "logs": logs,
            "metrics": service_metrics,
            "deployments": deployment_events,
            "code_changes": [code_change],
            "runbook": {
                "approval_required": scenario[
                    "approval_required"
                ],
                "expected_actions": scenario[
                    "expected_actions"
                ],
                "forbidden_actions": scenario[
                    "forbidden_actions"
                ],
            },
            "ground_truth": {
                "failure_type": failure_type,
                "root_cause": scenario[
                    "root_cause"
                ],
            },
        }

    def _previous_version(
        self,
        scenario: dict,
    ) -> str:
        versions = {
            "payments-api": "v1.8.1",
            "auth-api": "v2.4.0",
            "orders-api": "v3.1.9",
            "worker": "v1.4.8",
        }

        return versions.get(
            scenario["service"],
            "unknown",
        )

    def save_evidence(
        self,
        scenario_id: str,
        evidence: dict,
    ) -> Path:
        output_dir = (
            DATA_DIR
            / "incidents"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        path = (
            output_dir
            / f"{scenario_id}.json"
        )

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                evidence,
                file,
                indent=2,
            )

        return path

    def run(
        self,
        scenario_name: str,
        save: bool = True,
    ) -> dict:
        scenario = self.load_scenario(
            scenario_name
        )

        self.apply_failure(
            scenario
        )

        evidence = self.build_evidence(
            scenario
        )

        if save:
            self.save_evidence(
                scenario_id=scenario["id"],
                evidence=evidence,
            )

        return evidence


def print_evidence(
    evidence: dict,
) -> None:
    print("\n" + "=" * 70)
    print("OPSPILOT INCIDENT SIMULATOR")
    print("=" * 70)

    scenario = evidence["scenario"]

    print(
        f"Scenario   : {scenario['id']}"
    )
    print(
        f"Title      : {scenario['title']}"
    )
    print(
        f"Service    : {scenario['service']}"
    )
    print(
        f"Severity   : {scenario['severity']}"
    )
    print(
        f"Failure    : {scenario['failure_type']}"
    )

    print("\n--- Metrics ---")

    for key, value in evidence[
        "metrics"
    ].items():
        print(
            f"{key}: {value}"
        )

    print("\n--- Logs ---")

    for log in evidence["logs"]:
        print(log)

    print("\n--- Deployments ---")

    for deployment in evidence[
        "deployments"
    ]:
        print(deployment)

    print("\n--- Code Changes ---")

    for change in evidence[
        "code_changes"
    ]:
        print(change)

    print("\n--- Expected Actions ---")

    for action in evidence[
        "runbook"
    ]["expected_actions"]:
        print(
            f"- {action}"
        )

    print("\n--- Ground Truth ---")

    print(
        json.dumps(
            evidence["ground_truth"],
            indent=2,
        )
    )

    print("=" * 70 + "\n")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "Run an OpsPilot incident simulation."
        )
    )

    parser.add_argument(
        "scenario",
        help=(
            "Scenario name, e.g. slow_query"
        ),
    )

    parser.add_argument(
        "--no-save",
        action="store_true",
        help="Do not save generated evidence.",
    )

    args = parser.parse_args()

    simulator = IncidentSimulator()

    evidence = simulator.run(
        scenario_name=args.scenario,
        save=not args.no_save,
    )

    print_evidence(evidence)


if __name__ == "__main__":
    main()