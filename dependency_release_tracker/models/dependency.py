class Dependency:

    def __init__(
        self,
        name,
        current_version,
        repo_url=None,
        latest_version=None,
        notes=None,
        url=None,
        published_at=None,
    ):
        self.name = name
        self.current_version = current_version
        self.repo_url = repo_url
        self.latest_version = latest_version or current_version
        self.notes = notes
        self.url = url
        self.published_at = published_at

    def __str__(self):
        return f"{self.name} [{self.current_version} -> {self.latest_version}]"
