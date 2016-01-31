RSSNext-Django
===========

RSSNext is a very simple RSS reader: add feeds, then click a button to be taken to your next unread item. I've written this to demonstrate the flavor of my work in HTML, CSS, Django, RESTful APIs and social login.

See it in action at [http://php.rssnext.net](http://django.rssnext.net). Try creating an account, adding a feed (eg: http://feeds.bbci.co.uk/news/rss.xml), and using the 'Next' link.

Features
--------

### Responsive HTML

See [public_html/index.php](public_html/index.php) for examples of hand coded, attractive user-interfaces in simple HTML and CSS. Responsive styling is provided by the Bootstrap framework.

### RESTful Back-End API

### Reactive Front-End

The user control panel is populated by asynchronous JavaScript calls to the project's AJAX handler.


### Social Login

Visitors can either create an RSSNext account, or authenticate with two clicks using Facebook or Google.

### User Acceptance Testing

A comprehensive set of user acceptance tests allows the programmer to aggressively add features and refactor, without fear of introducing undetected bugs.

### Code Style Tests

Code style tests on every push encourage high, uniform code quality on each merge into production. This project is held to a superset of the [PSR2](http://www.php-fig.org/psr/psr-2/) standard by PHPCodeSniffer.

### Continuous Integration

Travis-CI provides this project with comprehensive tests on each push, allowing continuous merges into the production branch. This means that features can be rapidly added to the code base.


Things I Would Do Differently
-----------------------------

For a real-world, production project I would use a web framework such as [Symfony](https://symfony.com/), including an ORM like [Propel](http://propelorm.org/); frameworks like these provide reusable solutions to common tasks, and I've used similar tools to reduce project lines-of-code by 90%. But for this portfolio project, I chose instead to demonstrate basic design in HTML, PHP, and MySQL.

See the [issue tracker](https://github.com/UWEnrollmentManagement/Framework/issues/) for things that I would still like to improve about this project, including issues that I have already acted to close.

Installation
------------

Clone RSSNext-Django onto your server:

    $ git clone https://github.com/JASchilz/rssnext-php.git

Confirm the settings in `rssnext/settings.php`, and then create a `local_settings.php` in the same directory:

```
    // Example local_settings.php
    
    SECRET_KEY = 'mybiglongrandomdjangosecretkey'

    DB_PASSWORD = 'mybiglongrandomdjangodbpassword'
```
    
Include install instructions here


Requirements
------------

* Python 2.7 or 3.4


Getting Involved
----------------

Feel free to open pull requests or issues if you'd like to contribute. [GitHub](https://github.com/JASchilz/RSSNext-Django) is the canonical location of this project.

Here's the general sequence of events for code contribution:

1. Open an issue in the [issue tracker](https://github.com/JASchilz/RSSNext-Django/issues/).
2. In any order:
  * Submit a pull request with a **failing** test that demonstrates the issue/feature.
  * Get acknowledgement/concurrence.
3. Revise your pull request to pass the test in (2). Include documentation, if appropriate.
