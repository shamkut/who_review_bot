### About

`who_review_bot` - is a [telegram](https://telegram.org) bot aimed to help to define who is next to review

The bot suggests a review to the user, who has not reviewed for a long time

### Prerequisites

The bot is prepared to be run in docker with docker-composer config. 
It means that you need both docker and docker-composer installed (for this way of using)

### Installation & configuration
1. git clone [https://github.com/shamkut/who_review_bot.git](https://github.com/shamkut/who_review_bot.git)
2. rename example .\config\example.json to .\config\review.json</ul>
3. edit review.json
   - set the value of your token to the attribute "token"
   - set the value of your language to the attribute "language", if you need
4. run in you terminal command line ```$ docker-compose up -d ```
5. have fun

### Usage

Just add @who_review_me bot to the telegram group and type the backslash ("/") in message field to see the commands and its descriptions

### The bot commands

* /register - to register your user to the bot
* /review, /r - to request a review of an article by the link
   * common example: 
      * /review www.mysite.com/myarticle
      * /r www.mysite.com/myarticle
   * you may suggest more than one link to review: 
      * /r www.mysite.com/myarticle_1 www.mysite.com/myarticle_2
   * you may specify the reviewer you want, e.g., user natasha: 
      * /review www.mysite.com/myarticle @natasha
* /unregister - to unregister user
* /next - to show the next reviewer
* /reviewers - to show all of the reviewers
* /skip - to skip the bot user to review for the specified number of days
   * 7 days Alex's vacation example: 
      * /skip @alex 7
   * to stop skipping Alex: 
      * /skip @alex 0

<h3>Notes about language support</h3>
* If your language is english
  * you can just remove "language" and "dict" attributes from configuration

* If your language is not english
  * you can set your own translations in the attribute "dict" (if you want)
  * if you do not want set translations, the bot will translate it with the google translator to your language

You can find two-letter language codes [here](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
