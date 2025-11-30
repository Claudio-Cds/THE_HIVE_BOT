from dataclasses import dataclass

@dataclass
class BotConfig:
    token: str
    admin_ids: list[int]
    copy_enabled: bool = False


def load_config() -> BotConfig:
    return BotConfig(
        token="8249982976:AAGi41WZ33FCH_LRZoWZj_5_VxVUk5vxwc8",   # 🔴 coloque seu token do BotFather
        admin_ids=[8333494453],   # 🟢 seu ID de ADM
        copy_enabled=False,
    )
