# Casting Agency Specifications
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Models:
-  Movies with attributes id, title and release date
- Actors with attributes id, name, age and gender

## Endpoints:
- GET /actors and /movies
- DELETE /actors/ and /movies/
- POST /actors and /movies and
- PATCH /actors/ and /movies/

## Roles:
### Casting Assistant
- Can view actors and movies

### Casting Director
- All permissions a Casting Assistant has and…
- Add or delete an actor from the database
- Modify actors or movies
### Executive Producer
- All permissions a Casting Director has and…
- Add or delete a movie from the database

---

## Installation and Running Locally:
```sh
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 app.py
```

---
## Headers:
- Content-Type: 'application/json'
- Authorization: 'Bearer \<JWT_TOKEN>'

---

## Sample:
GET /actors
```
# Response body
{
    "actors": [
        {
            "age": 20,
            "gender": "male",
            "id": 1,
            "name": "Hazem"
        },
        {
            "age": 19,
            "gender": "male",
            "id": 2,
            "name": "Seif"
        },
        {
            "age": 20,
            "gender": "male",
            "id": 3,
            "name": "Omer"
        }
    ]
}
```

GET /actors/1
```
# Response body
{
    "age": 20,
    "gender": "male",
    "id": 1,
    "name": "Hazem"
}
```

POST /actors
```
# Request body
{
    "name": "Noor",
    "age": 35,
    "gender": "male"
}

# Response body
{
    "age": 35,
    "gender": "male",
    "id": 4,
    "name": "Noor"
}
```
PATCH /actors/1
```
# Request body
{
    "age": 21
}

# Response body
{
    "age": 21,
    "gender": "male",
    "id": 1,
    "name": "Hazem"
}
```

DELETE /actors/3
```
# Response body
{
    "deleted": 3
}
```