from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from werkzeug.exceptions import Forbidden

from server.db.models import (
	Tag)
from .helpers import is_feature_allowed
from ..api import api_response, api_abort


# Create a new tag
class CreateTagResource(Resource):
	@jwt_required()
	def post(self, company_id):
		# Check if the user is the current company employee and has access in the Navbar
		employee = is_feature_allowed(company_id, "projects")
		if not employee:
			raise Forbidden
		
		# Get the data from request
		data = request.get_json()
		# Tag data
		color = data.get('color')
		text = data.get('text')
		
		# If data available
		if all([color, text]):
			
			# Add the New tag into the Tag model
			new_tag = Tag(
				company_id=company_id,
				color=color,
				text=text)
			
			# Insert new tag
			new_tag.insert()
			
			# Return new tag
			return api_response(new_tag.get_all(), "Tag created")
		else:
			# raise Exception
			return api_abort(400, "Invalid data provided")
