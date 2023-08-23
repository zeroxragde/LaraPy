from enum import Enum

class HttpStatus(Enum):
    HTTP_CONTINUAR = '100 Continuar'
    HTTP_CAMBIO_PROTOCOLOS = '101 Cambio de protocolos'
    HTTP_PROCESANDO = '102 Procesando'
    HTTP_INDICACIONES_PREVIAS = '103 Indicaciones previas'
    HTTP_OK = '200 OK'
    HTTP_CREADO = '201 Creado'
    HTTP_ACEPTADO = '202 Aceptado'
    HTTP_INFORMACION_NO_AUTORIZADA = '203 Información no autorizada'
    HTTP_SIN_CONTENIDO = '204 Sin contenido'
    HTTP_REINICIAR_CONTENIDO = '205 Reiniciar contenido'
    HTTP_CONTENIDO_PARCIAL = '206 Contenido parcial'
    HTTP_MULTI_ESTADO = '207 Multi-Estado'
    HTTP_YA_INFORMADO = '208 Ya informado'
    HTTP_UTILIZADO = '226 Utilizado'
    HTTP_MULTIPLES_OPCIONES = '300 Múltiples opciones'
    HTTP_MOVIDO_PERMANENTEMENTE = '301 Movido permanentemente'
    HTTP_ENCONTRADO = '302 Encontrado'
    HTTP_VER_OTRO = '303 Ver otro'
    HTTP_NO_MODIFICADO = '304 No modificado'
    HTTP_UTILIZAR_PROXY = '305 Utilizar proxy'
    HTTP_REDIRIGIR_TEMPORALMENTE = '307 Redirigir temporalmente'
    HTTP_REDIRIGIR_PERMANENTEMENTE = '308 Redirigir permanentemente'
    HTTP_SOLICITUD_INCORRECTA = '400 Solicitud incorrecta'
    HTTP_NO_AUTORIZADO = '401 No autorizado'
    HTTP_PAGO_REQUERIDO = '402 Pago requerido'
    HTTP_PROHIBIDO = '403 Prohibido'
    HTTP_NO_ENCONTRADO = '404 No encontrado'
    HTTP_METODO_NO_PERMITIDO = '405 Método no permitido'
    HTTP_NO_ACEPTABLE = '406 No aceptable'
    HTTP_REQUIERE_AUTENTICACION_PROXY = '407 Requiere autenticación proxy'
    HTTP_TIEMPO_LIMITE_ESPERA = '408 Tiempo límite de espera'
    HTTP_CONFLICTO = '409 Conflicto'
    HTTP_NO_DISPONIBLE = '410 No disponible'
    HTTP_LONGITUD_REQUERIDA = '411 Longitud requerida'
    HTTP_PRECONDICION_FALLIDA = '412 Precondición fallida'
    HTTP_ENTIDAD_SOLICITADA_MUY_GRANDE = '413 Entidad solicitada muy grande'
    HTTP_URL_SOLICITADA_MUY_LARGA = '414 URL solicitada muy larga'
    HTTP_TIPO_MEDIO_NO_SOPORTADO = '415 Tipo de medio no soportado'
    HTTP_RANGO_NO_SATISFACTORIO = '416 Rango no satisfactorio'
    HTTP_ESPERA_FALLIDA = '417 Espera fallida'
    HTTP_SOY_UN_TETERA = '418 Soy una tetera'
    HTTP_SOLICITUD_INCORRECTA_DESTINO = '421 Solicitud incorrecta en el destino'
    HTTP_ENTIDAD_NO_PROCESABLE = '422 Entidad no procesable'
    HTTP_BLOQUEADO = '423 Bloqueado'
    HTTP_DEPENDENCIA_FALLIDA = '424 Dependencia fallida'
    HTTP_PRECONDICIONES_NO_CUMPLIDAS = '428 Precondiciones no cumplidas'
    HTTP_TROPAS_SOLICITADAS_EXCESO = '429 Tropas solicitadas en exceso'
    HTTP_CAMPOS_ENCABEZADO_SOLICITUD_MUY_GRANDES = '431 Campos de encabezado de la solicitud muy grandes'
    HTTP_NO_DISPONIBLE_POR_RAZONES_LEGALES = '451 No disponible por razones legales'
    HTTP_ERROR_INTERNO_SERVIDOR = '500 Error interno del servidor'
    HTTP_NO_IMPLEMENTADO = '501 No implementado'
    HTTP_GATEWAY_INCORRECTO = '502 Gateway incorrecto'
    HTTP_SERVICIO_NO_DISPONIBLE = '503 Servicio no disponible'
    HTTP_TIEMPO_LIMITE_GATEWAY = '504 Tiempo límite del gateway'
    HTTP_VERSION_HTTP_NO_SOPORTADA = '505 Versión HTTP no soportada'
    HTTP_VARIANTE_NEGOCIAR = '506 Variante a negociar'
    HTTP_ALMACENAMIENTO_INSUFICIENTE = '507 Almacenamiento insuficiente'
    HTTP_DETECCION_BUCLE = '508 Detección de bucle'
    HTTP_NO_EXTENDIDO = '510 No extendido'
    HTTP_AUTENTICACION_REQUERIDA_RED = '511 Autenticación requerida en red'