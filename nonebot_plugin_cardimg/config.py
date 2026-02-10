"""CardImg插件配置"""

from __future__ import annotations

from nonebot import get_plugin_config
from pydantic import BaseModel


class ConfigModel(BaseModel):
    """CardImg全局配置"""

    cardimg_use_global_config: bool = False
    """是否使用全局配置作为兜底（默认False）"""

    cardimg_image_format: str = "png"
    """全局图片格式：png或jpeg（默认png）"""

    cardimg_jpeg_quality: int = 85
    """全局JPEG质量：1-100（默认85）"""


config: ConfigModel = get_plugin_config(ConfigModel)
