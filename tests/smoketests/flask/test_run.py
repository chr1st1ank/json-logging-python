import signal
import subprocess
import sys
import time
from pathlib import Path

import requests


def test_flask_example():
    api_process = subprocess.Popen(
        [sys.executable, (Path(__file__).parent / "api.py")],
        stdout=sys.stdout,
        stderr=subprocess.STDOUT,
    )

    deadline = time.perf_counter() + 30.0
    while time.perf_counter() < deadline:
        time.sleep(1)
        with requests.Session() as session:
            session.trust_env = False
            try:
                response = requests.get("http://localhost:5000/", timeout=1)
                assert response.status_code == 200
            except requests.exceptions.Timeout:
                pass

    api_process.send_signal(signal.SIGTERM)
    api_process.wait(timeout=5.0)
