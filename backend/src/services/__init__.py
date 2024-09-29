# src/services/__init__.py
from .auth_service import register_user, login_user, get_user
from .script_service import (
    create_script, get_user_scripts, get_script_by_id, update_script, delete_script
)
from .openai_service import generate_text
