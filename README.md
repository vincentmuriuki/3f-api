# Fast Food Fast   [![Maintainability](https://api.codeclimate.com/v1/badges/a45a0bad4d14790897c1/maintainability)](https://codeclimate.com/github/tesh254/3f-api/maintainability) [![Coverage Status](https://coveralls.io/repos/github/tesh254/3f-api/badge.svg?branch=develop)](https://coveralls.io/github/tesh254/3f-api?branch=develop)          [![Build Status](https://travis-ci.org/tesh254/3f-api.svg?branch=develop)](https://travis-ci.org/tesh254/3f-api) ![python version](https://img.shields.io/pypi/pyversions/Django.svg?maxAge=2592000)


## Getting started

To get started with fast food api you will have clone this repo.

Mac OS/Unix:

```bash 
$ git clone https://github.com/tesh254/3f.git
```

Windows:
* You will have to download git tool in this url [https://git-scm.com/download/win](https://git-scm.com/download/win)

* Ensure you follow the recommended settings

* Open git bash and type this command

```bash
$ git clone https://github.com/tesh254/3f.git
```

## Endpoints for v1 (memory storage version)

| HTTP VERB | API ROUTE | FUNCTION |
|-----------|-----------|----------|
|GET|`/api/v1/orders`|Get all orders|
|POST|`/api/v1/orders`|Place an order|
|PUT|`/api/v1/orders/<identifier>`|Update an order status|
|DELETE|`/api/v1/orders/<identifier>`|Delete a specific order|
|DELETE|`/api/v1/orders`|Delete all orders created|

## NOTE:

In post and put http requests respond with json data

## Endpoints for v2 (database interaction version)

|HTTP VERB| API ROUTE | FUNCTION|USER ROLE|
|---------|-----------|---------|---------|
|POST|`/api/v2/auth/signup`|Signup into the site|user|
|POST|`/api/v2/auth/login`|Login into the site|user/admin|
|POST|`/api/v2/auth/logout`|Logout of the site|user/admin|
|GET|`/api/v2/user/orders`|Get orders you have ordered|user|
|GET|`/api/v2/orders`|Get all orders made by users|admin|
|GET|`/api/v2/orders/<identifier>`|Get a specific order by id|admin|
|PUT|`/api/v2/orders/<identifier>`|Update an order status with the id provided|admin|
|POST|`/api/v2/menu`|Add a meal to the catalog|admin|
|GET|`/api/v2/menu`|Get the menu|user/admin|
|GET|`/api/v2/categories`|Get meal categories|user/admin|
|POST|`/api/v2/categories`|Create a meal category|user/admin|

## Installing Dependencies

For everything to work perfectly as shown in the screen shots you need to install a couple of dependencies.

All OS:
* Install Postman from this url [Postman](https://www.getpostman.com/apps)

* Open your terminal 
    * ```bash
        $ cd [to your project directory]
        ```
* If installed python type this command on your terminal
 ```bash
    $ pip install -r requirements.txt
 ```

 * Type this coommand after installation
 ```bash
 $ python run.py
 ```

 * Open postman, in the {{url}} variable enter your flask url i.e. localhost:5000/api/v1/orders

 Go on testing the apis you can deploy your app to heroku, share the link, test, collaborate.


 ## Release History

 * v1
    * This versions data is stored in memory only if the server closes then all data is deleted.
* v2
    * All data in this version is stored in a postgres database
    * User authentication.

## Meta

Name `Erick Wachira`

Twitter `@wachira_dev`

Instagram `@i.am.wachira`

Email `ewachira254@gmail.com`

## Contributing 

This project is under an an `MIT LICENSE` so feel free to contribute.

1. Fork it (https://github.com/yourname/yourproject/fork)
1. Create your feature branch (git checkout -b feature/something)
1. Commit your changes (git commit -am 'Add some something')
1. Push to the branch (git push origin feature/something)
1. Create a new Pull Request