## Fmylife.com post generator
This simple scraper is built using Scrapy for Python. Its goal is to scrap simple information such as the post title, post, up
and downvotes, and amount of comments. More or less can be added, such as time of post, author name, etc.

## Getting Started

You'll need to download Scrapy either from their [website](https://scrapy.org/) or `pip install` it in the command line.
For Linux users :
* run `pip install scrapy`
* create and name a folder
* copy paste code into a new file ending with the `.py` extension
## Running the Scraper
In order to run the scraper in Linux, first open your command prompt.
* cd into the folder containing the `.py` file.
* run `scrapy runspider <filename.py>`
It couldt take around 2 -5 minutes to pull around 10,000 posts depending on your system.
## Modifying the Target Values
To modify what you want scraped, first go to the [fmylife.com](https://www.fmylife.com/) website and open `Inspect Element` in
your web browser. Use these [tutorials](https://www.tutorialspoint.com/scrapy/index.htm) or the official 
[documentation](https://docs.scrapy.org/en/latest/)
to help you select the targets you want based on their CSS attributes.
## Legal
Some websites have restrictions on what can and cannot be scraped. Research beforehand. This is for educational purposes only.
 
