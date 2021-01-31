from datetime import datetime as dt
import hashlib
import html
from typing import List
from urllib.request import urlopen, Request

from pyquery import PyQuery as pq


__version__ = '0.1.0'


FEED_TMPL = '''<?xml version="1.0" ?>
<rss version="2.0">
    <channel>
        <title>{{site_title}}</title>
        <link>{{site_url}}</link>
        <description>{{site_description}}</description>
        <managingEditor>{{site_author}}</managingEditor>

        {{posts}}
    </channel>
</rss>
'''

POST_TMPL = '''
<item>
    <guid>{{post_permalink}}</guid>
    <link>{{post_permalink}}</link>
    <title>{{post_title}}</title>
    <pubDate>{{post_pub_date}}</pubDate>
    <description>
        {{post_content}}
    </description>
</item>
'''


DEFAULT_USER_AGENT = f'feedify/{__version__}'
DEBUG = True


class Feedifier:
    def __init__(self, config, url, cache=None, user_agent=DEFAULT_USER_AGENT):
        self.config = config
        self.url = url
        self.cache = dict() if cache is None else cache
        self.latest_post_md5 = ''
        self.user_agent = user_agent
        self.content = self._fetch(url)
        self.feed_items = self._parse_site()

    def get_full_feed(self) -> str:
        feed = FEED_TMPL.replace('{{site_title}}', self.config['site_title'])
        feed = feed.replace('{{site_url}}', f'https://{self.url}')
        feed = feed.replace('{{site_description}}',
                            self.config['site_description'])
        feed = feed.replace('{{site_author}}', self.config['site_author'])
        feed = feed.replace('{{posts}}', '\n\n'.join(self.feed_items))

        return feed

    @property
    def _needs_to_fetch(self) -> bool:
        return self.cache.get(f'{self.url}_md5') != self.latest_post_md5 or DEBUG is True

    def _fetch(self, url: str) -> str:
        if self._needs_to_fetch:
            # TODO: error handling
            req = Request(f'https://{url}', headers={'User-Agent': self.user_agent})
            response = urlopen(req)
            if response.status == 200:
                self.cache[f'{self.url}_content'] = response.read()
        return self.cache[f'{self.url}_content']

    def _parse_site(self) -> List[str]:
        d = pq(self.content)
        posts = d(self.config.get('post_selector'))
        newest_post = str(posts.eq(0)).encode('utf-8')
        latest_post_md5 = hashlib.md5(newest_post).hexdigest()
        self.cache[f'{self.url}_md5'] = latest_post_md5

        feed_posts = []
        for post in posts:
            d = pq(post)
            feed_item = POST_TMPL

            date_elm = d(self.config['date_selector']).eq(0)
            pub_date = dt.strptime(date_elm.text(), self.config['date_format'])
            feed_item = feed_item.replace('{{post_pub_date}}', pub_date.strftime('%a, %d %b %Y %H:%M:%S -0000'))

            permalink = d(self.config['permalink_selector']).eq(0).attr('href')
            feed_item = feed_item.replace('{{post_permalink}}', permalink)

            title = d(self.config['title_selector']).eq(0).text()
            feed_item = feed_item.replace('{{post_title}}', title)

            content = d(self.config['content_selector']).eq(0).html()
            feed_item = feed_item.replace('{{post_content}}', html.escape(content))
            feed_posts.append(feed_item)
        return feed_posts
