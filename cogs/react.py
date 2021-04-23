from discord.ext import commands
import asyncio
import time
from core.setup import rsp, fluctlight_client
import core.functions as func
from core.classes import CogExtension, JsonApi


class React(CogExtension):

    @commands.Cog.listener()
    async def on_member_join(self, member):
        nts = JsonApi().get_json('NT')["id_list"]
        if (member.id in nts) or member.bot:
            return

        time_status = await func.get_time_title(func.now_time_info('hour'))

        msg = '\n'.join(rsp["join"]["opening"][time_status]) + '\n'
        msg += '\n'.join(rsp["join"]["opening"]["main"])
        await member.send(msg)
        await asyncio.sleep(60)

        msg = '\n'.join(rsp["join"]["hackmd_read"])
        await member.send(msg)

        def check(message):
            return message.channel == member.dm_channel and message.author == member

        try:
            deep_freeze_status = (await self.bot.wait_for('message', check=check, timeout=60.0)).content

            if deep_freeze_status == 'y':
                msg = '\n'.join(rsp["join"]["df_1"])
                deep_freeze_status = True
            elif deep_freeze_status == 'n':
                msg = '\n'.join(rsp["join"]["df_0"])
                deep_freeze_status = False
            else:
                msg = '\n'.join(rsp["join"]["invalid_syntax"])
                deep_freeze_status = False
        except asyncio.TimeoutError:
            msg = '\n'.join(rsp["join"]["time_out"])
            deep_freeze_status = False

        # another \n for last un-inserted \n
        msg += '\n' + '\n'.join(rsp["join"]["contact_method"])

        await member.send(msg)

        # create personal fluctlight data
        start_time = time.time()

        main_fluct_cursor = fluctlight_client["MainFluctlights"]
        vice_fluct_cursor = fluctlight_client["ViceFluctlights"]
        act_cursor = fluctlight_client["active-logs"]

        default_main_fluctlight = {
            "_id": member.id,
            "name": await func.get_member_nick_name(self.bot.guilds[0], member.id),
            "score": 0,
            "week_active": False,
            "contrib": 0,
            "lvl_ind": 0,
            "deep_freeze": deep_freeze_status
        }
        default_vice_fluctlight = {
            "_id": member.id,
            "du": 0,
            "mdu": 0,
            "oc_auth": 0,
            "sc_auth": 0,
        }
        default_act = {
            "_id": member.id,
            "log": ''
        }

        try:
            main_fluct_cursor.insert_one(default_main_fluctlight)
        except:
            pass

        try:
            vice_fluct_cursor.insert_one(default_vice_fluctlight)
        except:
            pass

        try:
            act_cursor.insert_one(default_act)
        except:
            pass

        end_time = time.time()

        msg = '\n'.join(rsp["join"]["fl_create_finish"])
        await member.send(msg)
        await member.send(f'順帶一提，我用了 {round(end_time - start_time, 2)} (sec) 建立你的檔案><!')


def setup(bot):
    bot.add_cog(React(bot))
