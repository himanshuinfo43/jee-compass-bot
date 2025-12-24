from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import sqlite3

# 🔑 BOT TOKEN
import os
BOT_TOKEN = os.getenv("BOT_TOKEN")


# ---------- DATABASE FUNCTIONS ----------

def get_chapter(name):
    conn = sqlite3.connect("physics.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM chapters WHERE chapter=?", (name,))
    row = cur.fetchone()
    conn.close()
    return row

def get_all_chapters():
    conn = sqlite3.connect("physics.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM chapters")
    rows = cur.fetchall()
    conn.close()
    return rows

def score(row):
    return (row[3] * 3) + (row[4] * 2) - row[5]

# ---------- BOT COMMANDS ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to JEE Compass 📍\n\n"
        "Commands:\n"
        "/importance <chapter>\n"
        "/compare <chapter1> <chapter2>\n"
        "/revision <days>\n\n"
        "Example:\n/compare Electrostatics Current Electricity"
    )

async def importance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chapter = " ".join(context.args)
    row = get_chapter(chapter)

    if not row:
        await update.message.reply_text("❌ Chapter not found")
        return

    s = score(row)

    await update.message.reply_text(
        f"📘 {row[2]}\n"
        f"Importance Score: {s}\n"
        f"Weightage: {row[3]}/5\n"
        f"PYQs: {row[4]}\n"
        f"Difficulty: {row[5]}/3\n"
        f"Revision Time: {row[6]} hrs"
    )

async def compare(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /compare ch1 ch2")
        return

    ch1 = context.args[0]
    ch2 = " ".join(context.args[1:])

    r1 = get_chapter(ch1)
    r2 = get_chapter(ch2)

    if not r1 or not r2:
        await update.message.reply_text("❌ Chapter name wrong")
        return

    s1 = score(r1)
    s2 = score(r2)

    better = r1[2] if s1 > s2 else r2[2]

    await update.message.reply_text(
        f"⚖️ Comparison Result\n\n"
        f"{better} is MORE IMPORTANT\n\n"
        f"{r1[2]}: {s1}\n"
        f"{r2[2]}: {s2}"
    )

async def revision(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        days = int(context.args[0])
    except:
        await update.message.reply_text("Usage: /revision 3")
        return

    chapters = get_all_chapters()
    chapters.sort(key=score, reverse=True)

    msg = "📅 Revision Plan:\n\n"
    for i in range(min(days, len(chapters))):
        msg += f"Day {i+1}: {chapters[i][2]} ({chapters[i][6]} hrs)\n"

    await update.message.reply_text(msg)

# ---------- RUN BOT ----------

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("importance", importance))
app.add_handler(CommandHandler("compare", compare))
app.add_handler(CommandHandler("revision", revision))

print("🔥 JEE Compass Bot Running...")
app.run_polling()

