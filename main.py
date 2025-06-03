from machine import Pin
import network
import time
from wifi import SSID, PASSWORD
from servidor import ServidorFirebase

# Configuración de LEDs
led_rojo = Pin(16, Pin.OUT)
led_amarillo = Pin(17, Pin.OUT)
led_verde = Pin(18, Pin.OUT)

# Configuración Firebase
FIREBASE_URL = "https://pico-w-f4dec-default-rtdb.firebaseio.com/"

# Tiempos de cada fase (en segundos)
TIEMPO_ROJO = 2.0
TIEMPO_AMARILLO = 0.5
TIEMPO_VERDE = 2.0

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    for i in range(10):
        if wlan.isconnected():
            break
        print(f"Conectando WiFi... ({i+1}/10)")
        time.sleep(2)
    
    if wlan.isconnected():
        print(f"¡WiFi OK! IP: {wlan.ifconfig()[0]}")
        return True
    else:
        print("Error: No se pudo conectar al WiFi")
        return False

def ciclo_semaforo(servidor):
    while True:
        modo = servidor.obtener_modo_control()
        
        if modo == "automatico":
            # Modo automático (ciclo normal)
            # 1. FASE ROJA (Detener)
            estado = {"rojo": True, "amarillo": False, "verde": False}
            led_rojo.value(1)
            led_amarillo.value(0)
            led_verde.value(0)
            servidor.actualizar_estado(estado)
            print("Estado: ROJO - Detener")
            time.sleep(TIEMPO_ROJO)
            
            # 2. FASE AMARILLA (Precaución ANTES de verde)
            estado = {"rojo": False, "amarillo": True, "verde": False}
            led_rojo.value(0)
            led_amarillo.value(1)
            servidor.actualizar_estado(estado)
            print("Estado: AMARILLO - Precaución")
            time.sleep(TIEMPO_AMARILLO)
            
            # 3. FASE VERDE (Avanzar)
            estado = {"rojo": False, "amarillo": False, "verde": True}
            led_amarillo.value(0)
            led_verde.value(1)
            servidor.actualizar_estado(estado)
            print("Estado: VERDE - Avanzar")
            time.sleep(TIEMPO_VERDE)
            
            # 4. FASE AMARILLA (Precaución ANTES de rojo)
            estado = {"rojo": False, "amarillo": True, "verde": False}
            led_verde.value(0)
            led_amarillo.value(1)
            servidor.actualizar_estado(estado)
            print("Estado: AMARILLO - Precaución")
            time.sleep(TIEMPO_AMARILLO)
        
        else:
            # Modo manual (controlado desde la web)
            estado_actual = {
                "rojo": led_rojo.value() == 1,
                "amarillo": led_amarillo.value() == 1,
                "verde": led_verde.value() == 1
            }
            servidor.sincronizar_estado_actual(estado_actual)
            time.sleep(0.1)  # Espera corta para respuesta rápida

# Programa principal
if not conectar_wifi():
    print("Reiniciando por fallo de conexión...")
    machine.reset()

# Crear instancia del servidor Firebase
servidor_fb = ServidorFirebase(FIREBASE_URL)

# Iniciar ciclo del semáforo
ciclo_semaforo(servidor_fb)
