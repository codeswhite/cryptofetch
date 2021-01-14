## CryptoFetch
A CLI tool to fetch and view cryptocurrencies prices, arrange in user-defined tables.
The script is currently using the following API: https://api.cryptowat.ch

### Screenshots
![Sample usage screenshot](https://i.imgur.com/UHlAeth.png) (https://imgur.com/a/ymkGbgU) 

*Paraphernalia: [Terminator](https://github.com/gnome-terminator/terminator), [Oh-my-zsh](https://github.com/ohmyzsh/ohmyzsh) with [bullet-train theme](https://github.com/caiogondim/bullet-train.zsh) and [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting)*

## Contributing
**This code is under MIT license and is welcoming any contribution, including feedbacks and ideas.**

## Installing

- Via pip: -> `$ pip install cryptofetch`

- From AUR repository install package: `python-cryptofetch`

## Usage
### Running

    $ cryptofetch -h

### Definitions:
A definition is a "pair in a exchange" represented as: `exchange pair`.

Few examples of **valid** defs:

    Binance BTC/USDT
    BitStamp ETH/USD
    biNaNcE btc/usdt
    bitstamp ethusd

A list of exchanges can be seen here: https://api.cryptowat.ch/exchanges