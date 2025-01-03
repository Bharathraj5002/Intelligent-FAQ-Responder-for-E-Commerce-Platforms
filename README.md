# Intelligent FAQ Responder for E-Commerce Platforms

## Project Overview
The **Intelligent FAQ Responder** is a Python-based application that automates responses to customer inquiries by processing emails, categorizing queries using NLP models, and sending appropriate replies. The system leverages pre-trained Sentence Transformer models for similarity detection between customer queries and a predefined FAQ dataset.

## Key Features
- **Automated Email Processing:** Connects to an email server, fetches unread emails, and processes their content.
- **Query Categorization:** Uses Sentence Transformer models to classify queries and find the most relevant FAQ response.
- **Email Response:** Sends personalized responses to the customer’s email.
- **Logging and Monitoring:** Outputs detailed logs for processing emails and sending responses.

## System Requirements
### Software
- Python 3.8 or higher
- Required Python libraries:
  - `os`
  - `time`
  - `imaplib`
  - `smtplib`
  - `email`
  - `datetime`
  - `sentence_transformers`
  - `pandas`
  - `pytz`

### Hardware
- Adequate RAM and CPU for running NLP models (minimum 4GB RAM recommended).

### Dependencies
- SMTP access for sending emails
- IMAP access for retrieving emails
- A pre-trained Sentence Transformer model (e.g., `all-MiniLM-L6-v2`)
- FAQ dataset in CSV format

## Installation Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-repo/intelligent-faq-responder.git
   cd intelligent-faq-responder
   ```

2. **Install Required Libraries:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare the FAQ Dataset:**
   - Place your FAQ dataset in the project directory with the name `Ecommerce_FAQs.csv`.
   - Ensure the CSV file has two columns: `prompt` (query) and `response` (answer).

4. **Configure Email Credentials:**
   - Update the following placeholders in the script:
     - `your_email`: Your email address
     - `#`: Your email password (use an App Password if applicable)

5. **Run the Application:**
   ```bash
   python main.py
   ```

## Usage
1. **Dataset Preparation:**
   - Ensure the FAQ dataset is complete and formatted correctly.
   - FAQ columns should include `prompt` and `response`.

2. **Script Execution:**
   - Run the script to start monitoring the email inbox for new queries.

3. **Email Responses:**
   - The script will automatically detect unseen emails, generate appropriate responses, and send them back to the customer.

## Folder Structure
```
intelligent-faq-responder/
├── main.py               # Main application script
├── Ecommerce_FAQs.csv    # FAQ dataset
├── sentence_transformer_model/  # Pre-trained model cache
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
```

## FAQ Dataset Example
| prompt                 | response                    |
|------------------------|-----------------------------|
| What is your return policy? | Our return policy lasts 30 days. |
| How can I track my order?   | You can track your order at this link. |

## Future Enhancements
- Multi-language query support.
- Real-time dashboard for monitoring email processing.
- Integration with additional customer support channels (e.g., chatbots).
- Advanced NLP models for better query understanding.

## Contributors
- **Your Name** - Project Lead
- **Team Members** - Contributors

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- Thanks to the Sentence Transformers library for pre-trained models.
- Inspired by automated customer support systems in e-commerce.
