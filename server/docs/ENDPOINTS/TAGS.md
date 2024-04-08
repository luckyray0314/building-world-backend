# Tags API

#### _Please read General API Information first_

## **1. Create a Tag**

```http
POST /api/company/company_id/tags/create
```

* Authorization: Access token

**Parameters:**

| Name       | Type | Required | Values(default) | Description            |
|------------|------|----------|-----------------|------------------------|
| company_id | int  | YES      |                 | Company_id of the user |
| color      | int  | YES      |                 | Color of the new Tag   |
| text       | int  | YES      |                 | Text of the new Tag    |

**Returns:** TagType

**Example:**

```http
POST /api/company/1/tags/create
```

* Body:

```json
{
  "color": "Purple",
  "text": "This is a new tag"
}
```

* Response:

```json
{
  "ok": true,
  "description": "Tag created",
  "result": {
    "id": 11,
    "company_id": 1,
    "color": "Purple",
    "text": "This is a new tag",
    "date": 1684663532.90692
  }
}
```