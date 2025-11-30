# 📦 جميع الملفات المطلوبة للمشروع

## 📁 الملف 1: `bot.py`
```python
import discord
from discord.ext import commands
from discord import app_commands
import os
from datetime import timedelta

# إعداد البوت
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.moderation = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Developer ID
DEVELOPER_ID = 123456789  # ضع ID الخاص بك هنا

@bot.event
async def on_ready():
    print(f'✅ Bot is ready! Logged in as {bot.user}')
    print(f'Developer: X_ERROR_X')
    try:
        synced = await bot.tree.sync()
        print(f'✅ Synced {len(synced)} commands')
    except Exception as e:
        print(f'❌ Error syncing commands: {e}')

# ========== أوامر الإدارة ==========

@bot.tree.command(name="kick", description="طرد عضو من السيرفر")
@app_commands.describe(member="العضو المراد طرده", reason="سبب الطرد")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "لا يوجد سبب"):
    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("❌ لا يمكنك طرد هذا العضو!", ephemeral=True)
        return
    
    await member.kick(reason=reason)
    
    embed = discord.Embed(
        title="✅ تم طرد العضو",
        color=discord.Color.orange(),
        description=f"**العضو:** {member.mention}\n**السبب:** {reason}\n**بواسطة:** {interaction.user.mention}"
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ban", description="حظر عضو من السيرفر")
@app_commands.describe(member="العضو المراد حظره", reason="سبب الحظر")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "لا يوجد سبب"):
    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("❌ لا يمكنك حظر هذا العضو!", ephemeral=True)
        return
    
    await member.ban(reason=reason)
    
    embed = discord.Embed(
        title="🔨 تم حظر العضو",
        color=discord.Color.red(),
        description=f"**العضو:** {member.mention}\n**السبب:** {reason}\n**بواسطة:** {interaction.user.mention}"
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="unban", description="إلغاء حظر عضو")
@app_commands.describe(user_id="ID العضو المراد إلغاء حظره")
@app_commands.checks.has_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, user_id: str):
    try:
        user = await bot.fetch_user(int(user_id))
        await interaction.guild.unban(user)
        
        embed = discord.Embed(
            title="✅ تم إلغاء الحظر",
            color=discord.Color.green(),
            description=f"**العضو:** {user.mention}\n**بواسطة:** {interaction.user.mention}"
        )
        await interaction.response.send_message(embed=embed)
    except:
        await interaction.response.send_message("❌ لم يتم العثور على العضو أو هو غير محظور!", ephemeral=True)

@bot.tree.command(name="timeout", description="كتم عضو مؤقتاً")
@app_commands.describe(
    member="العضو المراد كتمه",
    duration="المدة بالدقائق",
    reason="سبب الكتم"
)
@app_commands.checks.has_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, member: discord.Member, duration: int, reason: str = "لا يوجد سبب"):
    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("❌ لا يمكنك كتم هذا العضو!", ephemeral=True)
        return
    
    await member.timeout(timedelta(minutes=duration), reason=reason)
    
    embed = discord.Embed(
        title="🔇 تم كتم العضو",
        color=discord.Color.blue(),
        description=f"**العضو:** {member.mention}\n**المدة:** {duration} دقيقة\n**السبب:** {reason}\n**بواسطة:** {interaction.user.mention}"
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="untimeout", description="إلغاء كتم عضو")
@app_commands.describe(member="العضو المراد إلغاء كتمه")
@app_commands.checks.has_permissions(moderate_members=True)
async def untimeout(interaction: discord.Interaction, member: discord.Member):
    await member.timeout(None)
    
    embed = discord.Embed(
        title="✅ تم إلغاء الكتم",
        color=discord.Color.green(),
        description=f"**العضو:** {member.mention}\n**بواسطة:** {interaction.user.mention}"
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="clear", description="حذف عدد من الرسائل")
@app_commands.describe(amount="عدد الرسائل (1-100)")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    if amount < 1 or amount > 100:
        await interaction.response.send_message("❌ يجب أن يكون العدد بين 1 و 100", ephemeral=True)
        return
    
    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"✅ تم حذف {len(deleted)} رسالة", ephemeral=True)

@bot.tree.command(name="lock", description="قفل القناة")
@app_commands.checks.has_permissions(manage_channels=True)
async def lock(interaction: discord.Interaction):
    await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
    await interaction.response.send_message("🔒 تم قفل القناة")

@bot.tree.command(name="unlock", description="فتح القناة")
@app_commands.checks.has_permissions(manage_channels=True)
async def unlock(interaction: discord.Interaction):
    await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
    await interaction.response.send_message("🔓 تم فتح القناة")

@bot.tree.command(name="slowmode", description="تفعيل الوضع البطيء")
@app_commands.describe(seconds="عدد الثواني (0 لإيقافه)")
@app_commands.checks.has_permissions(manage_channels=True)
async def slowmode(interaction: discord.Interaction, seconds: int):
    await interaction.channel.edit(slowmode_delay=seconds)
    if seconds == 0:
        await interaction.response.send_message("✅ تم إيقاف الوضع البطيء")
    else:
        await interaction.response.send_message(f"⏱️ تم تفعيل الوضع البطيء: {seconds} ثانية")

@bot.tree.command(name="warn", description="تحذير عضو")
@app_commands.describe(member="العضو المراد تحذيره", reason="سبب التحذير")
@app_commands.checks.has_permissions(moderate_members=True)
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str = "لا يوجد سبب"):
    embed = discord.Embed(
        title="⚠️ تحذير",
        color=discord.Color.yellow(),
        description=f"**العضو:** {member.mention}\n**السبب:** {reason}\n**بواسطة:** {interaction.user.mention}"
    )
    await interaction.response.send_message(embed=embed)
    
    try:
        dm_embed = discord.Embed(
            title="⚠️ تحذير",
            color=discord.Color.yellow(),
            description=f"تم تحذيرك في **{interaction.guild.name}**\n**السبب:** {reason}"
        )
        await member.send(embed=dm_embed)
    except:
        pass

@bot.tree.command(name="serverinfo", description="معلومات عن السيرفر")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    
    embed = discord.Embed(
        title=f"📊 معلومات {guild.name}",
        color=discord.Color.blue(),
        timestamp=discord.utils.utcnow()
    )
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    embed.add_field(name="👑 المالك", value=guild.owner.mention, inline=True)
    embed.add_field(name="👥 الأعضاء", value=guild.member_count, inline=True)
    embed.add_field(name="📅 تاريخ الإنشاء", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="💬 القنوات", value=len(guild.channels), inline=True)
    embed.add_field(name="🎭 الرتب", value=len(guild.roles), inline=True)
    embed.add_field(name="😀 الإيموجي", value=len(guild.emojis), inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="userinfo", description="معلومات عن عضو")
@app_commands.describe(member="العضو")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    
    embed = discord.Embed(
        title=f"👤 معلومات {member.name}",
        color=member.color,
        timestamp=discord.utils.utcnow()
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="📝 الاسم", value=member.name, inline=True)
    embed.add_field(name="🆔 ID", value=member.id, inline=True)
    embed.add_field(name="📅 انضم للديسكورد", value=member.created_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="📅 انضم للسيرفر", value=member.joined_at.strftime("%Y-%m-%d"), inline=True)
    embed.add_field(name="🎭 الرتب", value=f"{len(member.roles)-1}", inline=True)
    embed.add_field(name="🏆 أعلى رتبة", value=member.top_role.mention, inline=True)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="help", description="قائمة الأوامر")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📚 قائمة الأوامر",
        description="البوت الإداري الاحترافي",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="🛡️ أوامر الإدارة",
        value="`/kick` - طرد عضو\n`/ban` - حظر عضو\n`/unban` - إلغاء حظر\n`/timeout` - كتم مؤقت\n`/untimeout` - إلغاء الكتم\n`/warn` - تحذير عضو",
        inline=False
    )
    
    embed.add_field(
        name="⚙️ أوامر القنوات",
        value="`/clear` - حذف رسائل\n`/lock` - قفل القناة\n`/unlock` - فتح القناة\n`/slowmode` - الوضع البطيء",
        inline=False
    )
    
    embed.add_field(
        name="📊 أوامر المعلومات",
        value="`/serverinfo` - معلومات السيرفر\n`/userinfo` - معلومات العضو\n`/help` - هذه القائمة",
        inline=False
    )
    
    embed.set_footer(text="Developer: X_ERROR_X")
    
    await interaction.response.send_message(embed=embed)

# معالجة الأخطاء
@bot.event
async def on_app_command_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ ليس لديك الصلاحيات الكافية!", ephemeral=True)
    else:
        await interaction.response.send_message(f"❌ حدث خطأ: {str(error)}", ephemeral=True)

# تشغيل البوت
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ Error: DISCORD_TOKEN not found in environment variables")
```

---

## 📁 الملف 2: `requirements.txt`
```
discord.py==2.3.2
python-dotenv==1.0.0
aiohttp==3.9.1
```

---

## 📁 الملف 3: `runtime.txt`
```
python-3.11.0
```

---

## 📁 الملف 4: `.gitignore`
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Database
*.db
*.sqlite
*.sqlite3
```

---

## 📁 الملف 5: `render.yaml`
```yaml
services:
  - type: web
    name: discord-admin-bot
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: python bot.py
    envVars:
      - key: DISCORD_TOKEN
        sync: false
      - key: PYTHON_VERSION
        value: 3.11.0
```

---

## 📁 الملف 6: `README.md`
```markdown
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
   - **Value:** التوكن الذي نسخته من
