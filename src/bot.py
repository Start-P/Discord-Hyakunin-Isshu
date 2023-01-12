import uuid
import time

import disnake
from disnake.ext import commands, tasks

bot = commands.InteractionBot()

game_queue = {}

with open("token.txt") as f:
    token = f.read().splitlines()[0]

@bot.slash_command(
    name="start",
    description="百人一首のゲーム募集をスタートします。",
)
async def slash_calc(inter):
    game_uuid = uuid.uuid4()

    view = disnake.ui.View()
    view.add_item(
        disnake.ui.Button(
            label="ゲームに参加する",
            style=disnake.ButtonStyle.green,
            custom_id=f"game_join.{uuid}"
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
    game_queue.update({uuid: str(time.time())})


@bot.event
async def on_button_click(inter):
    await inter.response.defer(ephemeral=False)

@tasks.loop(seconds=1)
async def loop():
    for uuid in game_queue:
        if int(time.time()) - int(game_queue[uuid]) == 10:
            game_queue.remove(uuid)


@bot.event
async def on_ready():
    print("run")

bot.run(token)
