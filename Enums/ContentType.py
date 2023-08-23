from enum import Enum

class ContentType(Enum):
    APPLICATION_JSON = 'application/json'
    APPLICATION_XML = 'application/xml'
    APPLICATION_PDF = 'application/pdf'
    APPLICATION_ZIP = 'application/zip'
    TEXT_HTML = 'text/html'
    TEXT_PLAIN = 'text/plain'
    IMAGE_JPEG = 'image/jpeg'
    IMAGE_PNG = 'image/png'
    AUDIO_MPEG = 'audio/mpeg'
    VIDEO_MP4 = 'video/mp4'