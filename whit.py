from flask import Flask, request, redirect
import twilio.twiml
from twilio.rest import TwilioRestClient
from urllib import urlopen
import json
from getSummary import getSummary
from bs4 import BeautifulSoup

#   CrunchBase API Key
api_key = '6susy5mbbncvm45hsav4rabd'

#   Bit.ly API Key
access_token = '794e02fd047d7fcc0c44543742d0f471e2f9ebc8'

#   Required for Google App Engine's app.yaml
app = Flask(__name__)

'''
   Requests information about a person from CrunchBase.
   Takes two strings:pi

   firstName: The person's first name.
   lastName: The person's last name.

''' 

def parsePerson(firstName, lastName):
    
    #   Define a URL to query - Returns a permalink for the relevant username. Also returns a relevant website, if applicable.
    summaryURL = 'http://api.crunchbase.com/v/1/people/permalink?first_name=' + firstName + '&last_name=' +lastName + '&api_key=' + api_key
    
    #   The URL returns a summary as a string, convert it to a JSON object
    queryResult = urlopen(summaryURL).read()
    summary = json.loads(queryResult)
    
    #   Read out the slug from the dictionary 
    slug = summary['permalink']
    
    #   This URL accesses the CrunchBase entry URL
    entryURL = 'http://api.crunchbase.com/v/1/person/' + slug + '.js?api_key=' + api_key
    
    #   The entry as a string
    entryString = urlopen(entryURL).read()
    entry = json.loads(entryString)
    
    #
    #   Adds bitly shortlink
    #

    #   Grab the CrunchBase URL
    crunchurl = summary['crunchbase_url']

    #   Prep a link to the 
    shortapi = "https://api-ssl.bitly.com/v3/shorten?access_token=" + access_token + "&longUrl=" + crunchurl
    shortLink = json.loads( urlopen(shortapi).read() )
    shortened = shortLink['data']['url']
    
    #return first ~140 characters with a bitly shortlink
    return getSummary( BeautifulSoup( entry["overview"] ).get_text() ) + str(shortened)[7:15]+str(shortened)[15:]

def parseCompany(company):
    #if company multiple words, add '%20' betweeen words
    #import pdb; pdb.set_trace()
    camt = company.split(' ')
    if camt.__len__() > 1:
        bamt = '%20'.join(camt)
        url = 'http://api.crunchbase.com/v/1/companies/permalink?name=' + str(bamt) + '&api_key=6susy5mbbncvm45hsav4rabd'

    else:
        url = 'http://api.crunchbase.com/v/1/companies/permalink?name=' + str(company) + '&api_key=6susy5mbbncvm45hsav4rabd'
                
    #r is a json file written as a string
    r = urlopen(url).read()
    
    #convert r to dictionary
    dict1 = json.loads(r)
    #perma is permalink to specfic page
    #try:
     #   dict1['permalink']
    #except NameError:
    a = dict1['permalink']
    url2 = 'http://api.crunchbase.com/v/1/company/' + a + '.js?api_key=6susy5mbbncvm45hsav4rabd'
    f = urlopen(url2).read()
    
    #load it as a json ( equivalent to json.loads(r) )
    dict2 = json.loads(f)
    
    #   adds bitly shortlink
    crunchurl = dict2['crunchbase_url']
    shortapi = "https://api-ssl.bitly.com/v3/shorten?access_token=794e02fd047d7fcc0c44543742d0f471e2f9ebc8&longUrl=" + crunchurl
    shortLink = json.loads( urlopen(shortapi).read() )
    shortened = shortLink['data']['url']
    return getSummary( BeautifulSoup( dict2["overview"] ).get_text() ) + str(shortened)[7:15]+str(shortened)[15:]


def parseCompanyNumber(company):
    #if company multiple words, add '%20' betweeen words
    camt = ""
    if company.split(" ").__len__() >= 2:
        camt = company.split(" ")[0]
        for i in range(1, company.__len__()):
             camt = camt + '%20' + company.split(" ")[i]

    url = 'http://api.crunchbase.com/v/1/companies/permalink?name=' + str(camt) + '&api_key=6susy5mbbncvm45hsav4rabd'
    
    #r is a json file written as a string
    r = urlopen(url).read()
    
    #convert r to dictionary
    dict1 = json.loads(r)
    
    #go to permalink and get overview
    url2 = 'http://api.crunchbase.com/v/1/company/' + dict1['permalink'] + '.js?api_key=6susy5mbbncvm45hsav4rabd'
    f = urlopen(url2).read()
    
    #load it as a json ( equivalent to json.loads(r) )
    dict2 = json.loads(f)
    
    crunchurl = dict1['crunchbase_url']
    shortapi = "https://api-ssl.bitly.com/v3/shorten?access_token=794e02fd047d7fcc0c44543742d0f471e2f9ebc8&longUrl=" + crunchurl
    shortened = shortapi['url']
    
    return "%s: %s %s" % (camt,dict2['phone_number',shortapi])

"""def parseSearch(search):

    url = 'http://api.crunchbase.com/v/1/search.js?query=' + str(search) + '&api_key=6susy5mbbncvm45hsav4rabd'

    r = urlopen(url).read()

    dict1 = json.loads(r)

    dict1Namespace = dict1['results'][0]['namespace']
    dict1Overview = dict1['results'][0]['overview']
    dict1Permalink = dict1['results'][0]['permalink']

    if dict1Namespace == 'company' and dict1Overview != 'null' and dict1Overview.__len__() > 0:
        url2 = 'http://api.crunchbase.com/v/1/company/' + dict1Permalink + '.js?api_key=6susy5mbbncvm45hsav4rabd'
    elif dict1Namespace == 'person' and dict1Overview != 'null' and dict1Overview.__len__() > 0:
        url2 = 'http://api.crunchbase.com/v/1/person/' + dict1Permalink + '.js?api_key=6susy5mbbncvm45hsav4rabd'
    
    f = urlopen(url2).read()
    dict2 = json.loads(f)
    crunchurl = dict1['results'][0]['crunchbase_url']
    shortapi = "https://api-ssl.bitly.com/v3/shorten?access_token=794e02fd047d7fcc0c44543742d0f471e2f9ebc8&longUrl=crunchurl"
    shortened = shortapi['url']
    
    return getSummary( BeautifulSoup( dict1Overview ).get_text() ) + str(shortened)[7:15]+str(shortened)[15:]
"""
def parseWiki(search):
    #import pdb; pdb.set_trace()
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
                twilioOutput = parsePerson(text_body[0][2:].lower(), text_body[1].lower())
            except:
                twilioOutput = "Sorry, no one named " + text_body[0][2:] + " exists in crunchbase."

        elif firstLetters.lower() == 'c:':
            try:
                twilioOutput = parseCompany(twilioInput[2:])
            except:
                twilioOutput = "Sorry, no company named '" + twilioInput[2:] + "' exists in crunchbase."

        elif inputString[:3] == 'c#:':
            try:
                twilioOutput = parseCompanyNumber(inputString[1:])
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