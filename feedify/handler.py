from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from pathlib import Path
import time

from feedify.converters import RSSFeedifier


class FeedifyHandler(BaseHTTPRequestHandler):
    def __init__(self, config, *args, **kwargs):
        self.config = config
        super().__init__(*args, **kwargs)

    @staticmethod
    def needs_refresh(url):
        mtime = None
        path = Path(f'.feeds/{url}.xml')
        if path.exists():
            mtime = path.stat().st_mtime

        # Doesn't need refresh if we modified this file in the last 15 minutes
        return not mtime or (time.time() - mtime) > (60 * 15)

    def not_found(self):
        headers = {'Content-Type': 'text/plain'}
        self.respond(HTTPStatus.NOT_FOUND, 'Not Found', headers)

    def respond(self, status, body, headers=None):
        headers = {} if headers is None else headers
        self.send_response(status)
        for label, value in headers.items():
            self.send_header(label, value)
        self.end_headers()
        self.wfile.write(body.encode())
        self.close_connection = True

    def do_GET(self):
        url = self.path.strip('/')

        if url not in self.config.get('sites', {}):
            self.not_found()
            return

        if FeedifyHandler.needs_refresh(url):
            feed = RSSFeedifier(self.config, url).get_full_feed()
            with Path(f'.feeds/{url}.xml').open(mode='w') as f:
                f.write(feed)
        else:
            with Path(f'.feeds/{url}.xml').open() as f:
                feed = f.read()

        headers = {'Content-Type': 'application/rss+xml'}
        self.respond(HTTPStatus.OK, feed, headers)

