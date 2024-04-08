# from flask import request, abort
# from flask_restful import Resource, Api
# from flask_jwt_extended import jwt_required
# from server.db.models import Deals, Navbar, Employee
# import logging
# from flask_jwt_extended import current_user


# app = Flask(__name__)
# api = Api(app)

# def check_permissions(func):
#     """
#     A decorator to check user permissions before executing an endpoint method.

#     Parameters:
#         func (function): The endpoint method to be decorated.

#     Returns:
#         function: The decorated function that checks user permissions.
#     """
#     def wrapper(self, *args, **kwargs):
#         # Check if user is authenticated
#         if not current_user:
#             logging.warning("No authorization provided!")
#             abort(401)

#         # Check if user has access to the company associated with the resource
#         company_id = kwargs.get('company_id')
#         employee = Employee.query.filter_by(user_id=current_user.id, company_id=company_id).first()
#         navbar = Navbar.query.filter_by(user_id=employee.id).first()

#         if not employee:
#             logging.warning("User does not have an associated employee!")
#             abort(403)

#         # Check if user has pipeline permission in navbar
#         elif not navbar.pipeline:
#             logging.warning("User does not have pipeline permission in navbar!")
#             abort(403)

#         # If all checks passed, execute the endpoint method
#         return func(self, *args, **kwargs)

#     return wrapper

# class DealsResource(Resource):
#     # GET request to retrieve a specific deal
#     @jwt_required()
#     @check_permissions
#     def get(self, deal_id):
#         # Query the database for the deal with the given ID
#         deal = Deals.query.filter_by(id=deal_id).first()
#         company_id = deal.company_id
#         if not deal:
#             # If the deal is not found, return an error message and status code 404
#             return {'message': 'Deal not found'}, 404
#         # If the deal is found, serialize the data and return it
#         return deal.serialize()

#     # POST request to create a new deal
#     @jwt_required()
#     def post(self):
#         # Get the JSON data from the request
#         data = request.get_json()
#         # Create a new Deals object with the data
#         deal = Deals(
#             name=data.get('name'),
#             counterpartie=data.get('counterpartie'),
#             status=data.get('status', 0),
#             pipeline_id=data.get('pipeline_id', 0)
#         )
#         # Insert the new deal into the database
#         deal.insert()
#         # Return a success message and status code 201
#         return {'message': 'Deal created successfully'}, 201

#     # PUT request to update an existing deal
#     @jwt_required()
#     @check_permissions
#     def put(self, deal_id):
#         # Get the JSON data from the request
#         data = request.get_json()
#         # Query the database for the deal with the given ID
#         deal = Deals.query.filter_by(id=deal_id).first()
#         company_id = deal.company_id

#         if not deal:
#             # If the deal is not found, return an error message and status code 404
#             return {'message': 'Deal not found'}, 404
#         # If the deal is found, update its attributes with the new data (if provided)
#         if data.get('name'):
#             deal.name = data.get('name')
#         if data.get('counterpartie'):
#             deal.counterpartie = data.get('counterpartie')
#         if data.get('status'):
#             deal.status = data.get('status')
#         if data.get('pipeline_id'):
#             deal.pipeline_id = data.get('pipeline_id')
#         # Update the deal in the database
#         deal.update()
#         # Return a success message
#         return {'message': 'Deal updated successfully'}

#     # DELETE request to delete an existing deal
#     @jwt_required()
#     @check_permissions
#     def delete(self, deal_id):
#         # Query the database for the deal with the given ID
#         deal = Deals.query.filter_by(id=deal_id).first()
#         company_id = deal.company_id

#         if not deal:
#             # If the deal is not found, return an error message and status code 404
#             return {'message': 'Deal not found'}, 404
#         # If the deal is found, delete it from the database
#         deal.delete()
#         # Return a success message
#         return {'message': 'Deal deleted successfully'}

#     # PUT request to update the status of an existing deal to "failed"
#     @jwt_required()
#     @check_permissions
#     def put_failed(self, deal_id):
#         # Query the database for the deal with the given ID
#         deal = Deals.query.filter_by(id=deal_id).first()
#         company_id = deal.company_id

#         if not deal:
#             # If the deal is not found, return an error message and status code 404
#             return {'message': 'Deal not found'}, 404
#         # If the deal is found, set its status to "failed"
#         deal.set_failed()
#         return {'message': 'Deal status updated to failed'}

#     @jwt_required()
#     @check_permissions
#     def put_completed(self, deal_id):
#         # retrieve the deal with the given deal_id
#         deal = Deals.query.filter_by(id=deal_id).first()
#         company_id = deal.company_id

#         if not deal:
#             return {'message': 'Deal not found'}, 404

#         # set the deal status to completed
#         deal.set_completed()
#         return {'message': 'Deal status updated to completed'}

#     @jwt_required()
#     @check_permissions
#     def put_pipeline(self, deal_id):
#         # retrieve the pipeline_id from the request data
#         data = request.get_json()
#         pipeline_id = data.get('pipeline_id')

#         # return an error response if pipeline_id is not provided in the request
#         if not pipeline_id:
#             return {'message': 'Pipeline ID not provided'}, 400

#         # retrieve the deal with the given deal_id
#         deal = Deals.query.filter_by(id=deal_id).first()
#         company_id = deal.company_id
#         if not deal:
#             return {'message': 'Deal not found'}, 404

#         # move the deal to the pipeline with the given pipeline_id
#         deal.move_to_pipeline(pipeline_id)
#         return {'message': 'Deal moved to pipeline successfully'}
