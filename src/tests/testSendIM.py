from src.helpers.instantMessage import sendIM
from pprint import pprint

# VARS
body = "Join Earth's mightiest heroes. Like Kevin Bacon."

# TEST FUNCTIONS
def test() -> None:
    output = sendIM(
        body=body,
        forceSend=True,  # send IM regardless of settings
    )
    print(">>> SUCCESS?")
    pprint(output)


# EXECUTE
test()
