import requests
from bs4 import BeautifulSoup
from pprint import pprint


def request_data(num_pages=1):
    links = []
    points = []
    for page in range(1, num_pages+1):
        response = requests.get(f"https://news.ycombinator.com?p={page}")
        soup = BeautifulSoup(response.text, "html.parser")  # converts website data from string to html object
        links += soup.select(".storylink")
        subtext = soup.select(".subtext")  # this is selected before points in the case that points has no value (0)
        for item in subtext:
            points += item.select(".score")  # therefore, if points = 0, its index will be None

    return links, points


def filter_list(formatted_list, min_points):
    filtered = []
    for i in range(len(formatted_list) - 1):
        if int(formatted_list[i]["points"]) >= min_points:
            filtered.append(formatted_list[i])
    return filtered


def format_data(links, points):
    new_list = []
    for index in range(len(links) - 1):
        title = links[index].text
        href = links[index].get("href")
        if points[index]:
            # each score object is a list of one item, hence [0]
            score = int(points[index].getText().rstrip(" points"))
        else:
            score = 0
        new_list.append({"title": title, "link": href, "points": score})

    return new_list


def get_min_points():
    while True:
        try:
            min_points = int(input("Enter minimum amount of points: "))
            if min_points < 0:
                print("Points cannot be negative")
            else:
                break
        except ValueError:
            print("Not a number")

    return min_points


def get_num_pages():
    while True:
        try:
            num_pages = int(input("Enter number of pages to search through: "))
            if num_pages < 0:
                print("Number of pages cannot be negative")
            else:
                break
        except ValueError:
            print("Not a number")

    return num_pages


def sort_by_points(d):
    sorted_dict = sorted(d, key=lambda k: k["points"], reverse=True)  # sorts by the points value for each link

    return sorted_dict


def main():
    min_points = get_min_points()
    num_pages = get_num_pages()
    response = request_data(num_pages)

    links = response[0]
    points = response[1]
    formatted = format_data(links, points)
    filtered = filter_list(formatted, min_points)
    sorted_list = sort_by_points(filtered)

    return sorted_list


if __name__ == "__main__":
    articles = main()

    pprint(articles)
    print(f"\nFound {len(articles)} articles")
