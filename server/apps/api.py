from flask import request, jsonify, make_response
import json

from server.db.models import User, Navbar
from flask_mail import Message

# from server.tools.mail_sender import send_email_verification
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    unset_jwt_cookies,
    jwt_required,
    JWTManager,
    create_refresh_token,
    current_user,
)
from flask_restful import Resource, Api, fields, marshal_with
from server.apps.errorhandlers import init_api_errorhandlers


def Jsonify(
    result: dict,
    description: str = "",
    status_code: int = 200,
):
    return (
        jsonify({"ok": True, "description": description, "result": result}),
        status_code,
    )


def api_response(result: dict = None, description: str = "", status_code: int = 200):
    return {"ok": True, "description": description, "result": result}, status_code


def api_abort(status_code: int = 400, description: str = ""):
    return {
        "ok": False,
        "description": description,
        "error_code": status_code,
    }, status_code


# When documentation of API is needed, we will uncomment these lines:

# from flask_apispec import marshal_with, doc
# from flask_apispec.views import MethodResource
# from marshmallow import Schema, fields
# class LoginSchema(Schema):
#     email = fields.String()
#     password = fields.String()

# class SignUpSchema(Schema):
#     email = fields.String()
#     password = fields.String()
#     first_name = fields.String()
#     phone_number = fields.String()
#     last_name = fields.String()


# change
# login_fields = {
#     'email': fields.String,
#     'password': fields.String
# }


# signup_fields = {
#     'email': fields.String,
#     'password': fields.String,
#     'first_name': fields.String
# }


from server.apps.apis.hierarchy import (
    MovingWorkerResource,
    HierarchyEmployeesResource,
    FireWorkerResource,
    HierarchyHireEmployeeInvitationSendResource,
    HierarchyHireEmployeeInvitationConfirmResource,
    HierarchyEmployeesOwnersResource,
    HierarchyEmployeesLeadersResource,
    HierarchyGetALeaderResource,
)
from server.apps.apis.tags import CreateTagResource

from server.apps.apis.registrations import (
    SignupResource,
    LoginResource,
    ConfirmEmailVerificationCode,
    SendEmailVerificationCode,
    CreateCompanyResource,
)
from server.apps.apis.main import (
    RefreshResource,
    WhoAmIResource,
    NavbarResource,
    CheckingApiWorking,
)
from server.apps.apis.chats import (
    ChatDeleteMessageResource,
    ChatEditMessageResource,
    ChatListResource,
    ChatReadMessageResource,
    ChatSendMessageResource,
    ChatMessageResource,
    ChatGroupCreateResource,
    GetChatInfoResource,
    ForwardMessageResource,
    PinMessageResource,
    ChatGetMessageResource,
    ChatStatusResource,
    LiveChatResource
)
from server.apps.apis.search import SearchWorkersResource
from server.apps.apis.profile import ProfileEditResource, ProfileUpdateStatusResource
from server.apps.apis.projects import (
    ProjectsCreateProjectResource,
    ProjectsSetProjectTaskStatus,
    ProjectsMoveProjectResource,
    ProjectsDeleteProjectResource,
    ProjectsCreateProjectTaskResource,
    ProjectsGetProjectTasksResource,
    ProjectsGetEmployeeTaskResource,
    ProjectsGetAllEmployeeTasksResource,
    ProjectsGetTaskAttachmentsResource,
    ProjectsGetTaskCommentsResource,
    ProjectsSetProjectStatus,
    ProjectsCreateProjectTaskTagResource,
)
from server.apps.apis.providers import GetProvidersResource
from server.apps.apis.products import EditProductResource
from server.apps.apis.orders import GetProviderOrdersListResource, GetCompanyOrdersListResource
from server.apps.apis.customers import GetCustomersResource



