from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from flask import request, jsonify
from schemas import PaginationSchema, AirportSchema, AirportDetailsArgs
from marshmallow import fields


from db import db
from models import PatrimonyModel, UserModel
from schemas import Schema, PatrimonySchema, patrimony_schema, SearchArgsSchema

blp = Blueprint("Patrimonies", __name__, description="Operações com patrimonio.")

@blp.route("/patrimonies")
class Patrimonies(MethodView):
    @blp.response(200, PatrimonySchema(many=True), description="Sucesso. Retorna uma lista de todos os patrimônios.")
    def get(self):
        """ Rota para listar todos os patrimônios."""
        patrimonies = PatrimonyModel.query.all()
        return patrimony_schema.dump(patrimonies, many=True)

@blp.route("/airports")
class Airports(MethodView):
    @blp.response(200, AirportSchema(many=True), description="Sucesso. Retorna uma lista de todos os aeroportos.")
    def get(self):
        """ Rota para listar todos os nomes dos aeroportos."""
        airport_names = PatrimonyModel.query.filter(PatrimonyModel.airport != '').with_entities(PatrimonyModel.airport).distinct().all()
        airport_schema = AirportSchema(many=True)
        return airport_schema.dump(airport_names)

@blp.route("/airport_details")
class AirportDetails(MethodView):
    @blp.arguments(Schema.from_dict({"airport": fields.String(required=True), "page": fields.Integer(), "items_per_page": fields.Integer(), "number": fields.String()}), location="query")
    @blp.response(200, PatrimonySchema(many=True), description="Sucesso. Retorna uma lista de todos os patrimônios relacionados ao aeroporto especificado.")
    def get(self, args):
        """ Rota para listar todos os patrimônios relacionados ao aeroporto especificado."""
        airport = args["airport"]
        number = args.get("number")
        page = args.get("page", 1)
        items_per_page = args.get("items_per_page")

        query = PatrimonyModel.query.filter(PatrimonyModel.airport == airport)
        if number:
            query = query.filter(PatrimonyModel.number == number)

        if items_per_page:
            patrimonies = query.paginate(page=page, per_page=items_per_page, error_out=False)
            return patrimony_schema.dump(patrimonies.items, many=True)
        else:
            patrimonies = query.all()
            return patrimony_schema.dump(patrimonies, many=True)


@blp.route("/search/<string:patrimony_number>")
class SearchPatrimony(MethodView):
    @jwt_required()
    @blp.response(200, PatrimonySchema, description="Sucesso. Retorna o patrimônio encontrado.")
    def get(self, patrimony_number):
        """ Rota para buscar um patrimônio pelo número e verificar se está relacionado ao usuário logado."""
        jwt_payload = get_jwt()
        user_id = jwt_payload["sub"]

        user = UserModel.query.get(user_id)
        if not user:
            abort(404, description="Usuário não encontrado.")

        patrimony = PatrimonyModel.query.filter_by(number=patrimony_number).first()

        if not patrimony:
            abort(404, description="Patrimônio não encontrado.")


        return patrimony_schema.dump(patrimony)

@blp.route("/my-patrimonies")
class MyPatrimonies(MethodView):
    @jwt_required()
    @blp.arguments(PaginationSchema, location="query", as_kwargs=True)
    @blp.response(200, PatrimonySchema(many=True), description="Sucesso. Retorna uma lista de patrimônios relacionados ao usuário.")
    def get(self, **kwargs):
        """ Rota para listar patrimônios relacionados ao usuário atual."""
        jwt_payload = get_jwt()
        user_id = jwt_payload["sub"]

        # Adiciona uma variável page que obtém o valor do parâmetro de consulta 'page' ou usa None por padrão
        page = request.args.get('page', None)
        if page is not None:
            page = int(page)

        user = UserModel.query.get(user_id)
        if not user:
            abort(404, description="Usuário não encontrado.")

        patrimonies_query = PatrimonyModel.query.filter_by(registry=user.registry).order_by(PatrimonyModel.verified.desc())

        if page is not None:
            patrimonies_query = patrimonies_query.limit(10).offset(10 * (page - 1))

        patrimonies = patrimonies_query.all()
        return patrimony_schema.dump(patrimonies, many=True)


@blp.route("/patrimonies/<string:patrimony_number>")
class PatrimonyResource(MethodView):
    #@jwt_required()
    @blp.arguments(PatrimonySchema(only=("verified",)), location="json")
    @blp.response(200, PatrimonySchema(many=True), description="Sucesso. Retorna os patrimônios atualizados.")
    def put(self, patrimony_data, patrimony_number):
        """ Rota para atualizar o status verificado de todos os patrimônios existentes com o mesmo número."""
        patrimonies = PatrimonyModel.query.filter(PatrimonyModel.number == patrimony_number).all()

        # Adicione esta linha para imprimir os resultados da consulta
        print("Resultado da consulta:", patrimonies)

        if not patrimonies:
            abort(404, description="Nenhum patrimônio encontrado com o número fornecido.")

        if "verified" in patrimony_data:
            for patrimony in patrimonies:
                patrimony.verified = patrimony_data["verified"]
            db.session.commit()
        else:
            abort(400, description="O campo 'verified' é necessário.")

        return patrimony_schema.dump(patrimonies, many=True)
