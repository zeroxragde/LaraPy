from Libs.Tools import Tools

app = {
    'NOMBRE_APP': Tools.env('NOMBRE_APP') or ' LarapiApp',
    'DB_NAME': Tools.env('DB_NAME') or 'ZeroXDB',
    'DB_MAX_USE': Tools.env('DB_MAX_USE') or 20,
    'API_PORT': Tools.env('API_PORT') or 41,
    'SECRET_KEY': Tools.env('SECRET_KEY') or 'ZeroXVel',
    'TOKEN_EXPIRATION_TIME_SEG': Tools.env('TOKEN_EXPIRATION_TIME_SEG') or 1800,
    "DEBUGGER_MODE": Tools.env('DEBUGGER_MODE') or "",
    "DIR_VIEWS": Tools.env('DIR_VIEWS') or "",
    "DIR_HILOS": Tools.env('DIR_HILOS') or "",
    'DIR_MIDDLEWARE': Tools.env('DIR_MIDDLEWARE') or "",
    "DIR_TAREAS": Tools.env('DIR_TAREAS') or "",
    'DIR_CONFIGURATIONS': Tools.env('DIR_CONFIGURATIONS') or 'Config',
    'DIR_ROUTES': Tools.env('DIR_ROUTES') or 'Routes',
    'DB_PATH': Tools.env('DB_PATH') or 'DB',
}
