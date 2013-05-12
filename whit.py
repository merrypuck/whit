from bs4 import BeautifulSoup               # HTML handling
from flask import Flask, request, redirect  # Routing
import getSummary                           # A home grown truncation tool
import json                                 # Python's built in JSON library
import twilio.twiml                         # Handle twilio responses
from twilio.rest import TwilioRestClient    # Handle twilio requests
from urllib import urlopen                  # General Python requests

#   CrunchBase API Key
api_key = '6susy5mbbncvm45hsav4rabd'

#   Bit.ly API Key
access_token = '794e02fd047d7fcc0c44543742d0f471e2f9ebc8'

#   Required for Google App Engine's app.yaml
app = Flask(__name__)

# ------------------------------------------------------
#    Utility method to get a bitly shortlink from a URL
# ------------------------------------------------------

def getShortlink(url):

    #   Prep a link to the bitly 
    shortapi = "https://api-ssl.bitly.com/v3/shorten?access_token=" + access_token + "&longUrl=" + url
    
    #   Ask bit.ly for the shortlink
    shortLinkResponse = json.loads( urlopen(shortapi).read() )

    #   Pull the result out of the response dictionary
    fullShortLink = shortLinkResponse['data']['url']

    #   Shorten the shortlink, haha!
    shortLinkToDisplay = str(shortLink)[7:15]+str(shortLink)[15:]

    # return
    return shortLinkToDisplay

# --------------------------
#   Replace spaces with %20
# --------------------------

def sanitize(url):

    #   Break up a URL by spaces
    url = url.split(' ');    

    # Put the %20 in
    url = '%20'.join(url)

    return str(url)

# -------------------------------------------------------
#   Retrieve the contents of a URL and return it as JSON
# -------------------------------------------------------

def JSONFromURL(url):

    #   Read the URL contents as a string
    urlContents = urlopen(url).read()

    #   Convert the string to JSON
    json = json.loads(urlContents)

    #   Return 
    return json

# --------------------------------------------------------
#   Retrieve the contents of a URL and return the summary
# --------------------------------------------------------

def summaryFromURL(url):
    
    #   Grab the JSON
    entry = JSONFromURL(url)

    #   Retrieve the overview
    entryText = entry["overview"]).get_text()

    #   Ensure the overview is well formed
    overview = BeautifulSoup(entryText)

    #   Summarize and return the overview
    return getSummary(overview)


# -------------------------------------------------------------
#   Retrieve the contents of a URL and return the phone number
# -------------------------------------------------------------

def phoneNumberFromURL(url):

    #   Grab the JSON
    entry = JSONFromURL(url)

    #   Retrieve the overview
    number = entry["phone_number"]).get_text()

    return number


# ------------------------------------------------------
#   Requests information about a person from CrunchBase.
#   
#   queryCrunchBaseForPerson takes two string arguments:
#
#   firstName: The person's first name.
#   lastName: The person's last name.
# ------------------------------------------------------

def queryCrunchBaseForPerson(firstName, lastName):

    # -----------------------------------------
    #   Retrieve the pernalink from CrunchBase
    # -----------------------------------------

    #   Define a URL to query - Returns a permalink for the relevant username. Also returns a relevant website, if applicable.
    summaryURL = 'http://api.crunchbase.com/v/1/people/permalink?first_name=' + firstName + '&last_name=' +lastName + '&api_key=' + api_key
    
    #   The URL returns a summary as a string, convert it to a JSON object
    summary = JSONFromURL(summaryURL)
    
    #   Read out the slug from the dictionary 
    slug = summary['permalink']
    
    # -----------------------
    #   Generate a shortlink
    # -----------------------

    shortLinkToDisplay = getShortlink(summary['crunchbase_url'])

    # -----------------------------------
    #   Retrieve and summarize the entry
    # -----------------------------------

    #   The CrunchBase entry URL
    entryURL = 'http://api.crunchbase.com/v/1/person/' + slug + '.js?api_key=' + api_key
    
    #   Summarize the overview
    entrySummary = summaryFromURL(entryURL)

    # ---------
    #   Return
    # ---------

    return entrySummary + shortLinkToDisplay
    

# -------------------------------------------------
#   Retrieve a company profile from CrunchBase
# -------------------------------------------------

def queryCrunchBaseForCompanySummary(company):

    # -------------------------------------------------
    #   Retrieve the summary permalink from CrunchBase
    # -------------------------------------------------

    #   Sanitize the name before passing to the CrunchBase API
    company = sanitize(company)

    #   Construct a summary URL
    summaryURL = 'http://api.crunchbase.com/v/1/companies/permalink?name=' + company + '&api_key=' + api_key

    #   Convert the summary to dictionary
    summary = JSONFromURL(summaryURL)

    #   Grab the permalink
    slug = summary['permalink']
    
    # -----------------------
    #   Generate a shortlink
    # -----------------------

    shortLinkToDisplay = getShortlink(summary['crunchbase_url'])

    # -----------------------------------
    #   Retrieve and summarize the entry
    # -----------------------------------

    #   Construct a URL to the actual CrunchBase Profile
    entryURL = 'http://api.crunchbase.com/v/1/company/' + slug + '.js?api_key=' + api_key
    
    #   Summarize the overview
    entrySummary = summaryFromURL(entryURL)

    # ---------
    #   Return
    # ---------

    return entrySummary + shortLinkToDisplay


# --------------------------------------------------
#   Retrieve a company phone number from CrunchBase
# --------------------------------------------------

