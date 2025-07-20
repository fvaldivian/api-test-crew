from crewai.tools import BaseTool
from typing import Optional,Type
from pydantic import BaseModel, Field
import requests


class HttpExecutorSchema(BaseModel):
    method: str = Field(..., description="Método HTTP a utilizar.")
    url: str = Field(..., description="URL completa del endpoint al que se va a realizar la petición.")
    params: Optional[dict] = Field(default=None, description="Parámetros de consulta a incluir en la URL. Debe ser un diccionario")
    json: Optional[dict] = Field(default=None, description="Cuerpo de la petición en formato JSON. Solo se utiliza en métodos como POST o PUT.")
    headers: Optional[dict] = Field(default=None, description="Cabeceras HTTP adicionales a incluir en la petición. Debe ser un diccionario.")

class HttpExecutorTool(BaseTool):
    name: str = "Herramienta de Ejecución HTTP"
    description: str = "Ejecuta peticiones HTTP contra un endpoint específico y devuelve la respuesta."
    args_schema: Type[HttpExecutorSchema] = HttpExecutorSchema

    def _run(self, method: str, url: str, params: dict = None, json: dict = None, headers: dict = None) -> dict:
        try:
            resp = self._send_request(method, url, params, json, headers)
            return self._parse_response(resp)
        except Exception as e:
            return self._handle_exception(e, url)

    def _send_request(self, method: str, url: str, params: dict, json: dict, headers: dict):
        return requests.request(method.upper(), url, params=params, json=json, headers=headers)

    def _parse_response(self, resp) -> dict:
        result = {
            "status_code": resp.status_code,
            "url": resp.url
        }
        try:
            result["json"] = resp.json()
        except Exception:
            result["content"] = resp.text
        return result

    def _handle_exception(self, e, fallback_url) -> dict:
        result = {"error": str(e)}
        resp = getattr(e, "response", None)
        result["status_code"] = resp.status_code if resp is not None else None
        result["headers"] = dict(resp.headers) if resp is not None else None
        result["url"] = resp.url if resp is not None else fallback_url
        if resp is not None:
            try:
                result["json"] = resp.json()
            except Exception:
                result["content"] = resp.text
        return result