#!/usr/bin/python

from pathlib import Path, PurePath

from PFERD import Pferd
from PFERD.organizer import ConflictType, FileConflictResolution

from config import ConfigLoader
from mail_sender import MailSender


def main():
    cwd = Path.cwd()
    pferd = Pferd(cwd)
    script_dir = Path(__file__).parent

    config = ConfigLoader(str(script_dir / "config.ini"))

    username = config.username
    password = config.password

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

    def resolve_no_delete(_path: PurePath, conflict: ConflictType) -> FileConflictResolution:
        # Update files
        if conflict == ConflictType.FILE_OVERWRITTEN:
            return FileConflictResolution.DESTROY_EXISTING
        if conflict == ConflictType.MARKED_FILE_OVERWRITTEN:
            return FileConflictResolution.DESTROY_EXISTING
        # But do not delete them
        return FileConflictResolution.KEEP_EXISTING

    for course in courses:
        # do not need to use windows path/character replacement, rclone provides character substitution for OneDrive
        # this gives similar-looking characters (https://rclone.org/onedrive/)
        pferd.ilias_kit(target=course["name"], course_id=course["id"], username=username, password=password,
                        cookies=str(script_dir / "cookies.txt"), file_conflict_resolver=resolve_no_delete)

    # Prints a summary listing all new, modified or deleted files
    pferd.enable_logging()
    pferd.print_summary()

    mail = MailSender(config)

    summary = pferd._download_summary
    # List[Path] -> List[str]
    new_files = list(map(lambda f: str(f.relative_to(cwd)), summary.new_files))
    updated_files = list(map(lambda f: str(f.relative_to(cwd)), summary.modified_files))
    mail.mail_update(new_files, updated_files)


if __name__ == "__main__":
    main()
