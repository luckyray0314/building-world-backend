# Deals Api 
#### _Please read General API Information first_

### check_permissions(func)
A decorator function that checks user permissions before executing an endpoint method.

#### Parameters
- `func` (function): The endpoint method to be decorated.
#### Returns
- `function`: The decorated function that checks user permissions.
#### Functionality
1. Check if user is authenticated. If not, log a warning and abort with a 401 (Unauthorized) status code.
2. Check if user has access to the company associated with the resource. If not, log a warning and abort with a 403 (Forbidden) status code.
3. Check if user has pipeline permission in the navbar. If not, log a warning and abort with a 403 (Forbidden) status code.
4. If all checks passed, execute the endpoint method.

Note: This decorator assumes that the `current_user` variable is available, which should be an instance of the `User` model.
Additionally, it requires that the endpoint method being decorated has a `company_id` keyword argument, which is used to determine which company the resource belongs to.

# **DealsResource**

### 1. Retrieve Deal
Retrieve a deal by ID.

```
GET /api/deals/<int:deal_id>
```
#### Request
#### Parameters
| Name	      | Type	 | Required | 	Description                              |
|------------|-------|----------|-------------------------------------------|
| deal_id    | 	int	 | YES	     | Unique identifier for the deal            |
#### Headers
Authorization: Access token, check permissions

#### Response
#### Status Codes
| Code | 	Description    |
|------|-----------------|
| 200  | 	OK             |
| 404  | 	Deal not found |

#### Example
- Request:
```
GET /api/deals/1
```
- Response:
```json
{
    "id": 1,
    "name": "Deal 1",
    "counterpartie": "Company A",
    "status": 0,
    "pipeline_id": 0
}
```

### 2.Create Deal
Create a new deal.

```http
POST /api/deals
```
#### Request
#### Parameters
| Name	         | Type  | 	Required | 	Description                                 |
|---------------|-------|-----------|----------------------------------------------|
| name	         | str	  | YES       | 	Name for the deal                           |
| counterpartie | 	str	 | YES	      | Counterpartie for the deal                   |
| status        | 	int  | 	NO       | 	Status for the deal (1=completed, 2=failed) |
| pipeline_id   | 	int	 | NO	       | Pipeline ID for the deal                     |


#### Headers
Authorization: Access token, check permissions

#### Example
- Request:
```json
{
    "name": "Deal 1",
    "counterpartie": "Company A",
    "status": 0,
    "pipeline_id": 0
}
```
- Response:
```json
{
    "message": "Deal created successfully"
}
```
### 3. Update Deal
Update an existing deal.

```http
PUT /api/deals/<int:deal_id>
```
#### Request
#### Parameters

| Name          | 	Type | 	Required | 	Description                                |
|---------------|-------|-----------|---------------------------------------------|
| deal_id       | 	int  | 	YES	     | Unique identifier for the deal              |
| name          | 	str  | 	NO	      | Name for the deal                           |
| counterpartie | 	str  | 	NO	      | Counterpartie for the deal                  |
| status        | 	int  | 	NO	      | Status for the deal (1=completed, 2=failed) |
| pipeline_id   | 	int  | 	NO	      | Pipeline ID for the deal                    |

#### Headers
Authorization: Access token, check permissions

#### Response
#### Status Codes

| Code | 	Description    |
|------|-----------------|
| 200  | 	OK             |
| 404  | 	Deal not found |

#### Example
- Request:
```json
{
    "name": "Deal 1",
    "counterpartie": "Company B",
    "status": 1,
    "pipeline_id": 1
}
```
- Response:
```json

{
    "message": "Deal updated successfully"
}
```
### 4. Delete Deal
Delete an existing deal.

```http
DELETE /api/deals/<int:deal_id>
```
#### Request
#### Parameters

| Name    | 	Type | 	Required | 	Description                    |
|---------|-------|-----------|---------------------------------|
| deal_id | 	int  | 	YES      | 	Unique identifier for the deal |

#### Headers
Authorization: Access token, check permissions

#### Response
#### Status Codes
| Code | 	Description    |
|------|-----------------|
| 200  | 	OK             |
| 404  | 	Deal not found |

#### Example
- Request:
```
DELETE /api/deals/1
```
- Response:
```json
{
    "message": "Deal deleted successfully"
}
```

### 5. Update Deal Status to Failed
Update the status of a deal to "failed".

```http
PUT /api/deals/<int:deal_id>/failed
```
#### Request
#### Parameters

| Name	      | Type | 	Required | 	Description                     |
|------------|------|-----------|----------------------------------|
| deal_id	   | int  | 	YES      | 	Unique identifier for a deal    |
| company_id | 	int | 	YES      | 	Unique identifier for a company |

#### Headers
Authorization: Access token, checks permission
#### Response:
#### Status Codes

| Code | 	Description                                                     |
|------|------------------------------------------------------------------|
| 200  | 	If the deal with the given deal_id is not found.                |
| 404  | 	 If the status of the deal is successfully updated to "failed". |

#### Example:

- Request:
```
PUT /api/deals/123/failed
```
- Response:
```json
{
    "message": "Deal status updated to failed"
}
```

### 6. Update Deal Status to Completed
Update the status of a deal to "completed".

```http
PUT /api/deals/<int:deal_id>/completed
```

#### Request
#### Parameters

| Name	      | Type | 	Required | 	Description                     |
|------------|------|-----------|----------------------------------|
| deal_id	   | int  | 	YES      | 	Unique identifier for a deal    |
| company_id | 	int | 	YES      | 	Unique identifier for a company |

#### Headers
Authorization: Access token, checks permission
#### Response:
#### Status Codes

| Code | 	Description                                                        |
|------|---------------------------------------------------------------------|
| 200  | 	If the deal with the given deal_id is not found.                   |
| 404  | 	 If the status of the deal is successfully updated to "completed". |

#### Example:

- Request:
```
PUT /api/deals/123/completed
```
- Response:
```json
{
    "message": "Deal status updated to completed"
}
```

### 7. Move Deal to Pipeline
Move a deal to a different pipeline.
```http
PUT /api/deals/<int:deal_id>/pipeline
```
#### Parameters:

| Name        | 	Type | 	Required | 	Values(default) | 	Description                                                |
|-------------|-------|-----------|------------------|-------------------------------------------------------------|
| pipeline_id | 	int  | 	YES      | 		Unique         | identifier for the pipeline to which the deal will be moved |

#### Headers
Authorization: Access token, checks permission


#### Response:
#### Status Codes
| Code | 	Description                                                                 |
|------|------------------------------------------------------------------------------|
| 404  | If the deal with the given deal_id is not found                              |
| 400  | If the pipeline_id is not provided in the request                            |
| 200  | If the deal is successfully moved to the pipeline with the given pipeline_id |

#### Example:

- Request:
```
PUT /api/deals/123/pipeline
{
    "pipeline_id": 3
}
```
- Response:
```json
{
    "message": "Deal moved to pipeline successfully"
}
```