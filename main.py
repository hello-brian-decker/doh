import argparse
from docker_client import DockerClient
from webapp.app import app
import os


def main(container_name):
    docker_client = DockerClient(container_name=container_name)
    response = docker_client.read_meta()
    print(response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')
    webapp = subparser.add_parser('webapp')
    webapp.add_argument('--port', type=str, required=False)
    parser.add_argument('--path', '-p', type=str, required=False)
    parser.add_argument('--output', '-o', type=str, required=False)
    parser.add_argument('--container', '-c', type=str, required=False)
    parser.add_argument('--render', '-r', type=str, required=False)
    args = parser.parse_args()
    if args.command == 'webapp':
        port = args.port if args.port else int(os.environ.setdefault("port", "7890"))
        app.run(debug=True, port=port)
    main(container_name=args.container)
