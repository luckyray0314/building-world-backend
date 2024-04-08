# Project Tasks API

#### _Please read General API Information first_

## **1. Create a new Project**

```http
POST /api/company/company_id/projects/create
```

* Authorization: Access token

**Parameters:**

| Name          | Type | Required | Values(default) | Description                  |
|---------------|------|----------|-----------------|------------------------------|
| company_id    | int  | YES      |                 | Company id of the user       |
| stage_id      | int  | YES      |                 | Stage Id of the pipeline     |
| name          | str  | YES      |                 | Name of the project          |
| description   | str  | NO       |                 | Project Description          |
| counter_party | str  | YES      |                 | Counter party of the project |
| budget        | str  | YES      |                 | Project budget               |

**Returns:** ShortProjectType

**Example:**

```http
POST /api/company/1/projects/create
```

* Body:

```json
{
  "stage_id": 111,
  "name": "New Project Created",
  "description": "Project Description",
  "counter_party": "1",
  "budget": 25000
}
```

* Response:

```json
{
  "ok": true,
  "description": "Project created",
  "result": {
    "stage_id": 111,
    "counter_party": "1",
    "name": "New Project Created",
    "description": "Project Description",
    "budget": 25000.0,
    "status": "active"
  }
}
```

## **2. Change the status of a Project**

```http
POST /api/projects/project_id/status
```

* Authorization: Access token

**Parameters:**

| Name       | Type | Required | Values(default) | Description               |
|------------|------|----------|-----------------|---------------------------|
| project_id | int  | YES      |                 | Id of the project         |
| status     | str  | YES      |                 | New status of the project |

**Returns:** ShortProjectType

**Example:**

```http
POST /api/projects/111/status
```

* Body:

```json
{
  "status": "Complete"
}
```

* Response:

```json
{
  "ok": true,
  "description": "Project status updated",
  "result": {
    "stage_id": 111,
    "counter_party": "1",
    "name": "Project1",
    "description": "description1",
    "budget": 25000.0,
    "status": "Complete"
  }
}
```

## **3. Change the stage of a Project**

```http
POST /api/projects/project_id/stage
```

* Authorization: Access token

**Parameters:**

| Name       | Type | Required | Values(default) | Description                 |
|------------|------|----------|-----------------|-----------------------------|
| project_id | int  | YES      |                 | Id of the project           |
| stage_id   | int  | YES      |                 | New stage id of the project |

**Returns:** ShortProjectType

**Example:**

```http
POST /api/projects/111/stage
```

* Body:

```json
{
    "stage_id": 111
}
```

* Response:

```json
{
    "ok": true,
    "description": "Project moved to new pipeline",
    "result": {
        "stage_id": 111,
        "counter_party": "1",
        "name": "Project1",
        "description": "description1",
        "budget": 25000.0,
        "status": "Complete"
    }
}
```

## **4. Delete a Project**

```http
POST /api/projects/project_id/delete
```

* Authorization: Access token

**Parameters:**

| Name       | Type | Required | Values(default) | Description       |
|------------|------|----------|-----------------|-------------------|
| project_id | int  | YES      |                 | id of the project |

**Returns:** null

**Example:**

```http
POST /api/projects/111/delete
```

* Body:

```json

```

* Response:

```json
{
    "ok": true,
    "description": "Project deleted",
    "result": null
}
```

## **5. Create a new Project Task**

```http
POST /api/projects/project_id/tasks/create
```

* Authorization: Access token

**Parameters:**

| Name        | Type | Required | Values(default) | Description          |
|-------------|------|----------|-----------------|----------------------|
| project_id  | int  | YES      |                 | Id of the project    |
| title       | str  | YES      |                 | Title of the task    |
| description | str  | NO       |                 | Task Description     |
| due_date    | str  | NO       |                 | Due date of the task |

**Returns:** ShortProjectTaskType

**Example:**

```http
POST /api/projects/111/tasks/create
```

* Body:

```json
{
    "title": "New Task",
    "description": "Task Description",
    "due_date": "2025-01-02"
}
```

* Response:

```json
{
    "ok": true,
    "description": "Task created",
    "result": {
        "title": "New Task",
        "description": "Task Description",
        "is_open": true,
        "is_in_work": false,
        "is_done": false,
        "date": 1683715399.175498,
        "due_date": 1735758000.0
    }
}
```

## **6. Create a new Task Tag**

```http
POST /api/projects/tasks/task_id/tags/create
```

* Authorization: Access token

**Parameters:**

| Name    | Type | Required | Values(default) | Description                                       |
|---------|------|----------|-----------------|---------------------------------------------------|
| task_id | int  | YES      |                 | Id of the task for which the tag is being created |
| tag_id  | str  | YES      |                 | Id of the new tag                                 |

**Returns:** ProjectTaskTagType

**Example:**

```http
POST /api/projects/tasks/123/tags/create
```

* Body:

