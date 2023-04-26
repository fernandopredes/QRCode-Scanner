from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    id = fields.Int(dump_only=True, description="id do usuário")
    name = fields.Str(required=True, description="nome do usuário")
    registry = fields.String(required=True, validate=[validate.Length(max=7), validate.Regexp(r'^\d{1,7}$')])
    password = fields.Str(required=True, load_only=True, description="senha do usuário")

    class Meta:
        description = "Define a estrutura de um usuário"

class PatrimonySchema(Schema):
    id = fields.Integer(dump_only=True)
    number = fields.Integer(required=True, validate=validate.Range(max=99999999))
    airport = fields.String(required=True, validate=validate.Length(max=50))
    description = fields.String(validate=validate.Length(max=255))
    price = fields.Float(required=True)
    responsible = fields.String(required=True, validate=validate.Length(max=50))
    registry = fields.String(required=True, validate=[validate.Length(max=7), validate.Regexp(r'^\d{1,7}$')])
    verified = fields.Boolean(required=False)


patrimony_schema = PatrimonySchema()

class UserLoginSchema(Schema):
    """
    Define como deve ser a estrutura para realizar o login de um usuário.
    """
    registry = fields.Str(required=True, validate=[validate.Length(max=7), validate.Regexp(r'^\d{1,7}$')])
    password = fields.Str(required=True, load_only=True, description="password do usuário")

    class Meta:
        description = "Define como um login de usuário deve ser representado"


class CreateUserSchema(Schema):
    """
    Define como deve ser a estrutura do dado após criação de usuário.
    """
    message = fields.String(description="Mensagem de usuário criado")

    class Meta:
        description = "Esquema de mensagem após a criação de usuário."

class UserTokenSchema(Schema):
    """
    Define como deve ser a estrutura do dado após um login.
    """
    access_token = fields.String(description="Token de acesso")
    user_id = fields.Int(description="Id do usuário")

    class Meta:
        description = "Esquema para resposta da rota de login do usuário"


class SearchArgsSchema(Schema):
    responsible = fields.Str(required=True, description="Responsável pelos patrimônios a serem pesquisados")

class PaginationSchema(Schema):
    page = fields.Integer(required=False, description="Número da página atual")

class AirportSchema(Schema):
    airport = fields.String()

class AirportDetailsArgs(Schema):
    airport = fields.String(required=True)
    page = fields.Integer(missing=0)
