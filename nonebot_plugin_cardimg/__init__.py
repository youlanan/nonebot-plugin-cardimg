from __future__ import annotations

from typing import Any

from nonebot import get_driver, logger
from nonebot.plugin import PluginMetadata

from .config import ConfigModel, config
from .base import BaseTemplate
from .templates import (
    MiNoteTemplate,
    SimpleTemplate,
    NcmZhuShaTemplate,
    NcmCardTemplate,
    BiliTemplate,
    HelpTemplate,
    TableTemplate,
)

__version__ = "0.1.2"
__plugin_meta__ = PluginMetadata(
    name="nonebot-plugin-cardimg",
    description="基于 nonebot_plugin_htmlkit 渲染的文本转图片模板插件",
    usage=(
        "提供预定义的HTML模板，简化图片渲染\n"
        "示例: img_bytes = await render('minote', title='标题', content='内容')\n"
        "可用模板: minote(小米便签), simple(简约), ncm_zhusha(网易云朱砂), "
        "ncm_card(网易云热评卡片), bili(哔哩哔哩壁纸), help(帮助文档), table(表格)"
    ),
    type="library",
    homepage="https://github.com/youlanan/nonebot-plugin-cardimg",
    config=ConfigModel,
    extra={"License": "MIT", "Author": "youlanan"},
)

_templates: dict[str, BaseTemplate] = {}
_initialized = False


def load_resources() -> None:
    """初始化资源"""
    global _initialized
    if _initialized:
        return

    _templates["minote"] = MiNoteTemplate()
    _templates["simple"] = SimpleTemplate()
    _templates["ncm_zhusha"] = NcmZhuShaTemplate()
    _templates["ncm_card"] = NcmCardTemplate()
    _templates["bili"] = BiliTemplate()
    _templates["help"] = HelpTemplate()
    _templates["table"] = TableTemplate()

    _initialized = True
    logger.success(f"模板库初始化完成: {len(_templates)} 个模板")


def get_template(name: str) -> BaseTemplate:
    """获取模板"""
    if not _initialized:
        raise RuntimeError("模板未初始化，请先调用 load_resources()")
    template = _templates.get(name)
    if not template:
        available = ", ".join(_templates.keys())
        raise ValueError(f"模板 '{name}' 不存在，可用: {available}")
    return template


def list_templates() -> list[str]:
    """列出所有可用模板

    :return: 模板名称列表
    """
    return list(_templates.keys())


async def cardimg_render(
    template: str,
    title: str = "",
    content: str = "",
    footer: str = "",
    htmlkit_params: dict[str, Any] | None = None,
    **kwargs: Any,
) -> bytes:
    """渲染模板为图片

    :param template: 模板名称（minote/simple/ncm_zhusha/ncm_card/bili/help/table）
    :param title: 标题
    :param content: 正文内容
    :param footer: 页脚
    :param htmlkit_params: htmlkit渲染参数（如 {"max_width": 800, "image_format": "jpeg"}）
    :param kwargs: 模板特定参数（如 simple/bili/help/table模板的 night_mode=True，help模板的 items 列表，table模板的 columns 和 data）
    :return: 图片字节数据
    """
    tmpl = get_template(template)

    render_options = {}

    if config.cardimg_use_global_config:
        render_options["image_format"] = config.cardimg_image_format
        render_options["jpeg_quality"] = config.cardimg_jpeg_quality

    template_options = tmpl.get_render_options()
    for key, value in template_options.items():
        render_options[key] = value

    if htmlkit_params:
        render_options.update(htmlkit_params)

    kwargs["_render_options"] = render_options

    return await tmpl.render(title=title, content=content, footer=footer, **kwargs)


render = cardimg_render


@get_driver().on_startup
async def _startup():
    """插件启动时加载资源"""
    try:
        load_resources()
        logger.success("CardImg 插件启动完成")
    except Exception as e:
        logger.error(f"CardImg 插件启动失败: {e}")


__all__ = [
    "render",
    "cardimg_render",
    "list_templates",
    "BaseTemplate",
]
