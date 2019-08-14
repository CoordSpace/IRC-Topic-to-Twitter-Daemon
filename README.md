  <h1 align="center">IRC Topic-to-Twitter Daemon</h3>

  <p align="center">
    A lightweight python daemon that pushes formatted IRC topic changes from 1+ channels to a central twitter account.
    <br />
    <a href="https://github.com/CoordSpace/IRC-Topic-to-Twitter-Daemon/issues">Report Bugs</a>
    ·
    <a href="https://github.com/CoordSpace/IRC-Topic-to-Twitter-Daemon/issues">Request Feature</a>
  </p>
</p>



## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Docker](#docker)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)



## About The Project

Used by IRC-based video gaming communities to alert their users of chatroom events in real time without needing to continually lurk in the channel(s). Additionally, the twitter feed also functions as an independent log of past topics which can be used for a variety of historical contexts.

In the current usage that was custom made for the independent game streaming community Dopefish_lives on Quakenet, this script extracts the first two elements from a topic string formatted as shown:

    Streamer: <item one> | Game: <item two> | Useless information
and tweets it out to the world in the following format:

    <item one> is playing <item two> @ Dopelives.com!

If there is demand, this project could be extended to support multiple channels, networks, or other configuration needs so feel free to <a href="https://github.com/CoordSpace/IRC-Topic-to-Twitter-Daemon/issues">request a feature!</a>



### Built With

* [IRC3](https://pypi.python.org/pypi/irc3/)
* [Twitter](https://pypi.python.org/pypi/twitter)



## Getting Started

To get a local copy up and running follow these simple steps.



### Prerequisites

 * Python 3.5+



### Installation
 
Note: It's recommended to run the daemon from within a [virtual environment](https://docs.python.org/3/library/venv.html).

First install all the requirements using:

`pip install -r requirements.txt`

Then copy the config.ini.sample to config.ini and edit it to your needs.

Make sure to input all the keys and access tokens supplied by twitter for your app so the bot can post to the service!

Then launch the bot with helpful debug using:

`irc3 -v -r config.ini`



### Docker

A Debian-slim based Docker image is also available for easy integration into existing containerized stacks:

`docker run -v /path/to/your/edited/config.ini:/app/config.ini coordspace/irctopic2twitter:latest`



## Roadmap

See the [open issues](https://github.com/CoordSpace/IRC-Topic-to-Twitter-Daemon/issues) for a list of proposed features (and known issues).



## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



## License

Distributed under the MIT License. See `LICENSE` for more information.



## Contact

Your Name - [@CoordSpace](https://twitter.com/CoordSpace) - chris@coord.space

Project Link: [https://github.com/CoordSpace/IRC-Topic-to-Twitter-Daemon](https://github.com/CoordSpace/IRC-Topic-to-Twitter-Daemon)

