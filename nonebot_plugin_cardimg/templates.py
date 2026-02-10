"""模板定义"""

from __future__ import annotations

import random
from typing import Any
from datetime import datetime
from pathlib import Path

from .base import BaseTemplate

_TEMPLATES_DIR = Path(__file__).parent / "templates"


class MiNoteTemplate(BaseTemplate):
    """小米便签模板 - MI Note风格（背景图+边框+四角装饰）"""

    __slots__ = ()

    def __init__(self):
        super().__init__("minote", _TEMPLATES_DIR)

    def get_render_options(self) -> dict[str, Any]:
        """模板默认渲染参数"""
        return {"max_width": 800, "allow_refit": True}

    async def render(self, title: str = "", content: str = "", footer: str = "", **kwargs: Any) -> bytes:
        """渲染模板为图片"""
        options = kwargs.pop("_render_options", self.get_render_options())
        templates = {
            "bg_image": self.get_resource("background.png"),
            "banner_01": self.get_resource("banner_01.png"),
            "banner_02": self.get_resource("banner_02.png"),
            "banner_03": self.get_resource("banner_03.png"),
            "banner_04": self.get_resource("banner_04.png"),
            "title": title,
            "content": content,
            "footer": footer,
        }
        return await self.to_pic_template("template.html", templates=templates, **options)


class SimpleTemplate(BaseTemplate):
    """Simple模板 - 纯色背景，支持夜间模式"""

    __slots__ = ("night_mode_enabled",)

    def __init__(self):
        super().__init__("simple", _TEMPLATES_DIR)
        self.night_mode_enabled = True

    def get_render_options(self) -> dict[str, Any]:
        """模板默认渲染参数"""
        return {"max_width": 600, "allow_refit": True}

    def _is_night_time(self) -> bool:
        """判断是否为夜间
        
        默认判断时间范围为18:00-6:00，子类可以重写此方法自定义昼夜切换时间
        
        :return: True表示夜间，False表示白天
        """
        hour = datetime.now().hour
        return hour >= 18 or hour < 6

    async def render(
        self,
        title: str = "",
        content: str = "",
        footer: str = "",
        night_mode: bool | None = None,
        **kwargs: Any,
    ) -> bytes:
        """渲染模板为图片"""
        use_night = night_mode if night_mode is not None else (self.night_mode_enabled and self._is_night_time())

        options = kwargs.pop("_render_options", self.get_render_options())
        templates = {
            "bg_color": "#1a1a1a" if use_night else "#ffffff",
            "text_color": "#e0e0e0" if use_night else "#000000",
            "footer_color": "#999999" if use_night else "#666666",
            "title": title,
            "content": content,
            "footer": footer,
        }
        return await self.to_pic_template("template.html", templates=templates, **options)


class NcmZhuShaTemplate(BaseTemplate):
    """网易云音乐模板 - 朱砂样式（红色背景+白色标题框）"""

    __slots__ = ()

    def __init__(self):
        super().__init__("ncm_zhusha", _TEMPLATES_DIR)

    def get_render_options(self) -> dict[str, Any]:
        """模板默认渲染参数"""
        return {"max_width": 680, "allow_refit": True}

    async def render(self, title: str = "", content: str = "", footer: str = "", **kwargs: Any) -> bytes:
        """渲染模板为图片"""
        options = kwargs.pop("_render_options", self.get_render_options())
        templates = {
            "title": title,
            "content": content,
            "footer": footer,
        }
        return await self.to_pic_template("template.html", templates=templates, **options)


class NcmCardTemplate(BaseTemplate):
    """网易云热评卡片模板"""

    __slots__ = ()

    def __init__(self):
        super().__init__("ncm_card", _TEMPLATES_DIR)

    def get_render_options(self) -> dict[str, Any]:
        """模板默认渲染参数"""
        return {"max_width": 800, "allow_refit": False}

    async def render(self, content: str = "", footer: str = "", **kwargs: Any) -> bytes:
        """渲染模板为图片
        
        :param title: 歌曲名（显示为"{title}下方评论"）
        :param content: 评论内容
        :return: 图片字节数据
        """
        options = kwargs.pop("_render_options", self.get_render_options())
        templates = {
            "bg_image": self.get_resource("background.png"),
            "content": content,
            "footer": footer,
        }
        return await self.to_pic_template("template.html", templates=templates, **options)


class BiliTemplate(BaseTemplate):
    """哔哩哔哩壁纸模板 - 支持昼夜模式（白/黑）"""

    __slots__ = ("night_mode_enabled",)

    def __init__(self):
        super().__init__("bili", _TEMPLATES_DIR)
        self.night_mode_enabled = True

    def get_render_options(self) -> dict[str, Any]:
        """模板默认渲染参数"""
        return {"max_width": 540, "device_height": 960, "allow_refit": False}

    def _is_night_time(self) -> bool:
        """判断是否为夜间
        
        默认判断时间范围为18:00-6:00，子类可以重写此方法自定义昼夜切换时间
        
        :return: True表示夜间，False表示白天
        """
        hour = datetime.now().hour
        return hour >= 18 or hour < 6

    async def render(
        self,
        content: str = "",
        footer: str = "",
        night_mode: bool | None = None,
        **kwargs: Any,
    ) -> bytes:
        """渲染模板为图片
        
        :param content: 正文内容
        :param footer: 页脚（通常为来源标注，如"——「歌曲名」"）
        :param night_mode: 夜间模式（True=黑色背景，False=白色背景，None=自动判断）
        :return: 图片字节数据
        """
        use_night = night_mode if night_mode is not None else (self.night_mode_enabled and self._is_night_time())

        if use_night:
            template_file = "night.html"
            bg_image = "bili_dark.jpg"
        else:
            template_file = "day.html"
            bg_image = "bili_light.jpg"

        options = kwargs.pop("_render_options", self.get_render_options())
        templates = {
            "bg_image": self.get_resource(bg_image),
            "content": content,
            "footer": footer,
        }
        return await self.to_pic_template(template_file, templates=templates, **options)


