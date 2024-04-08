from flask import request
from flask_jwt_extended import (
	jwt_required,
)
from flask_restful import Resource
from werkzeug.exceptions import Forbidden

from .helpers import is_feature_allowed
from ..api import api_response, api_abort
from ...db.models import Product, Provider, ProductImage


# Edit products
class EditProductResource(Resource):
	@jwt_required()
	def put(self, product_id):
		# Get the product
		product = Product.query.get(product_id)
		if not product:
			return api_abort(404, f"Product with id {product_id} not found")
		
		# If company_id exists
		if product.company_id:
			# Check if the user is a company employee and has Navbar access
			if not is_feature_allowed(product.company_id, "products"):
				raise Forbidden
		
		# Else, get the provider id and counter_party
		else:
			# Get the provider
			provider = Provider.query.get(product.provider_id)
			if not provider:
				return api_abort(404, f"Provider with id {product.provider_id} not found")
			
			# Check if the user is a company employee and has Navbar access
			if not is_feature_allowed(provider.counter_party, "products"):
				raise Forbidden
		
		# Get the data from request
		data = request.get_json()
		
		# New product data
		avatar = data.get('avatar')
		name = data.get('name')
		price = data.get('price')
		currency = data.get('currency')
		description = data.get('description')
		product_images = data.get('product_images')
		
		# Check if new data is provided to update the product
		if not any([avatar, name, price, currency, description, product_images]):
			return api_abort(400, "Need data to update the product")
		
		# If avatar was provided, set the avatar
		if avatar:
			product.avatar = avatar
		
		# If name was provided, set the name
		if name:
			product.name = name
		
		# If price was provided, set the price
		if price:
			product.price = price
		
		# If currency was provided, set the currency
		if currency:
			product.currency = currency
		
		# If description was provided, set the description
		if description:
			product.description = description
		
		# If product images were provided, set the images
		if product_images:
			# Get the old images and remove them
			images = ProductImage.query.filter_by(product_id=product_id).all()
			for image in images:
				image.delete()
			
			# Inset each new image in the ProductImages table
			for image in product_images:
				product_image = ProductImage(image=image, product_id=product_id)
				product_image.insert()
		
		# Update the product
		product.update()
		
		# Return the updated product
		return api_response(product.get_all(True), "Product data Updated")
