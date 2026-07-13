import json

from helm_worker import __version__
from helm_worker.__main__ import main
from helm_worker.health import health_payload


def test_worker_health_payload() -> None:
    assert health_payload() == {
        "status": "ok",
        "service": "helm-worker",
        "version": __version__,
    }


def test_worker_health_command(capsys) -> None:
    assert main(["health"]) == 0
    assert json.loads(capsys.readouterr().out) == health_payload()
