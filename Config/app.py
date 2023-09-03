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
    'DIR_MIDDLEWARE': Tools.env('DIR_MIDDLEWARE') or "",
    "DIR_TAREAS": Tools.env('DIR_TAREAS') or "",
    "DEBUGGER_MODE": Tools.env('DEBUGGER_MODE') or "",
    "WEB_FRAMEWORK": Tools.env('WEB_FRAMEWORK') or "RIOTJS",
    "DIR_VIEWS": Tools.env('DIR_VIEWS') or "",
    "DIR_FRAMEWORK_FILES": Tools.env('DIR_FRAMEWORK_FILES') or "",
    "FILE_PATH_INDEX_TEMPLATE": Tools.env('FILE_PATH_INDEX_TEMPLATE') or "",
}