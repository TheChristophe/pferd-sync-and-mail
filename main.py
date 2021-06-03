#!/usr/bin/python

from pathlib import Path

from PFERD.pferd import Pferd
from PFERD.__main__ import main as pferd_main
from PFERD.logging import log
from PFERD.utils import fmt_path

from config import ConfigLoader
from mail_sender import MailSender
from rich.markup import escape


def print_report(self) -> None:
    added_files = []
    changed_files = []
    deleted_files = []
    not_deleted_files = []

    cwd = Path.cwd()
    script_dir = Path(__file__).parent

    config = ConfigLoader(str(script_dir / "config.ini"))

    username = config.username
    password = config.password

    mail = MailSender(config)

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

    # List[Path] -> List[str]
    def map_to_local(path: Path):
        return path #str(path.relative_to(cwd))
    added_files = list(map(map_to_local, added_files))
    changed_files = list(map(map_to_local, changed_files))
    deleted_files = list(map(map_to_local, deleted_files))
    not_deleted_files = list(map(map_to_local, not_deleted_files))
    mail.mail_update(added_files, changed_files, deleted_files, not_deleted_files)


def main():
    Pferd.print_report = print_report
    pferd_main()

    courses = [
        # https://ilias.studium.kit.edu/goto_produktiv_crs_{id}.html
        # WS 2020/2021
        # { "title": "Höhere Mathematik 1", "id": "1253943" },
        # { "title": "Theoretische Grundlagen der Informatik", "id": "1271270" },
        # { "title": "Telematik", "id": "1252518" },
        # { "title": "Softwaretechnik 2", "id": "1231416" },
        # { "title": "WT/Statistik", "id": "1270362" },
        # { "title": "Programmierparadigmen", "id": "1261491" },
        # { "title": "BWL Finanzwirtschaft und Rechnungswesen", "id": "1280402" },
        # { "title":  "BWL Rechnungswesen", "id": "1280397" },
        # { "title":  "Algorithmen 2", "id": "1289021" },

        {"name": "Höhere Mathematik 2", "id": "1460343"},
        {"name": "Datenbanksysteme", "id": "1463481"},
        {"name": "Rechnernetze", "id": "1455593"},
        {"name": "Numerik", "id": "1466370"},
        {"name": "Lineare Algebra 2 für Informatiker", "id": "1471707"},

        {"name": "BWL S&O: Unternehmensführung und Strategisches Management", "id": "1459771"},
        {"name": "BWL S&O: Problemlösung, Kommunikation und Leadership", "id": "1456738"},

        {"name": "BWL EoF: Financial Management", "id": "1469665"},
        {"name": "BWL EoF: Investments", "id": "1478322"},

        {"name": "BWL MM: Marketing Mix", "id": "1453890"}
    ]


if __name__ == "__main__":
    main()
