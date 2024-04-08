from flask import request
from flask_jwt_extended import (
	jwt_required,
)
from flask_restful import Resource
from werkzeug.exceptions import Forbidden

from ..api import api_response, api_abort

from .helpers import is_feature_allowed

from ...db.models import Order, Provider

# Get Order of a company
class GetCompanyOrdersListResource(Resource):
	@jwt_required()
	def get(self, company_id):
		# Check if the user is a company employee and has Navbar access
		if not is_feature_allowed(company_id, "orders"):
			raise Forbidden
		
		# output settings
		page = int(request.args.get("page", 1))
		per_page = int(request.args.get("per_page", 10))
		
		# Get the status from request if selected
		status = request.args.get("status")
		
		# Send the query to the model and get orders
		orders_data = Order.get_orders(
			status=status,
			company_id=company_id,
			per_page=per_page,
			page=page)
		
		# Return orders
		return api_response(orders_data, "Got Company Order(s)")


# Get orders of a provider
class GetProviderOrdersListResource(Resource):
	@jwt_required()
	def get(self, provider_id):
		# Get provider
		provider = Provider.query.get(provider_id)
		if not provider:
			return api_abort(404, f"No providers exist with id {provider_id}")
		
		# Check if the user is a company employee and has Navbar access
		if not is_feature_allowed(provider.counter_party, "orders"):
			raise Forbidden

		# output settings
		page = int(request.args.get("page", 1))
		per_page = int(request.args.get("per_page", 10))
		
		# Get the status from request if selected
		status = request.args.get("status")
		
		# Send the query to the model and get orders
		orders_data = Order.get_orders(
			status=status,
			provider_id=provider_id,
			per_page=per_page,
			page=page)
		
		# Return orders
		return api_response(orders_data, "Got Provider Order(s)")
