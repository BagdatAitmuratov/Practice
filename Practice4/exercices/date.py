from datetime import datetime, timedelta

# 5 күн азайту
current_date = datetime.now()
five_days_ago = current_date - timedelta(days=5)
print(f"5 күн бұрын: {five_days_ago.strftime('%Y-%m-%d')}")

#Кеше бүгін ертең
today = datetime.now().date()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print(f"Кеше: {yesterday} | Бүгін: {today} | Ертең: {tomorrow}")

#Микросекундтарды алып тастау
now_no_ms = datetime.now().replace(microsecond=0)
print(f"Микросекундсыз: {now_no_ms}")

#Екі күннің айырмашылығы секундпен
d1 = datetime(2026, 2, 27, 12, 0, 0)
d2 = datetime(2026, 2, 28, 12, 0, 0)
print(f"Айырмашылық: {abs((d2 - d1).total_seconds())} секунд")