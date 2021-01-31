# feedify

`feedify` is a command line application for turning a website into an RSS feed.
Site support is added by the user via configuration.

## Installation

`feedify` is not currently avaialable on PyPI.
To use this software, please follow the instructions below:

```shell
$> git clone <path to this respository>
$> cd feedify
$> make setup
$> make run
```


## Running feedify

Once installed, you can run `feedify` with the `make run` command:

```shell
$> make run
```


## Developing `feedify`

In addition to the [Installation steps](#installation) steps above, if you intend to develop `feedify`, you will also need to install the dev requirements:

```shell
$> make setup_dev
```

Run `make help` for other (hopefully) helpful commands.

## License

`feedify` is Unlicensed. See the included `LICENSE` file.


## Author

[Bill Israel](http://billisrael.info/) - [bill.israel@hey.com](mailto:bill.israel@hey.com)
