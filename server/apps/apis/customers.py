from flask import request
from flask_jwt_extended import (
	jwt_required,
)
from flask_restful import Resource
from werkzeug.exceptions import Forbidden

from ..api import api_response

from .helpers import is_feature_allowed

from ...db.models import Customer

# Search for customers
class GetCustomersResource(Resource):
	@jwt_required()
	def get(self, company_id):
		# Check if the user is a company employee and has Navbar access
		if not is_feature_allowed(company_id, "customers"):
			raise Forbidden
		
		# output settings
		page = int(request.args.get("page", 1))
		per_page = int(request.args.get("per_page", 10))
		
		# Get the request parameters
		needle = request.args.get("needle")
		
		# send the query parameters and get the customers
		customers = Customer.get_customers(
			company_id=company_id,
			needle=needle,
			page=page, per_page=per_page)
		
		# Return provider
		return api_response(customers, "Got Customer(s)")
