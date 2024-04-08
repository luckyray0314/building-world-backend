from flask import request
from flask_jwt_extended import (
	jwt_required,
)
from flask_restful import Resource
from werkzeug.exceptions import Forbidden

from ..api import api_response

from .helpers import is_feature_allowed

from ...db.models import Provider


# Get providers based on types and user_name of the providers
class GetProvidersResource(Resource):
	@jwt_required()
	def get(self, company_id):
		# Check if user is a company employee and has Navbar access
		if not is_feature_allowed(company_id, "providers"):
			raise Forbidden
		
		# output settings
		page = int(request.args.get("page", 1))
		per_page = int(request.args.get("per_page", 10))
		
		# Get the request parameters
		types = request.args.getlist("type")
		name = request.args.get("name")
	
		# send the query parameters and get the providers
		providers = Provider.get_providers(
			types=types,
			name=name,
			company_id=company_id,
			per_page=per_page,
			page=page)
			
		# Return provider
		return api_response(providers, "Got Provider(s)")
