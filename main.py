from flask import Flask, request, jsonify, render_template_string
from bot import ask_ai
import json, os
from datetime import datetime

app = Flask(__name__, static_folder="static")  # <- اینجا هم name رو باید __name__ بذاری
FEEDBACK_FILE = "feedback.json"

def save_feedback(data):
    feedbacks = []  # پیشفرض

    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            try:
                feedbacks = json.load(f)
            except Exception:
                feedbacks = []

    data["time"] = datetime.now().strftime("%H:%M")
    feedbacks.append(data)
    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(feedbacks, f, ensure_ascii=False, indent=2)


@app.route("/")
def index(): 
    return render_template_string("""

<!DOCTYPE html>  <html lang="fa">  
<meta name="google-site-verification" content="HjrtrUik26UFlKsbD5anwM0FOW5EzQiSMelGs9o0Q0Q" />
<head>
<script>
            !function(e,t,n){e.yektanetAnalyticsObject=n,e[n]=e[n]||function(){e[n].q.push(arguments)},e[n].q=e[n].q||[];var a=t.getElementsByTagName("head")[0],r=new Date,c="https://cdn.yektanet.com/superscript/MLudF3eR/native-Redlighte.ir-45400/yn_pub.js?v="+r.getFullYear().toString()+"0"+r.getMonth()+"0"+r.getDate()+"0"+r.getHours(),s=t.createElement("link");s.rel="preload",s.as="script",s.href=c,a.appendChild(s);var l=t.createElement("script");l.async=!0,l.src=c,a.appendChild(l)}(window,document,"yektanet");
        </script>
<meta name="google-site-verification" content="v10a70r4wwCAfx1nS31l8sJT4cwykghFkAkvSeJRPgY" />
<meta charset="UTF-8">  
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" href="/static/favicon.png" type="image/png">
<title>Redlighte chat | هوش مصنوعي ردلايت</title>  <link href="https://cdn.jsdelivr.net/gh/rastikerdar/vazir-font@v30.1.0/dist/font-face.css" rel="stylesheet">  <style>  
@font-face {  
    font-family: 'Pacifico';  
    src: url('/static/pacifico-regular.ttf') format('truetype');  
    font-weight: 400;  
    font-style: normal;  
}  
  
* { font-family:'Vazir',Tahoma,sans-serif !important; font-weight:700; box-sizing:border-box; }  
:root{--chat-bg:#fff;--bot:#f1f1f1;--user:#8b0000;--text:#000;--theme-text:#000}  
body.dark{--chat-bg:#1e1e1e;--bot:#2b2b2b;--user:#cc0000;--text:#fff;--theme-text:#fff;}  
  
body{margin:0;height:100vh;display:flex;flex-direction:column;align-items:center;  
 background:linear-gradient(-45deg,#b30000,#ff1a1a,#660000,#cc0000);  
 background-size:400% 400%;animation:bg 12s ease infinite;}  
@keyframes bg{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}  
  
.chat-container{width:100%;max-width:420px;height:78vh;margin-top:20px;  
 background:var(--chat-bg);border-radius:20px;  
 box-shadow:0 10px 30px rgba(0,0,0,.35);  
 display:flex;flex-direction:column;overflow:hidden;}  
  
.chat-header{text-align:center;padding:6px 0;border-bottom:1px solid rgba(0,0,0,.15);position:relative;}  
  
.chat-header img{height:150px;margin-bottom:4px;  
 animation:logoPulse 2.6s infinite ease-in-out;  
 filter:drop-shadow(0 0 10px rgba(255,0,0,.6)) drop-shadow(0 0 30px rgba(255,0,0,.9));}  
@keyframes logoPulse{0%{filter:drop-shadow(0 0 8px rgba(255,0,0,.4))}50%{filter:drop-shadow(0 0 22px rgba(255,0,0,1))}100%{filter:drop-shadow(0 0 8px rgba(255,0,0,.4))}}  
  
.chat-header h1{  
 margin:0;font-size:36px;color:var(--text);  
 opacity:0; transform:translateY(-50px) scale(0.5) rotate(-15deg);  
 animation:titleAppear 2s ease forwards;  
 font-family: 'Pacifico', cursive;  
}  
@keyframes titleAppear{  
 0%{opacity:0; transform:translateY(-50px) scale(0.5) rotate(-15deg);}  
 50%{opacity:1; transform:translateY(10px) scale(1.2) rotate(5deg);}  
 70%{transform:translateY(-5px) scale(0.95) rotate(-2deg);}  
 100%{opacity:1; transform:translateY(0px) scale(1) rotate(0deg);}  
}  
  
.theme-btn{position:absolute;right:12px;top:10px;background:none;border:none;cursor:pointer;display:flex;flex-direction:column;align-items:center;}  
.theme-btn.animate .icon{animation:spin 0.6s ease;}  
@keyframes spin{to{transform:rotate(360deg)}}  
.theme-btn.animate .text{animation:popText .6s ease;}  
@keyframes popText{0%{transform:scale(.6);opacity:0}60%{transform:scale(1.3)}100%{transform:scale(1)}}  
.theme-btn .icon{font-size:22px}  
.theme-btn .text{font-size:9px;margin-top:3px;color:var(--theme-text)}  
  
.chat-box{flex:1;overflow-y:auto;padding:10px;display:flex;flex-direction:column;}  
.msg{max-width:78%;padding:10px 14px;margin:6px 0;border-radius:20px;animation:pop .25s ease;}  
@keyframes pop{from{transform:scale(.9);opacity:.4}to{transform:scale(1);opacity:1}}  
  
.user-msg{align-self:flex-end;background:var(--user);color:#fff;}  
.bot-msg{  
 align-self:flex-start;background:var(--bot);  
 animation:pulseGlow 2.5s infinite ease-in-out;  
 color:#000;  
}  
body.dark .bot-msg{background:#2b2b2b;color:#fff;}  
  
@keyframes pulseGlow{0%{box-shadow:0 0 10px rgba(255,0,0,.4)}50%{box-shadow:0 0 22px rgba(255,0,0,.9)}100%{box-shadow:0 0 10px rgba(255,0,0,.4)}}  
  
.time{font-size:9px;opacity:.6;margin-top:3px}  
  
.typing{display:flex;gap:4px}  
.typing span{width:6px;height:6px;border-radius:50%;background:#888;animation:blink 1.4s infinite;}  
@keyframes blink{0%{opacity:.2}20%{opacity:1}100%{opacity:.2}}  
  
.input-area{background:#eee;margin:10px;border-radius:999px;display:flex;align-items:center;padding:6px 10px;}  
body.dark .input-area{background:#2b2b2b}  
  
.send-btn,.feedback-btn{width:38px;height:38px;border-radius:50%;border:none;color:#fff;font-weight:900;cursor:pointer;}  
.send-btn{background:#cc0000;margin-left:6px;}  
.feedback-btn{background:#ff3300;margin-right:6px;box-shadow:0 0 10px rgba(255,51,0,.7);}  
  
.version{margin-top:8px;font-size:17px;color:#fff;opacity:.8;}  
textarea#textInput{flex:1; resize:none; border:none; outline:none; background:transparent; font-size:15px; color:var(--text); overflow-y:auto; min-height:24px; line-height:1.2;}  
  
.creator {  
  display: flex;  
  align-items: center;  
  justify-content: center;  
  gap: 4px;  
  font-size: 9px;      /* کوچیک‌تر از Alphabet */  
  opacity: 0.6;  
  color: #fff;  
  margin-top: 2px;  
}  
  
.creator img {  
  width: 20px;  
  height: 20px;  
}  
</style>  </head>  <body>  
<div class="chat-container">  
<div class="chat-header">  
<button class="theme-btn" id="themeBtn" onclick="toggleTheme()">  
 <span class="icon">🌓</span>  
 <span class="text" id="themeText">لایت مود</span>  
</button>  
<img src="https://s6.uupload.ir/files/inshot_20251225_164915200_i1sr.png">  
<h1>Redlighte chat</h1>  
</div>  <div class="chat-box" id="chatBox"></div>  <form class="input-area" id="chatForm">  
 <button class="feedback-btn" id="feedbackBtn">❗</button>  
 <textarea id="textInput" placeholder="Ask Redlighte..." rows="1"></textarea>  
 <button class="send-btn">➤</button>  
</form>  
</div>  <div class="version">  
  Alphabet 0.0.1  
  <div class="creator">  
    <span>by Red Boy</span>  
    <img src="https://s6.uupload.ir/files/inshot_20251227_204536460_j5j8.png">  
  </div>  
</div>  
<script>  
const messages = [  
    "نمی ای با من حرف بزنی کلک؟؟😅",  
    "دلم برات تنگه دیگه بیا حرف بزنیم!💞😎!",  
    "بیا یه چیزی بگو پرسیدم این گوشه😬🙂‍↕️❤️"  
];  // درخواست اجازه نوتیف
if ("Notification" in window) {
Notification.requestPermission();
}

// تابع ارسال نوتیف
function sendRandomNotification() {
if (Notification.permission === "granted") {
const msg = messages[Math.floor(Math.random() * messages.length)];
new Notification("Redlighte chat", { body: msg });
}
}

// هر ۱ ساعت یکبار نوتیف بده
setInterval(sendRandomNotification, 1000 * 60 * 60);

// اگر خواستی برای تست سریع، میتونی زمانو کم کنی:
// setInterval(sendRandomNotification, 5000); // هر ۵ ثانیه برای تست
</script>

<script>  
const box=document.getElementById("chatBox");  
const textInput=document.getElementById("textInput");  
const themeBtn=document.getElementById("themeBtn");  
const themeText=document.getElementById("themeText");  
let lastUser="", lastBot="";  
  
function toggleTheme(){  
 themeBtn.classList.remove("animate");  
 void themeBtn.offsetWidth;  
 themeBtn.classList.add("animate");  
 document.body.classList.toggle("dark");  
 themeText.innerText=document.body.classList.contains("dark")?"دارک مود":"لایت مود";  
 themeText.style.color=document.body.classList.contains("dark")?"#fff":"#000";  
}  
  
textInput.addEventListener('input', ()=>{  
 textInput.style.height='auto';  
 textInput.style.height=textInput.scrollHeight+'px';  
});  
  
function addMsg(text,type){  
 const d=document.createElement("div");  
 d.className="msg "+(type==="user"?"user-msg":"bot-msg");  
 d.innerHTML=`<div>${text}</div><div class="time">${new Date().toLocaleTimeString().slice(0,5)}</div>`;  
 box.appendChild(d); box.scrollTop=box.scrollHeight;  
 if(type==="user") lastUser=text;  
 if(type==="bot") lastBot=text;  
}  
  
chatForm.onsubmit=async e=>{  
 e.preventDefault();  
 if(!textInput.value.trim())return;  
 addMsg(textInput.value,"user");  
  
 const typing=document.createElement("div");  
 typing.className="msg bot-msg typing";  
 typing.innerHTML="<span></span><span></span><span></span>";  
 box.appendChild(typing); box.scrollTop=box.scrollHeight;  
  
 const res=await fetch("/chat",{method:"POST",headers:{"Content-Type":"application/json"},  
 body:JSON.stringify({message:textInput.value})});  
 const data=await res.json();  
  
 typing.remove();  
 addMsg(data.reply,"bot");  
 textInput.value="";  
 textInput.style.height='auto';  
};  
  
feedbackBtn.onclick=e=>{  
 e.preventDefault();  
 if(!lastBot)return;  
 fetch("/feedback",{method:"POST",headers:{"Content-Type":"application/json"},  
 body:JSON.stringify({userMsg:lastUser,botMsg:lastBot})});  
 alert("وايسا ببينم چيو نفهميدم ؟؟ اها فهميدم❤️❤️");  
};  
</script>  </body>  
</html>  
""")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("text")

    ai_reply = ask_ai(user_msg)

    return jsonify({"reply": ai_reply})

@app.route("/feedback", methods=["POST"])
def feedback():
    save_feedback(request.json)
    return jsonify({"ok": True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

application = app
