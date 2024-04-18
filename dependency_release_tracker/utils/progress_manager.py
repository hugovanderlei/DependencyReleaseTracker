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
        self.active = False

    def start_task(self, description, total):
        if not self.active:
            self.task = self.progress.add_task(description, total=total)
            self.progress.start()
            self.active = True

    def advance(self):
        if self.active:
            self.progress.update(self.task, advance=1)

    def finish(self):
        if self.active:
            self.progress.stop()
            self.progress.console.clear()
            self.active = False
