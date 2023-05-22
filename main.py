import argparse
from webapp.app import app
import os


def main():
    ...


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')
    webapp = subparser.add_parser('webapp')
    local = subparser.add_parser('local')
    webapp.add_argument('--port', type=str, required=False)
    local.add_argument('--path', '-p', type=str, required=True)
    local.add_argument('--output', '-o', type=str, required=False)
    local.add_argument('--container', '-c', type=str, required=False)
    args = parser.parse_args()
    if args.command == 'webapp':
        port = args.port if args.port else int(os.environ.setdefault("port", "7890"))
        app.run(debug=True, port=port)
