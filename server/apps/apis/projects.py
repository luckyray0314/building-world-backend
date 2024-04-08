import datetime

from flask import request
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from werkzeug.exceptions import Forbidden

from server.db.models import (
	Project,
	ProjectTask,
	Pipeline,
	ProjectTaskAttachment,
	ProjectTaskComment,
	PipelineStage,
	ProjectTaskTag,
	Company)
from .helpers import is_feature_allowed, get_company_id_from_project_id, is_task_member
from ..api import api_response, api_abort


# Create a new project
class ProjectsCreateProjectResource(Resource):
	@jwt_required()
	def post(self, company_id):
		# Check if the user is current company employee and has Navbar access
		if not is_feature_allowed(company_id, "projects"):
			raise Forbidden
		
		# Get the data from request
		data = request.get_json()
		# Project data
		stage_id = data.get('stage_id')
		name = data.get('name')
		description = data.get('description')
		counter_party = data.get('counter_party')
		budget = data.get('budget')
		currency = data.get('currency')
		
		# If data available
		if all([stage_id, name, description, counter_party, budget, currency]):
			
			# Get company of the counter_party
			company = Company.query.get(counter_party)
			if not company:
				return api_abort(404, f"No counterparty exist with Id: {counter_party}")
			
			# Get stage
			stage = PipelineStage.query.get(stage_id)
			if not stage:
				return api_abort(404, f"No stage exist with Id: {stage_id}")
			
			# Get pipeline
			pipeline = Pipeline.query.get(stage.pipeline_id)
			if not pipeline:
				return api_abort(404, f"No pipeline exist with Id: {stage.pipeline_id}")
			
			# New project
			new_project = Project(
				stage_id=stage_id, name=name,
				description=description,
				counter_party=counter_party,
				budget=budget, currency=currency)
			
			# Insert new project
			new_project.insert()
			
			# Return new project
			return api_response(new_project.get_all(True), "Project created")
		else:
			# raise Exception
			return api_abort(400, "Invalid data provided")


# Update the project status
class ProjectsSetProjectStatus(Resource):
	@jwt_required()
	def put(self, project_id):
		# Get the project
		project = Project.query.get(project_id)
		if not project:
			return api_abort(404, f"No projects exist with Id: {project_id}")
		
		# Check if the user is the current company employee and has access in the Navbar
		if not is_feature_allowed(project.counter_party, "projects"):
			raise Forbidden
		
		# Get the data from request
		data = request.get_json()
		# Project status
		status = data.get('status')
		
		# If data available
		if all([status]):
			# Check if status is valid
			if not status in ["assigned", "active", "succeeded", "failed"]:
				return api_abort(400, "Invalid status provided")
			
			# Set the status
			project.status = status
			project.update()
			
			# Return the updated project
			return api_response(project.get_all(True), "Project status updated")
		else:
			# raise Exception
			return api_abort(400, "Invalid data provided")


# Update project stage in pipeline
class ProjectsMoveProjectResource(Resource):
	@jwt_required()
	def put(self, project_id):
		# Get project
		project = Project.query.get(project_id)
		if not project:
			return api_abort(404, f"No projects exist with Id: {project_id}")
		
		# Check if the user is the current company employee and has access in the Navbar
		if not is_feature_allowed(project.counter_party, "projects"):
			raise Forbidden
		
		# Get the data from request
		data = request.get_json()
		# Stage Id
		stage_id = data.get('stage_id')
		
		# If data available
		if all([stage_id]):
			# Get pipeline stage
			pipeline_stage = PipelineStage.query.get(stage_id)
			if not pipeline_stage:
				return api_abort(404, f"No pipeline_stage exist with Id: {stage_id}")
			
			# Set the new stage
			project.stage_id = stage_id
			project.update()
			
			return api_response(project.get_all(True), "Project moved to new pipeline")
		else:
			# raise Exception
			return api_abort(400, "Invalid data provided")


# Delete the Project along with its children
class ProjectsDeleteProjectResource(Resource):
	@jwt_required()
	def delete(self, project_id):
		# Get project
		project = Project.query.get(project_id)
		if not project:
			return api_abort(404, f"No projects exist with Id: {project_id}")
		
		# Check if the user is current company employee and has Navbar access
		if not is_feature_allowed(project.counter_party, "projects"):
			raise Forbidden
		
		# Delete the project along with its children
		project.delete()
		
		# Return success
		return api_response(None, 'Project deleted')


# Create a new Task
class ProjectsCreateProjectTaskResource(Resource):
	@jwt_required()
	def post(self, project_id):
		# Get project
		project = Project.query.get(project_id)
		if not project:
			return api_abort(404, f"No projects exist with Id: {project_id}")
		
		# Check if the user is current company employee and has Navbar access
		if not is_feature_allowed(project.counter_party, "projects"):
			raise Forbidden
		
		# Get the data from request
		data = request.get_json()
		# Task Data
		title = data.get('title')
		description = data.get('description')
		due_date = data.get('due_date')
		
		# If data available
		if all([title, description, due_date]):
			
			# New task
			new_task = ProjectTask(
				project_id=project_id,
				title=title,
				description=description,
				due_date=datetime.datetime.strptime(due_date, '%Y-%m-%d'))
			
			# Insert the new task into the table
			new_task.insert()
			
			# Return new_task
			return api_response(new_task.get_all(True), "Task created")
		else:
			# raise Exception
			return api_abort(400, "Invalid data provided")


