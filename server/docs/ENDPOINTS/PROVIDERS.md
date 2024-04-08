# Providers Api

#### _Please read General API Information first_

### check_permissions(func)

A decorator function that checks user permissions before executing an endpoint method.

#### Parameters

- `func` (function): The endpoint method to be decorated.

#### Returns

- `function`: The decorated function that checks user permissions.

#### Functionality

1. Check if user is authenticated. If not, log a warning and abort with a 401 (Unauthorized) status code.
2. Check if user has access to the company associated with the resource. If not, log a warning and abort with a 403 (
   Forbidden) status code.
3. Check if user has pipeline permission in the navbar. If not, log a warning and abort with a 403 (Forbidden) status
   code.
4. If all checks passed, execute the endpoint method.

Note: This decorator assumes that the `current_user` variable is available, which should be an instance of the `User`
model. Additionally, it requires that the endpoint method being decorated has a `company_id` keyword argument, which is
used to determine which company the resource belongs to.

# **ProvidersResource**

## **1. Get providers**

```http
GET /api/providers/company/<int:company_id>
```

- Authorization: Access token

**Request Body:**

| Name      | Type | Required | Values(default) | Description                            |
|-----------|------|----------|-----------------|----------------------------------------|
| type      | str  | NO       | None            | Type(s) of the providers to filter by. |
| name      | str  | NO       | None            | Name of the provider to search for.    |

**Returns:** List of ShortProviderType

**Example:**

- URL:

```url
GET /api/providers/company/1
```

- Request Body:

```
```

```json
{
  "ok": true,
  "description": "Got Provider(s)",
  "result": [
    {
      "name": "bad baby",
      "avatar": "Provider Avatar 5",
      "description": "Provider Description 5",
      "company_id": 1,
      "counter_party": 1,
      "created": 1682881200.0,
      "last_deal_with": 1682881200.0
    },
    {
      "name": "good baby",
      "avatar": "Provider Avatar 4",
      "description": "Provider Description 4",
      "company_id": 1,
      "counter_party": 1,
      "created": 1680289200.0,
      "last_deal_with": 1680289200.0
    },
    {
      "name": "baby baby",
      "avatar": "Provider Avatar 3",
      "description": "Provider Description 3",
      "company_id": 1,
      "counter_party": 1,
      "created": 1677610800.0,
      "last_deal_with": 1677610800.0
    },
    {
      "name": "baby guy",
      "avatar": "Provider Avatar 2",
      "description": "Provider Description 2",
      "company_id": 1,
      "counter_party": 1,
      "created": 1675191600.0,
      "last_deal_with": 1675191600.0
    },
    {
      "name": "baby boy",
      "avatar": "Provider Avatar 1",
      "description": "Provider Description 1",
      "company_id": 1,
      "counter_party": 1,
      "created": 1672513200.0,
      "last_deal_with": 1672513200.0
    }
  ]
}
```

- URL:

```url
GET api/providers/company/1?user_name=boy
```

- Request Body:

```
```

```json
{
  "ok": true,
  "description": "Got Provider(s)",
  "result": [
    {
      "name": "baby boy",
      "avatar": "Provider Avatar 1",
      "description": "Provider Description 1",
      "company_id": 1,
      "counter_party": 1,
      "created": 1672513200.0,
      "last_deal_with": 1672513200.0
    }
  ]
}
```

- URL:

```url
GET api/providers/company/1?user_name=bad&type=type1
```

- Request Body:

```
```

```json
{
  "ok": true,
  "description": "Got Provider(s)",
  "result": [
    [
      {
        "name": "bad baby",
        "avatar": "Provider Avatar 5",
        "description": "Provider Description 5",
        "company_id": 1,
        "counter_party": 1,
        "created": 1682881200.0,
        "last_deal_with": 1682881200.0
      }
    ]
  ]
}
```