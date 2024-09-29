# src/services/script_service.py
from ..models.script import Script
from .. import db

def create_script(user_id: int, title: str, content: str) -> Script:
    script = Script(
        user_id=user_id,
        title=title,
        content=content
    )
    db.session.add(script)
    db.session.commit()
    return script

def get_user_scripts(user_id: int) -> list:
    return Script.query.filter_by(user_id=user_id).all()

def get_script_by_id(script_id: int, user_id: int) -> Script:
    return Script.query.filter_by(id=script_id, user_id=user_id).first()

def update_script(script_id: int, user_id: int, title: str = None, content: str = None) -> Script:
    script = get_script_by_id(script_id, user_id)
    if not script:
        raise Exception("Script not found.")
    if title:
        script.title = title
    if content:
        script.content = content
    db.session.commit()
    return script

def delete_script(script_id: int, user_id: int) -> bool:
    script = get_script_by_id(script_id, user_id)
    if not script:
        raise Exception("Script not found.")
    db.session.delete(script)
    db.session.commit()
    return True
