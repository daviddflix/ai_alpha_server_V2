from routes.news_bot.validations import find_matched_keywords, validate_content, title_in_blacklist, url_in_db, title_in_db
from config import AnalyzedArticle as ANALIZED_ARTICLE
from bs4 import BeautifulSoup
import requests

def validate_date_coingape(html):
    try:
        date_div = html.find('div', class_='publishby d-flex')
        if date_div:
            date_text = date_div.text.lower()
            if "mins ago" in date_text or "hours ago" in date_text:
                return date_text.strip()
        return False
    except Exception as e:
        print("Error processing the date in coingape > ", str(e))
        return None

def extract_image_urls(soup):
    try:
        image_urls = []
        img_elements = soup.find_all('img')
        for img in img_elements:
            src = img.get('src')

            if src and src.startswith('https://coingape.com/wp-content/uploads/'):
                image_urls.append(src)

        return image_urls
    except Exception as e:
        print("Error finding Images in coingape" , str(e))
        return None

# Function to validate the article using keywords
def validate_coingape_article(article_link, main_keyword, session_instance):
    normalized_article_url = article_link.strip().casefold()

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
        }

        article_response = requests.get(normalized_article_url, headers=headers)
        article_content_type = article_response.headers.get("Content-Type", "").lower()

        if not 'text/html' in article_content_type or article_response.status_code != 200:
            return None, None, None, None, None
        else:
            article_soup = BeautifulSoup(article_response.text, 'html.parser')

            #Firstly extract the title and content

            content = ""
            a_elements = article_soup.find_all("p")
            for a in a_elements:
                content += a.text.strip()

            title_element = article_soup.find('h1')
            title = title_element.text.strip() if title_element else None


            # These three following lines changes the status of the article to ANALIZED.
            is_url_analized = session_instance.query(ANALIZED_ARTICLE).filter(ANALIZED_ARTICLE.url == normalized_article_url).first()
            if is_url_analized:
                is_url_analized.is_analyzed = True
                session_instance.commit()

            try:
                if title and content:
                    is_title_in_blacklist = title_in_blacklist(title, session_instance)
                    is_valid_content = validate_content(main_keyword, content, session_instance)
                    is_url_in_db = url_in_db(normalized_article_url, session_instance)
                    is_title_in_db = title_in_db(title, session_instance)


                    # if the all conditions passed then go on
                    if not is_title_in_blacklist and is_valid_content and not is_url_in_db and not is_title_in_db:
                        valid_date = validate_date_coingape(article_soup)
                        image_urls = extract_image_urls(article_soup)
                       
                        if valid_date:
                            matched_keywords = find_matched_keywords(main_keyword, content, session_instance)
                            return title, content, valid_date, image_urls, matched_keywords
                        
                return None, None, None, None, None
                        
            except Exception as e:
                print("Inner Error in Coindesk" + str(e))
                return None, None, None, None, None

    except Exception as e:
        print(f"Error in Coindesk" + str(e))
        return None, None, None, None, None
      
