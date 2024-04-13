from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeRemainingColumn,
)


class ProgressManager:
    def __init__(self):
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("{task.description}"),
            BarColumn(),
            TimeRemainingColumn(),
        )

    def start_task(self, description, total):
        self.task = self.progress.add_task(description, total=total)
        self.progress.start()

    def advance(self):
        self.progress.update(self.task, advance=1)

    def finish(self):
        self.progress.stop()
