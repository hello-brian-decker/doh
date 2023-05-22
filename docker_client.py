import docker
import logging
import json
import inspect
import commands

logging.basicConfig(filename='doh.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


class DockerClient:
    def __init__(self, container_name):
        self.container_name = container_name
        self.response = None
        self.client = None
        self.container = None

    def docker_from_env(self):
        client = None
        try:
            client = docker.from_env()
        except docker.errors.DockerException as e:
            logging.error(f"ERROR: {e}")
            self.response = commands.docker_not_running
        return client

    def get_container(self):
        container = None
        try:
            container = self.client.containers.get(self.container_name)
        except docker.errors.NotFound:
            logging.error(f'ERROR: {self.container_name} not found')
            self.response = f'{self.container_name} Not Found'
        return container

    def read_meta(self):
        self.client = self.docker_from_env()
        if not self.response:
            self.container = self.get_container()
        if not self.response:
            cmd = f"cat {commands.meta_dir}"
            execute = self.container.exec_run(cmd=cmd)
            exit_code = execute.exit_code
            output = execute.output
            if exit_code == 0:
                try:
                    self.response = json.loads(output)
                except json.decoder.JSONDecodeError or TypeError as e:
                    frame = inspect.currentframe()
                    logging.error(f'ERROR: {frame.f_code.co_name} - {e}')
                    self.response = f"ERROR: in meta.json file - {e}"
            else:
                self.response = "{}"
                # self.response = "/usr/local/bin/meta.json Does Not Exist"
        return self.response

    def update_meta(self):
        ...