# Create a new task tag
class ProjectsCreateProjectTaskTagResource(Resource):
	@jwt_required()
	def post(self, task_id):
		# Get the task
		task = ProjectTask.query.get(task_id)
		if not task:
			return api_abort(404, f"No tasks exist with Id: {task_id}")
		
		# Get company_id
		company_id = get_company_id_from_project_id(task.project_id)
		
		# Check if the user is the current company employee and has access in the Navbar
		employee = is_feature_allowed(company_id, "projects")
		if not employee:
			raise Forbidden
		
		# Get the data from request
		data = request.get_json()
		# Tag data
		tag_id = data.get('tag_id')
		
		# If data available
		if all([tag_id]):
			# Add the new task tag into the ProjectTaskTag model
			new_task_tag = ProjectTaskTag(
				task_id=task_id,
				tag_id=tag_id)
			
			# Insert new tag
			new_task_tag.insert()
			
			# Return new tag
			return api_response(new_task_tag.get_all(), "Tag created")
		else:
			# raise Exception
			return api_abort(400, "Invalid data provided")


# Update the task status
class ProjectsSetProjectTaskStatus(Resource):
	@jwt_required()
	def put(self, task_id):
		# Get the task
		task = ProjectTask.query.get(task_id)
		if not task:
			return api_abort(404, f"No tasks exist with Id: {task_id}")
		
		# Get company_id
		company_id = get_company_id_from_project_id(task.project_id)
		
		# Check if the user is the current company employee and has access in the Navbar
		employee = is_feature_allowed(company_id, "projects")
		if not employee:
			raise Forbidden
		
		# Check if the current employee is a task member
		is_task_member(employee.id, task_id)
		
		# Get the data from request
		data = request.get_json()
		# Task status
		status = data.get('status')
		
		# If data available
		if all([status]):
			# Check if status is valid
			if not status in ["assigned", "active", "succeeded", "failed"]:
				return api_abort(400, "Invalid status provided")
			
			# Set the status
			task.status = status
			task.update()
			
			# Return the updated task
			return api_response(task.get_all(True), "Task status updated")
		else:
			# raise Exception
			return api_abort(400, "Invalid data provided")


# Get all the tasks of a project
class ProjectsGetProjectTasksResource(Resource):
	@jwt_required()
	def get(self, project_id):
		# Get project
		project = Project.query.get(project_id)
		if not project:
			return api_abort(404, f"No projects exist with Id: {project_id}")
		
		# Check if the user is the current company employee and has access in the Navbar
		if not is_feature_allowed(project.counter_party, "projects"):
			raise Forbidden
		
		# Get the tasks of the project
		project_tasks = ProjectTask.get_tasks(project_id=project_id)
		
		# Return the tasks
		return api_response(project_tasks, "Got Project Task(s)")


# Get a single task based on task_id that employee is participating
class ProjectsGetEmployeeTaskResource(Resource):
	@jwt_required()
	def get(self, task_id):
		# Get the task
		task = ProjectTask.query.get(task_id)
		if not task:
			return api_abort(404, f"No tasks exist with Id: {task_id}")
		
		# Get company_id
		company_id = get_company_id_from_project_id(task.project_id)
		
		# Check if the user is the current company employee and has access in the Navbar
		employee = is_feature_allowed(company_id, "projects")
		if not employee:
			raise Forbidden
		
		# Check if the current employee is a task member
		is_task_member(employee.id, task_id)
		
		# Return task
		return api_response(task.get_all(True), "Got Employee Task")


# Get all the tasks that are assigned to the employee
class ProjectsGetAllEmployeeTasksResource(Resource):
	@jwt_required()
	def get(self, company_id):
		# Check if the user has access to the project
		employee = is_feature_allowed(company_id, "projects")
		if not employee:
			raise Forbidden
		
		# output settings
		page = int(request.args.get("page", 1))
		per_page = int(request.args.get("per_page", 10))
		
		# Get tasks of the employee
		employee_tasks = ProjectTask.get_tasks(employee_id=employee.id, page=page, per_page=per_page)
		
		# Return tasks
		return api_response(employee_tasks, "Got Employee Tasks")


# Get task attachments based on task_id and employee_id
class ProjectsGetTaskAttachmentsResource(Resource):
	@jwt_required()
	def get(self, task_id):
		# Get the task
		task = ProjectTask.query.get(task_id)
		if not task:
			return api_abort(404, f"No tasks exist with Id: {task_id}")
		
		# Get company_id
		company_id = get_company_id_from_project_id(task.project_id)
		
		# Check if the user is the current company employee and has access in the Navbar
		employee = is_feature_allowed(company_id, "projects")
		if not employee:
			raise Forbidden
		
		# Check if the current employee is a task member
		is_task_member(employee.id, task_id)
		
		# output settings
		page = int(request.args.get("page", 1))
		per_page = int(request.args.get("per_page", 10))
		
		# Get attachments
		attachments = ProjectTaskAttachment.get_attachments(
			task_id=task_id,
			employee_id=employee.id,
			page=page, per_page=per_page)
		
		# Return attachments
		return api_response(attachments, "Got Task Attachment(s)")


# Get task comments based on task_id and employee_id
class ProjectsGetTaskCommentsResource(Resource):
	@jwt_required()
	def get(self, task_id):
		# Get the task
		task = ProjectTask.query.get(task_id)
		if not task:
			return api_abort(404, f"No tasks exist with Id: {task_id}")
		
		# Get company_id
		company_id = get_company_id_from_project_id(task.project_id)
		
		# Check if the user is the current company employee and has access in the Navbar
		employee = is_feature_allowed(company_id, "projects")
		if not employee:
			raise Forbidden
		
		# Check if the current employee is a task member
		is_task_member(employee.id, task_id)
		
		# output settings
		page = int(request.args.get("page", 1))
		per_page = int(request.args.get("per_page", 10))
		
		# Get comments
		comments = ProjectTaskComment.get_comments(
			task_id=task_id,
			employee_id=employee.id,
			page=page, per_page=per_page)
		
		# Return comments
		return api_response(comments, "Got Task Comment(s)")
