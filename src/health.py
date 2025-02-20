from pathlib import Path


class HealthCheck:
    def __init__(self):
        self.file = Path("/tmp/healthz")

    def healthy(self):
        self.file.touch()

    def unhealthy(self):
        self.file.unlink(True)


HEALTHCHECK = HealthCheck()
