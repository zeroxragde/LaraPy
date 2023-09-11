from Libs.Tools import Tools

app = {
    'NOMBRE_APP': Tools.env('NOMBRE_APP') or ' LarapiApp',
    'DB_PATH': Tools.env('DB_PATH') or 'DB',
    'DB_NAME': Tools.env('DB_NAME') or 'ZeroXDB',
    'DB_MAX_USE': Tools.env('DB_MAX_USE') or 20,
    'DIR_ROUTES': Tools.env('DIR_ROUTES') or 'Routes',
    'API_PORT': Tools.env('API_PORT') or 41,
    'DIR_CONFIGURATIONS': Tools.env('DIR_CONFIGURATIONS') or 'Config',
    'SECRET_KEY': Tools.env('SECRET_KEY') or 'ZeroXVel',
    'TOKEN_EXPIRATION_TIME_SEG': Tools.env('TOKEN_EXPIRATION_TIME_SEG') or 1800,
    'YOUTUBE_DEVELOPER_KEY': Tools.env('YOUTUBE_DEVELOPER_KEY') or "",
    'YOUTUBE_API_VERSION': Tools.env('YOUTUBE_API_VERSION') or "",
    'YOUTUBE_TOKEN': Tools.env('YOUTUBE_TOKEN') or "",
    'YOUTUBE_API_SERVICE_NAME': Tools.env('YOUTUBE_API_SERVICE_NAME') or "",
    'DIR_MIDDLEWARE': Tools.env('DIR_MIDDLEWARE') or "",
    "DIR_TAREAS": Tools.env('DIR_TAREAS') or "",
    "DEBUGGER_MODE":Tools.env('DEBUGGER_MODE') or "",
}