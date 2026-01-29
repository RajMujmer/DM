from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# In-memory storage
scheduled_posts = []
notes = []

@app.route("/")
def home():
    return render_template("index.html")

# --- SEO Analyzer ---
@app.route("/seo", methods=["GET", "POST"])
def seo():
    results = None
    if request.method == "POST":
        html = request.form.get("html_code")
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string if soup.title else "No title"
        headings = [h.get_text() for h in soup.find_all(re.compile("^h[1-6]$"))]
        meta_desc = soup.find("meta", attrs={"name": "description"})
        desc = meta_desc["content"] if meta_desc else "No description"
        results = {
            "title": title,
            "headings": headings,
            "description": desc,
            "word_count": len(soup.get_text().split())
        }
    return render_template("seo.html", results=results)

# --- Content Generator ---
@app.route("/content", methods=["GET", "POST"])
def content():
    generated = None
    if request.method == "POST":
        topic = request.form.get("topic")
        generated = f"Here is a sample SEO-friendly blog post about {topic}. " \
                    f"Include keywords, headings, and a call-to-action."
    return render_template("content.html", generated=generated)

# --- Social Media Scheduler ---
@app.route("/social", methods=["GET", "POST"])
def social():
    global scheduled_posts
    if request.method == "POST":
        post = request.form.get("post")
        time = request.form.get("time")
        scheduled_posts.append({"post": post, "time": time})
    return render_template("social.html", posts=scheduled_posts)

# --- Analytics Dashboard ---
@app.route("/analytics")
def analytics():
    data = {
        "visits": 1200,
        "bounce_rate": "45%",
        "conversions": 85,
        "avg_time": "2m 30s"
    }
    return render_template("analytics.html", data=data)

# --- Contact Page ---
@app.route("/contact", methods=["GET", "POST"])
def contact():
    message = None
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        msg = request.form.get("message")
        message = f"Thanks {name}, we received your message!"
    return render_template("contact.html", message=message)

if __name__ == "__main__":
    app.run(debug=True)
