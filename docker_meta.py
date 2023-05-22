import logging
from datetime import datetime
import inspect


class DockerMeta:
    def __init__(self, meta, container, container_name, notes):
        self.meta = meta
        self.name = container_name
        self.container = container
        self.timestamp = datetime.now()
        self.notes = notes
        self.users = self.get_users()

    def installed_packages(self):
        ignored_applications = []
        applications = self.container.exec_run("apt list | awk -F/ '{print $1}'")
        application_versions = self.container.exec_run("awk -F\"[{}]\" '/Test Machine/{print $2}'")
        application_map = dict(zip(applications, application_versions))
        for app in ignored_applications:
            if app in application_map:
                try:
                    del application_map[app]
                except KeyError as e:
                    frame = inspect.currentframe()
                    logging.error(f'ERROR: {frame.f_code.co_name} - {e}')
        return application_map

    def parse_scripts(self):
        ...

    def get_users(self):
        ignored_users = ['root', 'daemon', 'bin', 'sys', 'sync', 'games', 'man',
                         'lp', 'mail', 'news', 'uucp', 'proxy', 'www-data',
                         'backup', 'list', 'irc', 'gnats', 'nobody', '_apt']
        users = self.container.exec_run("cat /etc/passwd | awk - F: '{ print $1}'")
        installed_users = list(set(users) - set(ignored_users))
        return installed_users
