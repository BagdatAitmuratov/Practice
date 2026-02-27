from datetime import datetime, timedelta

# Бүгінгі күннен 5 күнді азайту
today = datetime.now()
five_days_ago = today - timedelta(days=5)

print("Бүгін:", today.strftime("%Y-%m-%d"))
print("5 күн бұрын:", five_days_ago.strftime("%Y-%m-%d"))