# Vacation Assistant 


class Vacation:

    # Constructor 
    def __init__(self, organizer_name, destination, group_size):
        self.organizer_name = organizer_name
        self.destination = destination 
        self.group_size = group_size

    # Method #1 
    def whoIsOrganizer(self):
        print(f"\nOrganizer's name: {self.organizer_name}")
        return
    
    # # Method #2
    # def vacationDetails(self):
    #     print("\nDestination options: Cabo San Lucas, La Paz, Cancun, Oaxaca, Mexico City.")
    #     self.destination = input(f"{self.organizer_name}, could you provide which destination from the list provided that you'd like to travel to?\n")
    #     print("\nThank you!\n")
    #     self.group_size = int(input(f"\nCan you provie how many travelers, including yourself, will be on this trip to {self.destination}?\n"))

    #     return f"\nThank you for providing this information {self.organizer_name}!\n"
    
    # # Method #3
    # def tripCostCalculator(self):
    #     destination_prices = {'Cabo San Lucas': 500, 'La Paz': 430, 'Cancun': 800, 'Oaxaca': 650, 'Mexico City': 480}
    #     total_price = 0
    #     per_person = 0

    #     for place in destination_prices:
    #         if place == self.destination:
    #             total_price = destination_prices[place] * self.group_size
    #             per_person = destination_prices[place]

    #     return f"\n{self.organizer_name} the total cost to travel to {self.destination} is ${total_price} for all {self.group_size} people.\nThe price per person is ${per_person}."

# Create Object 
newVacation = Vacation("kevin", "La Paz", 3)


newVacation.whoIsOrganizer()

# print(newVacation.vacationDetails())
# print(newVacation.tripCostCalculator())

