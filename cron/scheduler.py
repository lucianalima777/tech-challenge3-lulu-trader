import schedule
import time
import os
from datetime import datetime

def job():
    print(f"[{datetime.now()}] Executando coleta...")
    os.system("python src/data_collection/app.py")

# Agendamento para executar uma vez ao dia, às 9h
schedule.every().day.at("09:00").do(job)

print("Agendador iniciado. Pressione Ctrl+C para parar.")

while True:
    schedule.run_pending()
    time.sleep(60)
