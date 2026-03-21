import random
import string
from typing import Any, Optional

def generate_random_string(length: int = 32) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits+'_/@#$^&*', k=length))


def get_user_attr_value(attributes: list[dict[str, Any]], name: str) -> Optional[str]:
    """Cognito のユーザー属性リストから指定した Name の Value を取り出す。"""
    for attr in attributes:
        if attr.get("Name") == name:
            return attr.get("Value")
    return None