### "Who review me"

"Who review me" is a title of the `who_review_bot`

`who_review_bot` - is a [telegram](https://telegram.org) bot aimed to help to define who is next to review

The bot suggests a review to the user, who has not reviewed for a long time

### Prerequisites

The bot is prepared to be run in docker with docker-composer config. 
It means that you need both docker and docker-composer installed (for this way of using)

### Installation & configuration
1. git clone \<this repo link\>
2. rename example .\config\example.json to .\config\review.json</ul>
3. edit review.json
   - set the value of your token to the attribute "token"
   - set the value of your language to the attribute "language"

### Runing the bot

You can start and stop it using docker-composer commands in you terminal command line
* to start
```sh
$ docker-compose up -d
```
* to stop
```sh
$ docker-compose down
```

### Usage

Just add @who_review_me bot to the telegram group and type the backslash ("/") in message field to see the commands and its descriptions

### The bot commands

* /register - to register your user to the bot
* /review - to request a review of an article by the link
   * example: /review www.mysite.com/myarticle
   * you can point the reviewer, i.e., to @natasha: /review www.mysite.com/myarticle @natasha
* /unregister - to unregister user
* /next - to show the next reviewer
* /reviewers - to show all of the reviewers

<h3>Notes about language support</h3>
* If your language is english
  * you can just remove "language" and "dict" attributes from configuration

* If your language is not english
  * you can set your own translations in the attribute "dict" (if you want)
  * if you do not want set translations, the bot will translate it with the google translator to your language

You can find two-letter language codes [here](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
