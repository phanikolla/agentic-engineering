from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr
from datetime import datetime

# Load .env file if it exists (local development), otherwise use environment variables (App Runner)
load_dotenv(override=True)

# Debug: Print environment check (remove in production)
print(f"PERPLEXITY_API_KEY set: {bool(os.getenv('PERPLEXITY_API_KEY'))}", flush=True)
print(f"PUSHOVER_TOKEN set: {bool(os.getenv('PUSHOVER_TOKEN'))}", flush=True)

def push(text):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]


class Me:

    def __init__(self):
        self.openai = OpenAI(
            base_url="https://api.perplexity.ai",
            api_key=os.getenv("PERPLEXITY_API_KEY")
        )
        self.name = "Phani Kumar"
        
        # Get the directory where app.py is located
        app_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load LinkedIn PDF with error handling
        self.linkedin = ""
        pdf_path = os.path.join(app_dir, "me", "Linkedin_Phani.pdf")
        try:
            print(f"Loading PDF from: {pdf_path}", flush=True)
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    self.linkedin += text
            print(f"PDF loaded successfully, {len(self.linkedin)} characters", flush=True)
        except Exception as e:
            print(f"Error loading PDF: {e}", flush=True)
            self.linkedin = "LinkedIn profile not available"
        
        # Load summary with error handling
        summary_path = os.path.join(app_dir, "me", "summary.txt")
        try:
            print(f"Loading summary from: {summary_path}", flush=True)
            with open(summary_path, "r", encoding="utf-8") as f:
                self.summary = f.read()
            print(f"Summary loaded successfully, {len(self.summary)} characters", flush=True)
        except Exception as e:
            print(f"Error loading summary: {e}", flush=True)
            self.summary = "Summary not available"


    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(model="sonar-pro", messages=messages, tools=tools)
            if response.choices[0].finish_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content
    

