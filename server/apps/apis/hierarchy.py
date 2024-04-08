from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager, create_refresh_token, current_user
from flask_restful import Resource
from ..api import api_response, api_abort
from server.db.models import Company, Employee, User, Navbar, EmployeeLeader, CompanyInvitation
from flask import abort, request, current_app
from server.mailserver import FlaskMailServer
from ...tools.assists import set_attributes
import secrets


class MovingWorkerResource(Resource):
    @jwt_required()
    def put(self, company_id, move_worker_id):

        data = request.get_json()
        search_request = data.get('search_request')

        # stores downline
        downlines = []

        # gets the data of the employee that is signed in
        employee_signed_in = Employee.query.filter_by(user_id=current_user.id, company_id=company_id).first()

        move_employee_direct_leader_id = Employee.query.filter_by(id=move_worker_id).first().leader_id

        employee_downline = EmployeeLeader.query.filter(EmployeeLeader.leader_id==employee_signed_in.id, EmployeeLeader.employee_id != move_worker_id, EmployeeLeader.employee_id != move_employee_direct_leader_id).all()

        if not employee_downline or employee_downline == []:
            return api_response([], "you do not have any downline available for moving")
        
        downline_data = []

        response = []

        for id in range(0, len(employee_downline)):
            search_request = search_request.lower()

            employee = Employee.query.filter(Employee.id==employee_downline[id].employee_id).first()
            user = User.query.filter(User.id == employee.user_id).first()
            if user is not None:
                search_result = (search_request in user.first_name.lower()) or (search_request in user.last_name.lower()) or (search_request in employee.position.lower())
            else:
                search_result = search_request in employee.position.lower()

            if search_request == '':
                search_result = True

            if search_result:
                response.append(employee.get_all(True))


        return api_response(response, "Got list of the employees for moving.")

    @jwt_required()
    def patch(self, company_id, move_worker_id):
        data = request.get_json()
        new_leader_id = data.get('new_leader_id')
        move_with_team = data.get("move_with_team")
        # check if the data from the json file was collected successfully
        if not move_worker_id or not new_leader_id:
            return api_response("Please make sure you have the right key.")

        # if it is an employee not the owner of the company that signed in, so it spits only the employees downline
        employee_signed_in = Employee.query.filter(Employee.user_id==current_user.id, Employee.company_id==company_id).first()
        employee_to_be_moved  = Employee.query.filter(Employee.company_id == company_id, Employee.id == move_worker_id).first()

        # handles if employee data for a company does not exist
        if not employee_to_be_moved: abort(404, 'Employee can not be moved')

        # a boolean value that handles if employee is to be moved with team and if employee has no team so as not to leave a placeholder
        if move_with_team:

            if EmployeeLeader.query.filter(EmployeeLeader.leader_id == move_worker_id, EmployeeLeader.employee_id == new_leader_id).first() is not None:
                EmployeeLeader.query.filter(EmployeeLeader.leader_id == move_worker_id, EmployeeLeader.employee_id == new_leader_id).first().delete()
                
                employee_to_be_moved_team = EmployeeLeader.query.filter(EmployeeLeader.leader_id == move_worker_id).all()
                for employee_to_be_moved_team_member in employee_to_be_moved_team:
                    #if there is an employee in the moved worker team who is a leader of the new leader
                    if EmployeeLeader.query.filter(EmployeeLeader.leader_id == employee_to_be_moved_team_member.employee_id, EmployeeLeader.employee_id == new_leader_id).first() is not None:
                        EmployeeLeader.query.filter(EmployeeLeader.leader_id == employee_to_be_moved_team_member.employee_id, EmployeeLeader.employee_id == new_leader_id).first().delete()

            employee_to_be_moved_team = EmployeeLeader.query.filter(EmployeeLeader.leader_id == move_worker_id).all()
            employee_to_be_moved_leaders = EmployeeLeader.query.filter(EmployeeLeader.employee_id == move_worker_id).all()
            new_leader_leaders = EmployeeLeader.query.filter(EmployeeLeader.employee_id==new_leader_id).all()

            print('!!!!!!!!!!')
            print('!!!!!!!!!!')
            print('!!!!!!!!!!')
            print(employee_to_be_moved_team)
            print(employee_to_be_moved_leaders)
            print(new_leader_leaders)
            print('!!!!!!!!!!')
            print('!!!!!!!!!!')
            print('!!!!!!!!!!')

            for employee_to_be_moved_leader in employee_to_be_moved_leaders:
                if EmployeeLeader.query.filter_by(leader_id=employee_to_be_moved_leader.leader_id, employee_id=new_leader_id).first() is None:
                    print(employee_to_be_moved_team)
                    for employee_to_be_moved_team_member in employee_to_be_moved_team:
                        print(EmployeeLeader.query.filter_by(leader_id=employee_to_be_moved_leader.leader_id, employee_id=employee_to_be_moved_team_member.employee_id).first())
                        print(employee_to_be_moved_leader.leader_id)
                        print(employee_to_be_moved_team_member.employee_id)
                        EmployeeLeader.query.filter_by(leader_id=employee_to_be_moved_leader.leader_id, employee_id=employee_to_be_moved_team_member.employee_id).first().delete()
                        print('deleted')
                    employee_to_be_moved_leader.delete()
                    print('deleted')

            for new_leader_leader in new_leader_leaders:
                if EmployeeLeader.query.filter_by(leader_id=new_leader_leader.leader_id, employee_id=move_worker_id).first() is None:
                    for employee_to_be_moved_team_member in employee_to_be_moved_team:
                        EmployeeLeader(
                            leader_id=new_leader_leader.leader_id,
                            employee_id=employee_to_be_moved_team_member.employee_id
                        ).insert()
                    EmployeeLeader(
                        leader_id=new_leader_leader.leader_id,
                        employee_id=move_worker_id
                    ).insert()

            for employee_to_be_moved_team_member in employee_to_be_moved_team:
                if EmployeeLeader.query.filter(EmployeeLeader.leader_id == new_leader_id, EmployeeLeader.employee_id == employee_to_be_moved_team_member.employee_id).first() is None:
                    EmployeeLeader(
                        leader_id=new_leader_id,
                        employee_id=employee_to_be_moved_team_member.employee_id
                    ).insert()

            EmployeeLeader(
                leader_id=new_leader_id,
                employee_id=move_worker_id
            ).insert()


            if EmployeeLeader.query.filter(EmployeeLeader.leader_id == move_worker_id, EmployeeLeader.employee_id == new_leader_id).first() is not None:
                new_leader_employee = Employee.query.filter_by(id=new_leader_id).first()
                new_leader_employees_list = Employee.query.filter_by(leader_id=new_leader_id).all()

                for new_leader_employee_member in new_leader_employees_list:
                    new_leader_employee_member.leader_id = move_worker_id
                    new_leader_employee_member.update()
                    
                new_leader_employee.leader_id = employee_to_be_moved.leader_id
                new_leader_employee.update()

                EmployeeLeader.query.filter(EmployeeLeader.leader_id == move_worker_id, EmployeeLeader.employee_id == new_leader_id).first().delete()

            employee_to_be_moved.leader_id = new_leader_id
            employee_to_be_moved.update()

        else:

            # creates a new row on the employee table for the employee to be moved and assigns him to the new leader if not moving with team 
            _employee = Employee(
                user_id=move_worker_id,
                company_id=employee_to_be_moved.company_id,
                position=employee_to_be_moved.position,
                leader_id=new_leader_id
            )
            _employee.insert()

            # leaves a placeholder that stays in the team lead position(employee to be moved)
            employee_to_be_moved.user_id = None
            employee_to_be_moved.update()

        return api_response([])



