import typing
import requests

USERNAME_SMS = 'hamedan'  # noqa  # Sahand Sms username
PASSWORD_SMS = 'hamedan12345'  # noqa  # Sahand sms password


def send_sms(mobile: str = None, message: str = None) -> typing.Any:
    """ send sms to a number with custom message """

    url = f"http://webservice.sahandsms.com/newsmswebservice.asmx/SendPostUrl?" \
          f"username={USERNAME_SMS}&password={PASSWORD_SMS}" \
          f"&from=30002501&to={mobile}&message={message}"

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.request('GET', url, headers=headers)
    print(response)


if __name__ == "__main__":
    send_sms(mobile="09389657326", message="12345")