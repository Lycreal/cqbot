import re
import json
from lxml.html import etree
from plugins.live_monitor.general import Channel


class YoutubeChannel(Channel):
    def get_url(self):
        self.api_url = f'https://www.youtube.com/channel/{self.cid}/live'
        self.live_url = self.api_url

    def resolve(self, html_s):
        html: etree._Element = etree.HTML(html_s)
        script = html.xpath('body/script[contains(text(),"RELATED_PLAYER_ARGS")]/text()')[0]
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


def main():
    # quin = YoutubeChannel('UC1opHUrw8rvnsadT-iGp7Cg', 'aqua')
    # quin = YoutubeChannel('UCWCc8tO-uUl_7SJXIKJACMw', 'mea')
    quin = YoutubeChannel('UChN7P9OhRltW3w9IesC92PA', 'miu')
    # quin = YoutubeChannel('UCn14Z641OthNps7vppBvZFA', '千草はな')
    quin.update()
    print(quin)
    print(quin.notify())


if __name__ == '__main__':
    main()