class HierarchyEmployeesResource(Resource):
    @jwt_required()
    def get(self, company_id, employee_id):

        company : Company = Company.query.get(company_id)
        if not company: abort(404, 'There is no such company')
        current_emp = Employee.query.filter_by(company_id=company.id, user_id=current_user.id).first()
        
        _employees  = Employee.query.filter_by(company_id=company.id, leader_id=employee_id) if employee_id != '0' else Employee.query.filter_by(company_id=company.id, leader_id=None)
        if not _employees.count():
            return api_response([], "Got list of the employees")


        for i in _employees:
            get_leaders = [ii.leader_id for ii in EmployeeLeader.query.filter_by(employee_id=i.id).all()]
            try:
                get_leaders.index(current_emp.id)
                i.is_in_team = 1
            except ValueError:
                i.is_in_team = 0
        
        # def check_in_team(empl):
        #     empl.is_in_team = False
        #     if not empl.leader_id or empl.leader_id == current_emp.id:
        #         empl.is_in_team = True
        #     else:
        #         nextcheck = Employee.query.get(empl.leader_id)
        #         while nextcheck.leader_id:
        #             if nextcheck.leader_id != current_emp.id:
        #                 nextcheck = Employee.query.get(nextcheck.leader_id)
        #                 continue
        #             empl.is_in_team = True
        #             break
        
        # for i in _employees:
        #     check_in_team(i)
        #     print(i)

        return api_response([employee.get_all(True) | {'is_in_team': True if i.is_in_team == 1 else False} for employee in _employees], "Got list of the employees")



