from datetime import datetime as dt
import hashlib
import html
from typing import List
from urllib.request import urlopen, Request

from pyquery import PyQuery as pq

from feedify.templates import RSS_FEED_TMPL, RSS_POST_TMPL


class RSSFeedifier:
    def __init__(self, config, url, cache=None):
        self.site_config = config['sites'][url]
        self.url = url
        self.cache = dict() if cache is None else cache
        self.latest_post_md5 = ''
        self.user_agent = config['user_agent']
        self.debug = config['debug']
        self.content = self._fetch(url)
        self.feed_items = self._parse_site()

    def get_full_feed(self) -> str:
        feed = RSS_FEED_TMPL.replace('{{site_title}}', self.site_config['site_title'])
        feed = feed.replace('{{site_url}}', f'https://{self.url}')
        feed = feed.replace('{{site_description}}',
                            self.site_config['site_description'])
        feed = feed.replace('{{site_author}}', self.site_config['site_author'])
        feed = feed.replace('{{posts}}', '\n\n'.join(self.feed_items))

        return feed

    @property
    def _needs_to_fetch(self) -> bool:
        return self.cache.get(f'{self.url}_md5') != self.latest_post_md5 or self.debug

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
        posts = d(self.site_config.get('post_selector'))
        newest_post = str(posts.eq(0)).encode('utf-8')
        latest_post_md5 = hashlib.md5(newest_post).hexdigest()
        self.cache[f'{self.url}_md5'] = latest_post_md5

        feed_posts = []
        for post in posts:
            d = pq(post)
            feed_item = RSS_POST_TMPL

            date_elm = d(self.site_config['date_selector']).eq(0)
            pub_date = dt.strptime(date_elm.text(), self.site_config['date_format'])
            feed_item = feed_item.replace('{{post_pub_date}}', pub_date.strftime('%a, %d %b %Y %H:%M:%S -0000'))

            permalink = d(self.site_config['permalink_selector']).eq(0).attr('href')
            feed_item = feed_item.replace('{{post_permalink}}', permalink)

            title = d(self.site_config['title_selector']).eq(0).text()
            feed_item = feed_item.replace('{{post_title}}', title)

            content = d(self.site_config['content_selector']).eq(0).html()
            feed_item = feed_item.replace('{{post_content}}', html.escape(content))
            feed_posts.append(feed_item)
        return feed_posts
