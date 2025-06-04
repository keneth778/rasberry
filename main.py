from machine import Pin, reset
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
    
    if not wlan.isconnected():
        print('Conectando a la red...')
        wlan.connect(SSID, PASSWORD)
        
        for i in range(10):
            if wlan.isconnected():
                break
            print(f"Intentando conectar... ({i+1}/10)")
            time.sleep(2)
    
    if wlan.isconnected():
        print('¡Conexión exitosa!')
        print('Configuración de red:', wlan.ifconfig())
        return True
    else:
        print('No se pudo conectar a la red')
        return False

def inicializar_firebase(servidor):
    # Forzar modo automático al inicio
    servidor.establecer_modo_automatico()
    # Establecer estado inicial (rojo)
    estado_inicial = {"rojo": True, "amarillo": False, "verde": False}
    servidor.actualizar_estado(estado_inicial)
    return estado_inicial

def ciclo_semaforo(servidor):
    print("Iniciando ciclo del semáforo...")
    estado_actual = {"rojo": True, "amarillo": False, "verde": False}
    
    while True:
        try:
            modo = servidor.obtener_modo_control()
            print("Modo actual:", modo)
            
            if modo == "automatico":
                # Modo automático (ciclo normal)
                # 1. FASE ROJA (Detener)
                estado_actual = {"rojo": True, "amarillo": False, "verde": False}
                led_rojo.value(1)
                led_amarillo.value(0)
                led_verde.value(0)
                servidor.actualizar_estado(estado_actual)
                print("Estado: ROJO - Detener")
                time.sleep(TIEMPO_ROJO)
                
                # 2. FASE AMARILLA (Precaución ANTES de verde)
                estado_actual = {"rojo": False, "amarillo": True, "verde": False}
                led_rojo.value(0)
                led_amarillo.value(1)
                servidor.actualizar_estado(estado_actual)
                print("Estado: AMARILLO - Precaución")
                time.sleep(TIEMPO_AMARILLO)
                
                # 3. FASE VERDE (Avanzar)
                estado_actual = {"rojo": False, "amarillo": False, "verde": True}
                led_amarillo.value(0)
                led_verde.value(1)
                servidor.actualizar_estado(estado_actual)
                print("Estado: VERDE - Avanzar")
                time.sleep(TIEMPO_VERDE)
                
                # 4. FASE AMARILLA (Precaución ANTES de rojo)
                estado_actual = {"rojo": False, "amarillo": True, "verde": False}
                led_verde.value(0)
                led_amarillo.value(1)
                servidor.actualizar_estado(estado_actual)
                print("Estado: AMARILLO - Precaución")
                time.sleep(TIEMPO_AMARILLO)
            
            else:
                # Modo manual (controlado desde la web)
                estado_firebase = servidor.obtener_estado_actual()
                if estado_firebase:
                    led_rojo.value(1 if estado_firebase.get("rojo") == "ON" else 0)
                    led_amarillo.value(1 if estado_firebase.get("amarillo") == "ON" else 0)
                    led_verde.value(1 if estado_firebase.get("verde") == "ON" else 0)
                    estado_actual = {
                        "rojo": estado_firebase.get("rojo") == "ON",
                        "amarillo": estado_firebase.get("amarillo") == "ON",
                        "verde": estado_firebase.get("verde") == "ON"
                    }
                time.sleep(0.5)
        
        except Exception as e:
            print("Error en el ciclo:", str(e))
            time.sleep(5)

# Programa principal
print("Iniciando programa...")
if not conectar_wifi():
    print("Reiniciando por fallo de conexión...")
    reset()

# Crear instancia del servidor Firebase
try:
    servidor_fb = ServidorFirebase(FIREBASE_URL)
    print("Servidor Firebase inicializado")
    # Inicializar Firebase con valores por defecto
    estado_inicial = inicializar_firebase(servidor_fb)
    # Establecer estado inicial en los LEDs
    led_rojo.value(1 if estado_inicial["rojo"] else 0)
    led_amarillo.value(1 if estado_inicial["amarillo"] else 0)
    led_verde.value(1 if estado_inicial["verde"] else 0)
except Exception as e:
    print("Error al inicializar Firebase:", str(e))
    reset()

# Iniciar ciclo del semáforo
ciclo_semaforo(servidor_fb)
