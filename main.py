#!/usr/bin/python

from pathlib import Path

from PFERD.pferd import Pferd
from PFERD.__main__ import main as pferd_main
from PFERD.logging import log
from PFERD.utils import fmt_path

from config import ConfigLoader
from mail_sender import MailSender
from rich.markup import escape

added_files = []
changed_files = []
deleted_files = []
not_deleted_files = []

def print_report(self) -> None:
    global added_files
    global changed_files
    global deleted_files
    global not_deleted_files

    for name in self._crawlers_to_run:
        crawler = self._crawlers.get(name)
        if crawler is None:
            continue  # Crawler failed to load

        log.report("")
        log.report(f"[bold bright_cyan]Report[/] for {escape(name)}")

        something_changed = False
        for path in sorted(crawler.report.added_files):
            something_changed = True
            added_files.append(path)
            log.report(f"  [bold bright_green]Added[/] {fmt_path(path)}")
        for path in sorted(crawler.report.changed_files):
            something_changed = True
            changed_files.append(path)
            log.report(f"  [bold bright_yellow]Changed[/] {fmt_path(path)}")
        for path in sorted(crawler.report.deleted_files):
            something_changed = True
            deleted_files.append(path)
            log.report(f"  [bold bright_magenta]Deleted[/] {fmt_path(path)}")
        for path in sorted(crawler.report.not_deleted_files):
            something_changed = True
            not_deleted_files.append(path)
            log.report(f"  [bold bright_magenta]Not deleted[/] {fmt_path(path)}")

        if not something_changed:
            log.report("  Nothing changed")


def main():
    cwd = Path.cwd()
    script_dir = Path(__file__).parent

    config = ConfigLoader(str(script_dir / "config.ini"))

    mail = MailSender(config)

    Pferd.print_report = print_report
    pferd_main()

    global added_files
    global changed_files
    global deleted_files
    global not_deleted_files

    # List[Path] -> List[str]
    def map_to_local(path: Path):
        return str(path)  # str(path.relative_to(cwd))

    added_files = list(map(map_to_local, added_files))
    changed_files = list(map(map_to_local, changed_files))
    deleted_files = list(map(map_to_local, deleted_files))
    not_deleted_files = list(map(map_to_local, not_deleted_files))
    mail.mail_update(added_files, changed_files, deleted_files, not_deleted_files)


if __name__ == "__main__":
    main()
