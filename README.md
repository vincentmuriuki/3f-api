# Fast Food Fast   [![Maintainability](https://api.codeclimate.com/v1/badges/a45a0bad4d14790897c1/maintainability)](https://codeclimate.com/github/tesh254/3f-api/maintainability) [![Coverage Status](https://coveralls.io/repos/github/tesh254/3f-api/badge.svg?branch=develop)](https://coveralls.io/github/tesh254/3f-api?branch=develop)          [![Build Status](https://travis-ci.org/tesh254/3f-api.svg?branch=develop)](https://travis-ci.org/tesh254/3f-api) ![python version](https://img.shields.io/pypi/pyversions/Django.svg?maxAge=2592000)


## Installation

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

## Usage

To use this api, below is a couple of screenshots showing how to use them on postman.

`GET all orders`
`{{url}}/api/v1/orders`

![Getting all orders](img/getorders.png)

As you can see the enpoint returns all orders stored.
**Note**:This api does not request json data and always returns a `200 OK` status code even if no orders stored.

`POST place an order`
`{{url}}/api/v1/orders`

![Placing an order](img/placeorder.png)

To have a successfull response from the server you need to create a json body as shown then send. If an `400 Bad Request` is sent then it means there is something wrong, a field is missing. If successful, the server responds with `201 Created` status code meaning the order was placed.

`GET specific order`
`{{url}}/api/v1/orders/<identifier>`

![Getting specific order](img/getspecific.png)

The server will respond with a `404 Not Found` status if the resource was not found. A `200 OK` is sent if the specific order of that identifier is found.


`PUT update order status`
`{{url}}/api/v1/orders`

![Updating an order](img/update.png)

The reponse of the server if the order is not found is `404 Not Found`, if found `201 Created` meaning the order status was successfully created.


`DELETE delete an order`
`{{url}}/api/v1/orders/<identifier>`

![Deleting a specific order](img/deleteone.png)

`404 Not Found` if no order of that identifier if found a `204 No Content` status is sent meaning a successful delete to check if true try the url again it will repond with `404 Not Found` status.


`DELETE delete all orders`
`{{url}}/api/v1/orders`

![Deleting all orders](img/deleteall.png)

This endpoint clears all orders in storage the same status is sent for a succesful delete `204 No Content`.


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
    * All data in this version is stored in a postgres database(comming soon)

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