# SindiAI
#### Project participating in ASEF 2021

Sindi is a natural language AI assistant that doesn’t only play music for you but it can also chat with you, tell you jokes and more. 
It doesn't matter how you ask the question Sindi will always understand what you mean unless the feature is not available.
Here is a list of the features Sindi has right now:
  - Speak feature: *numbers and text*
  - Chat features: *Hello, Who are you?, Surname, Name, Thanks, full birthday, age (Sindi will know if you lie about yoyr age)*
  - Weather features: *What's the weather like?*
  - Music features: *What genres of music do I listen?, Play music, Play rock music, Play custom music*
  - Music controls: *Play, pause/continue, volume, mute/unmute, replay*
  - Exit app
  - Sindi will know if you are angry, neutral or happy based on your input

### Installation
SindiAI is built in [Python 3.6.6](https://www.python.org/downloads/release/python-366/) so make sure you have it installed together with *pip*
 
Next you need to clone the repository or just [download](https://github.com/0Shark/SindiAIDev/archive/main.zip) it 

```sh
git clone https://github.com/0Shark/SindiAIDev
```

After that you can change directory to there

```sh
cd /YOURFOLDER/sindiai/
```
We recommend creating a virtual environment to manage your modules more easily, in this case we used anaconda to create the environment like this:
```sh
conda create -n sindiai python==3.6.6
```
Now activate the environment:
```sh
conda activate sindiai
```
Now you can install all the required modules with this command:
```sh
pip install -r requirements.txt
```
After installing all the modules, make sure to have a MySQL local server running. In this case we are running Wamp(Windows, Apache, MySQL, and PHP).
Then you can run to create the database:
```sh
python create_db.py
```
After the database has been created you can start using SindiAI by running:
```sh
python server.py
```
And head over to 127.0.0.1:8000 on any web browser, or local ip of pc to use on other devices on your local network. *Example: 192.168.1.2:8000*

### Audio files

Sindi has a decent amount of speech audio generated with play.ht and music genres that can be modified to your preferences.

| Type | Items |
| ------ | ------ |
| text | 42 |
| number | 29 (base numbers that serve to create 1000 more) |
| jokes | 8 |
| months | 12 |
| music | 10 genres |

### Todos

 - More chat functions
 - Add Night Mode
 - Speech recognition
 - Activate on call (Hey Sindi)
 - Play youtube videos

License
----

MIT