class HierarchyEmployeesOwnersResource(Resource):
    @jwt_required()
    def get(self, company_id):
        _employees  =  Employee.query.filter_by(company_id=company_id, leader_id=None)
        if not _employees.count(): abort(404, 'No owners or such company')
        return api_response([employee.get_all(True) for employee in _employees], "Got list of the owners")


class HierarchyEmployeesLeadersResource(Resource):
    @jwt_required()
    def get(self, company_id, employee_id):
        
        employee = Employee.query.get(employee_id)
        if not employee:
            abort(404, "Employee not found")
        leader_id = employee.leader_id
        if not leader_id:
            return api_response([], "No leaders of employee")
        leader = Employee.query.get(leader_id)
        if not leader:
            abort(404, "Leader not found")
        leader_leader_id = leader.leader_id
        if not leader_leader_id:
            return api_response([i.get_all(True) for i in Employee.query.filter_by(company_id=company_id, leader_id=None)])
        parent_leader = Employee.query.get(leader_leader_id)
        if not parent_leader:
            abort(404, "Parent Leader not found")
        
        return api_response([i.get_all(True) for i in Employee.query.filter_by(company_id=company_id, leader_id=parent_leader.id)])



class HierarchyHireEmployeeInvitationSendResource(Resource):
    @jwt_required()
    def post(self):
        
            data = request.get_json()
            
            employee_data = data.get('employee')
            navbar_data = data.get('navbar')
            email = data.get('email')
            link : str = data.get('link')

            if not all((employee_data, navbar_data, email, link)):
              abort(400, "Some fields missing")

            new_Employee = Employee()
            set_attributes(new_Employee, employee_data)
            new_Employee.insert()
            
            new_Navbar = Navbar()
            set_attributes(new_Navbar, navbar_data)
            new_Navbar.employee_id = new_Employee.id
            new_Navbar.insert()
            
            new_Invitation = CompanyInvitation(email=email, employee_id=new_Employee.id, token=secrets.token_hex(32))
            new_Invitation.insert()


            link = link.format(TOKEN=new_Invitation.token)

            # "email"
            # "link"
            # "employee": {
            #     "work_hour": 6.5,
            #     "wage": 35,
            #     "position": "QA",
            #     "leader_id": 4,
            #     "company_id": 1
            # } 
            # "navbar": {
            #     "employee": false,
            #     "projects": true,
            #     "sales": true,
            #     "purchase": true,
            #     " ": true
            # }


            mail = FlaskMailServer(current_app)
            mail.send_email_invitation_to_company([email], link)

            return api_response(description="Email sent and Employee added", status_code=201)



class HierarchyHireEmployeeInvitationConfirmResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        token = data.get('token')
        
        invitation : CompanyInvitation = CompanyInvitation.query.filter_by(token=token).first()
        if not invitation:
            abort(400, 'No such invitation token')
        if not invitation.is_valid():
            invitation.delete()
            abort(401, 'Token expired or already used')
        
        if current_user.email != invitation.email:
            abort(402, 'This is not for current user')

        employee = Employee.query.get(invitation.employee_id)
        employee.user_id = current_user.id; employee.update()


        return api_response(employee.get_all(True), 'Token used successfully and employee updated')


class FireWorkerResource(Resource):
    @jwt_required()
    def delete(self):
        data = request.get_json()
        employee_id = data.get('employee_id')

        employee: Employee = Employee.query.get(employee_id)
        if not employee: abort(404, 'There is no such employee')

        if not employee.user_id:
            navbar: Navbar = Navbar.query.filter_by(employee_id=employee_id).first()
            employees_list = EmployeeLeader.query.filter_by(leader_id=employee_id).all()
            for empl in employees_list:
                empl.delete()
            leaders_list = EmployeeLeader.query.filter_by(employee_id=employee_id).all()
            for leader in leaders_list:
                leader.delete()
            if navbar:
                navbar.delete()
            employee.delete()# don't clean navbar data and other related data

            employees = Employee.query.filter_by(leader_id=employee_id).all()
            if employees:
                for empl in employees:
                    empl.leader_id = employee.leader_id
                    empl.update()
            return api_response(employee.get_all(True),'Employee was totally fired')
        
        employee.user_id = None
        employee.update()
        return api_response(employee.get_all(True), 'Employee was fired')


class HierarchyGetALeaderResource(Resource):
    
    def get(self, company_id, employee_id):
        employee = Employee.query.get(employee_id)
        if not employee: abort(404, "No such employee")
        leader_id = employee.leader_id
        if not leader_id:
            return api_response(None, "No leaders of employee")
        leader = Employee.query.get(leader_id)
        if not leader: 
            return api_response(None, "No leaders of employee")

        return api_response(
            leader.get_all(True)
        )


