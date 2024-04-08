

# Hiearchy Api 
#### _Please read General API Information first_

## **1. Employees**

```http
GET /api/hierarchy/employees/<COMPANY_ID>/<EMPLOYEE_ID>
```
* Authorization: Access token

**Parameters:** 

Name | Type | Required | Values(default) | Description
------------ | ------------ | ------------ | ------------ | ------------
COMPANY_ID | int | YES |     | Unique identifier for a company
EMPLOYEE_ID | int | YES |     | Unique identifier for an employee


**Returns:** Array of LShortEmployeeType

**Example:**


* URL:
```url
http://127.0.0.1:5000/api/hierarchy/employees/1/4
```


* Response:
```json
{
    "ok": true,
    "description": "Got list of the employees",
    "result": [
        {
            "employee_id": 5,
            "user_id": 9,
            "position": "designer",
            "name": "Tom",
            "avatar": null,
            "is_in_team": false
        },
        {
            "employee_id": 6,
            "user_id": 8,
            "position": "designer",
            "name": "Alex",
            "avatar": null,
            "is_in_team": false
        }
    ]
}
```


## **2. Fire employee**

```http
DELETE /api/hierarchy/fire
```
* Authorization: Access token

**Parameters:** 

Name | Type | Required | Values(default) | Description
------------ | ------------ | ------------ | ------------ | ------------
employee_id | int | YES |     | Unique identifier

> When you use this endpoint for the first time, an employee you sent will not be removed from the database totally as it is needed for a placeholder (dark) card on the list of employees. To delete absolutely, request again with the same json data.


**Example:**
* Body:
```json
{
    "employee_id": 11,
}
```
* Response:
```json
{
    "ok": true,
    "description": "Employee was totally fired",
    "result": {
        "id": 11,
        "user_id": null,
        "position": "worker"
    }
}
```

## **Hire employee**

### **3. Send an invitation and add an employee**
```http
POST /api/hierarchy/hire/invitation/send
```
* Authorization: Access token

**Parameters:** 

Name | Type | Required | Values(default) | Description
------------ | ------------ | ------------ | ------------ | ------------
email | str | YES |     | A targeted email
link | str | YES |    | Create a link contains the domain name, path etc so an invitation token generated by the server will be applied to this link. In this case, the link should contain string `{TOKEN}` which will be replaced with original token when an email sent (e.g. https://domain.com/invite/confirm?token={TOKEN}, https://domain.com/invt/{TOKEN}/confirm).
employee | object | YES |     | Employee details. Possibly fields are described below
navbar | object | YES |    | Navbar functions. Possibly fields are described below

<br>

* employee:
    Name | Type | Required | Values(default) | Description
    ------------ | ------------ | ------------ | ------------ | ------------
    work_hour | float | YES |     |
    wage | int | YES |    | 
    position | str | YES |     |
    leader_id | int | YES |    | 
    company_id | int | YES |     |


* navbar:
    Name | Type | Required | Values(default) | Description
    ------------ | ------------ | ------------ | ------------ | ------------
    employee | bool | YES |     |
    projects | bool | YES |    | 
    sales | bool | YES |     |
    purchase | bool | YES |    | 
    finance | bool | YES |     |



**Example:**
* Body:
```json
{
    "email": "myemail@gmail.com",
    "link": "http://localhost:3000/invitation/confirm/{TOKEN}",
    "employee": {
        "work_hour": 6.5,
        "wage": 35,
        "position": "QA",
        "leader_id": 4,
        "company_id": 1
    },
    "navbar": {
        "employee": false,
        "projects": true,
        "sales": true,
        "purchase": true,
        "finance": true
    }
}
```
* Response:
```json
{
    "ok": true,
    "description": "Email sent and Employee added",
    "result": null
}
```


### **4. Confirm an invitation and update an employee**
```http
POST /api/hierarchy/hire/invitation/confirm
```
* Authorization: Access token

**Parameters:** 

Name | Type | Required | Values(default) | Description
------------ | ------------ | ------------ | ------------ | ------------
token | str | YES |     | 



**Example:**
* Body:
```json
{
    "token": "a25492495f86b1be08317e2e7800ec2c9ccda74828c119f691ed99ee0c75149f"
}
```
* Response:
```json
{
    "ok": true,
    "description": "Token used successfully and employee updated",
    "result": {
        "employee_id": 23,
        "user_id": 1324,
        "position": "QA",
        "name": "Alexander Rybak",
        "avatar": null
    }
}
```
```json
{
    "description": "Token expired or already used",
    "error_code": 400,
    "ok": false
}
```






## **5. Hiearchy Leaders**
```http
GET /api/hierarchy/leaders/<COMPANY_ID>/<EMPLOYEE_ID>
```
* Authorization: Access token


**Parameters:** 

Name | Type | Required | Values(default) | Description
------------ | ------------ | ------------ | ------------ | ------------
COMPANY_ID | int | YES |     | Unique identifier for a company
EMPLOYEE_ID | int | YES |    | Unique identifier for an employee


**Returns:** Array of ShortEmployeeType


**Example:**
* URL:
```url
http://127.0.0.1:5000/api/hierarchy/leaders/1/9
```
* Response:
```json
{
    "ok": true,
    "description": "",
    "result": [
        {
            "employee_id": 8,
            "user_id": 6,
            "position": "leadA",
            "name": "Hela",
            "avatar": null
        },
        {
            "employee_id": 4,
            "user_id": 10,
            "position": "manager",
            "name": "Mila",
            "avatar": null
        }
    ]
}
```







## **6. Hiearchy Get A Leader Of An Employee**
```http
GET /api/hierarchy/aleader/<COMPANY_ID>/<EMPLOYEE_ID>
```
* Authorization: Access token


**Parameters:** 

Name | Type | Required | Values(default) | Description
------------ | ------------ | ------------ | ------------ | ------------
COMPANY_ID | int | YES |     | Unique identifier for a company
EMPLOYEE_ID | int | YES |    | Unique identifier for an employee


**Returns:** ShortEmployeeType


**Example:**
* URL:
```url
http://127.0.0.1:5000/api/hierarchy/aleader/1/7
```
* Response:
```json
{
    "ok": true,
    "description": "",
    "result": {
        "employee_id": 4,
        "user_id": 10,
        "position": "manager",
        "name": "Mila",
        "avatar": null
    }
}
```



