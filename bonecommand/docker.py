import bonecommand as bc
import asyncio


a = bc.SingleCommand("bash -c 'sleep 0.1 && echo $RANDOM'")

cmds = [a.run(), a.run(), a.run(), a.run()]


async def main():
    statuses = await asyncio.gather(*cmds)
    return list(map(lambda s: s.stdout, statuses))


print(asyncio.run(main()))
