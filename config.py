import configparser


class ConfigLoader:
    class SectionNotFound(Exception):
        pass

    class KeyNotFound(Exception):
        pass

    def __init__(self, file):
        self.config = configparser.ConfigParser()
        self.config.read(file)
        self.check_sections()
        self.check_keys()

        self.username = self.config['Credentials']['username']
        self.password = self.config['Credentials']['password']

        self.mail_host = self.config['Mail']['host']
        self.mail_port = int(self.config['Mail']['port'])
        self.mail_username = self.config['Mail']['username']
        self.mail_password = self.config['Mail']['password']
        self.mail_from = self.config['Mail']['from']
        self.mail_to = self.config['Mail']['to']

    def check_sections(self):
        needed_sections = ['Credentials', 'Mail']
        for section in needed_sections:
            if section not in self.config:
                raise self.SectionNotFound(section)

    def check_keys(self):
        needed_auth_keys = ['username', 'password']
        needed_mail_keys = ['username', 'password', 'from', 'to', 'host', 'port']
        for key in needed_auth_keys:
            if key not in self.config['Credentials']:
                raise self.KeyNotFound(key)
        for key in needed_mail_keys:
            if key not in self.config['Mail']:
                raise self.KeyNotFound(key)
