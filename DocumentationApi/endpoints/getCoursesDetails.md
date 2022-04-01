[:arrow_left: Atras](../documentacion.md)

# Get Courses

Usado para cojer informacion de un curso por id, si el usuario esta subscrito al curso

**URL** : `/api/get_course_details/`

**Method** : `GET`

**Token required** : YES

**Data constraints**

```json
{
    "courseID": "[valid course id]"
}
```

**Data example**

```json
{
    "courseID": "2"
}
```

## Success Response

**Content example**

```json
{
    "status": "OK",
    "course_list": {
        "title": "Curso de demostración",
        "description": "Curso para enseñar la web",
        "courseID": 2,
        "institutionID": 1,
        "status": true,
        "elements": {
            "links": [
                {
                    "linkID": 1,
                    "title": "Video informativo",
                    "link": "https://github.com/edupedu101"
                }
            ],
            "texts": [
                {
                    "textID": 1,
                    "autorID": 2,
                    "title": "Lorem Ipsum",
                    "texto": "lore ipsum sir amet bla bla bla"
                }
            ],
            "documents": [],
            "tasks": [
                {
                    "taskID": 1,
                    "title": "Ejercicio ejemplo",
                    "description": "",
                    "quote": "Ennunciado del ejercicio de ejemplo",
                    "maxQualification": 10.0,
                    "task_type": "no vr"
                },
                {
                    "taskID": 2,
                    "title": "Ejemplo VR",
                    "description": "",
                    "quote": "Enunciado ejercicio vr",
                    "maxQualification": 5.0,
                    "task_type": "vr"
                }
            ]
        }
    }
}
```

## Not Subscribed Response 

**Condition** : Si el usuario no esta subscrito al curso que intenta acceder

**Content** :

```json
{
    "status": "ERROR",
    "message": "Usuario no inscrito en el curso."
}
```

## Curso Not Found Response

**Condition** : Si el curso no existe

**Content** :

```json
{
    "status": "ERROR",
    "message": "Curso no encontrado."
}
```