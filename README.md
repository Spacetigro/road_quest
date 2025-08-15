# Telegram Quiz Bot

Простой бот для проведения викторин в Telegram.

## 🚀 Запуск на Railway
1. Создай бота через [@BotFather](https://t.me/BotFather) и получи токен.
2. Залей этот проект в свой репозиторий на GitHub.
3. Перейди на [Railway](https://railway.app), создай новый проект → Deploy from GitHub.
4. В **Variables** добавь:
   - `BOT_TOKEN` = токен от BotFather.
5. В **Start Command** укажи:
   ```
   python bot.py
   ```
6. Нажми **Deploy** — бот запустится.

## 📦 Локальный запуск
```bash
pip install -r requirements.txt
export BOT_TOKEN=ТВОЙ_ТОКЕН
python bot.py
```
