from gsuid_core.sv import SV
from gsuid_core.bot import Bot
from gsuid_core.models import Event
from gsuid_core.logger import logger
from gsuid_core.utils.plugins_config.gs_config import core_plugins_config
from gsuid_core.utils.plugins_update._plugins import (
    check_retcode,
    update_from_git,
    run_poetry_install,
    update_all_plugins,
    set_proxy_all_plugins,
)

sv_core_config = SV('Core管理', pm=0)


@sv_core_config.on_fullmatch(('core更新'))
async def send_core_update_msg(bot: Bot, ev: Event):
    logger.info('开始执行[更新] 早柚核心')
    log_list = update_from_git()
    await bot.send(log_list)


@sv_core_config.on_command(('core设置代理'))
async def send_core_set_proxy(bot: Bot, ev: Event):
    logger.info('开始执行[设置代理]')
    proxy_url = ev.text.strip() if ev.text else ''
    core_plugins_config.set_config('ProxyURL', proxy_url)
    await bot.send(
        f'设置成功!\n当前插件安装代理为{core_plugins_config.get_config("ProxyURL").data}'
        '\n之后新安装的插件均会应用此代理'
        '\n你也可以输入命令[core应用设置代理]以应用代理到现有全部插件。'
    )


@sv_core_config.on_command(('core应用设置代理'))
async def send_core_update_proxy(bot: Bot, ev: Event):
    logger.info('开始执行[应用设置代理]')
    proxy = ev.text if ev.text else None
    if '无' in ev.text:
        proxy = ''
    log_list = await set_proxy_all_plugins(proxy)
    await bot.send(log_list)


@sv_core_config.on_fullmatch(('core更新依赖'))
async def send_core_poetry_install(bot: Bot, ev: Event):
    logger.info('开始执行[更新] 早柚核心依赖')
    retcode = await run_poetry_install()
    im = check_retcode(retcode)
    await bot.send(im)


@sv_core_config.on_fullmatch(('core全部更新'))
async def send_core_all_update_msg(bot: Bot, ev: Event):
    logger.info('开始执行[更新] 全部更新')
    log_list = update_from_git()
    log_list.extend(update_all_plugins())
    await bot.send(log_list)
