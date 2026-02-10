"""基础设施 - 模板基类"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any
from functools import lru_cache

from nonebot import require, logger

require("nonebot_plugin_htmlkit")
from nonebot_plugin_htmlkit import template_to_pic, html_to_pic, md_to_pic, text_to_pic


class BaseTemplate(ABC):
    """模板基类 - 提供渲染能力"""

    __slots__ = ("name", "template_dir", "_cache")

    def __init__(self, name: str, templates_dir: Path):
        self.name = name
        self.template_dir = templates_dir / name
        self._cache: dict[str, str] = {}

    @abstractmethod
    async def render(self, **params: Any) -> bytes:
        """渲染为图片

        :param params: 模板参数
        :return: 图片字节数据
        """
        pass

    def get_render_options(self) -> dict[str, Any]:
        """获取模板默认渲染选项"""
        return {"max_width": 800, "allow_refit": True}

    def get_file(self, filename: str) -> str:
        """获取模板文件内容（带缓存）"""
        if filename not in self._cache:
            file_path = self.template_dir / filename
            if not file_path.exists():
                raise FileNotFoundError(f"模板文件不存在: {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                self._cache[filename] = f.read()
        return self._cache[filename]

    @lru_cache(maxsize=32)
    def get_resource(self, name: str) -> str:
        """获取模板资源路径（带缓存）"""
        resource_file = self.template_dir / name
        if not resource_file.exists():
            logger.warning(f"资源不存在: {resource_file}")
            return ""
        return str(resource_file.absolute())

    async def to_pic_html(self, html: str, **options: Any) -> bytes:
        """HTML转图片"""
        return await html_to_pic(html, **options)

    async def to_pic_md(self, md: str, **options: Any) -> bytes:
        """Markdown转图片"""
        return await md_to_pic(md=md, **options)

    async def to_pic_text(self, text: str, **options: Any) -> bytes:
        """纯文本转图片"""
        return await text_to_pic(text, **options)

    async def to_pic_template(
        self,
        filename: str,
        templates: dict[str, Any],
        **options: Any,
    ) -> bytes:
        """使用htmlkit的template_to_pic功能渲染模板"""
        return await template_to_pic(
            template_path=str(self.template_dir),
            template_name=filename,
            templates=templates,
            **options,
        )
