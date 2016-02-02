[![Build Status](https://travis-ci.org/JASchilz/RSSNext-Django.svg?branch=master)](https://travis-ci.org/JASchilz/RSSNext-Django)
[![Code Climate](https://codeclimate.com/github/JASchilz/RSSNext-Django/badges/gpa.svg)](https://codeclimate.com/github/JASchilz/RSSNext-Django)


RSSNext-Django
===========

RSSNext is a simple RSS reader: add feeds, then click a button to be taken to your next unread item. I've written this to demonstrate the flavor of my work in HTML, CSS, Django, and RESTful APIs.

See it in action at [https://django.rssnext.net](https://django.rssnext.net). Try creating an account, adding a feed (eg: http://feeds.bbci.co.uk/news/rss.xml), and using the 'Next' link.

Features
--------

### Responsive HTML

See [rssnext/templates/rssnext/home.html](rssnext/templates/rssnext/home.html) for examples of hand coded, attractive user-interfaces in simple HTML and CSS. Responsive styling is provided by the Bootstrap framework.

### User Acceptance Testing

A comprehensive set of user acceptance tests allows the programmer to aggressively add features and refactor, without fear of introducing undetected bugs.

### Code Style Tests

Code style tests on every push encourage high, uniform code quality on each merge into production. This project is held to the[PEP8](https://www.python.org/dev/peps/pep-0008/) standard by PyLint.

### Continuous Integration

Travis-CI provides this project with comprehensive tests on each push, allowing continuous merges into the production branch. This means that features can be rapidly added to the code base.

### API-First Design

Many web applications include an Application Programming Interface (API) which allows other applications to retrieve information from their systems. For example, Twitter features an API which developers can use to retrieve tweets without scraping through a Twitter web page.

Under *API-First* design, even an application's primary web page retrieves data indirectly through the application's API. This means that Django doesn't construct the RSSNext control panel directly. Instead, Django serves account information through a [RESTful](https://en.wikipedia.org/wiki/Representational_state_transfer) API; the JavaScript framework Angular is used to query this API and builds the results into the user's page.

An API-First design means that the application server is totally agnostic to the client used by the visitor; a native mobile client could be written for RSSNext-Django as easily as the included web client. It also means that as long as the API remains unchanges, changes made to either the client or the server will not adversely affect the other.


Things I Would Do Differently
-----------------------------

If I were writing RSSNext-Django for a real, production size project, I would pursue API-First design even more thoroughly by writing a version controlled API specification and separating the API server and web client into separate repositories.

See the [issue tracker](https://github.com/JASchilz/RSSNext-Django/issues/) for things that I would still like to improve about this project, including issues that I have already acted to close.


Requirements
------------

* Python 3.4


Getting Involved
----------------

Feel free to open pull requests or issues if you'd like to contribute. [GitHub](https://github.com/JASchilz/RSSNext-Django) is the canonical location of this project.

Here's the general sequence of events for code contribution:

1. Open an issue in the [issue tracker](https://github.com/JASchilz/RSSNext-Django/issues/).
2. In any order:
  * Submit a pull request with a **failing** test that demonstrates the issue/feature.
  * Get acknowledgement/concurrence.
3. Revise your pull request to pass the test in (2). Include documentation, if appropriate.
