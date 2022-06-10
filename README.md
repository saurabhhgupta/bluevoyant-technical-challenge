# BlueVoyant - Marvel Impossible Travel Challenge

This repository is private and available to view by invitation only. It is my submission to BlueVoyant's technical interview / take-home challenge.

Thanks to the BlueVoyant team for a fun challenge. I had a great time tackling it.

## Overview
In a nutshell, this project does 3 things:

1. Finds metadata for a desired character.
2. Using that metadata, finds the same metadata for all characters that the original character has worked with in every comic the character has been in.
3. Stores this information in a MySQL database.

The high-level algorithm uses an in-memory "cache". Basically, every time a character is obtained from the API call(s), the character ID (provided by Marvel) is checked against a cache. If the ID is in cache, we simply discard it and move on. If it's not in the cache, we key-value store the ID / metadata in the cache. The reason for using a cache is to avoid duplicates (e.g. if Person A worked with Person B in Comic X, and then Person B worked with Person A in Comic Y, then Person A would be exfiltrated twice).

This application is designed to be used with any desired character. Simply pass in the character name as a command line argument, and it will exfiltrate the desired data.

The persistence layer I decided to use for this challenge was MySQL. Because we know the API entity models, and we also know the structure of our data model, it made sense to use a relational database. I use a third-party Python library to connect to a MySQL instance, and I  use Pandas to take a CSV file that I generated and port it to MySQL.

All dependencies are thrown into a Docker file. There's a few things I did here:

- I created a script to automate the small commands (`build_docker.sh`). This is mainly to take care of the mundane tasks of stopping the old containers, removing old images, building the new image, running the container, and interacting with a bash shell inside of the container. This is the only command you have to run on your local machine, outside of the Docker container itself. It'll get everything set up for you.
- There's another shell script that I invoke from my Dockerfile (`docker_run_mysql.sh`). This is to start the MySQL service and seed the database with a schema, as well as creating specific users and granting privileges for those users. I feed it through `start.sql`.
- Connection to the database happens through a driver called `mysql-connector`. I use this connector in various places in my code (mostly in the `PersistenceFactory`). The fields needed to successfully connect to the database (e.g. host, username, password), as well as the table / database names, are all sourced from a configuration file (`configuration.ini`). Because I seed the database beforehand at startup, I have set those configuration values to match the seed file. I included a `generateConfiguration.py` script to create the configuration file. Perhaps I could have written a small script to generate the SQL seed file based on the configuration file.

To design my code, I followed the hexagonal architecture (also commonly known as the ports & adapters pattern). I find this design pattern extremely powerful, and allows my design to scale. In theory, the code should be very "plug and play" -- meaning, if I ever decide to use another database, or a Redis cache, or a totally different API layer (perhaps Marvel no longer wants to use REST), then I as the developer should not need to dig deep into the codebase. Simply put, I created "ports" and I interface with those ports, while passing in different "adapters". In the event where I need to use a different technology or approach as previously mentioned, I would just need to create additional adapters, and replace the existing adapters.

## Prerequisites

The only dependency you need is [Docker](https://www.docker.com/). If you're using macOS or Linux, I recommend using [brew](https://brew.sh/) to install Docker.

```bash
brew install docker
```

## How to run
First, create an `.env` file containing the following values:
```
MARVEL_PUBLIC_KEY=1234
MARVEL_PRIVATE_KEY=4321
```
Make sure there are no quotations or whitespaces in your `.env` file. This file will be passed into the Docker container, where the values will be injected as environment variables. I provided a reference file called `.env.example` that you may use.

After you have Docker fully set up, all you need to do is run this command from the top-level directory of the project:
```
sudo ./build_docker.sh .env
```

This will take care of everything Docker-related for you, including running the container, passing in your public/private API keys, and bringing you into the container.

In the spirit of making life as easy as possible, I created an alias for you to get to my project directory. Just type in `jump` and you will be taken to the top-level project directory (`/usr/src/bluevoyant_challenge_saurabh/app`).

From here, the fun starts. Run the following command to get started:
```
python3 main.py --character="Spectrum"
```
As mentioned earlier, you can replace Spectrum with any character of your choice. For example, try Deadpool, Doctor Strange, Thor, etc.

When I was writing this program, I kept getting issues where no data was being processed. This was a signal that the program was failing to retrieve data from the API. Usually, this was due to a key error. I created an extra argument to display the keys in the log. To do this, you may run:
```
python3 main.py --character="Spectrum" --showKeys
```
which will display your public and private keys in the console.

The program runs once and then exists, which means the in-memory "cache" is used for one exfiltration at a time. However, the persistence layer (i.e. MySQL) keeps all of the data from the executions. This was filling up the database, and sometimes I needed a way to work with a clean table. I created an extra argument to clean the table before exfiltrating data for that run. To do this, you may run:
```
python3 main.py --character="Spectrum" --cleanTable
```

Lastly, sometimes I wanted to see what records were in my database. I did not want to use MySQL Workbench, and I definitely did not want to keep running manual SQL commands in the instance itself. I created an extra argument to simply show the table in its current state. To do this, you may run:
```
python3 main.py --showTable
```

You can stack these flags on each other. For example, if you wanted to exfiltrate data about Thor, using a clean table, but you wanted to see the table records beforehand and also see your keys, you can run:
```
python3 main.py --character="Thor" --showKeys --cleanTable --showTable
```
and it will do exactly that.


## Analysis
Like with any project, there are considerations and assumptions I thought of:

1. The very first question I had was: how will the output be managed to understand possible errors / passing invalid data? For example, the Marvel API isn't perfect by any means. The description field for a few comic characters was actually some HTML code. I am not pruning or cleaning any data like that, but this is definitely an issue.

2. Another example of the above is the thumbnail: what if it's corrupt, or a bad URL? Imagine the data is being used to render information on a website. If we're not handling bad URL's, it will throw some ugly exceptions. It's probably best to leave the field blank and log "Image not found".

3. I'm using an in-memory datastore as a "cache", but ideally something like Redis would work here.

4. I'm not a fan of passing in my Marvel API private key as an environment variable. If this were a microservice and we exposed an endpoint where we could send the desired character name as a JSON post body (for example), then an option could be to deploy the service using Kubernetes and seal the API key as a secret. HashiCorp Vault is also another great option.

5. We aren't storing the desired character name with our database insertions. So, if we exfiltrated data for Spectrum, and then Deadpool, then there will be duplicates in the database, since the results could overlap. At runtime, this wouldn't happen, but for back-to-back exfiltrations, we will deal with duplicate entries. It all depends on what the use case is.

6. Obviously, the biggest thing I'm missing are tests. I never complete a project without writing tests, but for the sake of time, I decided to skip writing tests (which, I acknowledge, is bad practice -- but I hope I'm off the hook. Kidney stone pain takes first priority right now. 😁 )

P.S. Let me know if you find the easter egg!