# 🤖 Discord Admin Bot

بوت Discord إداري احترافي مع واجهة بالعربية

**Developer:** X_ERROR_X

## ✨ المميزات

### 🛡️ أوامر الإدارة
- `/kick` - طرد عضو من السيرفر
- `/ban` - حظر عضو نهائياً
- `/unban` - إلغاء حظر عضو
- `/timeout` - كتم عضو مؤقتاً
- `/untimeout` - إلغاء الكتم
- `/warn` - تحذير عضو

### ⚙️ إدارة القنوات
- `/clear` - حذف رسائل متعددة (1-100)
- `/lock` - قفل القناة
- `/unlock` - فتح القناة
- `/slowmode` - تفعيل الوضع البطيء

### 📊 معلومات
- `/serverinfo` - معلومات السيرفر
- `/userinfo` - معلومات عضو معين
- `/help` - قائمة جميع الأوامر

## 🚀 التنصيب على Render

### 1. إنشاء بوت Discord

1. اذهب إلى [Discord Developer Portal](https://discord.com/developers/applications)
2. انقر على "New Application"
3. اختر اسماً للبوت
4. اذهب إلى تبويب "Bot"
5. انقر على "Add Bot"
6. فعّل هذه الخيارات:
   - **SERVER MEMBERS INTENT**
   - **MESSAGE CONTENT INTENT**
   - **PRESENCE INTENT**
7. انسخ الـ Token

### 2. رفع الكود على GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin YOUR_REPO_URL
git push -u origin main
```

### 3. النشر على Render

1. اذهب إلى [Render.com](https://render.com)
2. سجّل دخول وانقر على "New +"
3. اختر "Web Service"
4. اربط حساب GitHub الخاص بك
5. اختر المستودع (Repository)
6. املأ التفاصيل:
   - **Name:** discord-admin-bot
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
7. أضف Environment Variable:
   - **Key:** `DISCORD_TOKEN`
   - **Value:** التوكن الذي نسخته من Discord
8. انقر على "Create Web Service"

### 4. دعوة البوت للسيرفر

استخدم هذا الرابط لإضافة البوت:
