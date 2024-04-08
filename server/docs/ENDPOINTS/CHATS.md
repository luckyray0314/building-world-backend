# Chats Api

** Please read General API Information first **

## Table of Contents

[1. List of Chat](#1-list-of-chats)<br>
[2. List of Chat Messages](#2-list-of-messages-of-a-chat)<br>
[3. Get Chat Info](#3-get-chat-info)<br>
[4. Create a Group Chat](#4-create-a-group-chat)<br>
[5. Forward Message](#5-forwardmessageresource)<br>
[6. Get Message Info](#6-get-a-message-info)<br>
[7. Live Chat](#7-live-chat)<br>
[8. Send/Reply Message](#8-sendreply-message)<br>
[9. Read Message](#9-read-message)<br>
[10. Delete Message](#10-delete-message)<br>
[11. Forward Message](#11-forward-message)<br>
[12. Edit Message](#12-edit-message)<br>
[13. Pin Message](#13-pin-message)<br>
[14. Set User Typing Status in Chat](#14-set-user-typing-status-in-chat)<br>

## **1. List of Chats**

```http
GET /api/company/<int:company_id>/chats?page=<int:page>&per_page=<int:per_page>&query=<str:query>
```

- Authorization: Access token

**Parameters:**

| Name       | Type | Required | Values(default) | Description                     |
| ---------- | ---- | -------- | --------------- | ------------------------------- |
| company_id | int  | YES      |                 |
| page       | int  | NO       | 1               | page to get                     |
| per_page   | int  | NO       | 10              | number of chats to get per page |
| query   | str  | NO       |               | name of the chat |

**Returns:** List of ChatMember | Chat | UChats

**Example:**

- URL:

```url
http://127.0.0.1:5000//api/company/1/chats?page=1&per_page=100&query=chat
```

- Response:

```json
{
  "ok": true,
  "description": "Got list of chats",
  "result": [
    {
      "chat_id": 1,
      "name": "First Chat",
      "date": 1683368507.087257,
      "avatar": null,
      "is_group": true,
      "participants": [
        {
          "employee_id": 1,
          "name": "Baby",
          "avatar": null
        },
        {
          "employee_id": 2,
          "name": "Tom",
          "avatar": null
        }
      ],
      "unread_count": 14
    },
    {
      "chat_id": 2,
      "name": "Second Chat",
      "date": 1683368507.091437,
      "avatar": null,
      "is_group": true,
      "participants": [
        {
          "employee_id": 3,
          "name": "Baby",
          "avatar": null
        },
        {
          "employee_id": 4,
          "name": "Alex",
          "avatar": null
        }
      ],
      "unread_count": 6
    },
    {
      "chat_id": 3,
      "name": "Third Chat",
      "date": 1683368507.096467,
      "avatar": null,
      "is_group": true,
      "participants": [
        {
          "employee_id": 5,
          "name": "Baby",
          "avatar": null
        },
        {
          "employee_id": 6,
          "name": "Mila",
          "avatar": null
        }
      ],
      "unread_count": 1
    }
  ]
}
```

## **2. List of messages of a chat**

```http
GET /api/chats/<int:chat_id>/messages?page=<int:page>&per_page=<int:per_page>&query=<str:query>
```

- Authorization: Access token

**Parameters:**

| Name     | Type | Required | Values(default) | Description                              |
| -------- | ---- | -------- | --------------- | ---------------------------------------- |
| chat_id  | int  | YES      |                 |
| page     | int  | NO       | 1               | page to get                              |
| per_page | int  | NO       | 10              | number of chat messages to get per page  |
| query    | str  | NO       |                 | get messages that contain the query text |

**Returns:** List of MessageType

**Example:**

- URL:

```url
http://127.0.0.1:5000/api/chats/1/messages?page=2&per_page=6&query=he
```

- Response:

```json
{
  "ok": true,
  "description": "Got messages",
  "result": [
    {
      "text": "Where is it? I don't know it.",
      "sender_name": "Tom",
      "files": []
    },
    {
      "text": "The Blue Café is nice. I love the tea there. heart",
      "sender_name": "Tom",
      "files": []
    }
  ]
}
```

## **3. Get Chat Info**

```http
GET /api/chats/<int:chat_id>
```

- Authorization: Access token

**Parameters:**

| Name    | Type | Required | Values(default) | Description                  |
| ------- | ---- | -------- | --------------- | ---------------------------- |
| chat_id | int  | YES      |                 | Unique identifier for a chat |

**Returns:** Chat

**Example:**

- URL:

```url
http://127.0.0.1:5000/api/chats/2
```

- Response:

```json
{
  "ok": true,
  "description": "Got chat info",
  "result": {
    "chat_id": 2,
    "name": "Second Chat",
    "date": 1683196341.055695,
    "avatar": null,
    "is_group": true,
    "participants": [
      {
        "employee_id": 3,
        "name": "Baby",
        "avatar": null
      },
      {
        "employee_id": 4,
        "name": "Alex",
        "avatar": null
      }
    ]
  }
}
```

## **4. Create a group chat**

```http
POST /api/chats/group/create
```

- Authorization: Access token

**Request Payload:**

| Name         | Type | Required | Values(default) | Description                                      |
| ------------ | ---- | -------- | --------------- | ------------------------------------------------ |
| company_id   | int  | YES      |                 | Unique identifier for a company                  |
| name         | str  | YES      |                 | Name for the group chat                          |
| participants | list | YES      |                 | List of company employees to add into group chat |
| avatar       | str  | NO       |                 | encoded avatar image                             |

**Returns:** Chat

**Example:**

- URL: `http://127.0.0.1:5000/api/chats/group/create`

- Body:

```json
{
  "company_id": 1,
  "name": "Pokemon",
  "participants": [1, 99, 2, 3]
}
```

- Response:

```json
{
  "ok": true,
  "description": "Group chat created",
  "result": {
    "chat_id": 28,
    "name": "Pokemon",
    "date": 1683259937.003848,
    "avatar": null,
    "is_group": true,
    "participants": [
      {
        "employee_id": 15,
        "name": "Baby",
        "avatar": null
      },
      {
        "employee_id": 16,
        "name": "Nolan",
        "avatar": null
      }
    ],
    "company_id": 1,
    "last_message": null
  }
}
```

## **5. ForwardMessageResource**

This resource allows a user to forward a message to one or more chats.

```http
POST /api/chats/messages/<int:message_id>/forward
```

- Authorization: Access token

**Parameters:**

| Name       | Type | Required | Values(default) | Description                            |
| ---------- | ---- | -------- | --------------- | -------------------------------------- |
| message_id | int  | YES      |                 | The ID of the message to be forwarded. |

**Request Payload:**

| Name               | Type | Required | Values(default) | Description                                             |
| ------------------ | ---- | -------- | --------------- | ------------------------------------------------------- |
| recipient_chat_ids | list | YES      |                 | The chat ids of to where the message is to be forwarded |

**Example:**

- URL:

```url
http://127.0.0.1:5000/api/chats/messages/2/forward
```

- Body:

```json
{
  "recipient_chat_ids": [2, 3, 6]
}
```

- Response:

```json
{
  "ok": true,
  "description": "Message Forwarded",
  "result": [
    {
      "message_id": 23,
      "text": null,
      "readers": [
        {
          "employee_id": 1,
          "is_read": true,
          "is_delivered": true
        },
        {
          "employee_id": 6,
          "is_read": false,
          "is_delivered": false
        }
      ],
      "chat_id": 2,
      "sender_id": 1,
      "is_edited": false,
      "replied": null,
      "date": 1683262979.920633,
      "files": [],
      "forwarded": {
        "text": "Hello? Hello?!?",
        "sender_name": "Baby",
        "files": []
      }
    },
    {
      "message_id": 24,
      "text": null,
      "readers": [
        {
          "employee_id": 1,
          "is_read": true,
          "is_delivered": true
        },
        {
          "employee_id": 4,
          "is_read": false,
          "is_delivered": false
        }
      ],
      "chat_id": 3,
      "sender_id": 1,
      "is_edited": false,
      "replied": null,
      "date": 1683262980.010285,
      "files": [],
      "forwarded": {
        "text": "Hello? Hello?!?",
        "sender_name": "Baby",
        "files": []
      }
    }
  ]
}
```

## **6. Get a message info**

```http
GET /api/chats/message/<int:message_id>
```

- Authorization: Access token

**Parameters:**

| Name       | Type | Required | Values(default) | Description |
| ---------- | ---- | -------- | --------------- | ----------- |
| message_id | int  | YES      |                 |             |

**Returns:** MessageType

**Example:**

- URL:

```url
http://127.0.0.1:5000/api/chats/message/1
```

- Response:

```json
{
  "ok": true,
  "description": "Got message info",
  "result": {
    "message_id": 1,
    "text": "Hi Aziz! Are you there?",
    "readers": [
      {
        "employee_id": 1,
        "is_read": true,
        "is_delivered": true
      },
      {
        "employee_id": 5,
        "is_read": false,
        "is_delivered": false
      }
    ],
    "chat_id": 1,
    "sender_id": 1,
    "is_edited": false,
    "replied": null,
    "date": 1683196521.2424,
    "files": [],
    "forwarded": null
  }
}
```

## **7. Live Chat**

### GET

```http
GET /api/chats/<int:chat_id>/live
```

- Authorization: Access token

**Parameters:**

| Name    | Type | Required | Values(default) | Description |
| ------- | ---- | -------- | --------------- | ----------- |
| chat_id | int  | YES      |                 |

**Returns:** Not Delivered Chat Messages

**Example:**

- URL:

```url
GET http://127.0.0.1:5000/api/chats/2/live
```

- Response:

```json
{
  "ok": true,
  "description": "Messages Received",
  "result": [
    {
      "message_id": 26,
      "text": null,
      "sender_name": "Baby",
      "files": []
    },
    {
      "message_id": 17,
      "text": "Okay, here is your document you said yesterday",
      "sender_name": "Baby",
      "files": [
        {
          "id": 1,
          "message_id": 25,
          "file": "SGkgdGhlcmUgYWdhaW4=",
          "type": "docs",
          "name": "pokemon",
          "size": 20
        }
      ]
    }
  ]
}
```

### PUT

```http
PUT /api/chats/<int:chat_id>/live
```

- Authorization: Access token

**Request Body:**

| Name        | Type | Required | Values(default) | Description                                             |
| ----------- | ---- | -------- | --------------- | ------------------------------------------------------- |
| message_ids | list | YES      |                 | List of message ids to update their status to delivered |

**Returns:** Not Delivered Chat Messages

**Example:**

- URL:

```url
PUT http://127.0.0.1:5000/api/chats/2/live
```

- Request body:

```json
{
  "message_ids": [1, 2, 19, 20, 17, 99]
}
```

- Response:

```json
{
  "ok": true,
  "description": "Messages ids updated",
  "result": [19, 20]
}
```

- **Extra info**
  - _will do nothing for message ids that don't exist_
  - _won't update the messages not belonging to chat_

## **8. Send/Reply Message**

### Send Message

```http
POST /api/chats/send/message
```

- Authorization: Access token

**Request Body:**

| Name    | Type | Required | Values(default) | Description                                         |
| ------- | ---- | -------- | --------------- | --------------------------------------------------- |
| chat_id | int  | YES      |                 | Represents the chat where the message is to be sent |

**Returns:** Message

**Example:**

- URL:

```url
/api/chats/send/message
```

- Request Body:

```json
{
  "chat_id": 1,
  "text": "hello to chat 1",
  "files": [
    {
      "file": "an encoded image",
      "fileName": "bob.png",
      "fileType": "png"
    },
    {
      "file": "an encoded pdf",
      "fileName": "banana.pdf",
      "fileType": "pdf"
    }
  ]
}
```

- Response Body:

```json
{
  "ok": true,
  "description": "Message sent",
  "result": {
    "message_id": 27,
    "text": "hello to chat 1",
    "readers": [
      {
        "employee_id": 1,
        "is_read": true,
        "is_delivered": true
      },
      {
        "employee_id": 5,
        "is_read": false,
        "is_delivered": false
      }
    ],
    "chat_id": 1,
    "sender_id": 1,
    "is_edited": false,
    "replied": null,
    "date": 1683353908.554515,
    "files": [
      {
        "id": 2,
        "message_id": 27,
        "file": "an encoded image",
        "type": "png",
        "name": "bob.png",
        "size": 16
      },
      {
        "id": 3,
        "message_id": 27,
        "file": "an encoded pdf",
        "type": "pdf",
        "name": "banana.pdf",
        "size": 14
      }
    ],
    "forwarded": null
  }
}
```

### Reply To Message

```http
POST /api/chats/send/message
```

- Authorization: Access token

**Request Body:**

| Name       | Type | Required | Values(default) | Description                        |
| ---------- | ---- | -------- | --------------- | ---------------------------------- |
| message_id | int  | YES      |                 | Represents the message to reply to |

**Returns:** Message

**Example:**

- URL:

```url
/api/chats/send/message
```

- Request Body:

```json
{
  "message_id": 27,
  "text": "hello to u too",
  "files": [
    {
      "file": "an encoded gif",
      "fileName": "bob.gif",
      "fileType": "gif"
    },
    {
      "file": "an encoded video",
      "fileName": "banana.mp4",
      "fileType": "mp4"
    }
  ]
}
```

- Response Body:

```json
{
  "ok": true,
  "description": "Reply message sent",
  "result": {
    "message_id": 28,
    "text": "hello to u too",
    "readers": [
      {
        "employee_id": 1,
        "is_read": true,
        "is_delivered": true
      },
      {
        "employee_id": 5,
        "is_read": false,
        "is_delivered": false
      }
    ],
    "chat_id": 1,
    "sender_id": 1,
    "is_edited": false,
    "replied": 27,
    "date": 1683354140.829069,
    "files": [
      {
        "id": 4,
        "message_id": 28,
        "file": "an encoded gif",
        "type": "gif",
        "name": "bob.gif",
        "size": 14
      },
      {
        "id": 5,
        "message_id": 28,
        "file": "an encoded video",
        "type": "mp4",
        "name": "banana.mp4",
        "size": 16
      }
    ],
    "forwarded": null
  }
}
```

## **9. Read Message**

```http
PATCH /api/chats/messages/<int:message_id>/read
```

- Authorization: Access token

**Parameters:**

| Name       | Type | Required | Values(default) | Description |
| ---------- | ---- | -------- | --------------- | ----------- |
| message_id | int  | YES      |                 |             |

**Returns:** Message

**Example:**

- URL:

```url
http://127.0.0.1:5000/api/chats/messages/20/read
```

- Response:

```json
{
  "ok": true,
  "description": "Message Read",
  "result": {
    "message_id": 20,
    "text": "i am good, how ab urs?",
    "readers": [
      {
        "employee_id": 1,
        "is_read": true,
        "is_delivered": true
      },
      {
        "employee_id": 6,
        "is_read": false,
        "is_delivered": false
      }
    ],
    "chat_id": 2,
    "sender_id": 1,
    "is_edited": false,
    "replied": null,
    "date": 1683196341.839645,
    "files": [],
    "forwarded": null
  }
}
```

## **10. Delete Message**

```http
PATCH /api/chats/messages/<int:message_id>/delete
```

- Authorization: Access token

- Extra info:
  - if the message isn't sent by the current user they can only delete it for themselves, and will be hidden when they call it
  * if the message is sent by the current user they have 2 choices
    1.  delete for themselves only or,
    2.  delete the message entirely

**Parameters:**

| Name       | Type | Required | Values(default) | Description |
| ---------- | ---- | -------- | --------------- | ----------- |
| message_id | int  | YES      |                 |             |

**Request Payload:**

| Name          | Type | Required | Values(default) | Description                                               |
| ------------- | ---- | -------- | --------------- | --------------------------------------------------------- |
| delete_for_me | bool | YES      |                 | specify whether to delete for current user only or others |

- _typically required when the sender is the current user_

**Returns:** Message

**Example 1:**

- URL:

```url
http://127.0.0.1:5000/api/chats/messages/1/delete
```

- Request Body:

```json
{
  "delete_for_me": true
}
```

- Response:

```json
{
  "ok": true,
  "description": "",
  "result": "Message Hidden"
}
```

**Example 2:**

- URL:

```url
http://127.0.0.1:5000/api/chats/messages/1/delete
```

- Request Body:

```json
{
  "delete_for_me": false
}
```

- Response:

```json
{
  "ok": true,
  "description": "Message Deleted",
  "result": []
}
```

## **11. Forward Message**

```http
POST /api/chats/messages/<int:message_id>/forward
```

- Authorization: Access token

**Parameters:**

| Name       | Type | Required | Values(default) | Description |
| ---------- | ---- | -------- | --------------- | ----------- |
| message_id | int  | YES      |                 |             |

**Request Payload:**

| Name               | Type | Required | Values(default) | Description                                                              |
| ------------------ | ---- | -------- | --------------- | ------------------------------------------------------------------------ |
| recipient_chat_ids | list | YES      |                 | specify the list of chat ids the current user can forward the message to |

**Returns:** Message

**Example:**

- URL:

```url
http://127.0.0.1:5000/api/chats/messages/6/forward
```

- Request Body:

```json
{
  "recipient_chat_ids": [2, 3, 6]
}
```

- Response:

```json
{
  "ok": true,
  "description": "Message Forwarded",
  "result": [
    {
      "message_id": 23,
      "text": null,
      "readers": [
        {
          "employee_id": 1,
          "is_read": true,
          "is_delivered": true
        },
        {
          "employee_id": 6,
          "is_read": false,
          "is_delivered": false
        }
      ],
      "chat_id": 2,
      "sender_id": 1,
      "is_edited": false,
      "replied": null,
      "date": 1683368812.053857,
      "files": [],
      "forwarded": {
        "message_id": 6,
        "text": "Would you like to meet for a coffee?",
        "sender_name": "Baby",
        "files": []
      }
    },
    {
      "message_id": 24,
      "text": null,
      "readers": [
        {
          "employee_id": 1,
          "is_read": true,
          "is_delivered": true
        },
        {
          "employee_id": 4,
          "is_read": false,
          "is_delivered": false
        }
      ],
      "chat_id": 3,
      "sender_id": 1,
      "is_edited": false,
      "replied": null,
      "date": 1683368812.13056,
      "files": [],
      "forwarded": {
        "message_id": 6,
        "text": "Would you like to meet for a coffee?",
        "sender_name": "Baby",
        "files": []
      }
    }
  ]
}
```

## **12. Edit Message**

```http
PUT /api/chats/message/<int:message_id>/edit
```

- Authorization: Access token

**Parameters:**

| Name       | Type | Required | Values(default) | Description |
| ---------- | ---- | -------- | --------------- | ----------- |
| message_id | int  | YES      |                 |             |

**Request Payload:**

| Name  | Type | Required | Values(default) | Description |
| ----- | ---- | -------- | --------------- | ----------- |
| text  | str  | NO       |                 |             |
| files | dict | NO       |                 |             |

**Files dict schema:**
| Name | Type | Required | Values(default) | Description |
| ------------------ | ---- | -------- | --------------- | ------------------------------------------------------------------------ |
| deleted | list | NO | | ids of the files to delete|
| added | list | YES | | |

**Added file single item schema**
| file | str | YES | | encoded file into string|
| fileName | str | YES | | name of the file |
| fileType | str | YES | | type of the file |

**Returns:** Message

**Example:**

- URL:

```url
http://127.0.0.1:5000/api/chats/message/6/edit
```

- Request Body:

```json
{
  "ok": true,
  "description": "Message edited",
  "result": {
    "message_id": 6,
    "text": "22",
    "readers": [
      {
        "employee_id": 1,
        "is_read": true,
        "is_delivered": true
      },
      {
        "employee_id": 5,
        "is_read": false,
        "is_delivered": false
      }
    ],
    "chat_id": 1,
    "sender_id": 1,
    "is_edited": true,
    "replied": null,
    "date": 1683368507.397168,
    "files": [
      {
        "id": 2,
        "message_id": 6,
        "file": "253",
        "type": "pdf",
        "name": "Nume",
        "size": 3
      },
      {
        "id": 3,
        "message_id": 6,
        "file": "567",
        "type": "png",
        "name": "ew",
        "size": 3
      },
      {
        "id": 4,
        "message_id": 6,
        "file": "pop",
        "type": "docs",
        "name": "21",
        "size": 3
      }
    ],
    "forwarded": null
  }
}
```

- Response:

```json
{
  "ok": true,
  "description": "Message Forwarded",
  "result": [
    {
      "message_id": 23,
      "text": null,
      "readers": [
        {
          "employee_id": 1,
          "is_read": true,
          "is_delivered": true
        },
        {
          "employee_id": 6,
          "is_read": false,
          "is_delivered": false
        }
      ],
      "chat_id": 2,
      "sender_id": 1,
      "is_edited": false,
      "replied": null,
      "date": 1683368812.053857,
      "files": [],
      "forwarded": {
        "message_id": 6,
        "text": "Would you like to meet for a coffee?",
        "sender_name": "Baby",
        "files": []
      }
    },
    {
      "message_id": 24,
      "text": null,
      "readers": [
        {
          "employee_id": 1,
          "is_read": true,
          "is_delivered": true
        },
        {
          "employee_id": 4,
          "is_read": false,
          "is_delivered": false
        }
      ],
      "chat_id": 3,
      "sender_id": 1,
      "is_edited": false,
      "replied": null,
      "date": 1683368812.13056,
      "files": [],
      "forwarded": {
        "message_id": 6,
        "text": "Would you like to meet for a coffee?",
        "sender_name": "Baby",
        "files": []
      }
    }
  ]
}
```

## **13. Pin Message**

```http
POST /api/chats/message/<int:message_id>/pin
```

- Authorization: Access token

**Parameters:**

| Name       | Type | Required | Values(default) | Description |
| ---------- | ---- | -------- | --------------- | ----------- |
| message_id | int  | YES      |                 |             |

**Returns:** Message

**Example:**

- URL:

```url
http://127.0.0.1:5000/api/chats/message/9/pin
```

- Response:

```json
{
  "ok": true,
  "description": "Message pinned successfully",
  "result": {
    "chat_id": 1,
    "name": "First Chat",
    "date": 1683368507.087257,
    "avatar": null,
    "is_group": true,
    "participants": [
      {
        "employee_id": 1,
        "name": "Baby",
        "avatar": null
      },
      {
        "employee_id": 2,
        "name": "Tom",
        "avatar": null
      }
    ],
    "company_id": 1,
    "last_message": {
      "message_id": 17,
      "text": "Okay, here is your document you said yesterday",
      "readers": [
        {
          "employee_id": 1,
          "is_read": true,
          "is_delivered": true
        },
        {
          "employee_id": 5,
          "is_read": false,
          "is_delivered": false
        }
      ],
      "chat_id": 1,
      "sender_id": 1,
      "is_edited": false,
      "replied": null,
      "date": 1683371567.663664,
      "files": [
        {
          "id": 1,
          "message_id": 17,
          "file": "SGkgdGhlcmUgYWdhaW4=",
          "type": "docs",
          "name": "pokemon",
          "size": 20
        }
      ],
      "forwarded": null
    }
  }
}
```

## **14. Chat Status Resource**

```http
PUT /api/chats/chat_id/status
GET /api/chats/chat_id/status
```

* Authorization: Access token

**Parameters:**

| Name    | Type | Required | Values(default) | Description                            |
|---------|------|----------|-----------------|----------------------------------------|
| chat_id | int  | YES      |                 | chat_id of the chat the user is in. |

**Returns:** ShortChatMemberType

**Example:**

* Body:

```json
```

* Response:

PUT /api/chats/1/status

```json
{
  "ok": true,
  "description": "User Typing Status updated",
  "result": {
    "status": "Ok"
  }
}
```

* Response:

GET /api/chats/1/status

```json
{
  "ok": true,
  "description": "Got chat user statuses",
  "result": [
    {
      "Employee_id": 5,
      "is_typing": false,
      "is_online": false,
      "time_difference": "6:07:16.642306"
    },
    {
      "Employee_id": 5,
      "is_typing": false,
      "is_online": false,
      "time_difference": "6:07:16.642454"
    },
    {
      "Employee_id": 1,
      "is_typing": false,
      "is_online": false,
      "time_difference": "6:05:12.909888"
    }
  ]
}
```
