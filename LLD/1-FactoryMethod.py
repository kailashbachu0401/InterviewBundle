from abc import ABC, abstractmethod
from collections import defaultdict

# Step 1: Create a common interface
class Notifier(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass

# Step 2: Concrete classes
class EmailNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"Sending EMAIL: {message}")


class SMSNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"Sending SMS: {message}")


class PushNotifier(Notifier):
    def send(self, message: str) -> None:
        print(f"Sending PUSH notification: {message}")

# Step 3: Create a factory class
class NotifierFactory:
    def get_notifier(self, notifier_type: str) -> Notifier:
        if notifier_type == "email":
            return EmailNotifier()
        elif notifier_type == "sms":
            return SMSNotifier()
        elif notifier_type == "push":
            return PushNotifier()
        else:
            raise ValueError(f"Invalid notifier type: {notifier_type}")

# Client code
def send_notification(channel: str, message: str) -> None:
    notifier = NotifierFactory.create_notifier(channel)
    notifier.send(message)


send_notification("email", "Your order has been shipped.")
send_notification("sms", "OTP is 123456.")
send_notification("push", "You have a new follower.")

'''
When we say factory method, we mean:
- a method whose main job is to create and return objects

Instead of the caller deciding which class to instantiate, the factory method does it.

Instead of client doing below:
if channel == "email":
    notifier = EmailNotifier()
elif channel == "sms":
    notifier = SMSNotifier()
elif channel == "push":
    notifier = PushNotifier()

Client just does:
NotifierFactory.create_notifier('email')

- The factory takes care of creating the right object.

Client doesn't care how the object i created, he just tells what he wants.

instead of:
if choice == "veg":
    pizza = VegPizza()
elif choice == "chicken":
    pizza = ChickenPizza()

client just does:
pizza = PizzaFactory.create_pizza(choice)

When should you use it?
Use Factory Method when:

object creation has conditions
you have multiple subclasses with the same interface
you want cleaner code
you want to avoid repeated if-else creation logic
you may add more object types later

The subclasses can also override to decide which object to be created or something
'''

'''
TODO Simple Factory vs Factory Method vs Abstract Factory
'''

'''
you can also re use objects with factory methods
- Object Pooling
'''

class NotifierFactory:
    _instances = defaultdict(list)  # cache

    @staticmethod
    def create_notifier(channel: str) -> Notifier:
        channel = channel.lower()

        # ✅ Reuse if already created
        if NotifierFactory._instances[channel]:
            print("Reusing existing instance...")
            return NotifierFactory._instances[channel].pop()

        # ❌ Otherwise create new
        if channel == "email":
            notifier = EmailNotifier()
        elif channel == "sms":
            notifier = SMSNotifier()
        elif channel == "push":
            notifier = PushNotifier()
        else:
            raise ValueError(f"Unsupported channel: {channel}")

        # ✅ Store for reuse
        NotifierFactory._instances[channel].append(notifier)

        return notifier