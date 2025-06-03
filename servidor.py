import urequests
import ujson
import time

class ServidorFirebase:
    def __init__(self, firebase_url):
        self.base_url = firebase_url
        self.semaforo_path = "semaforo.json"
        self.control_path = "control.json"
    
    def actualizar_estado(self, estado):
        """Actualiza el estado del semáforo en Firebase"""
        try:
            data = {
                "rojo": "ON" if estado["rojo"] else "OFF",
                "amarillo": "ON" if estado["amarillo"] else "OFF",
                "verde": "ON" if estado["verde"] else "OFF"
            }
            response = urequests.put(self.base_url + self.semaforo_path, json=data)
            response.close()
            return True
        except Exception as e:
            print(f"Error actualizando Firebase: {str(e)}")
            return False
    
    def obtener_modo_control(self):
        """Obtiene el modo de control desde Firebase"""
        try:
            response = urequests.get(self.base_url + self.control_path)
            control = response.json()
            response.close()
            return control.get("modo", "automatico")
        except Exception as e:
            print(f"Error leyendo control: {str(e)}")
            return "automatico"
    
    def sincronizar_estado_actual(self, estado):
        """Sincroniza el estado actual con Firebase"""
        return self.actualizar_estado(estado)
