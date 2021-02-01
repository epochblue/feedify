import argparse
from functools import partial
import json
from pathlib import Path
from wsgiref import simple_server

from . import __version__ as version
from .handler import FeedifyHandler

feeds_file_cache = Path('.feeds')
if not feeds_file_cache.is_dir():
    feeds_file_cache.mkdir(0o755)

parser = argparse.ArgumentParser(description='feedify: a command line website-to-RSS application.')
parser.add_argument('--config', dest='config_file', type=str, default='config.json',
                    help='A user-supplied configuration file.')
parser.add_argument('--version', action='version', version='feedify {}'.format(version))
args = parser.parse_args()

config = {}
config_path = Path(args.config_file).expanduser()
if config_path.exists():
    with open(config_path, 'rb') as f:
        config = json.load(f)

server = simple_server.WSGIServer(('', 8000), partial(FeedifyHandler, config))
server.serve_forever()
