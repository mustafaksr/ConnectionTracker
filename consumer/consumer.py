import pika

# Connection parameters
connection_params = pika.ConnectionParameters('rabbitmq', 5672)  # Update with your RabbitMQ host and port
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Declare the queue
queue_name = 'my_queue'  # Update with the queue name you're using
channel.queue_declare(queue=queue_name)

# Callback function to handle received messages
def callback(ch, method, properties, body):
    print(f"Received message: {body.decode()}")

# Subscribe to the queue and consume messages
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

print("Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
