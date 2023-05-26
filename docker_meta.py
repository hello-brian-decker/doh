import logging
from datetime import datetime
import inspect
import commands


class DockerMeta:
    def __init__(self, meta, container, container_name, notes):
        self.meta = meta
        self.name = container_name
        self.container = container
        self.timestamp = datetime.now()
        self.notes = notes
        self.users = self.get_users()

    def installed_packages(self):
        applications = self.container.exec_run(commands.application_list)
        application_versions = self.container.exec_run(commands.application_versions)
        application_map = dict(zip(applications, application_versions))
        for app in commands.ignored_applications:
            if app in application_map:
                try:
                    del application_map[app]
                except KeyError as e:
                    frame = inspect.currentframe()
                    logging.error(f'{frame.f_code.co_name} - {e}')
        return application_map

    def parse_scripts(self):
        ...

    def get_users(self):
        users = self.container.exec_run(commands.users)
        installed_users = list(set(users) - set(commands.ignored_users))
        return installed_users
