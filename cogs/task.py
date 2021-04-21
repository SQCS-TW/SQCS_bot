from core.setup import client
import core.functions as func
from cogs.quiz import quiz_start, quiz_end
import discord
from discord.ext import tasks
from core.classes import CogExtension, JsonApi
from core.setup import fluctlight_client


class Task(CogExtension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.quiz_data_cursor = client["quiz_data"]

        self.quiz_auto.start()
        self.nt_auto.start()
        self.bot_activity.start()

    @tasks.loop(minutes=10)
    async def quiz_auto(self):
        await self.bot.wait_until_ready()

        report_channel = discord.utils.get(self.bot.guilds[1].text_channels, name='sqcs-report')

        quiz_status = self.quiz_data_cursor.find_one({"_id": 0})["event_status"]

        if func.now_time_info('date') == 1 and func.now_time_info('hour') >= 6 and quiz_status == 0:
            await quiz_start(self.bot)
            await report_channel.send(f'[AUTO QUIZ START][{func.now_time_info("whole")}]')
        elif func.now_time_info('date') == 7 and func.now_time_info('hour') >= 23 and quiz_status == 1:
            await quiz_end(self.bot)
            await report_channel.send(f'[AUTO QUIZ END][{func.now_time_info("whole")}]')

    @tasks.loop(minutes=5)
    async def nt_auto(self):
        await self.bot.wait_until_ready()

        nt_list = JsonApi().get_json('NT')["id_list"]
        for member in self.bot.guilds[0].members:
            if member.id in nt_list:
                await member.send(':recycle:')
                await member.ban()

    @tasks.loop(minutes=10)
    async def bot_activity(self):
        await self.bot.wait_until_ready()

        fluctlight_cursor = fluctlight_client["light-cube-info"]
        member_count = fluctlight_cursor.find({}).count()

        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f'{member_count} 個活生生的搖光...'
            )
        )


def setup(bot):
    bot.add_cog(Task(bot))
