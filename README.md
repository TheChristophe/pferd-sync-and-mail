# Sync and mail wrapper for PFERD

Monkey-patch wrapper around PFERD to mail you the list of changed files after PFERD completes execution. Useful for use
in automated scripts and services.

Configuration:
1. Copy `config-example.ini` to `config.ini` in the same folder as pferd-sync-and-mail
1. Fill in your email configuration

For usage, run `main.py`, and see [PFERD](https://github.com/Garmelon/PFERD) for arguments.

### Legacy
For use with PFERD 2, see the v0.0-pferd2 tag.
