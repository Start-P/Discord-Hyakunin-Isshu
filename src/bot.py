import uuid
import time

import disnake
from disnake.ext import commands, tasks

from HyakuninIsshuManager import Hyakunin_Isshu_Manager

bot = commands.InteractionBot()

game_queue_deleter = {}
game_joiner_list = {}
game_manager = {}

with open("token.txt") as f:
    token = f.read().splitlines()[0]

@bot.slash_command(
    name="start",
    description="百人一首のゲーム募集をスタートします。",
)
async def slash_calc(inter):
    game_uuid = str(uuid.uuid4())
    view = disnake.ui.View()
    view.add_item(
        disnake.ui.Button(
            label="ゲームに参加する",
            style=disnake.ButtonStyle.green,
            custom_id=f"game_join.{game_uuid}"
        )
    )

    embed = disnake.Embed(
        title=f"{inter.user.name}の百人一首ゲーム",
        description="ここをクリックして百人一首に参加",
        color=disnake.Colour.blue(),
    )

    embed.set_author(
        name=inter.user.name,
        icon_url=inter.user.avatar.url
    )

    await inter.response.send_message(embed=embed, view=view)
    game_manager = {uuid: {"channel_id": inter.channel.id, "isshu_object": Hyakunin_Isshu_Manager()}}
    game_queue_deleter.update({game_uuid: time.time()})
    game_joiner_list.update({game_uuid: [inter.user.id]})


@bot.event
async def on_button_click(inter):
    await inter.response.defer(ephemeral=True)

    if inter.data.custom_id.startswith('game_join.'):
        custom_id = inter.data.custom_id.replace("game_join.", "")
        print(game_joiner_list, game_queue_deleter, custom_id)
        game = game_joiner_list.get(custom_id)
        if not game:
            await inter.send('ゲームが見つかりませんでした')
            return

        if inter.user.id in game:
            await inter.send('あなたはすでにゲームに参加しています。')
            return

        game.append(inter.user.id)
        game_joiner_list[custom_id] = game
        await inter.send('ゲームに参加しました！')



@tasks.loop(seconds=1)
async def loop():
    for uuid in list(game_queue_deleter):
        print(int(time.time()) - int(game_queue_deleter[uuid]))
        if int(time.time()) - int(game_queue_deleter[uuid]) == 10:
            del game_queue_deleter[uuid]


@bot.event
async def on_ready():
    print("run")

loop.start()
bot.run(token)
