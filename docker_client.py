import docker
import logging
import json
import inspect
import commands

logging.basicConfig(filename='doh.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


class DockerClient:
    def __init__(self, container_name, tag, namespace):
        self.client = self.docker_from_env()
        self.container_name = container_name
        self.namespace = namespace
        self.tag = tag
        self.container_full = f"{container_name}/{namespace}:{tag}" \
            if namespace else f"{container_name}:{tag}"
        self.container = None
        self.meta = None
        self.container = None
        self.local_images = self.client.images.list()
        self.is_local = self.local_images()

    @staticmethod
    def docker_from_env():
        client = None
        try:
            client = docker.from_env()
        except docker.errors.DockerException as e:
            logging.error(e)
            print(commands.docker_not_running)
            quit()
        return client

    def container_running_locally(self):
        try:
            self.container = self.client.containers.get(self.container_full)
        except docker.errors.NotFound:
            logging.info(f'{self.container_name} not found')
            print(f'{self.container_name} Not Found')
            return False
        return True

    def image_local(self):
        return True if self.container_full in self.local_images else False

    def image_pull(self):
        ...

    def get_container(self):
        ...

    def get_meta(self):
        self.client = self.docker_from_env()
        if self.container_running_locally():
            # do something
            ...
        else:
            if self.is_local:
                self.client.run(self.container_full)
            else:
                ...
        cmd = f"cat {commands.meta_dir}"
        execute = self.container.exec_run(cmd=cmd)
        exit_code = execute.exit_code
        output = execute.output
        if exit_code == 0:
            try:
                self.meta = json.loads(output)
            except json.decoder.JSONDecodeError or TypeError as e:
                frame = inspect.currentframe()
                logging.error(f'{frame.f_code.co_name} - {e}')
                print(f"ERROR: in meta.json file - {e}")
                quit()
        else:
            self.meta = "{}"

    def update_meta(self):
        ...
