from rich.console import Console
from rich.markdown import Markdown
from datetime import datetime
import pytz


class DependencyDisplay:
    def __init__(self):
        self.console = Console()

    def display(self, dependencies, simple_output=False):
        """
        Display the dependencies information in the console using simple prints.

        :param dependencies: A list of Dependency objects to display.
        :param simple_output: If True, display simplified output without release notes.
        """

        updated = "(UPDATED)"
        outdated = "(OUTDATED)"

        # Sorting the dependencies by published_at, handling None values appropriately
        sorted_dependencies = sorted(
            dependencies,
            key=lambda x: (
                datetime.fromisoformat(x.published_at.rstrip("Z")).replace(
                    tzinfo=pytz.utc
                )
                if x.published_at
                else datetime.min
            ),
            reverse=True,
        )

        for dependency in sorted_dependencies:
            version_status = (
                updated
                if dependency.current_version == dependency.latest_version
                else outdated
            )
            version_status_color = "green" if version_status == updated else "red"
            published_at = self.format_date(dependency.published_at)

            self.console.print(
                f"[yellow]{dependency.name} ({dependency.latest_version}) - "
                f"[white]{published_at} [{version_status_color}]{version_status}\n",
                style="bold",
            )

            if dependency.current_version != dependency.latest_version:
                self.console.print(
                    f"[red]Current version: {dependency.current_version}", style="bold"
                )

            if not simple_output:
                processed_notes = self.process_notes(dependency.notes)
                self.console.print(
                    Markdown(
                        f"Release notes:\n\n{processed_notes}\n\n[{dependency.url}]({dependency.url})\n\n---\n"
                    )
                )
                self.console.print("")

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
