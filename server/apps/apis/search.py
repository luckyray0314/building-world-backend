from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager, create_refresh_token, current_user
from flask_restful import Resource, Api, fields, marshal_with
from ..api import api_response
from server.db.models import Company, Employee, Chat, Message, User
from flask import abort, request



class SearchWorkersResource(Resource):
    @jwt_required()
    def post(self):
        
            data = request.get_json()
            needle = data.get('needle')
            results_per_page = data.get('results_per_page')
            page_num = data.get('page_num')
            if not needle: abort(400)

            if '*' in needle or '_' in needle: 
                looking_for = needle.replace('_', '__')\
                                    .replace('*', '%')\
                                    .replace('?', '_')
            else:
                looking_for = '%{0}%'.format(needle)
            company_id = Company.query.filter_by(owner_id=current_user.id).first().id

            if results_per_page and page_num:
                results = Employee.query.join(User, User.id==Employee.user_id).filter((Employee.position.ilike(looking_for))\
                                                                                        | (User.first_name.ilike(looking_for))\
                                                                                        | (User.last_name.ilike(looking_for)))\
                                                                                        .paginate(per_page=results_per_page, page=page_num)
            return api_response([i.get_all(True) for i in results.items])
        
        