class HelpTemplate(BaseTemplate):
    """帮助文档模板 - 支持随机颜色主题和昼夜模式"""

    __slots__ = ("night_mode_enabled",)

    def __init__(self):
        super().__init__("help", _TEMPLATES_DIR)
        self.night_mode_enabled = True

    def get_render_options(self) -> dict[str, Any]:
        """模板默认渲染参数"""
        return {"max_width": 800, "allow_refit": True}

    def _is_night_time(self) -> bool:
        """判断是否为夜间
        
        默认判断时间范围为18:00-6:00，子类可以重写此方法自定义昼夜切换时间
        
        :return: True表示夜间，False表示白天
        """
        hour = datetime.now().hour
        return hour >= 18 or hour < 6

    async def render(
        self,
        title: str = "",
        items: dict[str, str] = {},
        footer: str = "",
        night_mode: bool | None = None,
        **kwargs: Any,
    ) -> bytes:
        """渲染帮助模板为图片

        :param title: 标题
        :param items: 帮助项列表，每个item为 {"title": "标题", "content": "内容"} 格式
        :param footer: 页脚
        :param night_mode: 夜间模式（True=夜间主题，False=白天主题，None=自动判断）
        :return: 图片字节数据
        """
        use_night = night_mode if night_mode is not None else (self.night_mode_enabled and self._is_night_time())

        template_file = "night.html" if use_night else "day.html"

        color_themes = [
            {"header": "#FFA94C", "item": "#FFA94C", "item_bg": "#FFF4E6"},
            {"header": "#8076a3", "item": "#8076a3", "item_bg": "#C2CEFE"},
            {"header": "#3FE6A0", "item": "#3FE6A0", "item_bg": "#E6F7F0"},
            {"header": "#D1D4F5", "item": "#D1D4F5", "item_bg": "#F0F4FF"},
            {"header": "#66a9c9", "item": "#66a9c9", "item_bg": "#E6FBFC"},
            {"header": "#68b88e", "item": "#68b88e", "item_bg": "#E6F7F0"},
            {"header": "#51c4d3", "item": "#51c4d3", "item_bg": "#E6FBFC"},
            {"header": "#f9a633", "item": "#f9a633", "item_bg": "#FFF4E6"},
            {"header": "#a8456b", "item": "#a8456b", "item_bg": "#ffe9f1"},
            {"header": "#55bb8a", "item": "#55bb8a", "item_bg": "#E6F7F0"},
            {"header": "#d2b116", "item": "#d2b116", "item_bg": "#f0e9c9"},
            {"header": "#8076a3", "item": "#8076a3", "item_bg": "#F0EEF8"},
        ]

        theme = random.choice(color_themes)

        options = kwargs.pop("_render_options", self.get_render_options())
        templates = {
            "title": title,
            "items": items,
            "footer": footer,
            "header_color": theme["header"],
            "item_color": theme["item"],
            "item_bg": theme["item_bg"],
        }
        return await self.to_pic_template(template_file, templates=templates, **options)


class TableTemplate(BaseTemplate):
    """表格模板 - 支持随机颜色主题和昼夜模式"""

    __slots__ = ("night_mode_enabled",)

    def __init__(self):
        super().__init__("table", _TEMPLATES_DIR)
        self.night_mode_enabled = True

    def get_render_options(self) -> dict[str, Any]:
        """模板默认渲染参数"""
        return {"max_width": 1000, "allow_refit": True}

    def _is_night_time(self) -> bool:
        """判断是否为夜间
        
        默认判断时间范围为18:00-6:00，子类可以重写此方法自定义昼夜切换时间
        
        :return: True表示夜间，False表示白天
        """
        hour = datetime.now().hour
        return hour >= 18 or hour < 6

    async def render(
        self,
        title: str = "",
        tip: str = "",
        columns: list[str] | None = None,
        data: list[list[str]] | None = None,
        footer: str = "",
        night_mode: bool | None = None,
        **kwargs: Any,
    ) -> bytes:
        """渲染表格模板为图片

        :param title: 标题
        :param tip: 提示文本
        :param columns: 表头列表
        :param data: 表格数据，二维列表
        :param footer: 页脚
        :param night_mode: 夜间模式（True=夜间主题，False=白天主题，None=自动判断）
        :return: 图片字节数据
        """
        if columns is None:
            columns = []
        if data is None:
            data = []

        use_night = night_mode if night_mode is not None else (self.night_mode_enabled and self._is_night_time())

        template_file = "night.html" if use_night else "day.html"

        color_themes = [
            {"header": "#3FE6A0", "header_bg": "#E6F7F0", "hover": "#f0fcf7"},
            {"header": "#66a9c9", "header_bg": "#E6F3F7", "hover": "#f0f8fb"},
            {"header": "#f9a633", "header_bg": "#FFF4E6", "hover": "#fff9f0"},
            {"header": "#a8456b", "header_bg": "#F7E6EA", "hover": "#fbf0f3"},
        ]

        theme = random.choice(color_themes)

        options = kwargs.pop("_render_options", self.get_render_options())
        templates = {
            "title": title,
            "tip": tip,
            "columns": columns,
            "data": data,
            "footer": footer,
            "header_color": theme["header"],
            "header_bg": theme["header_bg"],
            "hover_bg": theme["hover"],
        }
        return await self.to_pic_template(template_file, templates=templates, **options)
