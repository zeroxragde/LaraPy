from flask import make_response, jsonify

from Enums.ContentType import ContentType
from Enums.HttpStatus import HttpStatus


class Response:

    def __init__(self,  *args):
        self._json = {}
        if len(args)==2:
            self._contructorData(args[0], args[1])
    def _contructorData(self,mensaje, status):
        self._mensaje=mensaje
        self._status = status

    def jsonResponse(self):
        return self._reponseDefault(ContentType.APPLICATION_JSON)
    def htmlResponse(self):
        return self._reponseDefault(ContentType.TEXT_HTML)
    def _reponseDefault(self, type:ContentType):
        if type == ContentType.APPLICATION_JSON:
            self._json['data']=self._mensaje
            return self._response(jsonify(self._json),type,self._status)
        if type == ContentType.TEXT_HTML:
            html='''
            <!DOCTYPE html>
                <html>
                <head>
                  <title>Respuesta API</title>
                  <style>
                    body {
                      font-family: Arial, sans-serif;
                      background-color: #f2f2f2;
                      margin: 0;
                      padding: 0;
                    }
                    
                    .response-container {
                      background-color: #ffffcc;
                      border: 2px solid black;
                      width: 400px;
                      margin: 20px auto;
                      padding: 20px;
                      position: relative;
                    }
                    
                    .response-container h2 {
                      margin: 0;
                      padding: 0;
                      font-size: 20px;
                      font-weight: bold;
                    }
                    
                    .response-container p {
                      margin-top: 10px;
                    }
                    
                    .back-arrow {
                      position: absolute;
                      top: 10px;
                      left: 10px;
                      width: 30px;
                      height: 30px;
                      background-color: #f2f2f2;
                      border: 1px solid black;
                      cursor: pointer;
                    }
                    
                    .back-arrow::before {
                      content: "";
                      position: absolute;
                      top: 50%;
                      left: 50%;
                      transform: translate(-50%, -50%) rotate(-45deg);
                      width: 12px;
                      height: 12px;
                      border-left: 2px solid black;
                      border-bottom: 2px solid black;
                    }
                  </style>
                </head>
                <body>
                  <div class="response-container">
                    <h2>Status: {STATUS}</h2>
                    <p>{MENSAJE}</p>
                    <div class="back-arrow" onclick="goBack()"></div>
                  </div>
                
                  <script>
                    function goBack() {
                      window.history.back();
                    }
                  </script>
                </body>
                </html>
            '''
            return self._response(html.replace("{MENSAJE}",self._mensaje).replace("{STATUS}",self._status.value), type, self._status)

    def jsonCustomResponse(self, json, status:HttpStatus):
        return self._response(json,ContentType.APPLICATION_JSON,status)

    @staticmethod
    def _response(mensaje, typo:ContentType=ContentType.APPLICATION_JSON, status:HttpStatus=HttpStatus.HTTP_OK):
        response = make_response(mensaje, status.value)
        response.headers['Content-Type'] = typo.value
        return response