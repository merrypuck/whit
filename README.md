whit
====

Whit is an open source project that allows you to query Wikipedia, CrunchBase, and several other APIs via SMS. Screenshots after the jump.


How it works:
---

Whit is written in Python for Google App Engine. Set up the whit instance, add your API keys, and text your query to your Twilio number. (Our implementation is running at `917-791-3098` Give it a try!)


Queries:
---

Put one of the following letters, a colon, and your query in your text. The letter helps whit route your query to the correct API.

- **p**: {a person's name}
- **c**: {a company's name}
- **s**: {a stock ticker code}
- **w**: {a wikipedia query name}

Screenshots:
---

As promised, here's a couple of screenshots, showing Whit in action:

![Person](images/person.png)
![Company](images/company.png)
![Stock](images/stock.png)
![Wiki](images/wiki.png)

