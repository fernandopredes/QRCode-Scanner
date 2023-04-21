from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt


from db import db
from models import PatrimonyModel, UserModel
from schemas import Schema, PatrimonySchema, patrimony_schema

blp = Blueprint("Patrimonies", __name__, description="Operações com patrimonio.")

@blp.route("/patrimonies")
class Patrimonies(MethodView):
    @blp.response(200, PatrimonySchema(many=True), description="Sucesso. Retorna uma lista de todos os patrimônios.")
    def get(self):
        """ Rota para listar todos os patrimônios."""
        patrimonies = PatrimonyModel.query.all()
        return patrimony_schema.dump(patrimonies, many=True)

@blp.route("/my-patrimonies")
class MyPatrimonies(MethodView):
    @jwt_required()
    @blp.response(200, PatrimonySchema(many=True), description="Sucesso. Retorna uma lista de patrimônios relacionados ao usuário.")
    def get(self):
        """ Rota para listar patrimônios relacionados ao usuário atual."""
        jwt_payload = get_jwt()
        user_id = jwt_payload["sub"]

        user = UserModel.query.get(user_id)
        if not user:
            abort(404, description="Usuário não encontrado.")

        patrimonies = PatrimonyModel.query.filter_by(registry=user.registry).all()
        return patrimony_schema.dump(patrimonies, many=True)


@blp.route("/patrimonies/<int:patrimony_id>")
class PatrimonyResource(MethodView):
    #@jwt_required()
    @blp.arguments(PatrimonySchema(only=("verified",)), location="json")
    @blp.response(200, PatrimonySchema, description="Sucesso. Retorna o patrimônio atualizado.")
    def put(self, patrimony_data, patrimony_id):
        """ Rota para atualizar o status verificado de um patrimônio existente pelo id."""
        patrimony = PatrimonyModel.query.get_or_404(patrimony_id)

        if "verified" in patrimony_data:
            patrimony.verified = patrimony_data["verified"]
            db.session.commit()
        else:
            abort(400, description="O campo 'verified' é necessário.")

        return patrimony_schema.dump(patrimony)
