from flask import Flask, render_template_string, request
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Define social media phishing prompts
social_media_roles = {
    'Instagram': {
        'subject': ["Your Instagram Account Has Been Temporarily Suspended", "Important: Instagram Account Security Update"],
        'body': [
            "Dear {{ username }},\n\nWe noticed suspicious activity in your Instagram account. To protect your account, please verify your identity by clicking the link below.",
            "Dear {{ username }},\n\nYour Instagram account has been flagged for unusual activity. To avoid losing access, please click the link to reset your password.",
            "Dear {{ username }},\n\nInstagram is conducting a routine security check. Please confirm your account details to avoid suspension.",
        ],
        'call_to_action': [
            "Click here to secure your Instagram account.",
            "Please verify your Instagram account now.",
            "Reset your Instagram password by clicking the link below."
        ]
    },
    'Facebook': {
        'subject': ["Your Facebook Account Needs Immediate Attention", "Facebook Security Alert: Action Required"],
        'body': [
            "Dear {{ username }},\n\nWe have detected suspicious activity on your Facebook account. Please confirm your account details to avoid being locked out.",
            "Dear {{ username }},\n\nFor security reasons, your Facebook account is temporarily suspended. Please click the link to verify your identity and restore access.",
            "Dear {{ username }},\n\nFacebook is performing routine checks on accounts. Please click below to verify your information and maintain access.",
        ],
        'call_to_action': [
            "Click here to verify your Facebook account.",
            "Restore your Facebook account by confirming your information.",
            "Please click here to confirm your Facebook identity."
        ]
    }
}

# Default urgent tone
urgent_tone = "This is an urgent matter that requires your immediate attention."

# Function to generate phishing email based on platform, username, and phishing link
def generate_phishing_email(platform, username, phishing_link):
    if platform not in social_media_roles:
        raise ValueError("Invalid platform. Please choose 'Instagram' or 'Facebook'.")
    
    # Select the random subject, body, and call to action
    subject = random.choice(social_media_roles[platform]['subject'])
    body = random.choice(social_media_roles[platform]['body']).replace("{{ username }}", username)
    call_to_action = random.choice(social_media_roles[platform]['call_to_action'])
    
    # Add the default urgent tone to the body of the email
    email_body = f"{urgent_tone}\n\n{body}\n\n{call_to_action}\n\nPlease follow this link: {phishing_link}"

    # Construct final phishing email
    email = f"Subject: {subject}\n\n{email_body}"
    return email

# Function to send the email using SMTP
def send_email(recipient_email, subject, body):
    sender_email = "sajid05541786@gmail.com"  # Your email
    sender_password = "xevv kltn dwhr ovci"  # Your email password (or app password if using Gmail)

    # Create the email content
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Set up the SMTP server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use your SMTP server's address
        server.starttls()  # Secure connection
        server.login(sender_email, sender_password)  # Login to your email account
        server.sendmail(sender_email, recipient_email, msg.as_string())  # Send email
        server.quit()  # Close the connection
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

# Flask route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    phishing_email = None
    error_message = None
    
    if request.method == 'POST':
        platform = request.form['platform']
        username = request.form['username']
        phishing_link = request.form['phishing_link']
        recipient_email = request.form['recipient_email']  # Get recipient email
        
        try:
            phishing_email = generate_phishing_email(platform, username, phishing_link)
            subject = phishing_email.split("\n")[0].replace("Subject: ", "")  # Extract subject
            body = phishing_email.split("\n", 1)[1]  # Extract body

            # Send the phishing email
            send_email(recipient_email, subject, body)
        except ValueError as e:
            error_message = str(e)
    
    # HTML template for the page
    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Social Media Phishing Email Generator</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
            }
            h1 {
                text-align: center;
            }
            .form-container {
                width: 300px;
                margin: 0 auto;
            }
            .form-container input, .form-container select {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
            }
            .email-output {
                margin-top: 20px;
                white-space: pre-wrap;
                background-color: #f4f4f4;
                padding: 15px;
                border-radius: 5px;
            }
            .error-message {
                color: red;
                text-align: center;
            }
        </style>
    </head>
    <body>

        <h1>Social Media Phishing Email Generator</h1>
        
        <div class="form-container">
            <form method="POST">
                <label for="platform">Select Platform:</label>
                <select name="platform" required>
                    <option value="Instagram">Instagram</option>
                    <option value="Facebook">Facebook</option>
                </select>

                <label for="username">Enter Username:</label>
                <input type="text" name="username" placeholder="Enter username" required>

                <label for="phishing_link">Phishing Link:</label>
                <input type="text" name="phishing_link" placeholder="Enter phishing link" required>
                
                <label for="recipient_email">Recipient Email:</label>
                <input type="email" name="recipient_email" placeholder="Enter recipient email" required>

                <input type="submit" value="Generate and Send Phishing Email">
            </form>
        </div>

        {% if phishing_email %}
            <h2>Generated Phishing Email</h2>
            <div class="email-output">
                <pre>{{ phishing_email }}</pre>
            </div>
        {% endif %}

        {% if error_message %}
            <div class="error-message">
                <p>{{ error_message }}</p>
            </div>
        {% endif %}
        
    </body>
    </html>
    '''
    
    return render_template_string(html_template, phishing_email=phishing_email, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
