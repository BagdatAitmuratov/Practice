from datetime import datetime, timedelta


current_date = datetime.now()
five_days_ago = current_date - timedelta(days=5)
print(f"After 5 days: {five_days_ago.strftime('%Y-%m-%d')}")


today = datetime.now().date()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
print(f"Yesterday: {yesterday} | Today: {today} | Tommarrow: {tomorrow}")


now_no_ms = datetime.now().replace(microsecond=0)
print(f"without microsecoud: {now_no_ms}")


d1 = datetime(2026, 2, 27, 12, 0, 0)
d2 = datetime(2026, 2, 28, 12, 0, 0)
print(f"Diference: {abs((d2 - d1).total_seconds())} sec")