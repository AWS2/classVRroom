# Get Courses

Te devuelve todos los cursos de todos los centros

**URL** : `/api/get_courses/`

**Method** : `GET`

**Token required** : SI

## Success Response

**Content example**

```json
{
    "status": "OK",
    "course_list": [
        {
            "courseID": 1,
            "title": "Enfermeria",
            "description": "Curso de enfermeria",
            "status": true,
            "center": 1,
            "subscribers": {
                "teachers": [
                    {
                        "UserID": 1,
                        "username": "superadmin",
                        "email": "super@admin.com"
                    },
                    {
                        "UserID": 11,
                        "username": "super-profe",
                        "email": "super@profe.com"
                    }
                ]
            }
        },
        {
            "courseID": 2,
            "title": "Curso de demostración",
            "description": "Curso para enseñar la web",
            "status": true,
            "center": 1,
            "subscribers": {
                "teachers": [
                    {
                        "UserID": 3,
                        "username": "pepe-profe",
                        "email": "profesor@demo.com"
                    },
                    {
                        "UserID": 1,
                        "username": "superadmin",
                        "email": "super@admin.com"
                    }
                ]
            }
        }
    ]
}
```

