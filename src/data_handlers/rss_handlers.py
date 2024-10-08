from lxml import etree
import data_handlers.web_data_handlers as WDHandlers

#represents RSS metadata of an article
class RSSArticleData:
    def __init__(self, title: str, link: str, author: str, pubdate: str):
        self.title = title
        self.link = link
        self.author = author
        self.pubdate = pubdate

    def __eq__(self, other):
        if isinstance(other, RSSArticleData):
            return (
                self.title == other.title and
                self.link == other.link and
                self.author == other.author and
                self.pubdate == other.pubdate
            )
        return False

#represents RSS Feed's metadata
#publication_title: tile of publication, magazine, news outlet, etcetera
#articles_data: contains metadata for each article in RSS Feed
class RSSFeedData:
    def __init__(self, publication_title: str, articles_data: list[RSSArticleData]):
        self.publication_title = publication_title
        self.articles_data = articles_data

    def __eq__(self, other):
        if isinstance(other, RSSFeedData):
            return (
                self.publication_title == other.publication_title and
                self.articles_data == other.articles_data
            )
        return False

#get RSS Feed metadata
#title of publication and metadata for each article
def getRSSFeedData(rss_feed: etree.Element):
    rss_articles_data: list[RSSArticleData] = []
    rss_feed_title: str = rss_feed.xpath('channel/title/text()')[0]
    for article in rss_feed.iter("item"):
        title: str = article.xpath('title/text()')[0]
        link: str = article.xpath('link/text()')[0]
        pubdate: str = article.xpath('pubDate/text()')[0]

        #Handles case where there may not be an author
        authors: list[str] = article.xpath('dc:creator/text()', namespaces={'dc': "http://purl.org/dc/elements/1.1/"})
        if not authors:
            author: str = 'Unknown'
        else:
            author: str = authors[0]

        rss_articles_data.append(RSSArticleData(title, link, author, pubdate))

    return RSSFeedData(rss_feed_title, rss_articles_data)

#returns a list of RSS urls from a specified file line-deliminated file
def getRSSUrls(rss_urls_filepath: str):
    return WDHandlers.getLineDelimitedData(rss_urls_filepath)

#gets metadata of all RSS Feeds in a line-deliminated file with urls to RSS Feeds
def getRSSFeedsDataFromRSSUrlsFile(rss_urls_filepath: str):
    rss_urls: list[str] = getRSSUrls(rss_urls_filepath)
    #parsed, but unprocessed rss feeds data
    rss_feeds_raw: list[etree.Element] = []
    #processed rss feeds data
    rss_feeds_data : dict[RSSFeedData] = {}

    for rss_feed_url in rss_urls:
        rss_feeds_raw.append(WDHandlers.getXMLData(rss_feed_url))
    
    for rss_feed_raw in rss_feeds_raw:
        rss_feed = getRSSFeedData(rss_feed_raw)
        rss_feeds_data[rss_feed.publication_title] = rss_feed.articles_data

    return rss_feeds_data