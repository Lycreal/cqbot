import re
import json
import lxml.html
from . import BaseChannel


class YoutubeChannel(BaseChannel):
    def set_url(self):
        self.api_url = f'https://www.youtube.com/channel/{self.cid}/live'
        self.live_url = self.api_url

    def resolve(self, html_s):
        html: lxml.html.HtmlElement = lxml.html.fromstring(html_s)
        script = html.xpath('body/script[contains(text(),"RELATED_PLAYER_ARGS")]/text()')
        if not script:
            self.live_status = '0'
            return
        json_s = re.search(r'\'RELATED_PLAYER_ARGS\':(.*),', script[0]).group(1)
        RELATED_PLAYER_ARGS = json.loads(json_s)

        json_s = RELATED_PLAYER_ARGS['watch_next_response']
        watch_next_response: dict = json.loads(json_s)

        videoMetadataRenderer: dict = \
            watch_next_response['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0][
                'itemSectionRenderer']['contents'][0]['videoMetadataRenderer']
        self.ch_name = videoMetadataRenderer['owner']['videoOwnerRenderer']['title']['runs'][0]['text']
        shareVideoEndpoint = videoMetadataRenderer['shareButton']['buttonRenderer']['navigationEndpoint'][
            'shareVideoEndpoint']
        self.title = shareVideoEndpoint['videoTitle']
        self.live_url = shareVideoEndpoint['videoShareUrl']

        if 'badges' in videoMetadataRenderer.keys():
            if 'liveBadge' in videoMetadataRenderer['badges'][0].keys():
                if videoMetadataRenderer['badges'][0]['liveBadge']['label']['simpleText'] == 'Live now':
                    self.live_status = '1'
                    return
        self.live_status = '0'
