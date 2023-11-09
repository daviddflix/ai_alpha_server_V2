from routes.news_bot.sites.ambcrypto import validate_ambcrypto_article
from routes.news_bot.sites.blockworks import validate_blockworks_article
from routes.news_bot.sites.coincodex import validate_coincodex_article
from routes.news_bot.sites.coinpedia import validate_coinpedia_article
from routes.news_bot.sites.cryptodaily import validate_cryptodaily_article
from routes.news_bot.sites.cryptopotato import validate_cryptopotato_article
from routes.news_bot.sites.cryptoslate import validate_cryptoslate_article
from routes.news_bot.sites.dailyhodl import validate_dailyhodl_article
from routes.news_bot.sites.decrypto import validate_decrypt_article
from routes.news_bot.sites.dlnews import validate_dlnews_article
from routes.news_bot.sites.investing import validate_investing_article
from routes.news_bot.sites.theblock import validate_theblock_article
from routes.news_bot.sites.utoday import validate_utoday_article
from routes.slack.templates.poduct_alert_notification import send_notification_to_product_alerts_slack_channel
from ..slack.templates.news_message import send_NEWS_message_to_slack, send_INFO_message_to_slack_channel
from routes.news_bot.sites.cointelegraph import validate_cointelegraph_article
from routes.news_bot.sites.beincrypto import validate_beincrypto_article
from routes.news_bot.sites.bitcoinist import validate_bitcoinist_article
from routes.news_bot.validations import title_in_blacklist, url_in_db
from routes.news_bot.sites.coindesk import validate_coindesk_article
from routes.news_bot.sites.coingape import validate_coingape_article
from models.news_bot.news_bot_model import SCRAPPING_DATA
from routes.twitter.index import send_tweets_to_twitter
from models.news_bot.articles_model import ARTICLE
from playwright.sync_api import sync_playwright
from .summarizer import summary_generator
from config import session

btc_slack_channel_id = 'C05RK7CCDEK'
eth_slack_channel_id = 'C05URLDF3JP'
lsd_slack_channel_id = 'C05UNS3M8R3'
hacks_slack_channel_id = 'C05UU8JBKKN'
solana_slack_channel_id = 'C05URM66B5Z'


def scrape_sites(site, base_url, website_name, is_URL_complete, main_keyword, main_container):

    article_urls = set()
    elements = []

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()

            page.goto(site, timeout=100000)
            page.wait_for_load_state("domcontentloaded")

          

            if main_container != "None":
                container = page.wait_for_selector(main_container)
                a_elements = container.query_selector_all('a')
                for link in a_elements:
                    href = link.get_attribute('href')
                    article_title = link.text_content().strip().casefold()

                    if href and article_title:
                        elements.append({'href': href, 'article_title': article_title})
            else:
                links = page.evaluate('''() => {
                    const anchors = Array.from(document.querySelectorAll('a'));
                    return anchors.map(a => ({
                        href: a.href,
                        text: a.textContent.trim().toLowerCase()
                    }));
                }''')

                for link in links:
                    href = link['href']
                    article_title = link['text']

                    if href and article_title:
                        elements.append({'href': href, 'article_title': article_title})

            keywords = []

            if main_keyword == 'bitcoin':
                keywords = ['bitcoin', 'btc']
            # elif main_keyword == 'ethereum':
            #     keywords = ['ethereum', 'ether', 'eth']

            for link in elements:
                href = link['href']
                article_title = link['article_title']
              
                article_url = base_url + href.strip() if not href.startswith('http') else href.strip()

                if main_keyword == 'bitcoin':
                    if any(keyword in article_title.lower() for keyword in keywords):
                        is_title_in_blacklist = title_in_blacklist(article_title)
                        is_url_in_db = url_in_db(article_url)
                        
                        if is_title_in_blacklist == False and is_url_in_db == False:
                            article_urls.add(article_url)
                else:
                    is_title_in_blacklist = title_in_blacklist(article_title)
                    is_url_in_db = url_in_db(article_url)
                    if is_title_in_blacklist == False and is_url_in_db == False:
                        article_urls.add(article_url)
           
            browser.close()
            return article_urls, website_name
        
    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return f'An error occurred: {str(e)}'
                 


