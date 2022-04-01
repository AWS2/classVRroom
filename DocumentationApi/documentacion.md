
# Documentacion de la Api

:warning: **Si el endpoint requiere token sigue esto**: El token se pasara por el header con el siguente formato

**Data constraints**

```json
{
    "Authorization": "Token [valid token]"
}
```

**Data example**

```json
{
    "Authorization": "Token 3d3fb2a2993aabada7741197d34c6e8b8061e70a"
}
```


*   [Login](./endpoints/login.md) : `GET /api/login`

*   [Logout](./endpoints/logout.md) : `GET /api/logout`

*   [Get Courses](./endpoints/getCourses.md) : `GET /api/get_courses`

*   [Get Courses Details](./endpoints/getCourses.md) : `GET /api/get_courses`

