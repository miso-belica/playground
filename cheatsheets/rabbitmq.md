# Exchanges
- fanout - broadcasts all the messages it receives to all the queues it knows, ignores binding/routing key
- direct - The routing algorithm behind a direct exchange sends a message to the queues whose binding key exactly matches the routing key of the message.
- topic - Messages sent to a topic exchange can't have an arbitrary routing_key - it must be a list of words, delimited by dots. The words can be anything, but usually they specify some features connected to the message.
- headers
