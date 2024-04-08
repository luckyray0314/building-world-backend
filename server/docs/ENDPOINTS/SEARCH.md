
# Search Api
#### _Please read General API Information first_
## **Search wrokers**

```http
POST /api/search/workers
```
* Authorization: Access token

**Parameters:** 

Name | Type | Required | Values(default) | Description
------------ | ------------ | ------------ | ------------ | ------------
needle | str | YES |   | Any string, like first name, last name, position
results_per_page | int | YES |  | Number of the results should be in a page
page_num | int | YES |  | Page number


**Example:**
* Body:
```json
{
    "needle": "s",
    "results_per_page": 5,
    "page_num": 1
}
```
* Response:
```json
{
    "ok": true,
    "description": "",
    "result": [
        {
            "id": 5,
            "user_id": 9,
            "position": "designer",
            "name": "Tom",
            "avatar_link": "https://xsgames.co/randomusers/assets/avatars/male/28.jpg"
        },
        {
            "id": 6,
            "user_id": 8,
            "position": "designer",
            "name": "Alex",
            "avatar_link": "https://xsgames.co/randomusers/assets/avatars/male/23.jpg"
        },
        {
            "id": 7,
            "user_id": 7,
            "position": "designer",
            "name": "Marcus",
            "avatar_link": "https://xsgames.co/randomusers/assets/avatars/male/2.jpg"
        },
        {
            "id": 9,
            "user_id": 5,
            "position": "worker",
            "name": "Sarah",
            "avatar_link": "https://xsgames.co/randomusers/assets/avatars/male/78.jpg"
        }
    ]
}
```

