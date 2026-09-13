import os
import re

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

llm = ChatGroq(
    model=os.getenv("GROQ_MODEL"),
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an expert web developer.

Create a simple website based on the user's request.

Return the response using these three sections:

HTML:
<your HTML code>

CSS:
<your CSS code>

JavaScript:
<your JavaScript code>

You can include explanations before the HTML section,
but do not add explanations between the three sections."""
    ),
    (
        "human",
        "{description}"
    ),
])

chain = prompt | llm

result = chain.invoke({
    "description": "Create a simple landing page for a coffee shop"
})

response = result.content

print(response)


html_match = re.search(
    r"---HTML START---(.*?)---HTML END---",
    response,
    re.DOTALL
)

if html_match:
    html = html_match.group(1).strip()
else:
    html = ""

css_match = re.search(
    r"CSS:\s*(.*?)(?=\nJavaScript:)",
    response,
    re.DOTALL
)

if css_match:
    css = css_match.group(1).strip()
else:
    css = ""

js_match = re.search(
    r"JavaScript:\s*(.*)",
    response,
    re.DOTALL
)

if js_match:
    js = js_match.group(1).strip()
else:
    js = ""



with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

with open("style.css", "w", encoding="utf-8") as f:
    f.write(css)

with open("script.js", "w", encoding="utf-8") as f:
    f.write(js)