import pandas as pd

df = pd.read_csv("hotels.csv", dtype={"id": str})
df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pd.read_csv("card_security.csv", dtype=str)

class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    # we want the function to act upon the class -
    # think about it like the class is the semantic patient

    def book(self):
        """Book a hotel by changing its availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """check if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class SpaHotel(Hotel):

    def book_spa(self):
        pass


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here is your booking information:
        Name: {self.customer_name}
        Hotel name: {self.hotel.name}
        """
        return content


class SpaTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object
    def generate(self):
        content = f"""
        Thank you for your spa reservation!
        Here is your booking information:
        Name: {self.customer_name}
        Hotel name: {self.hotel.name}
        """
        return content

class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {"number": self.number, "expiration": expiration,
                     "holder": holder, "cvc": cvc}
        if card_data in df_cards:
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_cards_security.loc[df_cards_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False


if __name__ == "__main__":
    print(df)
    hotel_ID = input("Enter the id of the hotel: ")
    hotel = SpaHotel(hotel_ID)
    if hotel.available():
        # in a real-world app, we would ask user for this info:
        # card_number = input("Credit card number: ")
        # card_expire_date = input("Card expiration date: ")
        # cardholder_name = input("Cardholder name: ")
        # cvc_code = input("Card CVC code: ")
        credit_card = SecureCreditCard(number="1234567890123456")
        if credit_card.validate(expiration="12/26",
                                 holder="JOHN SMITH", cvc="123"):
            # card_pass = input("card password: ")
            if credit_card.authenticate(given_password="mypass"):
                hotel.book()
                name = input("Enter your name: ")
                reservation_ticket = ReservationTicket(customer_name=name,
                                                       hotel_object=hotel)
                print(reservation_ticket.generate())

                spa_response = input("Would you like to book a spa package? ")
                if spa_response == "yes":
                    hotel.book_spa()
                    spa_ticket = SpaTicket(customer_name=name,
                                            hotel_object=hotel)
                    print(spa_ticket.generate())
            else:
                print("Credit card authentication failed")
        else:
            print("There was a problem with your payment")
    else:
        print("Hotel is not available")
