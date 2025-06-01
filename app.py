from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_fallback_response(user_message):
    user_message = user_message.lower()

    if any(word in user_message for word in ['health', 'insurance', 'medical', 'benefits', 'coverage', 'plan', 'healthcare']):
        return "Your health insurance options include: 1) Premium Plan (100% company paid), 2) Standard Plan (80% paid), 3) Basic Plan (60% paid). Dental and Vision are 100% covered. Need help choosing?"

    elif any(word in user_message for word in ['time off', 'vacation', 'sick', 'leave', 'pto', 'holiday', 'days off']):
        return "Time Off Info: 20 PTO days, 10 sick days, 12 holidays. Submit time off in the portal under 'Time Off Requests'. You have 15 vacation days left."

    elif any(word in user_message for word in ['salary', 'pay', 'compensation', 'wage', 'money', 'paycheck', 'pay stub', 'income']):
        return "Salary: $64,900/year. HR Specialist range is $70k–$90k. Paid bi-weekly (Fridays). Pay stubs are in the 'Payroll' section of the portal."

    elif any(word in user_message for word in ['career', 'promotion', 'development', 'training', 'skills', 'growth', 'advancement', 'path']):
        return "Career Path: HR Specialist → Sr. HR Specialist → HR Manager → HR Director. Resources: LinkedIn Learning, workshops, mentorship, $5k tuition reimbursement."

    elif any(word in user_message for word in ['policy', 'policies', 'handbook', 'rules', 'code', 'conduct', 'guidelines']):
        return "Policies include: 1) Code of Conduct, 2) Remote Work (3 days/week), 3) Expense Reimbursement (within 30 days), 4) Dress Code (business casual). Full handbook is on the intranet."

    elif any(word in user_message for word in ['it', 'computer', 'technical', 'software', 'password', 'login', 'system', 'tech', 'laptop']):
        return "IT Support: Restart your device, check IT knowledge base (intranet), submit a ticket or email ithelp@company.com. Call ext. 1234 for urgent help (8 AM–6 PM)."

    elif any(word in user_message for word in ['401k', 'retirement', 'pension', '401(k)', 'savings', 'match']):
        return "401(k): 4% company match. Immediate vesting for your contributions. Match vests in 2 years. Change contributions anytime in the portal. 2024 limit is $23,000."

    elif any(word in user_message for word in ['manager', 'supervisor', 'boss', 'report', 'reporting']):
        return "Your manager: Sarah Johnson (sarah.johnson@company.com, ext. 5678). For escalations, contact HR at hr@company.com or ext. 9999."

    elif any(word in user_message for word in ['hours', 'schedule', 'work time', 'flexible', 'remote', 'office']):
        return "Standard hours: 9 AM–5 PM, M–F. Flexible core hours: 10 AM–3 PM. Remote work allowed up to 3 days/week. Office: 123 Business St, SF. Free parking provided."

    elif any(word in user_message for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
        return "Hello! I’m your HR assistant. Ask about: insurance, time off, salary, policies, IT help, 401(k), and more. What can I help you with?"

    elif any(word in user_message for word in ['help', 'assist', 'what can you do', 'options']):
        return "I can assist with: Benefits, Time Off, Salary, Training, Policies, IT Support, 401(k), Work Schedules, Manager info. Ask about any of these!"

    else:
        return "I can help with HR-related topics like benefits, time off, salary, policies, and tech issues. Please clarify your question for better assistance."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        if openai.api_key and openai.api_key != "your_openai_api_key_here":
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful HR assistant for Theresa Calderon (Employee ID: 1234, HR Specialist, Sales Department, San Francisco). Provide specific, detailed answers about benefits, policies, time off, salary, career development, and workplace questions. Be conversational and helpful."
                        },
                        {"role": "user", "content": user_message}
                    ],
                    temperature=0.7,
                    max_tokens=300
                )

                ai_response = response['choices'][0]['message']['content'].strip()
                return jsonify({
                    'response': ai_response,
                    'timestamp': datetime.now().isoformat()
                })

            except Exception as api_error:
                print(f"OpenAI API Error: {api_error}")
                fallback = get_fallback_response(user_message)
                return jsonify({'response': fallback, 'timestamp': datetime.now().isoformat()})

        else:
            fallback = get_fallback_response(user_message)
            return jsonify({'response': fallback, 'timestamp': datetime.now().isoformat()})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'response': 'Sorry, I’m experiencing technical difficulties. Please try again later.',
            'timestamp': datetime.now().isoformat()
        })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
