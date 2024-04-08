from .models import (User, Company, Employee, Chat, Navbar, Message, ChatMember, Project, ProjectTask,
					 ProjectTaskComment, Email, PhoneNumber, ProjectTaskAttachment, Provider,
					 ProviderType, Product, Order, OrderItem, Customer, ProductImage, ProjectTaskTag, ProjectTaskMember,
					 Tag, Pipeline, PipelineStage, Warehouse, WarehouseProduct
					 )
import random, datetime
from faker import Faker


def recreate_sample_test_data():
	fake = Faker()
	us = [
		User(first_name="Baby", email="baby", password="baby"),  # id = 1
		User(first_name="John", email="john6@mail.com", password="123123"),  # 2
		User(first_name="Brown", email="brown3434@mail.com", password="123456", ),  # 3
		User(first_name="George", email="george567@mail.com", password="121212"),  # 4
		User(first_name="Sarah", email="sarah23@mail.com", password="343434", ),  # 5
		User(first_name="Hela", email="hela@mail.com", password="343434", ),  # 6
		User(first_name="Marcus", email="marcus4567@mail.com", password="123123", ),  # 7
		User(first_name="Alex", email="alex3456@mail.com", password="alex123"),  # 8
		User(first_name="Tom", email="tom@mail.com", password="343434", ),  # 9
		User(first_name="Mila", email="mila@mail.com", password="123123"),  # 10
		User(first_name="Nolan", email="nolan23@mail.com", password="nolan123"),  # 11
		User(first_name="Fernando", email="fernando23@mail.com", password="fernando123"),  # 12
		User(first_name="Taylor", email="taylor23@mail.com", password="taylor123"),  # 13
		User(first_name="Joe", email="joe1212@mail.com", password="joe123"),  # 14
		User(first_name="Joe2", email="joe12123@mail.com", password="joe1231"),  # 15
		User(first_name="Joe3", email="joe121234@mail.com", password="joe12313"),  # 16
		User(first_name="Joe4", email="joe1212345@mail.com", password="joe123135"),  # 17
		User(first_name="Joe5", email="joe12123456@mail.com", password="joe1231356"),  # 18
	]
	for u in us:
		# u.is_active = True
		u.phone_number = random.randint(10000, 99999)
		u.confirmed_on = datetime.datetime.now(datetime.timezone.utc)
		u.insert()
	
	e1 = Email(email="amazon1@gmail.com")
	p1 = PhoneNumber(phone_number="123")
	e2 = Email(email="amazon2@gmail.com")
	p2 = PhoneNumber(phone_number="223")
	
	cs = [
		Company(name="Amazon1", name_in_law="Amazon1 LLC", owner_id=1, emails=[e1, ], phone_numbers=[p1, ]),  # emp = 1
		Company(name="Amazon2", name_in_law="Amazon2 LLC", owner_id=2, emails=[e2, ], phone_numbers=[p2, ]),  # emp = 2
	]
	for c in cs:
		c.insert()
	
	es = [
		Employee(user_id=1, company_id=1, position="deputy"),  # 1
		Employee(user_id=2, company_id=1, position="manager"),  # 2
		Employee(user_id=3, company_id=1, position="deputy"),  # 3
		Employee(user_id=4, company_id=1, position="manager"),  # 4
		Employee(user_id=5, company_id=1, position="designer", leader_id=4),  # 5
		Employee(user_id=6, company_id=1, position="designer", leader_id=4),  # 6
		Employee(user_id=7, company_id=1, position="designer", leader_id=4),  # 7
		Employee(user_id=8, company_id=1, position="leadA", leader_id=4),  # 8
		Employee(user_id=9, company_id=1, position="worker", leader_id=8),  # 9
		Employee(user_id=10, company_id=1, position="worker", leader_id=1),  # 10
		Employee(user_id=11, company_id=1, position="worker", leader_id=8),  # 11
		Employee(user_id=12, company_id=1, position="assistant", leader_id=9),  # 12
		Employee(user_id=13, company_id=1, position="assistant", leader_id=9),  # 13
		Employee(user_id=14, company_id=1, position="assistant", leader_id=9),  # 14
		Employee(user_id=15, company_id=1, position="worker2", leader_id=10),  # 15
		Employee(user_id=16, company_id=1, position="worker2", leader_id=1),  # 16
		Employee(user_id=17, company_id=1, position="worker3", leader_id=16),  # 17
		Employee(user_id=18, company_id=1, position="worker4", leader_id=17),  # 18
	]
	for e in es:
		e.insert()
	
	cs = [
		Chat(company_id=1, name="First Chat", is_group=False),  # 1
		Chat(company_id=1, name="Second Chat", is_group=False),  # 2
		Chat(company_id=1, name="Third Chat", is_group=False),  # 3
		Chat(company_id=1, name="Group Chat 1", owner_id=1, is_group=True),  # 4
		
		Chat(company_id=1, name="Fifth Chat", is_group=False),  # 5
		Chat(company_id=1, name="Sixth Chat", is_group=False),  # 6
		Chat(company_id=1, name="Seventh Chat", is_group=False),  # 7
		Chat(company_id=1, name="Group Chat 2", owner_id=1, is_group=True),  # 8
		
		Chat(company_id=1, name="Ninth Chat", is_group=False),  # 9
		Chat(company_id=1, name="Tenth Chat", is_group=False),  # 10
		Chat(company_id=1, name="Eleventh Chat", is_group=False),  # 11
		Chat(company_id=1, name="Group Chat 3", owner_id=1, is_group=True),  # 12
		
		Chat(company_id=1, name="Thirteenth Chat", is_group=False),  # 13
		Chat(company_id=1, name="Fourteenth Chat", is_group=False),  # 14
		Chat(company_id=1, name="Fifteenth Chat", is_group=False),  # 15
		Chat(company_id=1, name="Group Chat 4", owner_id=1, is_group=True),  # 16
	]
	for i in range(23):
		cs.append(Chat(company_id=random.choice([1, 2]), is_group=True, name=fake.name()))
	
	for c in cs:
		c.insert()
	
	cm = [
		ChatMember(chat_id=1, employee_id=1),
		ChatMember(chat_id=1, employee_id=2),  # P Chat 1, between employee 1 and employee 5
		
		ChatMember(chat_id=2, employee_id=1),
		ChatMember(chat_id=2, employee_id=3),
		
		ChatMember(chat_id=3, employee_id=1),
		ChatMember(chat_id=3, employee_id=4),
		
		ChatMember(chat_id=4, employee_id=1),  # G Chat 4, has these members
		ChatMember(chat_id=4, employee_id=2),
		ChatMember(chat_id=4, employee_id=3),
		ChatMember(chat_id=4, employee_id=4),
		ChatMember(chat_id=4, employee_id=5),
		ChatMember(chat_id=4, employee_id=6),
		ChatMember(chat_id=4, employee_id=7),
		ChatMember(chat_id=4, employee_id=8),
		ChatMember(chat_id=4, employee_id=9),
		ChatMember(chat_id=4, employee_id=10),
		ChatMember(chat_id=4, employee_id=11),
		
		ChatMember(chat_id=5, employee_id=1),
		ChatMember(chat_id=5, employee_id=5),  # P Chat 1, between employee 1 and employee 5
		
		ChatMember(chat_id=6, employee_id=1),
		ChatMember(chat_id=6, employee_id=6),
		
		ChatMember(chat_id=7, employee_id=1),
		ChatMember(chat_id=7, employee_id=7),
		
		ChatMember(chat_id=8, employee_id=1),  # G Chat 4, has these members
		ChatMember(chat_id=8, employee_id=2),
		ChatMember(chat_id=8, employee_id=3),
		ChatMember(chat_id=8, employee_id=4),
		ChatMember(chat_id=8, employee_id=5),
		ChatMember(chat_id=8, employee_id=6),
		ChatMember(chat_id=8, employee_id=7),
		ChatMember(chat_id=8, employee_id=8),
		ChatMember(chat_id=8, employee_id=9),
		ChatMember(chat_id=8, employee_id=10),
		ChatMember(chat_id=8, employee_id=11),
		
		ChatMember(chat_id=9, employee_id=1),
		ChatMember(chat_id=9, employee_id=8),  # P Chat 1, between employee 1 and employee 5
		
		ChatMember(chat_id=10, employee_id=1),
		ChatMember(chat_id=10, employee_id=9),
		
		ChatMember(chat_id=11, employee_id=1),
		ChatMember(chat_id=11, employee_id=10),
		
		ChatMember(chat_id=12, employee_id=1),  # G Chat 4, has these members
		ChatMember(chat_id=12, employee_id=2),
		ChatMember(chat_id=12, employee_id=3),
		ChatMember(chat_id=12, employee_id=4),
		ChatMember(chat_id=12, employee_id=5),
		ChatMember(chat_id=12, employee_id=6),
		ChatMember(chat_id=12, employee_id=7),
		ChatMember(chat_id=12, employee_id=8),
		ChatMember(chat_id=12, employee_id=9),
		ChatMember(chat_id=12, employee_id=10),
		ChatMember(chat_id=12, employee_id=11),
		
		ChatMember(chat_id=13, employee_id=1),
		ChatMember(chat_id=13, employee_id=11),  # P Chat 1, between employee 1 and employee 5
		
		ChatMember(chat_id=14, employee_id=1),
		ChatMember(chat_id=14, employee_id=12),
		
		ChatMember(chat_id=15, employee_id=1),
		ChatMember(chat_id=15, employee_id=13),
		
		ChatMember(chat_id=16, employee_id=1),  # G Chat 4, has these members
		ChatMember(chat_id=16, employee_id=2),
		ChatMember(chat_id=16, employee_id=3),
		ChatMember(chat_id=16, employee_id=4),
		ChatMember(chat_id=16, employee_id=5),
		ChatMember(chat_id=16, employee_id=6),
		ChatMember(chat_id=16, employee_id=7),
		ChatMember(chat_id=16, employee_id=8),
		ChatMember(chat_id=16, employee_id=9),
		ChatMember(chat_id=16, employee_id=10),
		ChatMember(chat_id=16, employee_id=11),
	]
	for i in cm:
		i.insert()
	
	Message.send_message(1, 1, "Hi Aziz! Are you there?", ),
	Message.send_message(1, 1, "Hello? Hello?!?", ),
	Message.send_message(1, 5, "Hi! I'm here! I'm here.", ),
	Message.send_message(1, 1, "Good. smiley", ),
	Message.send_message(1, 5, "What's up, Neira?", ),
	Message.send_message(1, 1, "Would you like to meet for a coffee?", ),
	Message.send_message(1, 1, "I'm working now, but I finish work at five. Maybe at 5.15?", ),
	Message.send_message(1, 5, "That's difficult for me. Can we meet 30 minutes later?", ),
	Message.send_message(1, 1, "OK. Where?", ),
	Message.send_message(1, 5, "The Blue Café is nice. I love the tea there. heart", ),
	Message.send_message(1, 1, "It's closed on Mondays. Let's go to Rocket Boy. It's new.", ),
	Message.send_message(1, 5, "Is it good?", ),
	Message.send_message(1, 1, "It's very good!", ),
	Message.send_message(1, 5, "Where is it? I don't know it.", ),
	Message.send_message(1, 1, "It's next to the school. See you there?", ),
	Message.send_message(1, 5, "See you there at 5.45!", ),
	Message.send_message(2, 1, "Hello :)"),
	Message.send_message(2, 6, "hi how r u ??"),
	Message.send_message(2, 1, "i am good, how ab urs?"),
	Message.send_message(2, 1, "I am texting you cuz I need some data ab company"),
	Message.send_message(2, 1, "and employees as well"),
	Message.send_message(1, 1, "Okay, here is your document you said yesterday",
						 files=[{"fileName": "pokemon", "file": "SGkgdGhlcmUgYWdhaW4=", "fileType": "docs", }, ], ),
	
	navbar = [
		Navbar(employee_id=1, hierarchy=True, employees=True, search_workers=True, chats=True, projects=True,
			   pipelines=True, my_tasks=True, statistics=True, purchases=True, providers=True, customers=True,
			   products=True, orders=True, sales=True, forecasts=True, finance=True, accounts=True, flow_and_funds=True,
			   mutual_settlements=True, warehouses=True, stock_lists=True, planned_shipments=True),
		
		Navbar(employee_id=2, hierarchy=True, employees=True, search_workers=False, chats=True, projects=True,
			   pipelines=True, my_tasks=True, statistics=True, purchases=True, providers=True, customers=True,
			   products=True, orders=True, sales=True, forecasts=False, finance=True, accounts=True,
			   flow_and_funds=True,
			   mutual_settlements=True, warehouses=True, stock_lists=True, planned_shipments=False),
		
		Navbar(employee_id=3, hierarchy=True, employees=True, search_workers=False, chats=True, projects=True,
			   pipelines=True, my_tasks=True, statistics=True, purchases=True, providers=True, customers=True,
			   products=True, orders=True, sales=False, forecasts=True, finance=True, accounts=True,
			   flow_and_funds=True,
			   mutual_settlements=True, warehouses=False, stock_lists=True, planned_shipments=True),
		
		Navbar(employee_id=4, hierarchy=True, employees=True, search_workers=True, chats=True, projects=True,
			   pipelines=True, my_tasks=True, statistics=True, purchases=True, providers=True, customers=True,
			   products=True, orders=True, sales=True, forecasts=False, finance=True, accounts=True,
			   flow_and_funds=True,
			   mutual_settlements=True, warehouses=False, stock_lists=True, planned_shipments=True),
		
		Navbar(employee_id=5, hierarchy=True, employees=True, search_workers=True, chats=True, projects=True,
			   pipelines=True, my_tasks=False, statistics=True, purchases=True, providers=True, customers=True,
			   products=True, orders=True, sales=False, forecasts=True, finance=True, accounts=True,
			   flow_and_funds=True,
			   mutual_settlements=True, warehouses=True, stock_lists=True, planned_shipments=False),
		
		Navbar(employee_id=6, hierarchy=True, employees=True, search_workers=True, chats=True, projects=True,
			   pipelines=True, my_tasks=True, statistics=True, purchases=True, providers=True, customers=True,
			   products=True, orders=True, sales=True, forecasts=True, finance=True, accounts=True, flow_and_funds=True,
			   mutual_settlements=True, warehouses=True, stock_lists=True, planned_shipments=True),
		
		Navbar(employee_id=7, hierarchy=True, employees=True, search_workers=True, chats=True, projects=True,
			   pipelines=True, my_tasks=False, statistics=True, purchases=True, providers=True, customers=True,
			   products=True, orders=True, sales=True, forecasts=False, finance=True, accounts=False,
			   flow_and_funds=True,
			   mutual_settlements=True, warehouses=True, stock_lists=True, planned_shipments=False),
		
		Navbar(employee_id=8, hierarchy=False, employees=False, search_workers=False, chats=False, projects=False,
			   pipelines=False, my_tasks=False, statistics=False, purchases=False, providers=False, customers=False,
			   products=True, orders=False, sales=True, forecasts=True, finance=True, accounts=True,
			   flow_and_funds=True,
			   mutual_settlements=False, warehouses=False, stock_lists=False, planned_shipments=False),
		
		Navbar(employee_id=9, hierarchy=True, employees=True, search_workers=True, chats=True, projects=True,
			   pipelines=True, my_tasks=True, statistics=False, purchases=True, providers=True, customers=True,
			   products=True, orders=True, sales=False, forecasts=True, finance=True, accounts=True,
			   flow_and_funds=True,
			   mutual_settlements=True, warehouses=True, stock_lists=False, planned_shipments=True),
		
		Navbar(employee_id=10, hierarchy=True, employees=True, search_workers=True, chats=True, projects=True,
			   pipelines=True, my_tasks=True, statistics=True, purchases=True, providers=True, customers=True,
			   products=True, orders=True, sales=False, forecasts=True, finance=True, accounts=True,
			   flow_and_funds=True,
			   mutual_settlements=True, warehouses=False, stock_lists=True, planned_shipments=True),
		
		Navbar(employee_id=11, hierarchy=True, employees=True, search_workers=True, chats=True, projects=True,
			   pipelines=True, my_tasks=True, statistics=True, purchases=True, providers=True, customers=True,
			   products=True, orders=True, sales=False, forecasts=True, finance=True, accounts=False,
			   flow_and_funds=True,
			   mutual_settlements=True, warehouses=True, stock_lists=True, planned_shipments=False),
		
		Navbar(employee_id=12, hierarchy=False, employees=True, search_workers=True, chats=True, projects=True,
			   pipelines=True, my_tasks=True, statistics=True, purchases=True, providers=True, customers=True,
			   products=True, orders=True, sales=False, forecasts=False, finance=True, accounts=True,
			   flow_and_funds=True,
			   mutual_settlements=True, warehouses=True, stock_lists=True, planned_shipments=True),
		
		Navbar(employee_id=13, hierarchy=True, employees=True, search_workers=True, chats=True, projects=True,
			   pipelines=True, my_tasks=True, statistics=True, purchases=True, providers=True, customers=True,
			   products=True, orders=True, sales=True, forecasts=True, finance=True, accounts=True, flow_and_funds=True,
			   mutual_settlements=True, warehouses=True, stock_lists=True, planned_shipments=True),
		
		Navbar(employee_id=14, hierarchy=True, employees=True, search_workers=False, chats=True, projects=True,
			   pipelines=False, my_tasks=False, statistics=True, purchases=True, providers=True, customers=True,
			   products=True, orders=False, sales=True, forecasts=True, finance=False, accounts=True,
			   flow_and_funds=True,
			   mutual_settlements=True, warehouses=True, stock_lists=False, planned_shipments=True),
		
		Navbar(employee_id=15, hierarchy=True, employees=True, search_workers=True, chats=True, projects=True,
			   pipelines=True, my_tasks=True, statistics=True, purchases=True, providers=True, customers=True,
			   products=True, orders=False, sales=True, forecasts=True, finance=True, accounts=True,
			   flow_and_funds=True,
			   mutual_settlements=True, warehouses=True, stock_lists=False, planned_shipments=True),
		
		Navbar(employee_id=16, hierarchy=True, employees=True, search_workers=True, chats=True, projects=True,
			   pipelines=True, my_tasks=True, statistics=True, purchases=False, providers=True, customers=True,
			   products=True, orders=True, sales=True, forecasts=False, finance=True, accounts=True,
			   flow_and_funds=True,
			   mutual_settlements=True, warehouses=True, stock_lists=True, planned_shipments=True),
		
		Navbar(employee_id=17, hierarchy=True, employees=True, search_workers=True, chats=True, projects=True,
			   pipelines=True, my_tasks=True, statistics=True, purchases=True, providers=True, customers=True,
			   products=True, orders=True, sales=True, forecasts=False, finance=True, accounts=True,
			   flow_and_funds=True,
			   mutual_settlements=True, warehouses=True, stock_lists=True, planned_shipments=True),
		
		Navbar(employee_id=18, hierarchy=True, employees=True, search_workers=True, chats=True, projects=True,
			   pipelines=True, my_tasks=False, statistics=False, purchases=True, providers=False, customers=True,
			   products=True, orders=True, sales=True, forecasts=True, finance=True, accounts=True, flow_and_funds=True,
			   mutual_settlements=True, warehouses=True, stock_lists=True, planned_shipments=True),
	
	]
	for nav in navbar:
		nav.insert()
	
	pl = [
		
		Pipeline(id=111, name="Pipeline1", company_id=1),
		Pipeline(id=222, name="Pipeline2", company_id=1),
		Pipeline(id=333, name="Pipeline3", company_id=1),
	
	]
	for i in pl:
		i.insert()
	
	pl_stages = [
		
		PipelineStage(id=111, pipeline_id=111, order_number=1, name="Project1"),
		PipelineStage(id=222, pipeline_id=222, order_number=1, name="Project2"),
		PipelineStage(id=333, pipeline_id=333, order_number=1, name="Project3"),
	
	]
	for i in pl_stages:
		i.insert()
	
	proj = [
		
		Project(id=111, stage_id=111, name="Project1", description="description1", counter_party=1, budget=25000,
				currency="USD", status="assigned"),
		Project(id=222, stage_id=222, name="Project2", description="description2", counter_party=1, budget=26000,
				currency="USD", status="succeeded"),
		Project(id=333, stage_id=333, name="Project3", description="description3", counter_party=1, budget=27000,
				currency="USD", status="active")]
	for i in proj:
		i.insert()
	
	proj_tsk = [
		
		ProjectTask(id=123, project_id=111, title="Task-1", description="This is task description", status="assigned",
					date="2023-01-01", due_date="2023-02-01"),
		ProjectTask(id=234, project_id=222, title="Task-2", description="This is task description", status="active",
					date="2023-01-01", due_date="2023-02-01"),
		ProjectTask(id=345, project_id=333, title="Task-3", description="This is task description", status="succeeded",
					date="2023-01-01", due_date="2023-02-01"),
		ProjectTask(id=456, project_id=111, title="Task-4", description="This is task description", status="failed",
					date="2023-01-01", due_date="2023-02-01"),
	]
	for i in proj_tsk:
		i.insert()
	
	tags = [
		
		Tag(company_id=1, text="This is tag 1", color="Red"),
		Tag(company_id=1, text="This is tag 2", color="Blue"),
		Tag(company_id=1, text="This is tag 3", color="Green"),
		Tag(company_id=1, text="This is tag 4", color="Yellow"),
		Tag(company_id=1, text="This is tag 5", color="Purple"),
		Tag(company_id=1, text="This is tag 6", color="Indigo"),
		Tag(company_id=1, text="This is tag 7", color="Brown"),
		Tag(company_id=1, text="This is tag 8", color="Grey"),
		Tag(company_id=1, text="This is tag 9", color="Mint"),
	
	]
	for i in tags:
		i.insert()
	
	proj_tsk_tags = [
		
		ProjectTaskTag(task_id=123, tag_id=1),
		ProjectTaskTag(task_id=123, tag_id=2),
		ProjectTaskTag(task_id=123, tag_id=3),
		ProjectTaskTag(task_id=123, tag_id=4),
		ProjectTaskTag(task_id=234, tag_id=5),
		ProjectTaskTag(task_id=234, tag_id=6),
		ProjectTaskTag(task_id=345, tag_id=7),
		ProjectTaskTag(task_id=456, tag_id=8),
	]
	for i in proj_tsk_tags:
		i.insert()
	
	tsk_mbr = [
		
		ProjectTaskMember(task_id=123, employee_id=1, date="2023-01-04"),
		ProjectTaskMember(task_id=234, employee_id=1, date="2023-02-03"),
		ProjectTaskMember(task_id=345, employee_id=1, date="2023-03-02"),
		ProjectTaskMember(task_id=456, employee_id=1, date="2023-04-01"),
		
		ProjectTaskMember(task_id=123, employee_id=2, date="2023-01-04"),
		ProjectTaskMember(task_id=234, employee_id=2, date="2023-02-03"),
		ProjectTaskMember(task_id=345, employee_id=2, date="2023-03-02"),
		ProjectTaskMember(task_id=456, employee_id=2, date="2023-04-01"),
		
		ProjectTaskMember(task_id=123, employee_id=3, date="2023-01-04"),
		ProjectTaskMember(task_id=234, employee_id=3, date="2023-02-03"),
		ProjectTaskMember(task_id=345, employee_id=3, date="2023-03-02"),
		ProjectTaskMember(task_id=456, employee_id=3, date="2023-04-01"),
	]
	for i in tsk_mbr:
		i.insert()
	
	proj_tsk_cmt = [
		
		ProjectTaskComment(task_id=123, employee_id=1, text="This is a comment", date="2023-02-01"),
		ProjectTaskComment(task_id=123, employee_id=1, text="This is a comment", date="2023-01-05"),
		ProjectTaskComment(task_id=123, employee_id=1, text="This is a comment", date="2023-01-05"),
		ProjectTaskComment(task_id=123, employee_id=1, text="This is a comment", date="2023-05-10"),
		ProjectTaskComment(task_id=234, employee_id=1, text="This is a comment", date="2023-02-01"),
		ProjectTaskComment(task_id=234, employee_id=1, text="This is a comment", date="2023-01-05"),
		ProjectTaskComment(task_id=234, employee_id=1, text="This is a comment", date="2023-01-05"),
		ProjectTaskComment(task_id=234, employee_id=1, text="This is a comment", date="2023-05-10"),
		ProjectTaskComment(task_id=345, employee_id=1, text="This is a comment", date="2023-02-01"),
		ProjectTaskComment(task_id=345, employee_id=1, text="This is a comment", date="2023-01-05"),
		ProjectTaskComment(task_id=345, employee_id=1, text="This is a comment", date="2023-01-05"),
		ProjectTaskComment(task_id=345, employee_id=1, text="This is a comment", date="2023-05-10"),
		ProjectTaskComment(task_id=456, employee_id=1, text="This is a comment", date="2023-02-01"),
		ProjectTaskComment(task_id=456, employee_id=1, text="This is a comment", date="2023-01-05"),
		ProjectTaskComment(task_id=456, employee_id=1, text="This is a comment", date="2023-01-05"),
		ProjectTaskComment(task_id=456, employee_id=1, text="This is a comment", date="2023-05-10"),
	]
	for i in proj_tsk_cmt:
		i.insert()
	
	proj_tsk_atc = [
		
		ProjectTaskAttachment(task_id=123, employee_id=1, file="This is an attachment", text="This is a text",
							  date="2023-02-01"),
		ProjectTaskAttachment(task_id=123, employee_id=1, file="This is an attachment", text="This is a text",
							  date="2023-02-01"),
		ProjectTaskAttachment(task_id=123, employee_id=1, file="This is an attachment", text="This is a text",
							  date="2023-02-01"),
		ProjectTaskAttachment(task_id=123, employee_id=1, file="This is an attachment", text="This is a text",
							  date="2023-02-01"),
		
		ProjectTaskAttachment(task_id=234, employee_id=1, file="This is an attachment", text="This is a text",
							  date="2023-02-01"),
		ProjectTaskAttachment(task_id=234, employee_id=1, file="This is an attachment", text="This is a text",
							  date="2023-02-01"),
		ProjectTaskAttachment(task_id=234, employee_id=1, file="This is an attachment", text="This is a text",
							  date="2023-02-01"),
		ProjectTaskAttachment(task_id=234, employee_id=1, file="This is an attachment", text="This is a text",
							  date="2023-02-01"),
		
		ProjectTaskAttachment(task_id=345, employee_id=1, file="This is an attachment", text="This is a text",
							  date="2023-02-01"),
		ProjectTaskAttachment(task_id=345, employee_id=1, file="This is an attachment", text="This is a text",
							  date="2023-02-01"),
		ProjectTaskAttachment(task_id=345, employee_id=1, file="This is an attachment", text="This is a text",
							  date="2023-02-01"),
		ProjectTaskAttachment(task_id=345, employee_id=1, file="This is an attachment", text="This is a text",
							  date="2023-02-01"),
		
		ProjectTaskAttachment(task_id=456, employee_id=1, file="This is an attachment", text="This is a text",
							  date="2023-02-01"),
		ProjectTaskAttachment(task_id=456, employee_id=1, file="This is an attachment", text="This is a text",
							  date="2023-02-01"),
		ProjectTaskAttachment(task_id=456, employee_id=1, file="This is an attachment", text="This is a text",
							  date="2023-02-01"),
		ProjectTaskAttachment(task_id=456, employee_id=1, file="This is an attachment", text="This is a text",
							  date="2023-02-01"),
	]
	for i in proj_tsk_atc:
		i.insert()
	
	prov = [
		Provider(counter_party=1, created="2023-01-01", last_deal_with="2023-01-01",
				 description="Provider Description 1", name="baby boy", avatar="Provider Avatar 1"),
		Provider(counter_party=1, created="2023-02-01", last_deal_with="2023-02-01",
				 description="Provider Description 2", name="baby guy", avatar="Provider Avatar 2"),
		Provider(counter_party=1, created="2023-03-01", last_deal_with="2023-03-01",
				 description="Provider Description 3", name="baby baby", avatar="Provider Avatar 3"),
		Provider(counter_party=1, created="2023-02-01", last_deal_with="2023-02-01",
				 description="Provider Description 2", name="john guy", avatar="Provider Avatar 2"),
		Provider(counter_party=1, created="2023-04-01", last_deal_with="2023-04-01",
				 description="Provider Description 4", name="good john", avatar="Provider Avatar 4"),
		Provider(company_id=1, counter_party=2, created="2023-04-01", last_deal_with="2023-04-01",
				 description="Provider Description 4", name="good baby", avatar="Provider Avatar 4"),
		Provider(company_id=1, counter_party=2, created="2023-05-01", last_deal_with="2023-05-01",
				 description="Provider Description 5", name="bad baby", avatar="Provider Avatar 5"),
		Provider(company_id=2, counter_party=1, created="2023-01-01", last_deal_with="2023-01-01",
				 description="Provider Description 1", name="john boy", avatar="Provider Avatar 1"),
		Provider(company_id=2, counter_party=1, created="2023-03-01", last_deal_with="2023-03-01",
				 description="Provider Description 3", name="john john", avatar="Provider Avatar 3"),
		Provider(company_id=2, counter_party=1, created="2023-05-01", last_deal_with="2023-05-01",
				 description="Provider Description 5", name="bad john", avatar="Provider Avatar 5")]
	for i in prov:
		i.insert()
	
	protp = [
		ProviderType(provider_id=1, type="type1"),
		ProviderType(provider_id=2, type="type2"),
		ProviderType(provider_id=3, type="type1"),
		ProviderType(provider_id=4, type="type2"),
		ProviderType(provider_id=5, type="type1"),
		
		ProviderType(provider_id=6, type="type2"),
		ProviderType(provider_id=7, type="type1"),
		ProviderType(provider_id=8, type="type2"),
		ProviderType(provider_id=9, type="type1"),
		ProviderType(provider_id=10, type="type2")]
	for i in protp:
		i.insert()
	
	wh = [
		Warehouse(company_id=1, coordinates="00:11:22:33:44:55"),
		Warehouse(company_id=1, coordinates="00:12:23:34:45:56"),
		Warehouse(company_id=2, coordinates="55:44:33:22:11:00"),
	]
	for w in wh:
		w.insert()
	
	prd = [
		Product(provider_id=1, avatar="Avatar", name="Shampoo", price=10, currency="USD", description="Dove Shampoo"),
		Product(provider_id=1, avatar="Avatar", name="Bread", price=5, currency="USD", description="Sliced Bread"),
		Product(company_id=1, avatar="Avatar", name="Cola", price=2.5, currency="USD", description="Can of soda"),
		Product(company_id=1, avatar="Avatar", name="Sugar", price=25, currency="USD", description="10lb Sugar"),
		Product(company_id=1, avatar="Avatar", name="Sugar", price=25, currency="USD", description="10lb Sugar"),
		Product(company_id=1, avatar="Avatar", name="Sugar", price=25, currency="USD", description="10lb Sugar"),
		Product(company_id=1, avatar="Avatar", name="Cola", price=2.5, currency="USD", description="Can of soda"),
		Product(provider_id=2, avatar="Avatar", name="Shampoo", price=10, currency="USD", description="Dove Shampoo"),
		Product(provider_id=2, avatar="Avatar", name="Bread", price=5, currency="USD", description="Sliced Bread"),
		Product(provider_id=3, avatar="Avatar", name="Shampoo", price=10, currency="USD", description="Dove Shampoo"),
		Product(provider_id=3, avatar="Avatar", name="Bread", price=5, currency="USD", description="Sliced Bread")]
	for i in prd:
		i.insert()
	
	prdImg = [
		ProductImage(image="image1", product_id=1),
		ProductImage(image="image2", product_id=1),
		ProductImage(image="image3", product_id=1),
		ProductImage(image="image4", product_id=1),
		ProductImage(image="image5", product_id=1),
		
		ProductImage(image="image1", product_id=5),
		ProductImage(image="image2", product_id=5),
		ProductImage(image="image3", product_id=5),
		ProductImage(image="image4", product_id=5),
		ProductImage(image="image5", product_id=5)]
	for i in prdImg:
		i.insert()
	
	wh = [
		WarehouseProduct(warehouse_id=1, product_id=1, product_quantity=11),
		WarehouseProduct(warehouse_id=1, product_id=2, product_quantity=11),
		WarehouseProduct(warehouse_id=1, product_id=3, product_quantity=11),
		WarehouseProduct(warehouse_id=1, product_id=4, product_quantity=11),
		WarehouseProduct(warehouse_id=1, product_id=5, product_quantity=11),
		WarehouseProduct(warehouse_id=1, product_id=6, product_quantity=11),
		WarehouseProduct(warehouse_id=1, product_id=7, product_quantity=11),
		WarehouseProduct(warehouse_id=1, product_id=8, product_quantity=11),
		WarehouseProduct(warehouse_id=1, product_id=9, product_quantity=11),
		WarehouseProduct(warehouse_id=1, product_id=10, product_quantity=11),
		WarehouseProduct(warehouse_id=1, product_id=11, product_quantity=11),
	]
	for w in wh:
		w.insert()
	
	orders = [
		Order(provider_id=1, company_id=1, status="pending", tracking_status="ordered"),
		Order(provider_id=1, company_id=1, status="paid", tracking_status="ordered"),
		Order(provider_id=1, company_id=1, status="paid", tracking_status="in_transit"),
		Order(provider_id=1, company_id=1, status="refunded", tracking_status="delivered"),
		Order(provider_id=2, company_id=1, status="pending", tracking_status="ordered"),
		Order(provider_id=2, company_id=1, status="paid", tracking_status="ordered"),
		Order(provider_id=2, company_id=1, status="accepted", tracking_status="in_transit"),
		Order(provider_id=3, company_id=1, status="refunded", tracking_status="delivered"),
		Order(provider_id=3, company_id=1, status="accepted", tracking_status="ordered"),
		Order(provider_id=3, company_id=1, status="paid", tracking_status="ordered"),
		Order(provider_id=3, company_id=1, status="cancelled", tracking_status="in_transit")
	]
	for i in orders:
		i.insert()
	
	odrItem = [
		OrderItem(product_id=1, order_id=1, product_quantity=2),
		OrderItem(product_id=2, order_id=2, product_quantity=3),
		OrderItem(product_id=3, order_id=1, product_quantity=5),
		OrderItem(product_id=4, order_id=2, product_quantity=7),
		OrderItem(product_id=1, order_id=1, product_quantity=1),
		OrderItem(product_id=2, order_id=2, product_quantity=3),
		OrderItem(product_id=3, order_id=1, product_quantity=4),
		OrderItem(product_id=4, order_id=2, product_quantity=5),
		OrderItem(product_id=1, order_id=1, product_quantity=3),
		OrderItem(product_id=2, order_id=2, product_quantity=1),
		OrderItem(product_id=3, order_id=1, product_quantity=2)
	]
	for i in odrItem:
		i.insert()
	
	cust = [
		Customer(company_id=1, first_name="baby", last_name="boy", phone_number=1234567890,
				 email="baby@mail.com"),
		Customer(company_id=1, first_name="baby", last_name="guy", phone_number=1234567891,
				 email="guy@mail.com"),
		Customer(company_id=1, first_name="man", last_name="baby", phone_number=1234567892,
				 email="man@mail.com"),
		Customer(company_id=1, first_name="john", last_name="doe", phone_number=1234567893,
				 email="john@mail.com"),
		Customer(company_id=1, first_name="doe", last_name="deo", phone_number=1234567894,
				 email="deo@mail.com"),
		Customer(company_id=1, first_name="doe", last_name="john", phone_number=1234567895,
				 email="john2@mail.com"),
		Customer(company_id=1, first_name="anon", last_name="boy", phone_number=1234567896,
				 email="anon@mail.com"),
		Customer(company_id=1, first_name="misty", last_name="girl", phone_number=1234567897,
				 email="misty@mail.com"),
		Customer(company_id=1, first_name="isabella", last_name="gayer", phone_number=1234567898,
				 email="isabella@mail.com"),
		Customer(company_id=1, first_name="bron", last_name="gayer", phone_number=1234567899,
				 email="bron@mail.com"),
		Customer(company_id=1, first_name="lola", last_name="doe", phone_number=12345678910,
				 email="lola@mail.com")
	]
	for i in cust:
		i.insert()
