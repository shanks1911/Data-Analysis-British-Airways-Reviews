from bs4 import BeautifulSoup

with open('home.html','r') as html_file:
    content = html_file.read()
    
    # args - html file, parsor method
    soup = BeautifulSoup(content, 'lxml')

    # to find content associated with a particular tag
    # it finds the first element and then stops execution
    # tags = soup.find('h5')

    # to find all the instances of a particular tag, we use find_all
    # tags = soup.find_all('h5')
    # print(tags)

    # modified version to print only the text and not the html tags
    # courses_tags = soup.find_all('h5')
    # for course in courses_tags:
    #     print(course.text)

    # we use _ after class since class is a reserved keyword
    course_cards = soup.find_all('div', class_='card')
    for course in course_cards:
        course_name = course.h5.text
        course_price = course.a.text.split()[-1]

        print(f"{course_name} for {course_price}")
        
