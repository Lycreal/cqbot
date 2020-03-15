from typing import List, Dict
from datetime import datetime, timedelta
import nonebot


class MessageBuffer:
    def __init__(self):
        self.buffer: Dict[str, List[str]] = {}
        # {target: [msg1,msg2,...]}
        self.clock: Dict[str, List[datetime]] = {}
        # {target: [first_clock, last_clock]}

    def input(self, targets: List[str], msg: str):
        for target in targets:
            # 将消息加入缓冲区
            for m in self.buffer.setdefault(target, []):
                if msg.split()[-1] == m.split()[-1]:
                    self.buffer[target].remove(m)
            self.buffer[target].append(msg)
            # 设置时刻
            now = datetime.now()
            self.clock.setdefault(target, [now, now])[1] = now

    async def send(self, target: str):
        # 发送消息并清空缓冲区
        # target_type, target_body = target[:1], target[1:]
        target_type, target_body = 'g', target
        if target_type == 'g':
            await nonebot.get_bot().send_group_msg(group_id=int(target_body), message='\n'.join(self.buffer[target]))
        # elif target_type == 'p':
        #     await nonebot.get_bot().send_private_msg(user_id=int(target_body), message='\n'.join(self.buffer[target]))
        self.buffer.pop(target)
        self.clock.pop(target)

    async def check(self):
        for target, msg_array in list(self.buffer.items()):
            count = len(msg_array)
            first_clock, last_clock = self.clock[target]
            all_waited = datetime.now() - first_clock
            last_waited = datetime.now() - last_clock

            if count >= 6 or last_waited >= timedelta(seconds=20) or all_waited >= timedelta(seconds=60):
                await self.send(target)


buffer = MessageBuffer()


@nonebot.scheduler.scheduled_job('interval', seconds=5)
async def _():
    await buffer.check()
