import requests # type: ignore
from bs4 import BeautifulSoup # type: ignore
import pandas as pd # type: ignore

def scrape_reviews():
    base_url = "https://www.airlinequality.com/airline-reviews/british-airways"
    pages = 10
    page_size = 100

    reviews = []
    rating = []
    ratings_dict = {
        "seat_comfort": [],
        "cabin_staff_service": [],
        "food_and_beverages": [],
        "inflight_entertainment": [],
        "ground_service": [],
        "wifi_and_connectivity": [],
        "value_for_money": [],
    }
    recommended = []

    for i in range (1,pages + 1):
        print(f"Scraping page {i}")
        url = f"{base_url}/page{i}/?sortby=post_date%3ADesc&pagesize={page_size}"

        response = requests.get(url)
        content = response.content
        parsed_content = BeautifulSoup(content, 'html.parser')

        # reviews
        for para in parsed_content.find_all('div', class_='text_content'):
            reviews.append(para.get_text())   

        # rating
        for rate in parsed_content.find_all('span',itemprop='ratingValue'):
            if not rate.find_parent("div", class_="rating-10 rating-large"):
                rating.append(rate.text)

        # recommend
        for recommendation in parsed_content.find_all('td', class_="review-value"):
                if recommendation.find_parent("tr").find("td", class_="review-rating-header recommended"):
                    recommended_status = recommendation.text.strip()
                    recommended.append(recommended_status)
        
        print(f"Found {len(reviews)} reviews")

        # Find all review sections (assuming each review is inside a div with class="body")
        review_rows = parsed_content.find_all("div", class_="body")

        for review in review_rows:
            for category in ratings_dict.keys():
                # Find the specific <td> for this category within the review
                rating_td = review.find("td", class_=f"review-rating-header {category}")

                if rating_td:
                    # Get the next <td> sibling that contains the stars
                    star_td = rating_td.find_next_sibling("td", class_="review-rating-stars stars")

                    if star_td:
                        star_count = len(star_td.find_all("span", class_="star fill"))
                        ratings_dict[category].append(star_count)
                    else:
                        ratings_dict[category].append("NA")  # No stars found
                else:
                    ratings_dict[category].append("NA")  # No rating found

        print(f"Collected {len(review_rows)} reviews on page {i}")

    # Ensure all lists match expected review count (1000 total)
    for key in ratings_dict:
        while len(ratings_dict[key]) < 1000:  
            ratings_dict[key].append("NA")

    print(f"Final counts: { {k: len(v) for k, v in ratings_dict.items()} }")

    df_1 = pd.DataFrame({"Reviews": reviews, "Overall Ratings": rating, "Recommended":recommended})
    df_2 = pd.DataFrame(ratings_dict)

    if len(df_1)!=len(df_2):
        raise ValueError("Mismatch in number of reviews and ratings!")
    df = pd.concat([df_1,df_2], axis=1)

    # write to File
    df.to_csv("BA_reviews.csv", index=False)

    print("Data saved to BA_reviews.csv")
    return df
