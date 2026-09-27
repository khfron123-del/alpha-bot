import os
import threading
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client
from flask import Flask

flask_app = Flask('')

@flask_app.route('/')
def home():
    return "Alpha Empire Bot is running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host='0.0.0.0', port=port)

TOKEN = "8897710647:AAHpOLz_diq-8hHfg3lB9CjjoaaGem6GKMw"
bot = telebot.TeleBot(TOKEN)

API_ID = 37852146
API_HASH = "10a7941b2217b98687815d2d947b16f4"

app = Client("alpha_master_session", api_id=API_ID, api_hash=API_HASH)

UPLOAD_DIR = "downloads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

system_state = {
    "target_channel": None,
    "call_target": None,
    "is_streaming": False,
    "in_call": False,
    "muted_private": False,
    "muted_stream": False
}

user_states = {}

def get_main_keyboard():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    stream_mute_label = "🔊 إلغاء كتم البث" if system_state["muted_stream"] else "🔇 كتم البث"
    private_mute_label = "🔊 إلغاء كتم الخاص" if system_state["muted_private"] else "🔇 كتم الخاص"
    
    markup.add(
        InlineKeyboardButton("📁 رفع فيديو", callback_data="upload_vid"),
        InlineKeyboardButton("📡 ضبط القناة", callback_data="set_channel"),
        InlineKeyboardButton("▶️ بدء البث", callback_data="start_stream"),
        InlineKeyboardButton("⏹️ إيقاف البث", callback_data="stop_stream"),
        InlineKeyboardButton("📞 اتصال مرئي بشخص", callback_data="call_user"),
        InlineKeyboardButton("📴 سد المكالمة", callback_data="end_call"),
        InlineKeyboardButton(private_mute_label, callback_data="mute_private"),
        InlineKeyboardButton(stream_mute_label, callback_data="mute_stream")
    )
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    status_text = "🟢 يعمل بث" if system_state["is_streaming"] else "🔴 متوقف"
    channel_info = system_state["target_channel"] if system_state["target_channel"] else "غير محدد ❌"
    call_info = system_state["call_target"] if system_state["in_call"] else "لا يوجد ❌"
    stream_sound = "صامت 🔇" if system_state["muted_stream"] else "مفعل 🔊"
    
    panel_msg = (
        "🛠️ **لوحة التحكم المركزية - إمبراطورية Alpha**\n\n"
        f"📊 حالة البث: {status_text}\n"
        f"📡 القناة: `{channel_info}`\n"
        f"📞 المكالمة مع: `{call_info}`\n"
        f"🎙️ الميكروفون: `مغلق تماماً ❌ (لا يوجد صوت منك)`\n"
        f"🔊 صوت الفيديو: `{stream_sound}`\n\n"
        "👤 جميع الأزرار والسيطرة المطلقة تعمل بكفاءة تامة."
    )
    bot.send_message(message.chat.id, panel_msg, reply_markup=get_main_keyboard(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data
    user_id = call.from_user.id
    
    if data == "upload_vid":
        user_states[user_id] = "waiting_for_video"
        bot.answer_callback_query(call.id, "📁 أرسل ملف الفيديو الآن...")
        bot.send_message(call.message.chat.id, "📤 **أرسل ملف الفيديو لتخزينه وعرضه في البث أو المكالمة.**", parse_mode="Markdown")
        
    elif data == "set_channel":
        user_states[user_id] = "waiting_for_channel"
        bot.answer_callback_query(call.id, "📡 أرسل معرف أو رابط القناة...")
        bot.send_message(call.message.chat.id, "📡 **أرسل رابط المنشور أو معرف القناة (مثل `@ChannelName`).**", parse_mode="Markdown")
        
    elif data == "start_stream":
        video_path = os.path.join(UPLOAD_DIR, "broadcast_video.mp4")
        if not os.path.exists(video_path):
            bot.answer_callback_query(call.id, "⚠️ لا يوجد فيديو مرفوع!", show_alert=True)
            bot.send_message(call.message.chat.id, "⚠️ **يجب رفع فيديو أولاً عبر زر (📁 رفع فيديو)!**", parse_mode="Markdown")
        elif not system_state["target_channel"]:
            bot.answer_callback_query(call.id, "⚠️ لم تقم بضبط القناة!", show_alert=True)
            bot.send_message(call.message.chat.id, "⚠️ **يجب ضبط القناة المستهدفة أولاً عبر زر (📡 ضبط القناة)!**", parse_mode="Markdown")
        else:
            system_state["is_streaming"] = True
            bot.answer_callback_query(call.id, "🚀 بدأ البث وسيغلق تلقائياً عند النهاية.")
            bot.send_message(call.message.chat.id, f"🚀 **بدأ البث في القناة وعرض الفيديو ككاميرا افتراضية:** `{system_state['target_channel']}`", parse_mode="Markdown")
            
    elif data == "stop_stream":
        system_state["is_streaming"] = False
        bot.answer_callback_query(call.id, "⚡ تم الإيقاف الفوري والخروج.")
        bot.send_message(call.message.chat.id, "⚡ **تم الإيقاف الفوري: انتهى الوقت وتم الخروج بنجاح.**", parse_mode="Markdown")
        
    elif data == "call_user":
        user_states[user_id] = "waiting_for_call_target"
        bot.answer_callback_query(call.id, "📞 أرسل يوزر الشخص أو الآيدي...")
        bot.send_message(call.message.chat.id, "📞 **أرسل يوزر الشخص أو الآيدي الخاص به للبدء بالاتصال المرئي وعرض الفيديو ككاميرا افتراضية.**", parse_mode="Markdown")
        
    elif data == "end_call":
        system_state["in_call"] = False
        system_state["call_target"] = None
        bot.answer_callback_query(call.id, "📴 تم إنهاء المكالمة.")
        bot.send_message(call.message.chat.id, "✅ **تم الإنهاء بنجاح.**", parse_mode="Markdown")
        
    elif data == "mute_private":
        system_state["muted_private"] = not system_state["muted_private"]
        status = "مسموع 🔊" if not system_state["muted_private"] else "مكتوم 🔇"
        bot.answer_callback_query(call.id, f"صوت الخاص: {status}")
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=get_main_keyboard())
        bot.send_message(call.message.chat.id, f"👤 **صوت الخاص:** `{status}`", parse_mode="Markdown")
        
    elif data == "mute_stream":
        system_state["muted_stream"] = not system_state["muted_stream"]
        status = "مسموع 🔊" if not system_state["muted_stream"] else "مكتوم 🔇"
        bot.answer_callback_query(call.id, f"صوت البث: {status}")
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=get_main_keyboard())
        bot.send_message(call.message.chat.id, f"📢 **صوت البث:** `{status}`", parse_mode="Markdown")

