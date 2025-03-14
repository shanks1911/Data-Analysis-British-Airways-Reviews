# to get all ratings for all reviews

for i in range(1, pages + 1):
    print(f"Scraping page {i}")
    url = f"{base_url}/page{i}/?sortby=post_date%3ADesc&pagesize={page_size}"

    response = requests.get(url)
    content = response.content
    parsed_content = BeautifulSoup(content, 'html.parser')    

    
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