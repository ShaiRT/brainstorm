# BrainStorm

Brain computer interface project for advanced system design course in TAU.

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:ShaiRT/BrainStorm.git
    ...
    $ cd BrainStorm/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [brainstorm] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:


    ```sh
    $ pytest tests/
    ...
    ```

## Usage

The `brainstorm` package provides the following class:

- `Thought`

    This class encapsulates the concept of `thought`.

    It provides the `serialize` method to serialize thoughts, and the
    `deserialize` method to deserialize them.

    ```pycon
    >>> from brainstorm import Thought
    >>> import datetime as dt
    >>> user_id = 1
    >>> timestamp = dt.datetime(2000, 1, 1, 12, 0)
    >>> thought = "I'm hungry"
    >>> thought = Thought(user_id, timestamp, thought)
    >>> thought
    Thought(user_id=1, timestamp=datetime.datetime(2000, 1, 1, 12, 0), thought="I'm hungry")
    >>> print(thought)
    [2000-01-01 12:00:00] user 1: I'm hungry
    >>> thought.serialize()
	b"\x01\x00\x00\x00\x00\x00\x00\x00 \xd0m8\x00\x00\x00\x00\n\x00\x00\x00I'm hungry"
    >>> Thought.deserialize(thought.serialize())
    Thought(user_id=1, timestamp=datetime.datetime(2000, 1, 1, 12, 0), thought="I'm hungry")
    ```


The `brainstorm` package also provides the following commands
with a command-line interface:

- `upload_thought(address, user_id, thought)`

	This method uploads a thought with a user id to the server in specified address.

```sh
$ python -m brainstorm upload-thought 0.0.0.0:5000 1 "I'm hungry"
```

- `run_server(address, data_dir)`

	This method runs a server in given address, which recieves serialized thoughts, and save them in given directory.

```sh
$ python -m brainstorm run-server 0.0.0.0:5000 /data
```

- `run_webserver(address, data)`

	This method runs a website at given address, which displays data from given directory.

```sh
$ python -m brainstorm run-webserver 0.0.0.0:5000 /data
```