import gradio as gr
from groq import Groq
import json
import os

# Set your API key directly here
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your_groq_api_key_here")

client = Groq(api_key=GROQ_API_KEY)

MODEL = "llama-3.3-70b-versatile"


def create_prompt(domain, interest, skills, budget, audience, country):
    return f"""
You are an expert startup consultant.

Generate one startup idea.

Return ONLY JSON.

Format:

{{
"overview":"",
"validation":"",
"revenue":"",
"competitors":"",
"marketing":""
}}

Domain : {domain}

Interest : {interest}

Skills : {skills}

Budget : {budget}

Audience : {audience}

Country : {country}
"""


def generate_business_idea(domain, interest, skills, budget, audience, country):
    prompt = create_prompt(domain, interest, skills, budget, audience, country)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content

    try:
        data = json.loads(result)
        return (
            data["overview"],
            data["validation"],
            data["revenue"],
            data["competitors"],
            data["marketing"]
        )
    except Exception as e:
        return (
            result,
            "",
            "",
            "",
            ""
        )


# Create Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# 🚀 AI Business Idea Generator")

    with gr.Row():
        domain = gr.Textbox(label="Business Domain")
        interest = gr.Textbox(label="Your Interest")

    skills = gr.Textbox(label="Skills")
    budget = gr.Textbox(label="Budget")
    audience = gr.Textbox(label="Target Audience")
    country = gr.Textbox(label="Country")

    generate_btn = gr.Button("Generate Idea 🚀")
    clear_btn = gr.Button("Clear")

    # OUTPUTS
    overview = gr.Markdown()
    validation = gr.Markdown()
    revenue = gr.Markdown()
    competitors = gr.Markdown()
    marketing = gr.Markdown()

    # BUTTON EVENTS
    generate_btn.click(
        fn=generate_business_idea,
        inputs=[domain, interest, skills, budget, audience, country],
        outputs=[overview, validation, revenue, competitors, marketing]
    )

    clear_btn.click(
        fn=lambda: ("", "", "", "", ""),
        outputs=[overview, validation, revenue, competitors, marketing]
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