if __name__ == "__main__":
    me = Me()
    
    # Custom CSS for professional styling
    custom_css = """
    .gradio-container {
        max-width: 1200px !important;
        margin: 0 auto !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        min-height: 100vh;
    }
    
    .chat-container {
        background: rgba(255, 255, 255, 0.95) !important;
        border-radius: 20px !important;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        margin: 20px !important;
        padding: 20px !important;
    }
    
    .message.user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 15px 15px 5px 15px !important;
        margin-left: 20% !important;
        padding: 15px !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1) !important;
    }
    
    .message.bot {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
        border-radius: 15px 15px 15px 5px !important;
        margin-right: 20% !important;
        padding: 15px !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1) !important;
    }
    
    .input-container textarea {
        background: rgba(255, 255, 255, 0.9) !important;
        border-radius: 25px !important;
        border: 2px solid #667eea !important;
        padding: 15px 20px !important;
        font-size: 16px !important;
    }
    
    .send-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 20px !important;
        color: white !important;
        padding: 12px 25px !important;
        font-weight: bold !important;
        transition: all 0.3s ease !important;
        font-size: 16px !important;
    }
    
    .send-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    .header-text {
        text-align: center !important;
        color: white !important;
        font-size: 2.5em !important;
        font-weight: bold !important;
        margin: 20px 0 !important;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3) !important;
    }
    
    .subtitle-text {
        text-align: center !important;
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1.2em !important;
        margin-bottom: 30px !important;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    
    .footer-text {
        text-align: center !important;
        color: rgba(255, 255, 255, 0.7) !important;
        font-size: 0.9em !important;
        margin-top: 20px !important;
    }
    
    .quick-btn {
        background: rgba(255, 255, 255, 0.2) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        color: white !important;
        padding: 8px 16px !important;
        margin: 5px !important;
        transition: all 0.3s ease !important;
    }
    
    .quick-btn:hover {
        background: rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-1px) !important;
    }
    
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #4CAF50;
        border-radius: 50%;
        margin-right: 8px;
        animation: blink 2s infinite;
    }
    
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.3; }
    }
    """
    
    # Enhanced chat function
    def enhanced_chat(message, history):
        if not message.strip():
            return history, ""
        
        # Convert history format for the Me.chat method
        formatted_history = []
        for user_msg, bot_msg in history:
            if user_msg:
                formatted_history.append({"role": "user", "content": user_msg})
            if bot_msg:
                formatted_history.append({"role": "assistant", "content": bot_msg})
        
        try:
            response = me.chat(message, formatted_history)
            history.append([message, response])
        except Exception as e:
            error_msg = f"I apologize, but I'm experiencing technical difficulties. Please try again in a moment. 🔧"
            history.append([message, error_msg])
            print(f"Error in chat: {e}")
        
        return history, ""
    
    # Quick action handlers
    def handle_quick_action(action_msg, history):
        return enhanced_chat(action_msg, history)
    
    # Create the interface with custom theme and styling
    with gr.Blocks(
        css=custom_css,
        title="Phani Kumar - AI Assistant",
        theme=gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="purple",
            neutral_hue="slate"
        )
    ) as demo:
        
        # Header section
        gr.HTML("""
            <div class="header-text">
                💼 Phani Kumar
            </div>
            <div class="subtitle-text">
                <span class="status-indicator"></span>
                AI-Powered Professional Assistant | Available 24/7
            </div>
        """)
        
        # Main chat interface
        with gr.Column(elem_classes="chat-container"):
            chatbot = gr.Chatbot(
                value=[],
                elem_id="chatbot",
                height=500,
                show_label=False
            )
            
            with gr.Row():
                with gr.Column(scale=9):
                    msg = gr.Textbox(
                        placeholder="💬 Ask me about Phani's experience, skills, or get in touch...",
                        show_label=False,
                        container=False,
                        elem_classes="input-container"
                    )
                with gr.Column(scale=1, min_width=100):
                    submit_btn = gr.Button(
                        "Send 🚀",
                        elem_classes="send-button",
                        variant="primary"
                    )
            
            # Quick action buttons
            with gr.Row():
                intro_btn = gr.Button("👋 Introduction", size="sm", elem_classes="quick-btn")
                exp_btn = gr.Button("💼 Experience", size="sm", elem_classes="quick-btn") 
                skills_btn = gr.Button("🛠️ Skills", size="sm", elem_classes="quick-btn")
                contact_btn = gr.Button("📧 Contact", size="sm", elem_classes="quick-btn")
        
        # Footer
        gr.HTML(f"""
            <div class="footer-text">
                🤖 Powered by AI • Last updated: {datetime.now().strftime("%B %Y")} • 
                <a href="mailto:pkkolla24@gmail.com" style="color: rgba(255,255,255,0.9);">Get in Touch</a>
            </div>
        """)
        
        # Event handlers
        submit_btn.click(
            enhanced_chat,
            inputs=[msg, chatbot],
            outputs=[chatbot, msg]
        )
        
        msg.submit(
            enhanced_chat,
            inputs=[msg, chatbot],
            outputs=[chatbot, msg]
        )
        
        # Quick action button events
        intro_btn.click(
            lambda history: handle_quick_action("👋 Tell me about yourself and your background", history),
            inputs=[chatbot],
            outputs=[chatbot, msg]
        )
        
        exp_btn.click(
            lambda history: handle_quick_action("💼 What's your professional experience?", history),
            inputs=[chatbot],
            outputs=[chatbot, msg]
        )
        
        skills_btn.click(
            lambda history: handle_quick_action("🛠️ What are your key skills and technologies?", history),
            inputs=[chatbot],
            outputs=[chatbot, msg]
        )
        
        contact_btn.click(
            lambda history: handle_quick_action("📧 How can I get in touch with you?", history),
            inputs=[chatbot],
            outputs=[chatbot, msg]
        )
    
    # Check if running in Lambda environment
    if os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        # Running in Lambda - create ASGI app for API Gateway compatibility
        from mangum import Mangum
        
        # Create the ASGI app
        app = demo.app
        
        # Wrap with Mangum for Lambda compatibility
        handler = Mangum(app, lifespan="off")
        
        # For Lambda Web Adapter (Function URL), also start the server
        if os.getenv("AWS_LWA_INVOKE_MODE"):
            demo.launch(
                server_name=os.getenv("GRADIO_SERVER_NAME", "0.0.0.0"),
                server_port=int(os.getenv("GRADIO_SERVER_PORT", "7860")),
                share=False,
                show_error=True,
                quiet=False
            )
    else:
        # Running locally
        demo.launch(
            server_name=os.getenv("GRADIO_SERVER_NAME", "127.0.0.1"),
            server_port=int(os.getenv("GRADIO_SERVER_PORT", "7860")),
            share=False,
            show_error=True,
            quiet=False
        )
    