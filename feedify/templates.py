RSS_FEED_TMPL = '''<?xml version="1.0" ?>
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

RSS_POST_TMPL = '''
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
