from typing import List, Tuple, Type, Optional

from src.plugin_system import (
    BasePlugin,
    register_plugin,
    BaseCommand,
    ComponentInfo,
)

from jmcomic import JmOption, JmAlbumDetail


# ================== JM Client ==================
jm_client = JmOption.default().new_jm_client()


# ================== JM 查询 Command ==================
class JmSearchCommand(BaseCommand):
    """
    JM查询 Command
    用户输入：JM427413
    """

    command_name = "jm_search"
    command_description = "根据 JM+数字 查询禁漫本子信息"

    command_pattern = r"^JM(?P<jm_id>\d+)$"

    async def execute(self) -> Tuple[bool, Optional[str], bool]:
        """
        执行 JM 查询
        """

        # 从 matched_groups 取参数
        jm_id = self.matched_groups.get("jm_id")
        if not jm_id:
            return False, "JM编号解析失败", True

        try:
            page = jm_client.search_site(search_query=jm_id)
            album: JmAlbumDetail = page.single_album

            title = album.title
            tags = ", ".join(album.tags)

            message = (
                f" JM{jm_id}\n"
                f"标题：{title}\n"
                f"标签：{tags}"
            )

            await self.send_text(message)
            return True, f"JM{jm_id} 查询成功", True

        except Exception as e:
            await self.send_text(f" JM{jm_id} 查询失败")
            return False, str(e), True


# ================== 插件主类 ==================
@register_plugin
class HelloWorldPlugin(BasePlugin):

    plugin_name = "jm_query_plugin"
    enable_plugin = True
    dependencies = []
    python_dependencies = ["jmcomic"]
    config_file_name = "config.toml"
    config_schema = {}

    def get_plugin_components(self) -> List[Tuple[ComponentInfo, Type]]:
        return [
            (JmSearchCommand.get_command_info(), JmSearchCommand),
        ]
