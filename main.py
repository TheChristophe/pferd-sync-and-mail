#!/usr/bin/python

from pathlib import Path

from PFERD import Pferd

from config import ConfigLoader
from mail_sender import MailSender


def main():
    cwd = Path.cwd()
    pferd = Pferd(cwd)

    config = ConfigLoader("config.ini")

    username = config.username
    password = config.password

    courses = [
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

    for course in courses:
        # do not need to use windows path/character replacement, rclone provides character substitution for OneDrive
        # this gives similar-looking characters (https://rclone.org/onedrive/)
        pferd.ilias_kit(target=course["name"], course_id=course["id"], username=username, password=password,
                        cookies="cookies.txt")

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
