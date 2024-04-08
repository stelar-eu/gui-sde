from confluent_kafka import Producer

# Kafka broker(s) configuration
bootstrap_servers = "localhost:9092"

# Create Producer instance
producer = Producer({
    'bootstrap.servers': bootstrap_servers
})

# Define the Kafka topic to which you want to send messages
topic = "OUT"

# Produce a message
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Asynchronous message production
for i in range(5):
    value = f"Message {i}"  # Your message content
    producer.produce(topic, value.encode('utf-8'), callback=delivery_report)

# Wait for all messages to be delivered
producer.flush()