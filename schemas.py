from marshmallow import Schema, fields, validate

class PatrimonySchema(Schema):
    number = fields.Integer(required=True, validate=validate.Range(max=99999999))
    airport = fields.String(required=True, validate=validate.Length(max=50))
    description = fields.String(validate=validate.Length(max=255))
    price = fields.Float(required=True)
    responsible = fields.String(required=True, validate=validate.Length(max=50))