def init_rest_api(app):
    # This function is connected to app

    Api.error_router = lambda self, hnd, e: hnd(e)
    api = Api(app)

    # init_api_errorhandlers(api)

    api.add_resource(CheckingApiWorking, "/api/api")

    api.add_resource(LoginResource, "/api/login")
    api.add_resource(SignupResource, "/api/signup")

    api.add_resource(SendEmailVerificationCode, "/api/verification/email/send")
    api.add_resource(ConfirmEmailVerificationCode, "/api/verification/email/verify")

    api.add_resource(NavbarResource, "/api/navbar/<int:employee_id>")
    api.add_resource(RefreshResource, "/api/refresh")
    api.add_resource(WhoAmIResource, "/api/whoami")

    api.add_resource(ProfileEditResource, "/api/edit/profile")
    api.add_resource(ProfileUpdateStatusResource, "/api/profile/updateStatus")

    api.add_resource(SearchWorkersResource, "/api/search/workers")

    api.add_resource(CreateCompanyResource, "/api/create/company")
    api.add_resource(
        HierarchyEmployeesOwnersResource, "/api/hierarchy/owners/<int:company_id>"
    )
    api.add_resource(
        HierarchyEmployeesResource,
        "/api/hierarchy/employees/<int:company_id>/<int:employee_id>",
    )
    api.add_resource(
        HierarchyEmployeesLeadersResource,
        "/api/hierarchy/leaders/<int:company_id>/<int:employee_id>",
    )
    api.add_resource(
        HierarchyGetALeaderResource,
        "/api/hierarchy/aleader/<int:company_id>/<int:employee_id>",
    )

    api.add_resource(
        MovingWorkerResource,
        "/api/hierarchy/moving/<int:company_id>/<int:move_worker_id>",
    )
    api.add_resource(FireWorkerResource, "/api/hierarchy/fire")
    api.add_resource(
        HierarchyHireEmployeeInvitationSendResource,
        "/api/hierarchy/hire/invitation/send",
    )
    api.add_resource(
        HierarchyHireEmployeeInvitationConfirmResource,
        "/api/hierarchy/hire/invitation/confirm",
    )

    api.add_resource(CreateTagResource, "/api/company/<int:company_id>/tags/create")

    api.add_resource(ChatListResource, "/api/company/<int:company_id>/chats")
    api.add_resource(ChatMessageResource, "/api/chats/<int:chat_id>/messages")
    api.add_resource(LiveChatResource, "/api/chats/<int:chat_id>/live")
    api.add_resource(GetChatInfoResource, "/api/chats/<int:chat_id>")
    
    # api.add_resource(ChatGroupCreateResource, "/api/company/<int:company_id>/chats/group/create")
    api.add_resource(ChatGroupCreateResource, "/api/chats/group/create")
    api.add_resource(ChatSendMessageResource, "/api/chats/send/message")
    # api.add_resource(ChatMessageResource, '/api/chats/messages/<int:chat_id>')
    api.add_resource(ChatReadMessageResource, "/api/chats/messages/<int:message_id>/read")
    api.add_resource(
        ChatDeleteMessageResource, "/api/chats/messages/<int:message_id>/delete"
    )
    api.add_resource(
        ForwardMessageResource, "/api/chats/messages/<int:message_id>/forward"
    )
    api.add_resource(
        ChatEditMessageResource, "/api/chats/message/<int:message_id>/edit"
    )
    # api.add_resource(ChatReplyResource, "/api/chats/reply/message")
    # api.add_resource(ForwardMessageResource, "/api/chats/forward/message")
    api.add_resource(PinMessageResource, "/api/chats/message/<int:message_id>/pin")
    api.add_resource(ChatGetMessageResource, "/api/chats/message/<int:message_id>")

    api.add_resource(ChatStatusResource, "/api/chats/<int:chat_id>/status")
    
    api.add_resource(ProjectsCreateProjectResource, '/api/company/<int:company_id>/projects/create')
    api.add_resource(ProjectsSetProjectStatus, "/api/projects/<int:project_id>/status")
    api.add_resource(ProjectsMoveProjectResource, '/api/projects/<int:project_id>/stage')
    api.add_resource(ProjectsDeleteProjectResource, '/api/projects/<int:project_id>/delete')
    api.add_resource(ProjectsCreateProjectTaskResource, "/api/projects/<int:project_id>/tasks/create")
    api.add_resource(ProjectsCreateProjectTaskTagResource, "/api/projects/tasks/<int:task_id>/tags/create")
    api.add_resource(ProjectsSetProjectTaskStatus, "/api/projects/tasks/<int:task_id>/status")
    api.add_resource(ProjectsGetProjectTasksResource, "/api/projects/<int:project_id>/tasks")
    api.add_resource(ProjectsGetEmployeeTaskResource, "/api/projects/tasks/<int:task_id>")
    api.add_resource(ProjectsGetAllEmployeeTasksResource, "/api/company/<int:company_id>/projects/tasks")
    api.add_resource(ProjectsGetTaskAttachmentsResource, "/api/projects/tasks/<int:task_id>/attachments")
    api.add_resource(ProjectsGetTaskCommentsResource, "/api/projects/tasks/<int:task_id>/comments")

    api.add_resource(GetProvidersResource, "/api/providers/company/<int:company_id>")
    
    api.add_resource(EditProductResource, "/api/products/<int:product_id>/edit")
    
    api.add_resource(GetCompanyOrdersListResource, "/api/company/<int:company_id>/orders")
    api.add_resource(GetProviderOrdersListResource, "/api/providers/<int:provider_id>/orders")

    api.add_resource(GetCustomersResource, "/api/company/<int:company_id>/customers")

    # When documentation of API is needed, we will uncomment these lines:

    # from apispec import APISpec
    # from apispec.ext.marshmallow import MarshmallowPlugin
    # from flask_apispec.extension import FlaskApiSpec

    # app.config.update({
    #     'APISPEC_SPEC': APISpec(
    #         title='API Documentation',
    #         version='v1',
    #         plugins=[MarshmallowPlugin()],
    #         openapi_version='2.0.0'
    #     ),
    #     'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    #     'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
    # })
    # docs = FlaskApiSpec(app)

    # docs.register(LoginResource)
    # docs.register(SignUpResource)
    # docs.register(RefreshResource)
