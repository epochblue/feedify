from functools import partial
import json
from pathlib import Path
from wsgiref import simple_server

from .handler import FeedifyHandler

feeds_file_cache = Path('.feeds')
if not feeds_file_cache.is_dir():
    feeds_file_cache.mkdir(0o755)

# TODO: Give this more of a CLI interface
config_path = Path('config.json')
if config_path.exists():
    with open(config_path, 'rb') as f:
        config = json.load(f)
else:
    config = {}

server = simple_server.WSGIServer(('', 8000), partial(FeedifyHandler, config))
server.serve_forever()