```json
{
    "tag_id": 1
}
```

* Response:

```json
{
    "ok": true,
    "description": "Tag created",
    "result": {
        "id": 9,
        "tag_id": 1,
        "tag_color": "Red",
        "tag_text": "This is tag 1",
        "date": 1684663607.062717
    }
}
```

## **7. Change the status of a Project Task**

```http
POST /api/projects/tasks/task_id/status
```

* Authorization: Access token

**Parameters:**

| Name    | Type | Required | Values(default) | Description            |
|---------|------|----------|-----------------|------------------------|
| task_id | int  | YES      |                 | Id of the task         |
| status  | str  | YES      |                 | New status of the task |

**Returns:** ShortProjectTaskType

**Example:**

```http
POST /api/projects/tasks/123/status
```

* Body:

```json
{
    "status": "done"
}
```

* Response:

```json
{
    "ok": true,
    "description": "Task status updated",
    "result": {
        "title": "Task-1",
        "description": "This is task description",
        "is_open": false,
        "is_in_work": false,
        "is_done": true,
        "date": 1672513200.0,
        "due_date": 1675191600.0
    }
}
```

## **8. Get all tasks of a Project**

```http
POST /api/projects/project_id/tasks
```

* Authorization: Access token

**Parameters:**

| Name       | Type | Required | Values(default) | Description       |
|------------|------|----------|-----------------|-------------------|
| project_id | int  | YES      |                 | Id of the project |

**Returns:** List of ShortProjectTaskType | ShortProjectTaskTagType | ShortProjectTaskMemberType

**Example:**

```http
POST /api/projects/111/tasks
```

* Body:

```json

```

* Response:

```json
{
    "ok": true,
    "description": "Got Project Task(s)",
    "result": {
        "assigned": [
            {
                "id": 123,
                "project_id": 111,
                "title": "Task-1",
                "description": "This is task description",
                "status": "assigned",
                "date": 1672513200.0,
                "due_date": 1675191600.0,
                "task_tags": [
                    {
                        "employee_id": 1,
                        "text": "This is a tag",
                        "tag_color": "Red",
                        "date": 1675191600.0
                    }
                ],
                "task_members": [
                    {
                        "id": 1,
                        "task_id": 123,
                        "employee_id": 1
                    },
                    {
                        "id": 5,
                        "task_id": 123,
                        "employee_id": 2
                    },
                    {
                        "id": 9,
                        "task_id": 123,
                        "employee_id": 3
                    }
                ]
            }
        ],
        "active": [],
        "succeeded": [],
        "failed": [
            {
                "id": 456,
                "project_id": 111,
                "title": "Task-4",
                "description": "This is task description",
                "status": "failed",
                "date": 1672513200.0,
                "due_date": 1675191600.0,
                "task_tags": [
                    {
                        "employee_id": 1,
                        "text": "This is a tag",
                        "tag_color": "Yellow",
                        "date": 1675191600.0
                    }
                ],
                "task_members": [
                    {
                        "id": 4,
                        "task_id": 456,
                        "employee_id": 1
                    },
                    {
                        "id": 8,
                        "task_id": 456,
                        "employee_id": 2
                    },
                    {
                        "id": 12,
                        "task_id": 456,
                        "employee_id": 3
                    }
                ]
            }
        ]
    }
}
```

## **9. Get a single tasks of an employee**

```http
POST /api/projects/tasks/task_id
```

* Authorization: Access token

**Parameters:**

| Name    | Type | Required | Values(default) | Description            |
|---------|------|----------|-----------------|------------------------|
| task_id | int  | YES      |                 | Id of the task         |

**Returns:** ShortProjectTaskType | ShortProjectTaskTagType | ShortProjectTaskMemberType

**Example:**

```http
POST /api/projects/tasks/234
```

* Body:

```json

```

* Response:

```json
{
    "ok": true,
    "description": "Got Employee Task",
    "result": {
        "id": 234,
        "project_id": 222,
        "title": "Task-2",
        "description": "This is task description",
        "is_open": true,
        "is_in_work": false,
        "is_done": false,
        "date": 1672513200.0,
        "due_date": 1675191600.0,
        "tags": [
            {
                "employee_id": 1,
                "text": "This is a tag",
                "tag_color": "Blue",
                "date": 1675191600.0
            },
            {
                "employee_id": 1,
                "text": "This is a tag",
                "tag_color": "Green",
                "date": 1675191600.0
            }
        ],
        "participants": [
            {
                "employee_id": 1,
                "name": "Baby",
                "avatar": null
            },
            {
                "employee_id": 2,
                "name": "John",
                "avatar": null
            },
            {
                "employee_id": 3,
                "name": "Nolan",
                "avatar": null
            }
        ]
    }
}
```

## **10. Get all tasks of an employee**

```http
POST /api/company/company_id/projects/tasks
```

* Authorization: Access token

**Parameters:**

