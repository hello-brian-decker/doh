import docker
import logging
import json
import inspect

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
meta_dir = "/usr/local/etc/meta.json"


def docker_from_env(container_name, read_file):
    client = docker.from_env()
    container = get_container_by_name(client=client, container_name=container_name)
    if read_file:
        meta = check_container_for_meta(container)
        return meta


def check_container_for_meta(container):
    meta = {}
    file = container.exec_run(f'cat {meta_dir} 2>/dev/null')
    if file:
        try:
            meta = json.loads(file)
        except json.decoder.JSONDecodeError as e:
            frame = inspect.currentframe()
            logging.error(f'ERROR: {frame.f_code.co_name} - {e}')
    return meta


def get_container_by_name(client, container_name):
    try:
        container = client.containers.get('container_name')
    except docker.errors.NotFound:
        logging.error(f'ERROR: {container_name} not found')
        print(f'{container_name} not found')
        return
    return container


def update_meta():
    ...