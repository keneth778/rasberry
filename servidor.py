import urequests
import ujson
import time

class ServidorFirebase:
    def __init__(self, firebase_url):
        self.base_url = firebase_url.rstrip('/') + '/'  # Asegurar formato correcto
        self.semaforo_path = "semaforo.json"
        self.control_path = "control.json"
        print("Configurado Firebase en:", self.base_url)
    
    def establecer_modo_automatico(self):
        """Establece el modo automático en Firebase"""
        try:
            data = {"modo": "automatico"}
            url = self.base_url + self.control_path
            print("Estableciendo modo automático...")
            response = urequests.put(url, json=data)
            response.close()
            return True
        except Exception as e:
            print(f"Error estableciendo modo automático: {str(e)}")
            return False
    
    def actualizar_estado(self, estado):
        """Actualiza el estado del semáforo en Firebase"""
        try:
            data = {
                "rojo": "ON" if estado.get("rojo", False) else "OFF",
                "amarillo": "ON" if estado.get("amarillo", False) else "OFF",
                "verde": "ON" if estado.get("verde", False) else "OFF"
            }
            url = self.base_url + self.semaforo_path
            print("Actualizando estado en:", url)
            response = urequests.put(url, json=data)
            response.close()
            return True
        except Exception as e:
            print(f"Error actualizando Firebase: {str(e)}")
            return False
    
    def obtener_modo_control(self):
        """Obtiene el modo de control desde Firebase"""
        try:
            url = self.base_url + self.control_path
            print("Obteniendo modo de:", url)
            response = urequests.get(url)
            control = response.json()
            response.close()
            return control.get("modo", "automatico")
        except Exception as e:
            print(f"Error leyendo control: {str(e)}")
            return "automatico"
    
    def obtener_estado_actual(self):
        """Obtiene el estado actual del semáforo desde Firebase"""
        try:
            url = self.base_url + self.semaforo_path
            print("Obteniendo estado de:", url)
            response = urequests.get(url)
            estado = response.json()
            response.close()
            return estado
        except Exception as e:
            print(f"Error leyendo estado semáforo: {str(e)}")
            return None
    
    def sincronizar_estado_actual(self, estado):
        """Sincroniza el estado actual con Firebase"""
        return self.actualizar_estado(estado)