| Name       | Type | Required | Values(default) | Description            |
|------------|------|----------|-----------------|------------------------|
| company_id | int  | YES      |                 | Company Id of the user |

**Returns:** List of ShortProjectTaskType | ShortProjectTaskTagType | ShortProjectTaskMemberType

**Example:**

```http
POST /api/company/1/projects/tasks
```

* Body:

```json

```

* Response:

```json
{
    "ok": true,
    "description": "Got Employee Tasks",
    "result": {
        "assigned": [
            {
                "id": 123,
                "project_id": 111,
                "title": "Task-1",
                "description": "This is task description",
                "status": "assigned",
                "date": 1672513200.0,
                "due_date": 1675191600.0,
                "task_tags": [
                    {
                        "employee_id": 1,
                        "text": "This is a tag",
                        "tag_color": "Red",
                        "date": 1675191600.0
                    }
                ],
                "task_members": [
                    {
                        "id": 1,
                        "task_id": 123,
                        "employee_id": 1
                    },
                    {
                        "id": 5,
                        "task_id": 123,
                        "employee_id": 2
                    },
                    {
                        "id": 9,
                        "task_id": 123,
                        "employee_id": 3
                    }
                ]
            }
        ],
        "active": [
            {
                "id": 234,
                "project_id": 222,
                "title": "Task-2",
                "description": "This is task description",
                "status": "active",
                "date": 1672513200.0,
                "due_date": 1675191600.0,
                "task_tags": [
                    {
                        "employee_id": 1,
                        "text": "This is a tag",
                        "tag_color": "Blue",
                        "date": 1675191600.0
                    }
                ],
                "task_members": [
                    {
                        "id": 2,
                        "task_id": 234,
                        "employee_id": 1
                    },
                    {
                        "id": 6,
                        "task_id": 234,
                        "employee_id": 2
                    },
                    {
                        "id": 10,
                        "task_id": 234,
                        "employee_id": 3
                    }
                ]
            }
        ],
        "succeeded": [
            {
                "id": 345,
                "project_id": 333,
                "title": "Task-3",
                "description": "This is task description",
                "status": "succeeded",
                "date": 1672513200.0,
                "due_date": 1675191600.0,
                "task_tags": [
                    {
                        "employee_id": 1,
                        "text": "This is a tag",
                        "tag_color": "Green",
                        "date": 1675191600.0
                    }
                ],
                "task_members": [
                    {
                        "id": 3,
                        "task_id": 345,
                        "employee_id": 1
                    },
                    {
                        "id": 7,
                        "task_id": 345,
                        "employee_id": 2
                    },
                    {
                        "id": 11,
                        "task_id": 345,
                        "employee_id": 3
                    }
                ]
            }
        ],
        "failed": [
            {
                "id": 456,
                "project_id": 111,
                "title": "Task-4",
                "description": "This is task description",
                "status": "failed",
                "date": 1672513200.0,
                "due_date": 1675191600.0,
                "task_tags": [
                    {
                        "employee_id": 1,
                        "text": "This is a tag",
                        "tag_color": "Yellow",
                        "date": 1675191600.0
                    }
                ],
                "task_members": [
                    {
                        "id": 4,
                        "task_id": 456,
                        "employee_id": 1
                    },
                    {
                        "id": 8,
                        "task_id": 456,
                        "employee_id": 2
                    },
                    {
                        "id": 12,
                        "task_id": 456,
                        "employee_id": 3
                    }
                ]
            }
        ]
    }
}
```

## **11. Get attachments of a task**

```http
POST /api/projects/tasks/task_id/attachments
```

* Authorization: Access token

**Parameters:**

| Name    | Type | Required | Values(default) | Description            |
|---------|------|----------|-----------------|------------------------|
| task_id | int  | YES      |                 | Id of the task         |

**Returns:** ShortProjectTaskAttachmentType

**Example:**

```http
POST /api/projects/tasks/123/attachments
```

* Body:

```json

```

* Response:

```json
{
    "ok": true,
    "description": "Got Task Attachment(s)",
    "result": [
        {
            "task_id": 123,
            "employee_id": 1,
            "text": "This is a text",
            "file": "This is an attachment"
        }
    ]
}
```

## **12. Get comments of a task**

```http
POST /api/projects/tasks/task_id/comments
```

* Authorization: Access token

**Parameters:**

| Name    | Type | Required | Values(default) | Description            |
|---------|------|----------|-----------------|------------------------|
| task_id | int  | YES      |                 | Id of the task         |

**Returns:** ShortProjectTaskCommentType

**Example:**

```http
POST /api/projects/tasks/123/comments
```

* Body:

```json

```

* Response:

```json
{
    "ok": true,
    "description": "Got Task Comment(s)",
    "result": [
        {
            "task_id": 123,
            "employee_id": 1,
            "text": "This is a comment",
            "date": 1675191600.0
        }
    ]
}
```
