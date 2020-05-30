[![Build Status](https://travis-ci.org/ShaiRT/brainstorm.svg?branch=master)](https://travis-ci.org/ShaiRT/brainstorm)
[![codecov](https://codecov.io/gh/ShaiRT/brainstorm/branch/master/graph/badge.svg)](https://codecov.io/gh/ShaiRT/brainstorm)
[![Documentation Status](https://readthedocs.org/projects/brainstormproject/badge/?version=latest)](https://brainstormproject.readthedocs.io/en/latest/?badge=latest)
![GitHub repo size](https://img.shields.io/github/repo-size/ShaiRT/brainstorm?color=BA51F7)
![GitHub top language](https://img.shields.io/github/languages/top/ShaiRT/brainstorm)
![GitHub language count](https://img.shields.io/github/languages/count/ShaiRT/brainstorm?color=E90E0E)
![Awesome Badges](https://img.shields.io/badge/badges-awesome-F23077.svg)

# BrainStorm

Brain computer interface project for advanced system design course in TAU.

See API documentation [here](https://brainstormproject.readthedocs.io/en/latest/).

## Overview

This project includes a [client](#Client), which streams cognition snapshots to a [server](#Server), which then publishes them to a [message queue](#Message-Queue), where multiple [parsers](#Parsers) read the snapshot, parse various parts of it, and publish the parsed results, which are then [saved](#Saver) to a [database](#Database).

The results are then exposed via a RESTful [API](#API), which is consumed by a [CLI](#CLI); there's also a [GUI](#GUI), which visualizes the results in various ways.


## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:ShaiRT/brainstorm.git
    ...
    $ cd brainstorm/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [brainstorm] $ # you're good to go!
    ```

    > Note:
    > Before running this script make sure you have `docker` and `docker-compose` installed.
    > If not, use ```$ ./scripts/install-docker.sh``` to install it.

3. To check that everything is working as expected, run the tests:

    ```sh
    $ ./scripts/run-tests.sh
    ...
    $
    ```

## Usage

### Running the pipeline

To run the entire pipeline, run:
```sh
$ ./scripts/run-pipeline.sh
```
This will run the follwing services on a [Docker](https://www.docker.com/) host:

|program   |host         |port|protocol  |package            |
|----------|-------------|----|:--------:|-------------------|
|server    |0 . 0 . 0 . 0|8000|http      |`brainstorm.server`|
|api server|0 . 0 . 0 . 0|5000|http      |`brainstorm.api`   |
|gui server|0 . 0 . 0 . 0|8080|http      |`brainstorm.gui`   |

> Note: this will also run docker containers with [rabbitmq](https://www.rabbitmq.com/) on 0.0.0.0:5672, and [mogodb](https://www.mongodb.com/) on 0.0.0.0:27017.

This will also activate a `brainstorm.saver` and the following parsers:

- color image parser
- depth image parser
- feelings parser
- pose parser

See [Client](#Client) to learn about uploading data to the server, and [CLI](#CLI) to learn how to access the information via command line.
Also see [example](#Example).

### Command Line Interface

> Note:
> In all of the following commands, message queue and database urls must be in the form `'scheme://host:port'`. The scheme must be supported by `brainstorm.mq_draivers` and `brainstorm.database_drivers`, and the message queue / database are assumed to already be running in the given host and port.

> Note:
> To get more help on the following commands use the `--help` flag.

#### Client

To upload data to the server, use the client's upload-sample command:
```sh
$ python -m brainstorm.client upload-sample \
-h/--host '127.0.0.1' \
-p/--port 8000 \
'snapshot.mind.gz'
```

To view information from a sample in terminal without sending to server use the client's read command:
```sh
$ python -m brainstorm.client read 'sample.mind.gz'
```
> Note:
> The sample format has to be supported by `brainstorm.client.reader_drivers`.
> The default format is `protobuf` as specified in the [documentation]([https://brainstormproject.readthedocs.io/en/latest/brainstorm.client.reader_drivers.html#brainstorm-client-reader-drivers-protobuf-driver-module](https://brainstormproject.readthedocs.io/en/latest/brainstorm.client.reader_drivers.html#brainstorm-client-reader-drivers-protobuf-driver-module)).
> To use a different format see `--help`.
> To add a new driver see instructions [here]([https://brainstormproject.readthedocs.io/en/latest/brainstorm.client.reader_drivers.html#brainstorm-client-reader-drivers-package](https://brainstormproject.readthedocs.io/en/latest/brainstorm.client.reader_drivers.html#brainstorm-client-reader-drivers-package)).

#### Server

To run the server use the following command:
```sh
$ python -m brainstorm.server run-server \
-h/--host '127.0.0.1' \
-p/--port 8000 \
'rabbitmq://127.0.0.1:5672'
```
> Note: This will create a `data` directory in your current working directory with the images the server receives. To specify a different directory use the `--path` flag.
 
#### Message Queue

Various parts of this project use a message queue to publish and consume information.
The current implementation supports [RabbitMQ](https://www.rabbitmq.com/) as a message queue.
See [documentation]([https://brainstormproject.readthedocs.io/en/latest/brainstorm.mq_drivers.html](https://brainstormproject.readthedocs.io/en/latest/brainstorm.mq_drivers.html)) to learn about adding a new message queue driver.

#### Parsers

`brainstorm.parsers` provides the following command line interface:

-  The following command will use a specified parser to parse a snapshot in a given file. The file should contain a snapshot `dict` in json format, with a `'datetime'` and a `'user'` field.
```sh
$ python -m brainstorm.parsers parse pose 'snapshot.raw'
```
In this example `pose` is the name of the parser and `snapshot.raw` is the path to the file to parse.

- The next command will run a specified parser to listen to a message queue with given url, parse data, and post back to the message queue:
```sh
$ python -m brainstorm.parsers run-parser feelings 'rabbitmq://127.0.0.1:5672/'
```
In this example `feelings` is the name of the parser and `rabbitmq://127.0.0.1:5672/` is the message queue url.

The implemented parsers are:
- pose
- feelings
- color_image
- depth_image

To add new parsers to the `brainstorm.parsers` package, simply add a `.py` file to the packge containing a `parse_parser_name(snapshot)` function or a `ParserNameParser` class with a `self.parse(snapshot)` method.
** files starting with `_` will be ignored.

#### Saver

The saver reads data from a message queue and saves it in a database.
The following commands are supported:
- To save information from a file to a database run:
```sh
$ python -m brainstorm.saver save \
-d/--database mongodb://localhost:27017 \
'result.data'
```
In this example `mongodb://localhost:27017` is the database url, and `result.data` is the path to a file that should contain a snapshot `dict` in json format, with a `'datetime'` and a `'user'` field.

- To run the saver to save data from a message queue to a database run:
```sh
$ python -m brainstorm.saver run-saver \
mongodb://localhost:27017   \
rabbitmq://127.0.0.1:5672
```
Here `mongodb://localhost:27017` is the database url, and `rabbitmq://127.0.0.1:5672` is the message queue url.

#### Database

Various parts of this project use a database to save and read information.
The current implementation supports [MongoDB](https://www.mongodb.com/) as a database.
See [documentation]([https://brainstormproject.readthedocs.io/en/latest/brainstorm.database_drivers.html](https://brainstormproject.readthedocs.io/en/latest/brainstorm.database_drivers.html)) to learn about adding a new database driver.

#### API

To run `brainstorm.api` simply use
```sh
$ python -m brainstorm.api run-server \
-h/--host '127.0.0.1'  \
-p/--port 5000  \
-d/--database 'mongodb://127.0.0.1:27017'
```
The API server will respond to the following requests:

- GET /users  
  Returns a list of IDs and names of all supported users.
 
- GET /users/\<user-id>
  Returns the specified user's details: ID, name, birthday and gender.
 
- GET /users/\<user-id>/snapshots  
  Returns a list of the specified user's snapshot IDs and datetimes.
 
- GET /users/\<user-id>/snapshots/\<snapshot-id>
  Returns the specified snapshot's details: ID, datetime, and the available results' names.
 
- GET /users/\<user-id>/snapshots/\<snapshot-id>/\<result-name>  
  Returns the specified snapshot's result (if available).
 
- GET /users/\<user-id>/snapshots/\<snapshot-id>/\<result-name>/data
  Returns the specified snapshot's result data (i.e. image).
  Supported results: color_image, depth_image (if available).

#### CLI

The CLI is available via `brainstorm.cli` and supports the following commands:

```sh
$ python -m brainstorm.cli get-users
```
```sh
$ python -m brainstorm.cli get-user 1
```
```sh
$ python -m brainstorm.cli get-snapshots 1
```
```sh
$ python -m brainstorm.cli get-snapshot 1 2
```
```sh
$ python -m brainstorm.cli get-result 1 2 pose
```
>Use the `--help` flag to learn more about these commands.

> Make sure the api server is running on the default host and port (or specify a different host and port) before running the CLI commands.

#### GUI

Run the GUI server to serve results at `'http://host:port'`:

```sh
$ python -m brainstorm.gui run-server \  
-h/--host '127.0.0.1'  \
-p/--port 8080  \
-H/--api-host '127.0.0.1'  \
-P/--api-port 5000
```

> Note:
> Before running this command for the first time run ```$ ./scripts/build-gui.sh```.
> This is only necessary when running this command without ```./scripts/run-pipeline.sh```.


### Example

Here is an example of running the pipeline and uploading a sample:

```sh
$ ./scripts/run-pipeline.sh
...

$ python -m brainstorm.client upload-sample sample.mind.gz
uploading...
done!

$ # to see the users that were uploaded:

$ python -m brainstorm.cli get-users
+-------------+----------------+
|   user_id   |    username    |
+-------------+----------------+
|      12     |   Shai Rahat   |
+-------------+----------------+
```
After running the pipline like this, results will be available at [http://localhost:8080](http://localhost:8080).

To shut down the pipline:
```sh
$ ./scripts/stop-pipeline.sh
...
$
```
_________________________

**Happy BrainStorming !**
