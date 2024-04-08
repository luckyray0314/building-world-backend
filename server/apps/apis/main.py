from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager, create_refresh_token, current_user
from flask_restful import Resource, Api, fields, marshal_with
from ..api import api_response
from server.db.models import Navbar, Employee
from flask import abort, request



class CheckingApiWorking(Resource):
    def get(self):
        return api_response(description="Checking API running")


class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def get(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return api_response({
            "access_token": new_access_token
            })


class WhoAmIResource(Resource):
    @jwt_required()
    def get(self):
        obj = current_user.get_all()
        for i in obj['companies']:
            em = Employee.query.filter_by(user_id=current_user.id, company_id=i['company_id']).first()
            if em:
                i['employee_id'] = em.id
                i['position'] = em.position
        return api_response(obj, "Got user details")


class NavbarResource(Resource):
    @jwt_required()
    def get(self, employee_id):
        navbar = Navbar.query.filter_by(employee_id=employee_id).first()
        if not navbar:
            abort(400)
        
        navbar_details = [{'name': 'Employee', 'enabled': navbar.employees,
                           'subitems': [{
                                'name': 'Hierarchy', 'url': '/hierarchy', 'enabled': navbar.hierarchy},
                                {'name': 'Search Workers', 'url': '/search_workers', 'enabled': navbar.search_workers},
                                {'name': 'Chat', 'url': '/chat', 'enabled': navbar.chats},
                            ]},
                          {'name': 'Projects','enabled': navbar.projects,
                           'subitems': [{
                               'name': 'Pipeline', 'url': '/pipeline', 'enabled': navbar.pipelines},
                               {'name': 'My tasks', 'url': '/my_tasks', 'enabled': navbar.my_tasks},
                               {'name': 'Statistic', 'url': '/statistic', 'enabled': navbar.statistics},
                           ]},
                          {'name': 'Purchase', 'enabled': navbar.purchases,
                          'subitems': [{
                              'name': 'Providers', 'url': '/providers', 'enabled': navbar.providers},
                              {'name': 'Order', 'url': '/order', 'enabled': navbar.orders},
                               {'name': 'Statistic', 'url': '/statistic', 'enabled': navbar.statistics},
                          ]},
                          {'name': 'Sales', 'enabled': navbar.sales,
                          'subitems': [{
                              'name': 'Stock_lists', 'url': '/stock_lists', 'enabled': navbar.stock_lists},
                              {'name': 'Planned_shipments', 'url': '/planned_shipments', 'enabled': navbar.planned_shipments},
                               {'name': 'Statistic', 'url': '/statistic', 'enabled': navbar.statistics},
                          ]},
                          {'name': 'Finance', 'enabled': navbar.finance,
                           'subitems': [{
                               'name': 'Account', 'url': '/account', 'enabled': navbar.accounts},
                               {'name': 'Flow and Fund', 'url': '/flow_and_fund', 'enabled': navbar.flow_and_funds},
                               {'name': 'Mutual Settlement', 'url': '/mutual_settlement', 'enabled': navbar.mutual_settlements},
                               {'name': 'Statistic', 'url': '/statistic', 'enabled': navbar.statistics},
                           ]},]
        

        navbar_res = [item for item in navbar_details if item['enabled']]

        return api_response(
            navbar_res, "Got navbar"
        )