def scrape_articles(sites, main_keyword):

    try:
        site = sites.site
        base_url = sites.base_url
        website_name = sites.website_name
        is_URL_complete = sites.is_URL_complete
        main_container = sites.main_container

        print(f'Web scrape of {main_keyword} STARTED for {website_name}')

        article_urls, website_name = scrape_sites(site,base_url,
                                                   website_name,
                                                   is_URL_complete,
                                                   main_keyword,
                                                   main_container)
        

        
        if not article_urls:
            print(f'No articles found for {website_name} of {main_keyword}')
            return f'No articles found for {website_name}'
         
        print('article_urls > ', article_urls)
        
        if article_urls:
            for article_link in article_urls:

                article_to_save = []
                
                if website_name == 'Ambcrypto':
                    title, content, valid_date, image_urls = validate_ambcrypto_article(article_link, main_keyword)
                    if title and content and valid_date:
                        article_to_save.append((title, content, valid_date, article_link, website_name, image_urls))

                if website_name == 'Beincrypto':
                    title, content, valid_date, image_urls = validate_beincrypto_article(article_link, main_keyword)
                    if title and content and valid_date:
                        article_to_save.append((title, content, valid_date, article_link, website_name, image_urls))

                if website_name == 'Bitcoinist':
                    title, content, valid_date, image_urls = validate_bitcoinist_article(article_link, main_keyword)
                    if title and content and valid_date:
                        article_to_save.append((title, content, valid_date, article_link, website_name, image_urls))
                
                if website_name == 'Blockworks':
                    title, content, valid_date, image_urls = validate_blockworks_article(article_link, main_keyword)
                    if title and content and valid_date:
                        article_to_save.append((title, content, valid_date, article_link, website_name, image_urls))
                
                if website_name == 'Coincodex':
                    title, content, valid_date, image_urls = validate_coincodex_article(article_link, main_keyword)
                    if title and content and valid_date:
                        article_to_save.append((title, content, valid_date, article_link, website_name, image_urls))

                if website_name == 'Cointelegraph':
                    title, content, valid_date, image_urls = validate_cointelegraph_article(article_link, main_keyword)
                    if title and content and valid_date:
                        article_to_save.append((title, content, valid_date, article_link, website_name, image_urls))

                if website_name == 'Coingape':
                    title, content, valid_date, image_urls = validate_coingape_article(article_link, main_keyword)
                    if title and content and valid_date:
                        article_to_save.append((title, content, valid_date, article_link, website_name, image_urls))

                if website_name == 'Coindesk':
                    title, content, valid_date, image_urls = validate_coindesk_article(article_link, main_keyword)
                    if title and content and valid_date:
                        article_to_save.append((title, content, valid_date, article_link, website_name, image_urls))
                        
                if website_name == 'Coinpedia':
                    title, content, valid_date, image_urls = validate_coinpedia_article(article_link, main_keyword)
                    if title and content and valid_date:
                        article_to_save.append((title, content, valid_date, article_link, website_name, image_urls))
                
                if website_name == 'Dailyhodl':
                    title, content, valid_date, image_urls = validate_dailyhodl_article(article_link, main_keyword)
                    if title and content and valid_date:
                        article_to_save.append((title, content, valid_date, article_link, website_name, image_urls))
                
                if website_name == 'Cryptodaily':
                    title, content, valid_date, image_urls = validate_cryptodaily_article(article_link, main_keyword)
                    if title and content and valid_date:
                        article_to_save.append((title, content, valid_date, article_link, website_name, image_urls))
                        
                if website_name == 'Utoday':
                    title, content, valid_date, image_urls = validate_utoday_article(article_link, main_keyword)
                    if title and content and valid_date:
                        article_to_save.append((title, content, valid_date, article_link, website_name, image_urls))
                
                if website_name == 'Cryptonews':
                    title, content, valid_date, image_urls = validate_coindesk_article(article_link, main_keyword)
                    if title and content and valid_date:
                        article_to_save.append((title, content, valid_date, article_link, website_name, image_urls))
                        
                if website_name == 'Coincodex':
                    title, content, valid_date, image_urls = validate_coindesk_article(article_link, main_keyword)
                    if title and content and valid_date:
                        article_to_save.append((title, content, valid_date, article_link, website_name, image_urls))
                
                if website_name == 'Cryptopotato':
                    title, content, valid_date, image_urls = validate_cryptopotato_article(article_link, main_keyword)
                    if title and content and valid_date:
                        article_to_save.append((title, content, valid_date, article_link, website_name, image_urls))
                
                if website_name == 'Cryptoslate':
                    title, content, valid_date, image_urls = validate_cryptoslate_article(article_link, main_keyword)
                    if title and content and valid_date:
                        article_to_save.append((title, content, valid_date, article_link, website_name, image_urls))
                
                if website_name == 'Decrypt':
                    title, content, valid_date, image_urls = validate_decrypt_article(article_link, main_keyword)
                    if title and content and valid_date:
                        article_to_save.append((title, content, valid_date, article_link, website_name, image_urls))
                        
                if website_name == 'Dlnews':
                    title, content, valid_date, image_urls = validate_dlnews_article(article_link, main_keyword)
                    if title and content and valid_date:
                        article_to_save.append((title, content, valid_date, article_link, website_name, image_urls))
                
                if website_name == 'Investing':
                    title, content, valid_date, image_urls = validate_investing_article(article_link, main_keyword)
                    if title and content and valid_date:
                        article_to_save.append((title, content, valid_date, article_link, website_name, image_urls))
                
                if website_name == 'Theblock':
                    title, content, valid_date, image_urls = validate_theblock_article(article_link, main_keyword)
                    if title and content and valid_date:
                        article_to_save.append((title, content, valid_date, article_link, website_name, image_urls))
                
                if not article_to_save:
                    print(f'{website_name} has no articles to save')
                
                # if len(article_to_save) > 0:
                #     print('title: ', article_to_save[0])
                #     print('Date: ', article_to_save[2])
                #     print('Link: ', article_to_save[3]) 
                   
               
                for article_data in article_to_save:
                    title, content, valid_date, article_link, website_name, image_urls = article_data
                    print('\ntitle > ', title)
                    print('article_link > ', article_link)
                    print('valid_date > ', valid_date)
                    
                    if main_keyword == 'bitcoin':
                        channel_id = btc_slack_channel_id
                    elif main_keyword == 'ethereum':
                        channel_id = eth_slack_channel_id
                    elif main_keyword == 'hacks':
                        channel_id = hacks_slack_channel_id
                    elif main_keyword == 'solana':
                        channel_id = solana_slack_channel_id
                    else:
                        channel_id = lsd_slack_channel_id

                    summary = summary_generator(content, main_keyword)
                    
                    if summary:
                        print('-----There is a summary-----')
                        send_NEWS_message_to_slack(channel_id=channel_id, 
                                            title=title,
                                            date_time=valid_date,
                                            url=article_link,
                                            summary=summary,
                                            images_list=image_urls,
                                            main_keyword=main_keyword
                                            )

                        if main_keyword == 'bitcoin':
                            response, status = send_tweets_to_twitter(content=summary,
                                                                      title=title)

                            if status == 200:
                                send_INFO_message_to_slack_channel(channel_id=channel_id,
                                                                title_message="New Notification from AI Alpha",
                                                                sub_title="Response",
                                                                message=response
                                                                )
                        
                        new_article = ARTICLE(title=title,
                        content=content,
                        date=valid_date,
                        url=article_link,
                        website_name=website_name
                        )

                        session.add(new_article)
                        session.commit()
                        print(f'\nArticle: "{title}" has been added to the DB, Link: {article_link} from {website_name} in {main_keyword.capitalize()}.')
                    else:
                        print('------ there is no summary -----')
                        continue
                    
            return f'Web scrapping of {website_name} finished', 200
        
    except Exception as e:
        return f'Error in scrape_articles: {str(e)}', 500
    

def start_periodic_scraping(main_keyword):

    scrapping_data_objects = session.query(SCRAPPING_DATA).filter(SCRAPPING_DATA.main_keyword == main_keyword).all()

    if not scrapping_data_objects:
        print(f'Bot with keyword {main_keyword} was not found')
        return f'Bot with keyword {main_keyword} was not found'
    else:
        sites = scrapping_data_objects[0].sites
        for site in sites:
            scrape_articles(site, main_keyword)

        return f'All {str(main_keyword).casefold().capitalize()} sites scraped', 200