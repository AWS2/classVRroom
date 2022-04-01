[:arrow_left: Atras](../README.md)

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


*   [Ping](./endpoints/ping.md) : `GET /api/ping`

*   [Login](./endpoints/login.md) : `GET /api/login`

*   [Logout](./endpoints/logout.md) : `GET /api/logout`

*   [Get Courses](./endpoints/getCourses.md) : `GET /api/get_courses`

*   [Get Courses Details](./endpoints/getCourses.md) : `GET /api/get_courses`

*   [Pin Request](./endpoints/pinRequest.md) : `GET /api/pin_request`

*   [Start Vr Exercise](./endpoints/startVrExercise.md.md) : `GET /api/start_vr_exercise`