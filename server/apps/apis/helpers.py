import logging

from werkzeug.exceptions import Forbidden

from server.db.models import (
    Company,
    ChatMember,
    Employee,
    Chat,
    Navbar,
    Project,
    Pipeline,
    PipelineStage,
    ProjectTaskMember
)

from flask_jwt_extended import current_user
from flask import abort


# def check_employee_belongs_to_chat(company_id, chat_id):
def is_current_user_in_chat(chat_id):
    # TODO: this can still be improved, we can get company_id from chat_id also

    chat = Chat.query.get(chat_id)
    if not chat:
        abort(404, "No such chat exist")

    company_id= chat.company_id
    
    # if a user isn't an employee they can't participate in chat
    if employee := is_current_user_company_employee(company_id):
        chat_member = ChatMember.query.filter_by(
            employee_id=employee.id, chat_id=chat_id
        ).first()
        return chat_member
    return False


def is_current_user_company_employee(company_id):
    if not Company.query.get(company_id):
        abort(404, f"No such company exist")
    current_employee = Employee.query.filter_by(
        user_id=current_user.id, company_id=company_id
    ).first()
    return current_employee


def is_company_employee(company_id, employee_id):
    if not Company.query.get(company_id):
        abort(404, f"No such company exist")
    if employee_id:
        company_employee = Employee.query.filter_by(
            id=employee_id, company_id=company_id
        ).first()
    return company_employee


def get_company_id_from_project_id(project_id):
    # Get project
    project = Project.query.get(project_id)
    if not project:
        return abort(404, f"No projects exist with Id: {project_id}")
    
    # Get pipeline stage
    pipeline_stage = PipelineStage.query.get(project.stage_id)
    if not pipeline_stage:
        return abort(404, f"No pipeline_stage exist with Id: {project.stage_id}")
    
    # Get pipeline
    pipeline = Pipeline.query.get(pipeline_stage.pipeline_id)
    if not pipeline:
        return abort(404, f"No pipeline exist with Id: {pipeline_stage.pipeline_id}")

    return pipeline.company_id


def is_task_member(employee_id, task_id):
    # Check if the employee is a task member
    task_member = ProjectTaskMember.query.filter_by(employee_id=employee_id, task_id=task_id).first()
    if not task_member:
        raise Forbidden
    return task_member


def is_feature_allowed(company_id, feature: str, employee_id=None):
    """Check if the current user has access to the feature
        args:
            - company_id(str): company id
            - feature(str): - feature can be pipeline, hierarchy,etc
            - employee_id
        Returns:
            - employee if no error
            - Forbidden if error or no access
    """
    if not employee_id:
        employee = is_current_user_company_employee(company_id=company_id)
    else:
        employee = is_company_employee(company_id=company_id, employee_id=employee_id)
    if not employee or not getattr(Navbar.query.filter_by(employee_id=employee.id).first(), feature):
        logging.error(f"Not an employee or has no {feature} in navbar")
        return None
    return employee