from flask import Flask, request, jsonify, render_template_string
from bot import ask_ai
import json, os
from datetime import datetime
from github_logger import push_chat_to_github
from flask import send_from_directory
from image_gen import generate_image
import base64


app = Flask(__name__, static_folder="static", static_url_path="")  # <- اینجا هم name رو باید __name__ بذاری



@app.route("/")
def index(): 
    return render_template_string("""

<!DOCTYPE html>  <html lang="fa">  
<meta name="google-site-verification" content="HjrtrUik26UFlKsbD5anwM0FOW5EzQiSMelGs9o0Q0Q" />
<head>
<script>
            !function(e,t,n){e.yektanetAnalyticsObject=n,e[n]=e[n]||function(){e[n].q.push(arguments)},e[n].q=e[n].q||[];var a=t.getElementsByTagName("head")[0],r=new Date,c="https://cdn.yektanet.com/superscript/MLudF3eR/native-Redlighte.ir-45400/yn_pub.js?v="+r.getFullYear().toString()+"0"+r.getMonth()+"0"+r.getDate()+"0"+r.getHours(),s=t.createElement("link");s.rel="preload",s.as="script",s.href=c,a.appendChild(s);var l=t.createElement("script");l.async=!0,l.src=c,a.appendChild(l)}(window,document,"yektanet");
        </script>
<script>
if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/sw.js");
}
</script>
<meta name="google-site-verification" content="v10a70r4wwCAfx1nS31l8sJT4cwykghFkAkvSeJRPgY" />
<meta charset="UTF-8">  
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Redlighte Chat | هوش مصنوعی فارسی برای گفتگو، پاسخ به سوالات، کمک در یادگیری و تجربه یک چت آنلاین سریع و هوشمند با ردلایت.">
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#8b0000">
<link rel="icon" href="https://s8.uupload.ir/files/favicon_nw0z.png" type="image/png">
<link rel="apple-touch-icon" href="https://s8.uupload.ir/files/favicon_nw0z.png">
<meta property="og:image" content="https://s8.uupload.ir/files/favicon_nw0z.png">
<title>Redlighte chat | هوش مصنوعي ردلايت</title>  <link href="https://cdn.jsdelivr.net/gh/rastikerdar/vazir-font@v30.1.0/dist/font-face.css" rel="stylesheet">  <style>  
<meta name="description" content="Redlighte Chat | هوش مصنوعی فارسی برای گفتگو، پاسخ به سوالات، کمک در یادگیری و تجربه یک چت آنلاین سریع و هوشمند با ردلایت.">
<link rel="icon" href="https://s8.uupload.ir/files/favicon_nw0z.png" type="image/png">
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
.footer{
  margin-top:12px;
  display:flex;
  flex-direction:column;
  align-items:center;
  gap:6px;
  color:#fff;
  opacity:.85;
}

.release{
  font-size:20px;
}

.creator{
  display:flex;
  align-items:center;
  gap:6px;
  font-size:11px;
  opacity:.7;
}

.creator img{
  width:26px;
  height:26px;
}
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
  width: 30px;  
  height: 30px;  
}  

.legal{
  margin-top:8px;
  font-size:12px;
  color:#aaa;
  text-align:center;
}

.legal span{
  cursor:pointer;
  transition:.3s;
}

.legal span:hover{
  color:#ff0033;
  text-shadow:0 0 6px rgba(255,0,51,.6);
}

.legal-modal{
  position:fixed;
  inset:0;
  background:rgba(0,0,0,.6);
  display:none;
  align-items:center;
  justify-content:center;
  z-index:999;
}

.legal-box{
  background:#111;
  color:#eee;
  width:90%;
  max-width:420px;
  max-height:80vh;
  overflow-y:auto;
  padding:20px;
  border-radius:14px;
  box-shadow:0 0 30px rgba(255,0,0,.4);
}

.legal-box h2{
  margin-top:0;
  color:#ff0033;
  text-align:center;
}

.legal-box button{
  width:100%;
  margin-top:16px;
  padding:10px;
  background:#ff0033;
  border:none;
  border-radius:10px;
  color:#fff;
  font-weight:bold;
  cursor:pointer;
}
</style>  </head>  <body>  
<div class="legal-modal" id="legalModal">
  <div class="legal-box">
    <h2>قوانین و حریم خصوصی ردلایت</h2>

    <div class="legal-content">
      <!-- ⛔️ متن‌ها رو بعداً اینجا می‌ذاری -->
      <p>تمامی اطلاعات ردلایت محفوظ است.
حریم خصوصی کاربران در ردلایت به طور کامل از طریق repo پرایوت در گیت هاب تامین می شود.


قوانین و توضیحات و حریم خصوصی کاربران ردلایت (redlighte) به طور کامل به شرح زیر می باشد:

1-تیم توسعه دهنگی پسر قرمز تمامی مسیولیت ها را در برابر جواب های داده شده به کاربران گردن می گیرد و در برابر شکایت ها در مایکت برای اپلیکیشن ردلایت پاسخ گو ست.

2-تمامی چت های کاربران همراه با اطلاعات کامل اعم از 1-زمان دقیق چت و fetch جواب 2-ip هش شده کاربر 3-سِشِن ای دی کاربر که برای کاربر قاعدتا متفاوت است 4-تعداد کاراکتر های پیام کاربر و پیام ردلایت همراه تکست انها فقط و فقط برای انالیز پیام های ردلایت برای بهبود جمله بندی ها و سانسور برخی جمله ها و الفاظ ممنوعه که باید به انها رسیدگی شود

3-سایت ردلایت که می توانید ان را به عنوان web view یا PWA یا به صورت اپ در مایکت مشاهده کنید که هیچ یک از انها هیج شنودی خارج از سایت ندارد و این کار را دور از انسانیت دانسته و برای اثبات ان می توانید به git hub رفته و repo ی "Redlightee" را جست و جو کرده و تمامی سورس کد های ردلایت را مشاهده کرده و از این حرف اطمینان حاصل کنید.

4-ردلایت هیچ گونه کپی برداری از هیچ محصول هوش مصنوعی ندارد. و ردلایت محصولی مستقل است.

5-تمامی اطلاع رسانی های ردلایت برای نسخه ها و تغییرات در کانال ایتا ردلایت قرار می گیرد . ادرس در ایتا :@redlighte

6-ردلایت هیچ گونه طرفداری سیاسی و یا مذهبی ندارد و کاملا بی طرف رفتار می کند



""این قوانین و اطلاعات دایما درحال به روز رسانی است و هر لحظه امکان تغییر ان وجود دارد""

سپاس از انتخاب شما
-تیم توسعه دهندگی سحاب قرمز (Red Boy)</p>
    </div>

    <button id="closeLegal">بستن</button>
  </div>
</div>
<div class="chat-container">  
<div class="chat-header">  
<button class="theme-btn" id="themeBtn" onclick="toggleTheme()">  
 <span class="icon">🌓</span>  
 <span class="text" id="themeText">لایت مود</span>  
</button>  
<img src="https://s6.uupload.ir/files/inshot_20251225_164915200_i1sr.png">  
<h1>Redlighte chat</h1>  
</div>  <div class="chat-box" id="chatBox"></div>  <form class="input-area" id="chatForm">  
 <textarea id="textInput" placeholder="Ask Redlighte..." rows="1"></textarea>  
 <button class="send-btn">➤</button>  
</form>  
</div>

<div class="footer">

  <div class="release">
    Release 1.9
  </div>

  <div class="creator">
    <span>by Red Boy</span>
    <img src="https://s6.uupload.ir/files/inshot_20251227_204536460_j5j8.png">
  </div>

  <div class="legal">
    <span id="openLegal">
      تمامی اطلاعات ردلایت محفوظ است | قوانین
    </span>
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
 if(type==="bot"){
   lastBot=text;
   vibrateBot();
   }
}
function isImagePrompt(text){
  return text.startsWith("/img ");
}


chatForm.onsubmit = async e => {
    e.preventDefault();
    const text = textInput.value.trim();
    if (!text) return;

    // اگه پرامت تصویر هست
    if (text.startsWith("/img ")) {
        addMsg(text, "user");  // نمایش پیام کاربر

        const prompt = text.replace("/img ", "");
        const typing = document.createElement("div");
        typing.className = "msg bot-msg typing";
        typing.innerHTML = "<span></span><span></span><span></span>";
        box.appendChild(typing); 
        box.scrollTop = box.scrollHeight;

        try {
            const res = await fetch("/image", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ prompt })
            });
            const data = await res.json();
            typing.remove();

            if (data.image) {
                const imgMsg = document.createElement("div");
                imgMsg.className = "msg bot-msg";
                imgMsg.innerHTML = `<img src="${data.image}" style="max-width:100%;border-radius:14px;">`;
                box.appendChild(imgMsg);
                box.scrollTop = box.scrollHeight;
            } else {
                addMsg("❌ خطا در ساخت تصویر", "bot");
            }
        } catch (err) {
            typing.remove();
            addMsg("❌ خطا در ساخت تصویر", "bot");
            console.error(err);
        }

        textInput.value = "";
        textInput.style.height = 'auto';
        return;  // همینجا تموم می‌شه، دیگه پیام عادی نمی‌ره
    }

    // پیام معمولی (chat bot)
    addMsg(text, "user");

    const typing = document.createElement("div");
    typing.className = "msg bot-msg typing";
    typing.innerHTML = "<span></span><span></span><span></span>";
    box.appendChild(typing);
    box.scrollTop = box.scrollHeight;

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        typing.remove();
        addMsg(data.reply, "bot");
    } catch (err) {
        typing.remove();
        addMsg("❌ خطا در دریافت پاسخ", "bot");
        console.error(err);
    }
}

    textInput.value = "";
    textInput.style.height = 'auto';
};

  
 const res=await fetch("/chat",{method:"POST",headers:{"Content-Type":"application/json"},  
 body:JSON.stringify({message:textInput.value})});  
 const data=await res.json();  
  
 typing.remove();  
 addMsg(data.reply,"bot");  
 textInput.value="";  
 textInput.style.height='auto';  
};  

const openLegal = document.getElementById("openLegal");
const legalModal = document.getElementById("legalModal");
const closeLegal = document.getElementById("closeLegal");

openLegal.onclick = () => {
  legalModal.style.display = "flex";
};

closeLegal.onclick = () => {
  legalModal.style.display = "none";
};

function vibrateBot(){
  if (navigator.vibrate) {
    navigator.vibrate([30, 40, 30]); // 20 میلی‌ثانیه، خیلی ظریف
  }
}

</script>  </body>  
</html>  
""")

@app.route("/manifest.json")
def manifest():
    return send_from_directory(".", "manifest.json", mimetype="application/manifest+json")

@app.route("/sw.js")
def sw():
    return send_from_directory(".", "sw.js", mimetype="application/javascript")

@app.route("/icon-192.png")
def icon192():
    return send_from_directory(".", "icon-192.png")

@app.route("/icon-512.png")
def icon512():
    return send_from_directory(".", "icon-512.png")


@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")

    ai_reply = ask_ai(user_msg)

    push_chat_to_github(user_msg, ai_reply)
    
    return jsonify({"reply": ai_reply})

@app.route("/image", methods=["POST"])
def image():
    prompt = request.json.get("prompt")

    img_bytes = generate_image(prompt)
    if not img_bytes:
        return jsonify({"error": "image_failed"}), 500

    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    return jsonify({
        "image": f"data:image/png;base64,{img_base64}"
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

application = app
