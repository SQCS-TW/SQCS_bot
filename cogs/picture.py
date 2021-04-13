from core.classes import Cog_Extension, JsonApi
from discord.ext import commands
import random


class Picture(Cog_Extension):

    @commands.group()
    async def pic(self, ctx):
        pass

    @pic.command()
    @commands.has_any_role('總召', 'Administrator')
    async def add(self, ctx, link: str):

        pic_json = JsonApi().get_json('DynamicSettingJson')

        pic_json['group_pic'].append(link)

        JsonApi().put_json('DynamicSettingJson', pic_json)

        await ctx.send(f':white_check_mark: Object {link} successfully added!')

    @pic.command()
    @commands.has_any_role('總召', 'Administrator')
    async def remove(self, ctx, index: int):

        pic_json = JsonApi().get_json('DynamicSettingJson')

        if index >= int(len(pic_json['group_pic'])):
            await ctx.send('Index out of range!')
            return

        del_object = pic_json['group_pic'][index]
        del(pic_json['group_pic'][index])

        JsonApi().put_json('DynamicSettingJson', pic_json)

        await ctx.send(f'Object {del_object} successfully deleted!')

    @pic.command()
    async def list(self, ctx):

        pic_json = JsonApi().get_json('DynamicSettingJson')

        pic_str = str()
        for i, pic in enumerate(pic_json['group_pic']):
            pic_str += f'{i}: {pic_json["group_pic"][i]}\n'

            if len(pic_str) > 1600:
                await ctx.send(pic_str)

        if len(pic_str) > 0:
            await ctx.send(pic_str)

    @pic.command()
    async def random(self, ctx):

        pic_json = JsonApi().get_json('DynamicSettingJson')

        random_picture = random.choice(pic_json['group_pic'])
        await ctx.send(random_picture)


def setup(bot):
    bot.add_cog(Picture(bot))
