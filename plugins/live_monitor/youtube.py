import re
import json
from lxml.html import etree
from plugins.live_monitor.general import BaseChannel


class YoutubeChannel(BaseChannel):
    def get_url(self):
        self.api_url = f'https://www.youtube.com/channel/{self.cid}/live'
        self.live_url = self.api_url

    def resolve(self, html_s):
        html: etree.Element = etree.HTML(html_s)
        script_ = html.xpath('body/script[contains(text(),"RELATED_PLAYER_ARGS")]/text()')
        if not script_:
            with open('debug.html', 'w', encoding='utf8') as f:
                f.write(html.text)
        script = script_[0]
        json_s = re.search(r'\'RELATED_PLAYER_ARGS\':(.*),', script).group(1)
        RELATED_PLAYER_ARGS = json.loads(json_s)

        json_s = RELATED_PLAYER_ARGS['watch_next_response']
        watch_next_response = json.loads(json_s)

        videoMetadataRenderer = \
            watch_next_response['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0][
                'itemSectionRenderer']['contents'][0]['videoMetadataRenderer']
        self.ch_name = videoMetadataRenderer['owner']['videoOwnerRenderer']['title']['runs'][0]['text']
        shareVideoEndpoint = videoMetadataRenderer['shareButton']['buttonRenderer']['navigationEndpoint'][
            'shareVideoEndpoint']
        self.title = shareVideoEndpoint['videoTitle']
        self.live_url = shareVideoEndpoint['videoShareUrl']
        if 'liveBadge' in list(videoMetadataRenderer['badges'][0].keys()) and \
                videoMetadataRenderer['badges'][0]['liveBadge']['label']['simpleText'] == 'Live now':
            self.live_status = '1'
        else:
            self.live_status = '0'
