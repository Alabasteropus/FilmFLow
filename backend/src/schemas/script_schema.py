# src/schemas/script_schema.py
from marshmallow import Schema, fields, validate, ValidationError

class ScriptSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    content = fields.Str(required=True, validate=validate.Length(min=1))
