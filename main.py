# Database for this project
# Helped by Professor Bulat Filin (Medgar Evers College)
#https://raw.githubusercontent.com/LearnDataSci/articles/master/Python%20Pandas%20Tutorial%20A%20Complete%20Introduction%20for%20Beginners/IMDB-Movie-Data.csv
#https://volkanpaksoy.com/archive/2013/08/03/imdb-data-parsing-with-regular-expressions/

import re
import csv
import datetime

class regexMovie:

  def __init__(self, debug = False, filename = "IMDB-Movie-Data.csv", usaddress = "US.csv"):
    "Constructor for regexMovie class which intializes the filename and other internal values"
    self.match = None
    self.filename = filename
    self.db = list(csv.DictReader(open(filename,'r')))
    # self.db = open(filename,'r').read().split('\n')
    # self.dbus = list(csv.DictReader(open(usaddress,'r'),delimiter='\t')) # enable to use US.csv db of addresses
    # https://raw.githubusercontent.com/midwire/free_zipcode_data/develop/all_us_zipcodes.csv
    self.dbus = open(usaddress,'r').read().split('\n')
    self.pattern = "(^.+)"
    self.movieToPurchase = None
    self.userInputGroups = None
    self.debug = debug
    self.search = None
    self.okToPurchase = False
    self.purchaseInfo = {"first_name": None, "last_name": None, 
                        "name_suffix": None,"email_address":None, "street_address": None,
                        "state":None,
                        "zipcode": None,"city": None, "card_number":None,
                        "card_expr": None, "card_sec": None }

  
  def isOkToPurchase(self):
    if self.okToPurchase != True:
      print("Purchase was not authorized, ERROR 404")
      exit()
  
  def lookupMoviesByYear(self):
    print("\n Performing lookup by Year ")
    print(" ========================= ")
    found = False
    for element in self.db:
      x = re.findall(self.search, element["Year"])
      if x:
        self.movieToPurchase=element
        print(self)
        answer = self.getAnswer(">> Is this the movie that your looking for Y|N: \n")
        if answer == 'y':
          found = True
          break
        else:
          self.movieToPurchase = None

    if found:
      print("\nGreat we've found the movie you searched for")
      answer = self.getAnswer(">> would you like to purchase it, Y|N: ")
      if answer == 'y':
        self.okToPurchase = True
      else:
        print("Please come back next time to the Movie app!")
        exit()
    else:
      print("Sorry we couldn't find a film for you, please come soon")
      print("We are always adding new films")
      exit()
 

  # spell checker for the movie app if user types in a wrong word
  def lookupMoviesByTitle(self):
    "Search, Retrieve and print the user(s) selected movie and sets up movie to be purchase by user(s)"
    print("\n Performing lookup by Title ")
    print(" ========================== ")
    found = False
    for element in self.db:
      x = re.fullmatch(self.search, element["Title"], re.IGNORECASE)
      if x:
          self.movieToPurchase=element
          found = True
          print(self)
          break
    if not found:
      print("This exact film was not found")
      answer = self.getAnswer(">> Do you want a more extensive search\nbased on partial match of particular title Y|N: ")
      if answer == 'y': # please set user(s) input to lowercase for best/simple matching
        # search data for partial format
        for element in self.db:
          x = re.findall(self.search, element["Title"], re.IGNORECASE)
          if x:
            self.movieToPurchase=element
            print(self)
            answer = self.getAnswer(">> Is this the movie that your looking for Y|N: \n")
            if answer == 'y':
              found = True
              break
            else:
              self.movieToPurchase = None
      else:
        print("You ended the search, please come back next to the Movie app!")
        exit()
    
    if found:
      print("\nGreat we've found the movie you searched for")
      answer = self.getAnswer(">> would you like to purchase it, Y|N: ")
      if answer == 'y':
        self.okToPurchase = True
      else:
        print("Please come back next time to the Movie app!")
        exit()
    else:
      print("Sorry this particular film was not found")
      exit()
    
    
  def getAnswer(self, message, c1 = 'y', c2 = 'n'):
    answer = input(message)
    if answer.lower() == c1.lower() or answer.lower() == c2.lower():
      return answer.lower()
    else:
      print('Answer must be', c1 + '|' + c2)
      return self.getAnswer(message, c1, c2)


  def __getValue__(self, pattern, message, errorMsg = None, flags = re.IGNORECASE):
    'Gets value from user(s) input for their first and last name'
    value = input(message)
    results = re.fullmatch(pattern, value, flags)
    if results != None:
      return value
    else:
      if errorMsg != None:
        print(errorMsg)
      return self.__getValue__(pattern, message, errorMsg)


  def getName(self, control = "all"):
    # https://www.oreilly.com/library/view/regular-expressions-cookbook/9780596802837/ch04s18.html
    #https://stackoverflow.com/questions/20353995/extracting-first-name-and-last-name-in-python
    self.isOkToPurchase()
    "Gets user(s) first, last and suffix name"
    namePattern = "([A-z]{1}[a-z]+)([ -]*)([A-z]{1}[a-z]+)*"
    suffix_name_pattern = '(?:[iI][xX]|[iI][vV]|[Vv]?[iI]{0,3}|[JSjs][rR]|[nN]/?[aA])$'
    if control == "all" or control == "first_name":
      self.purchaseInfo["first_name"] = self.__getValue__(namePattern, "Please enter your first name: ")
    if control == "all" or control == "last_name":
      self.purchaseInfo["last_name"] = self.__getValue__(namePattern, "Please enter your last name: ")
    if control == "all" or control == "name_suffix":
      self.purchaseInfo["name_suffix"] = self.__getValue__(suffix_name_pattern, "Please enter your suffix, or enter n/a: ")

    #https://stackoverflow.com/questions/46079770/validate-card-numbers-using-regex-python
    #http://blog.unibulmerchantservices.com/10-signs-of-a-valid-american-express-card/#:~:text=What%20does%20the%20AmEx%20card,Discover's%20%E2%80%94%20with%20%E2%80%9C6%E2%80%9D
    #https://www.oasis-open.org/khelp/kcommerce/user_help/html/your_security_code.html


  def getSecurityCodeOfCard(self):
    "Get and verify credit/debit security code"
    self.isOkToPurchase()
    securityCode = "(?:([0-9]{3}|[0-9]{4}))"
    self.purchaseInfo["card_sec"] = self.__getValue__(securityCode, "Please enter your card's security code: ")
    visa_master_discover_startNumbers = ['4', '5', '6']
    if self.purchaseInfo["card_number"][0] == '3' and len(self.purchaseInfo["card_sec"]) != 4:
      print("Invalid security code for AMEX credit/debit card")
      self.getSecurityCodeOfCard()
    elif self.purchaseInfo["card_number"][0] in visa_master_discover_startNumbers and len(self.purchaseInfo["card_sec"]) != 3:
      print("Invalid security code for Visa/MasterCard/Discover credit/debit card")
      self.getSecurityCodeOfCard()

 
  def getCreditOrDebitCard(self):
    "Get and verify credit/debit card number"
    self.isOkToPurchase()
    visa_master_discover = "(?:([4-6]{1}[0-9]{3}-)([0-9]{4}-){2})[0-9]{4}|[4-6]{1}[0-9]{15}"
    amex = "|[3]{1}[47]{1}[0-9]{2}-[0-9]{6}-[0-9]{5}|[3]{1}[47]{1}[0-9]{13}"
    all_cards = visa_master_discover + amex
    self.purchaseInfo["card_number"] = self.__getValue__(all_cards, "Please enter your credit/debit number: ")

  
  def getCardExpirationDate(self):
    "Get and verify credit/debit card expiration date"
    self.isOkToPurchase()
    current_year = str(datetime.datetime.now().year)
    # exprDate_regex = "(?:([0]{1}[1-9]{1}|[1]{1}[0-2]{1})/([2]{1}[1-6]{1}))"
    exprDate_regex = "(?:([0]{1}[1-9]{1}|[1]{1}[0-2]{1})/(%s{1}[%s-%s]{1}))" %(current_year[2], current_year[3], int(current_year[3]) + 6)
    self.purchaseInfo["card_expr"] = self.__getValue__(exprDate_regex, "Please enter your expiration date: ", "Invalid input or expiration date: format should be: MM/YY")

  
  #https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
  #https://stackoverflow.com/questions/9238640/how-long-can-a-tld-possibly-be
  def getEmailAddress(self):
    "Get and verify user(s) email address"
    self.isOkToPurchase()
    email_regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,24}$'
    #prior to 2015 this would have worked for all of the domains on the internet due to them sharing the same patterns.
    #regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    self.purchaseInfo["email_address"] = self.__getValue__(email_regex, "Please enter your email address: ")

  
  #https://stackoverflow.com/questions/7425860/regular-expression-get-us-zip-code
  def getZipCode(self):
    "Gets the user(s) zip code for billing purposes"
    self.isOkToPurchase() 
    # fix that we only capture 5 digits
    zipcode_regex = '^\d{5}(-\d{4})?$'
    self.purchaseInfo["zipcode"] = self.__getValue__(zipcode_regex, "Please enter your zip code: ", flags = 0)
    # 99950,Ketchikan,AK,KETCHIKAN GATEWAY,,55.542007,-131.432682
    found = False
    # check against the database of us addresses, there must be a match between zip and state
    for x in self.dbus:
        if re.fullmatch('^%s,.*,%s.*$' % (self.purchaseInfo["zipcode"], self.purchaseInfo["state"]),x):
            found = True
            break
    if not found:
        print("Billing info is not correct, state and zip do not match")
        self.purchaseInfo["zipcode"] = None
        self.getZipCode()


  def getCity(self):
    "Gets the user(s) city for billing purposes"
    self.isOkToPurchase() 
    city_regex = '^[A-Z]{1}[a-z]*[ -]?[A-Za-z]*$'
    self.purchaseInfo["city"] = self.__getValue__(city_regex, "Please enter the city: ")
    found = False
    for x in self.dbus:
        if re.fullmatch('^%s,%s,%s,.*$' % (self.purchaseInfo["zipcode"], self.purchaseInfo["city"], self.purchaseInfo["state"]),x, re.IGNORECASE):
            found = True
            break
    if not found:
        print("Billing info is not correct, city does not match state and zip")
        self.purchaseInfo["city"] = None
        self.getCity()



  #https://stackoverflow.com/questions/2313032/regex-for-state-abbreviations-python
  def getState(self):
    "Gets the user(s) state they reside in or billing address"
    self.isOkToPurchase()
    states = ['IA', 'KS', 'UT', 'VA', 'NC', 'NE', 'SD', 'AL', 'ID', 'FM', 'DE', 'AK', 'CT', 'PR', 'NM', 'MS', 'PW', 'CO', 'NJ', 'FL', 'MN', 'VI', 'NV', 'AZ', 'WI', 'ND', 'PA', 'OK', 'KY', 'RI', 'NH', 'MO', 'ME', 'VT', 'GA', 'GU', 'AS', 'NY', 'CA', 'HI', 'IL', 'TN', 'MA', 'OH', 'MD', 'MI', 'WY', 'WA', 'OR', 'MH', 'SC', 'IN', 'LA', 'MP', 'DC', 'MT', 'AR', 'WV', 'TX']
    state_regex = '^' + '|'.join(states) + '$'
    self.purchaseInfo["state"] = self.__getValue__(state_regex, "Please enter your state in two letter format, For example VA: ")

  
  #https://www.codeproject.com/Tips/989012/Validate-and-Find-Addresses-with-RegEx
  #https://stackoverflow.com/questions/18368086/find-a-us-street-address-in-text-preferably-using-python-regex
  def getStreetAdress(self):
    "Gets the user(s) street address for billing purposes"
    self.isOkToPurchase()
    street_regex = '\d+[ -](broadway|(?:[A-Za-z0-9.-]+[ ]?)+(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd|lane|ln|place|pl)\W?(?=\s|$))'
    self.purchaseInfo["street_address"] = self.__getValue__(street_regex, "Please enter your street address: ")


  def completeMissingInfo(self, key):
    "Process missing in billing information"
    if key == "first_name":
      self.getName(key)
    elif key == "last_name":
      self.getName(key)
    elif key == "name_suffix":
      self.getName(key)
    elif key == "street_address":
      self.getStreetAdress()
    elif key == "email_address":
      self.getEmailAddress()
    elif key == "state":
      self.getState()
    elif key == "zipcode":
      self.getZipCode()
    elif key == "city":
      self.getCity()
    elif key == "card_number":
      self.getCreditOrDebitCard()
    elif key == "card_expr":
      self.getCardExpirationDate()
    elif key == "card_sec":
      self.getSecurityCodeOfCard()
    else:
      print("Invalid infomation detected")
      exit()

      
  def confirmPurchase(self):
    self.isOkToPurchase()
    for key in self.purchaseInfo.keys():
      if self.purchaseInfo[key] == None:
        # print("Sorry your purchase info is incorrect or incomplete, please resubmit and correct or complete the following:", key)
        self.completeMissingInfo(key)
        print("Processing: ", key)
    print("Congratulations, your purchase is complete you will receive your receipt through your email")
    self.displayReceipt()
 

  def displayReceipt(self):
    print("\nYour receipt for your purchase today is: ")
    i = 0
    s = ""
    # s += "========================================\n"
    for key in self.movieToPurchase.keys():
      if i >= 1 and i <= 7:
        s = s + key + ": " + self.movieToPurchase[key] + "\n"
      i+=1
    s += "========================================\n"
    print(s)
    print("Total price: $10.00")
    print()


  def displayWelcomeScreen(self):
    print("\n   Welcome to the Movie app")
    print("==================================================================\n")
    print("There are two ways to search for a movie, either search my title or search by year, please choose one that you prefer")
    print("==================================================================\n")
    answer = self.getAnswer(">> Do you want to search by Title or Year, Title|Year: ", 'Title','Year')
    if answer == 'title':
      # self.search = input().rstrip()
      self.search = self.__getValue__(self.pattern, "Please enter the title of the movie: ")
      self.lookupMoviesByTitle()
    else:
        min_year_db = min([x.get('Year') for x in self.db])
        max_year_db = max([x.get('Year') for x in self.db])
        # lowest year 1900 - highest year 2021, will autodetect until 2029
        #year_regex = ':?19[0-9]{2}|20[0-1]{1}\d|202[0-%s]' % (current_year[-1])
        #This regex is ment for the database
        year_regex = ':?20(0[6-9]|1[0-6])'
        print("The years range from", min_year_db, "-", max_year_db, "in this application")
        self.search = self.__getValue__(year_regex, "Please enter the year of the movie: ", "We dont have films made in that year, please try from 2006 to 2016")
        self.lookupMoviesByYear()
    print(" >>", end=" ")
    
  
  def __repr__(self):
    "Controls what information is printed to the screen"
    if self.movieToPurchase != None:
      i = 0
      s = ""
      # s += "========================================\n"
      for key in self.movieToPurchase.keys():
        if i >= 0 and i <= 9 or  i == 11:
          s = s + key + ": " + self.movieToPurchase[key] + "\n"
        i+=1
      s += "========================================\n"
      return s
    else:
      return "film element not setup" 

# end of the regexMovie Class

def main():

  debug = False
  movieWanted =  regexMovie(debug)
  while(True):
    movieWanted.displayWelcomeScreen()
    movieWanted.confirmPurchase()
    if(movieWanted.getAnswer("Would you like to search again, Y|N :") == 'n'):
      break
  print("Please come back to the Movie app next time!")

if __name__ == "__main__":
  main() 