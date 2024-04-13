from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table
from datetime import datetime
import pytz


class DependencyDisplay:
    def __init__(self):
        self.console = Console()

    def display(self, dependencies, simple_output=False):
        """
        Display the dependencies information in the console.

        :param dependencies: A list of Dependency objects to display.
        :param simple_output: If True, display simplified output without release notes.
        """
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Name", style="bold cyan")
        table.add_column("Current Version", justify="right")
        table.add_column("Latest Version", justify="right")
        table.add_column("Status", justify="right")
        table.add_column("Published Date", justify="right")
        table.add_column("Notes" if not simple_output else "")

        for dependency in dependencies:
            version_status = (
                "Outdated"
                if dependency.current_version != dependency.latest_version
                else "Updated"
            )
            version_status_color = "red" if version_status == "Outdated" else "green"
            published_date = self.format_date(dependency.published_at)

            if simple_output:
                table.add_row(
                    dependency.name,
                    dependency.current_version,
                    dependency.latest_version,
                    f"[{version_status_color}]{version_status}",
                    published_date,
                )
            else:
                processed_notes = (
                    self.process_notes(dependency.notes)
                    if dependency.notes
                    else "No release notes found."
                )
                table.add_row(
                    dependency.name,
                    dependency.current_version,
                    dependency.latest_version,
                    f"[{version_status_color}]{version_status}",
                    published_date,
                    Markdown(processed_notes),
                )

        self.console.print(table)

    @staticmethod
    def format_date(date_str):
        """
        Format the date string to a readable format.
        """
        if date_str:
            date_obj = datetime.fromisoformat(date_str.rstrip("Z")).replace(
                tzinfo=pytz.utc
            )
            return date_obj.astimezone().strftime("%Y-%m-%d %H:%M:%S")
        return "Unknown"

    @staticmethod
    def process_notes(notes):
        """
        Process the release notes to add markdown formatting for better readability.
        """
        processed_lines = []
        for line in notes.split("\n"):
            if line.startswith("## "):
                header_text = line[3:].strip()
                processed_lines.append(f"**{header_text}**")
            elif line.startswith("### "):
                header_text = line[4:].strip()
                processed_lines.append(f"**{header_text}**")
            else:
                processed_lines.append(line)
        return "\n".join(processed_lines)
