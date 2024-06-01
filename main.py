import requests
from lxml import html
import random


def random_year():
    """
    this function is designed to pick a random year from 1 c.e. to the present
    :return: returns year string that can be added to the end of the url
    """
    rand_year = random.randint(1, 2024)
    return rand_year


def random_eve(year_frag):
    """
    this function takes a usable year fragment and return a list of events that happened
    during the year specified.
    :param year_frag: this would ideally be string returned from random_year() but doesn't necessarily have to be
    :return: returns a list of events that happened in the year provided as a parameter, from wikipedia
    """
    url = "https://en.wikipedia.org/wiki/"
    usable_url = f'{url}{year_frag}'
    page = requests.get(usable_url)
    tree = html.fromstring(page.content)
    events_section = tree.xpath('//span[@id="Events"]/following::ul[1]//li')
    return events_section


# This keeps looping through trivia questions until the user ends the game, and 'gaming' becomes false
gaming = True
average = 0
question = 1
score = 0
while gaming:
    year = random_year()
    # this changes 'year' into a form that can be attached to the
    # generic wikipedia url. Some single year pages have 'AD_' formating and some don't, and this is accounted for here.
    if int(year) <= 150 or int(year) == 1000 or int(year) == 500:
        year = "AD_", year
    # This creates a list variable of all the random events in a given year
    random_event = random_eve(year)
    # This loop basically makes sure the year generated actually has notable events (some don't)
    # and regenerates the list until a year with events is chosen
    while len(random_event) == 0:
        year = random_year()
        random_event = random_eve(year)
    # picks a specific random event to ask the user
    random_date = random_event[random.randint(0, len(random_event)-1)].text_content()
    # The next few lines are just for eliminating some of the brackets wikipedia uses at the end of some of the strings
    # that are created, it's just for cleaner print-outs
    last_period_index = random_date.rfind('.')
    if last_period_index > 0:
        random_date = random_date[:last_period_index+1]
    print(random_date)
    # This loop will keep querying the user for a valid integer (which is ideally a valid year)
    # until they provide them, and then moves on
    while True:
        guess = input("Guess the date this happened? ")
        try:
            int(guess)
        except ValueError:
            print("Please enter a real year...")
            continue
        else:
            break
    # Actually changes the string to an int after finding out if it will crash the program or not
    guess = int(guess)
    # saves how close the user was with their guess
    distance = abs(guess-year)
    # I'm awarding points if the user can get within 100 years of the event. Some of the random
    # events are pretty obscure, so the closer they are, the more points the user gets.
    if distance <= 100:
        score = 10000-(10000*(distance/100.0))
        if score == 10000:
            print("Wow!!! You really know your history, that's exactly right.", end=" ")
        else:
            print("Not quite right. You got kinda close, so you get partial credit.")
            print("The correct answer was: ", year, end=" ")
        print("Your score is:", int(score))
    else: print("Not even close... \nThe correct answer was", year, "C.E.")
    # After the user is told the correct answer, they get the option to keep playing or not.
    again = input("Would you like to play again? Type 'y' for Yes and 'n' for No: ")
    average = int((average+score)/question)
    print("Average score for this session is:", average)
    question+=1
    # if the user enters 'n', or anything else really, gaming will be false, and the game will end.
    if again != "y":
        gaming = False
