import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from confluent_kafka import Consumer, KafkaException

SMTP_SERVER = "smtp.gmail.com"  # Use the SMTP server of your email provider
SMTP_PORT = 587                # SMTP port (Gmail uses 587 for TLS)
EMAIL_SENDER = "harishkalyanml@gmail.com"
EMAIL_PASSWORD = "abpauomaawqpbzhp"  # Use app-specific password for Gmail
EMAIL_RECIPIENT = "harishkalyanml@gmail.com"


def message_handler(msg):
    """Handle received messages."""
    print(f"Received message: {msg.value().decode('utf-8')}")
    send_email("Current Weather",msg.value().decode('utf-8'))

def send_email(subject, body):
    try:
        # Set up the MIME message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECIPIENT
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))  # Plain text email body

        # Connect to SMTP server and send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")



def kafka_consumer():
    kafka_broker = 'kafka:9092'
    consumer = Consumer({
        'bootstrap.servers': kafka_broker,
        'group.id': 'weather_group',
        'auto.offset.reset': 'earliest',
    })

    topic = "weather_topic"
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(timeout=1000)
            # consumer.consume(num_messages=1, timeout=1000, callback=message_handler)
            if msg is None:
                print("No message received in this poll interval.")
                continue
            if msg.error():
                raise KafkaException(msg.error())
            message_handler(msg)
    except KeyboardInterrupt:
        print("Consumer Interrupted")
    finally:
        consumer.close()

if __name__ == '__main__':
    kafka_consumer()