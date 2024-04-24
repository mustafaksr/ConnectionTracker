import pika
import requests

def callback(ch, method, properties, body):
    # Process the message
    message = body.decode('utf-8')
    print(f"Received message: {message}")
    
    # Send the message to the backend API
    backend_url = "http://backend:3000/api/messages"  # Update with your actual backend URL
    response = requests.post(backend_url, json={"message": message})
    
    if response.status_code == 200:
        print("Message sent to backend successfully")
    else:
        print("Failed to send message to backend")

# Define your RabbitMQ connection parameters and setup
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
# Declare the queue and set up the callback
channel.queue_declare(queue='your_queue_name')
channel.basic_consume(queue='your_queue_name', on_message_callback=callback, auto_ack=True)



# This block ensures that the code runs only when executed as the main program
if __name__ == '__main__':
    # Start consuming messages
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
