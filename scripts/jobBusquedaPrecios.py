import schedule
import time
from datetime import datetime
import PriceAmazon as price

# Define la tarea que deseas ejecutar
def my_task():
    print("Tarea ejecutada. ¡Esto sucede cada minuto!")
    now = datetime.now()
    format = now.strftime('%Y%m%d-%H%M%S')
    print(now)
    print(format)
    price.findPriceFromAmazon(format)

# Programa la tarea para que se ejecute cada 12 horas
#Se ejecuta cada 10 segundos para probar
schedule.every(10).seconds.do(my_task)
#schedule.every(12).hours.do(my_task)
print("Iniciando el scheduler. Presiona Ctrl+C para detener.")

# Ejecuta un bucle infinito para mantener el scheduler funcionando
while True:
    schedule.run_pending()
    time.sleep(1)  # Espera un segundo para evitar consumir demasiados recursos