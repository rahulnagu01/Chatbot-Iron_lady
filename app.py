
from flask import Flask, render_template, request
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()  # loads variables from .env

app = Flask(__name__)
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Real Iron Lady FAQ fallback
# ironlady_faq = {
#     "live": "Yes — both sessions are conducted live and interactive.",
#     "recording": ("The Day 1 session is recorded and shared afterward; "
#                   "Day 2 is not recorded to protect privacy."),
#     "language": "The programs are conducted in English.",
#     "age limit": ("There is no age limit, but the program is tailored for women "
#                   "who are already in their professional journey aiming to fast-track their careers."),
#     "programs": "Iron Lady offers Leadership, Mentorship, and Career Development programs.",
#     "program": "Iron Lady offers Leadership, Mentorship, and Career Development programs.",
#     "duration": "Program duration ranges from 4 to 12 weeks depending on the course.",
#     "mode": "Programs are available both online and offline.",
#     "certificates": "Yes, certificates are provided upon completion.",
#     "certificate": "Yes, certificates are provided upon completion.",
#     "mentors": "Our mentors are experienced leaders and industry professionals.",
#     "mentor": "Our mentors are experienced leaders and industry professionals.",
#     "found":"Meet our Founder &amp; Director – Rajesh Bhat: The visionary entrepreneur behind Head Held High, 1Bridge, Iron Lady, Winner Bench, and C-Suite League."
# }

SYSTEM_PROMPT = (
    "You are a helpful chatbot answering FAQs about Iron Lady’s leadership programs, "
    "including details on live sessions, recordings, language, age limit, and mentorship."
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.form["message"].lower()

    # Check fallback
    # for key, ans in ironlady_faq.items():
    #     if key in user_message:
    #         return ans

    # Otherwise, ask Groq AI
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.5,
        max_tokens=200
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    app.run(debug=True)