def queryCrunchBaseForCompanyNumber(company):

    # -------------------------------------------------
    #   Retrieve the summary permalink from CrunchBase
    # -------------------------------------------------

    #   Sanitize the company
    company = sanitize(company)

    #   summary URL
    summaryURL = 'http://api.crunchbase.com/v/1/companies/permalink?name=' + company + '&api_key=' + api_key
    
    #   Convert the summary to dictionary
    summary = JSONFromURL(summaryURL)

    #   Grab the permalink slug
    slug = summary['permalink']

    # -----------------------
    #   Generate a shortlink
    # -----------------------

    shortLinkToDisplay = getShortlink(summary['crunchbase_url'])
        
    # -----------------------------------
    #   Retrieve and summarize the entry
    # -----------------------------------

    entryURL = 'http://api.crunchbase.com/v/1/company/' + slug + '.js?api_key=' + api_key
    
    #   Summarize the overview
    number = phoneNumberFromURL(entryURL)
    
    # ---------
    #   Return
    # ---------

    return company + ': ' + number

def parseWiki(search):

    url = 'http://en.wikipedia.org/w/api.php?format=json&action=opensearch&search=' + search + '&prop=revisions&rvprop=content'

    r = urlopen(url).read()

    dict1 = json.loads(r)

    dict2 = dict1['1'][0]

    url2 = 'http://en.wikipedia.org/wiki/' + dict2

    '''
    #Finding page id:
    dict3 = dict2.split(" ")
    if dict3.length() > 1:
        dict3 = dict2[0]
        for i in range(1, company.length()):
             dict3 = dict3 + '_' + dict2.split(" ")[i]

    url2 = 'http://en.wikipedia.org/wiki/' + dict3
    http://en.wikipedia.org/w/api.php?action=query&titles=Albert%20Einstein&prop=info&format=jsonfm
    '''
    #parse article
    p = 'http://en.wikipedia.org/w/api.php?action=parse&prop=text&page=' + dict2 + '&format=json'
    p1 = urlopen(p).read()
    p2 = json.loads(p1)
    p3 = p2['parse']['text']['*']
    p4 = BeautifulSoup(p3)
    p5 = p4.find_all('p')
    p6 = p5[0]
    p7 = p6.getText()

    #create bitly shortlink
    shortapi = "https://api-ssl.bitly.com/v3/shorten?access_token=794e02fd047d7fcc0c44543742d0f471e2f9ebc8&longUrl=" + url2
    shortLink = json.loads( urlopen(shortapi).read() )
    shortened = shortLink['data']['url']

    return getSummary(p7 ) + str(shortened)[7:15]+str(shortened)[15:]

def parseStock(ticker):
    url = 'http://dev.markitondemand.com/Api/Quote/json?symbol=' + ticker + '&callback=myFunction'
    r = urlopen(url).read()

    e = json.loads(r)

    return str(e['Data']['Name']) + '[' + str(e['Data']['Symbol']) + ']: ' + 'is priced $'+ str(e['Data']['LastPrice']) + ". Since " + str(e['Data']['Timestamp'])


@app.route("/", methods=['GET', 'POST'])
def hello_monkey():

    twilioInput = request.form['Body']
    text_body = twilioInput.split(" ")
    
    inputString = text_body[0]
    firstLetter = text_body[0][0]
    firstLetters = text_body[0][:2]

    # p for person
    # c for company 
    # # for company number
    # w for wiki
    # text_body[0] is first name, text_body[1] is last name
    if inputString.__len__() > 0:
        if firstLetters.lower() == 'p:':
            try:
                twilioOutput = queryCrunchBaseForPerson(text_body[0][2:].lower(), text_body[1].lower())
            except:
                twilioOutput = "Sorry, no one named " + text_body[0][2:] + " exists in crunchbase."

        elif firstLetters.lower() == 'c:':
            try:
                twilioOutput = queryCrunchBaseForCompanySummary(twilioInput[2:])
            except:
                twilioOutput = "Sorry, no company named '" + twilioInput[2:] + "' exists in crunchbase."

        elif inputString[:3] == 'c#:':
            try:
                twilioOutput = queryCrunchBaseForCompanyNumber(inputString[1:])
            except:
                twilioOutput = "Sorry, no number exists for this company." 

        elif firstLetters.lower() == 'w:':
            try: 
                twilioOutput = parseWiki(twilioInput[2:])
            except:
                twilioOutput = "Sorry, no matches came up for your wiki query, please refine your search."

        elif firstLetters.lower() == 's:':
            try:
                twilioOutput = parseStock(inputString[2:])
            except:
                twilioOutput = "Sorry, no matches came up for your stock query, please refine your search."

        elif twilioInput.lower() == 'h':
            twilioOutput = "Input is of any form. Special commands include P:'person', C:'company', S:'Stock', W:'wikiSearch'\nP:Bill Gates\nC:Google\nC#:google\nS:aapl\nW:obama" 
        
        else:
            try:
                twilioOutput = parseWiki(twilioInput)
            except:
                "Please enter a valid wiki search query. Type * for more options."
    else:
        try:
            twilioOutput = parseWiki(twilioInput)
        except:
            "Please enter a valid wiki search query. Type * for more options."

#twilioOutput = "Input is of any form. Special commands include P:'person', C:'company', S:'Stock', W:'wikiSearch'\nP:Bill Gates\nC:Google\nC#:google\n S:aapl\nW:new york"
    
    '''
    account_sid = "ACa1c928ab9eb750ba1fb4ed0953f0f032"
    auth_token = "9365adeb7fe7068e0859bb8c89437607"
    client = TwilioRestClient(account_sid, auth_token)

    from_number = request.values.get('From', None)
    message = client.sms.messages.create(to=from_number, from_="+19177913098", body="From the Hackathon:")
    '''
    resp = twilio.twiml.Response()
    resp.sms(twilioOutput)
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)