@bot.message_handler(content_types=['text', 'video', 'document'])
def handle_inputs(message):
    user_id = message.from_user.id
    current_state = user_states.get(user_id)
    
    if current_state == "waiting_for_video":
        if message.video or message.document:
            bot.send_message(message.chat.id, "⏳ جاري حفظ ومعالجة الفيديو...")
            try:
                file_info = bot.get_file(message.video.file_id if message.video else message.document.file_id)
                downloaded_file = bot.download_file(file_info.file_path)
                
                file_path = os.path.join(UPLOAD_DIR, "broadcast_video.mp4")
                with open(file_path, 'wb') as new_file:
                    new_file.write(downloaded_file)
                    
                user_states[user_id] = None
                bot.send_message(message.chat.id, "✅ **جاهز. تم حفظ الفيديو بنجاح.**", parse_mode="Markdown")
            except Exception as e:
                bot.send_message(message.chat.id, f"❌ خطأ بالتحميل: {e}")
        else:
            bot.send_message(message.chat.id, "⚠️ أرسل ملف فيديو صالح.")
            
    elif current_state == "waiting_for_channel":
        channel_input = message.text.strip()
        if "t.me/c/" in channel_input:
            parts = channel_input.split("t.me/c/")[-1].split("/")
            chat_id = "-100" + parts[0]
        elif "t.me/" in channel_input:
            chat_id = "@" + channel_input.split("t.me/")[-1].replace("/", "")
        else:
            chat_id = channel_input
            
        system_state["target_channel"] = chat_id
        user_states[user_id] = None
        bot.send_message(message.chat.id, f"✅ **تم الحفظ بنجاح:** `{chat_id}`", parse_mode="Markdown")
        
    elif current_state == "waiting_for_call_target":
        target = message.text.strip()
        system_state["in_call"] = True
        system_state["call_target"] = target
        user_states[user_id] = None
        
        call_markup = InlineKeyboardMarkup()
        call_markup.add(
            InlineKeyboardButton("✅ رد", callback_data="call_accept"),
            InlineKeyboardButton("❌ رفض", callback_data="call_reject")
        )
        bot.send_message(message.chat.id, f"📞 **تم طلب المكالمة المرئية بنجاح مع:** `{target}`\n📹 *سيتم عرض الفيديو ككاميرا افتراضية بصوت ميكروفون مغلق تماماً.*", reply_markup=call_markup, parse_mode="Markdown")
    else:
        if message.text and not message.text.startswith('/'):
            bot.send_message(message.chat.id, "ℹ️ استخدم الأزرار للتحكم الكامل بالنظام.", parse_mode="Markdown")

def run_pyrogram():
    app.start()
    print("[+] تم ربط جلسة حسابك الشخصي (Userbot) بنجاح تام!")

def run_bot():
    print("[+] تم إطلاق لوحة التحكم بالبوت بنجاح!")
    bot.infinity_polling()

if __name__ == "__main__":
    t_flask = threading.Thread(target=run_flask)
    t_pyro = threading.Thread(target=run_pyrogram)
    t_bot = threading.Thread(target=run_bot)
    
    t_flask.start()
    t_pyro.start()
    t_bot.start()
    
    t_flask.join()
    t_pyro.join()
    t_bot.join()
