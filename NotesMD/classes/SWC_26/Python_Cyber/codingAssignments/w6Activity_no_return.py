# Vacation Assistant 


class Vacation:

    # Constructor 
    def __init__(self):
        self.organizer_name = "" 
        self.destination = ""
        self.group_size = 0 
        self.price_per_person= 0 

    # Method #1 
    def whoIsOrganizer(self):
        self.organizer_name = input(f"\nHello, this is your vacation assistant. Please provide your name:\n")
        print(f"\nNice to meet you {self.organizer_name}, Looking forward to helping plan your next vacation!")
        return
    
    # Method #2
    def vacationDetails(self):
        print("\nDestination options: Cabo San Lucas, La Paz, Cancun, Oaxaca, Mexico City.")
        self.destination = input(f"{self.organizer_name}, could you provide which destination from the list provided that you'd like to travel to?\n")
        print("\nThank you!\n")
        self.group_size = int(input(f"\nCan you provie how many travelers, including yourself, will be on this trip to {self.destination}?\n"))

        print(f"\nThank you for providing this information {self.organizer_name}!\n")
        return
    
    # Method #3
    def tripCostCalculator(self):
        destination_prices = {'Cabo San Lucas': 500, 'La Paz': 430, 'Cancun': 800, 'Oaxaca': 650, 'Mexico City': 480}
        total_price = 0
        per_person = 0

        for place in destination_prices:
            if place == self.destination:
                total_price = destination_prices[place] * self.group_size
                per_person = destination_prices[place]

        print(f"\n{self.organizer_name} the total cost to travel to {self.destination} is ${total_price} for all {self.group_size} people.\nThe price per person is ${per_person}.")
        return

newVacation2 = Vacation()



newVacation = Vacation()
newVacation.whoIsOrganizer()
newVacation.vacationDetails()
newVacation.tripCostCalculator()