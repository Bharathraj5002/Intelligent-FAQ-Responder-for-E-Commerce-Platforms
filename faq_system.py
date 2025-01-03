import os
import time
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from datetime import datetime
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import pytz  # Import pytz for timezone handling

# Load your CSV file with FAQs
faq_df = pd.read_csv("Ecommerce_FAQs.csv")
faq_df.columns = faq_df.columns.str.strip()  # Remove any leading/trailing spaces in the column names

# Load a pre-trained model from sentence-transformers with a custom cache directory
model_dir = os.path.join(os.getcwd(), "sentence_transformer_model")
model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder=model_dir)

# Encode the FAQ prompts to create embeddings for efficient similarity lookup
faq_embeddings = model.encode(faq_df['prompt'].tolist(), convert_to_tensor=True)

def get_response(user_query):
    # Encode the user's query using the sentence transformer model
    user_query_embedding = model.encode(user_query, convert_to_tensor=True)
    
    # Compute cosine similarities between the query and stored FAQ embeddings
    similarities = util.pytorch_cos_sim(user_query_embedding, faq_embeddings)[0]
    
    # Get the index of the most similar FAQ based on the highest similarity score
    best_match_index = similarities.argmax().item()
    
    # Retrieve and return the corresponding response from the FAQ CSV
    best_response = faq_df['response'].iloc[best_match_index]
    return best_response

def check_email_and_respond(start_time):
    # Email credentials
    EMAIL = "your_email"
    PASSWORD = "#"  # Replace with your App Password
    SMTP_SERVER = "smtp.gmail.com"
    IMAP_SERVER = "imap.gmail.com"
    
    # Connect to the IMAP server and login
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        print("Successfully connected to the IMAP server.")
    except Exception as e:
        print(f"Error connecting to the IMAP server: {e}")
        return

    mail.select("inbox")  # Select the inbox

    while True:
        try:
            # Re-select inbox to ensure we have the latest information
            mail.select("inbox")  

            # Search for unseen emails
            result, data = mail.search(None, 'UNSEEN')  # Searching all unseen emails
            email_ids = data[0].split()
            print(f"Found {len(email_ids)} new unseen emails.")

            # If there are new emails, process them
            for email_id in email_ids:
                # Fetch the complete email using the ID
                result, msg_data = mail.fetch(email_id, '(RFC822)')
                msg = email.message_from_bytes(msg_data[0][1])

                # Get the email subject and sender's email address
                subject = msg["subject"]
                from_email = email.utils.parseaddr(msg["from"])[1]  # Extract only the email address

                # Get the email content (body)
                email_body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            email_body = part.get_payload(decode=True).decode()
                else:
                    email_body = msg.get_payload(decode=True).decode()

                print(f"New Email from: {from_email}, Subject: {subject}, Body: {email_body}")

                # Get the email date and convert it to a timezone-aware datetime
                email_date = email.utils.parsedate_to_datetime(msg['Date']).astimezone(pytz.utc)

                # Check if the email was received after the script started
                if email_date > start_time:
                    # Generate a response based on the email body content
                    response = get_response(email_body)
                    print(f"Generated response: {response}")

                    # Send the response via email
                    send_email(from_email, response, SMTP_SERVER, EMAIL, PASSWORD)

                    # Mark the email as "seen" to prevent reprocessing
                    mail.store(email_id, '+FLAGS', '\\Seen')
                    print(f"Marked email from {from_email} as seen.")

        except Exception as e:
            print(f"Error processing emails: {e}")

        # Wait before checking for new emails again
        time.sleep(2)  # Check for new emails every 2 seconds

def send_email(to_email, response, smtp_server, from_email, password):
    try:
        # Create the email response content
        msg = MIMEText(response)
        msg['Subject'] = "Re: Your Inquiry"
        msg['From'] = from_email
        msg['To'] = to_email

        print(f"Attempting to send email to {to_email}...")  # Log the target email address

        # Send the email using SMTP
        with smtplib.SMTP(smtp_server, 587) as server:
            server.starttls()  # Upgrade to a secure connection
            print("SMTP connection established.")
            server.login(from_email, password)
            print(f"Logged in to SMTP server as {from_email}.")
            server.sendmail(from_email, to_email, msg.as_string())
            print(f"Email sent successfully to {to_email}!")  # Log on successful send

    except Exception as e:
        print(f"Failed to send email to {to_email}. Error: {e}")  # Log the error if sending fails

if __name__ == "__main__":
    print("Starting the email FAQ responder...")
    start_time = datetime.now(pytz.utc)  # Record the current time when the script starts (timezone-aware)
    print(f"Start time recorded as: {start_time}")
    
    try:
        check_email_and_respond(start_time)
    except Exception as e:
        print(f"Error in email responder: {e}")
