import requests
import re
import json
from .utils import Utils

URL = "https://open.kattis.com/problems/"


def problems(pages=1) -> dict:
    """
    Fetches all Kattis problems

    :param pages: number of problem pages, defaults to 1
    :rtype: list of problem objects
    """
    ret = []
    for page in range(pages):
        probs = Utils.html_page(requests.get(URL + "?page={}".format(page)))
        for problem_id in problem_list(probs):
            ret.append(problem(problem_id))
    return ret

def problems_ordered(pages=1) -> dict:
    """
    Fetches all Kattis problems

    :param pages: number of problem pages, defaults to 1
    :rtype: list of problem objects
    """
    ret_id = []
    ret_diff = []
    for page in range(pages):
        print("Fetching page " + str(page) + "...")
        probs = Utils.html_page(requests.get(URL + "?order=difficulty_category" + "&page={}".format(page)))
        [id, diff] = extract_difficulty_from_list(probs)
        ret_id = ret_id + id
        ret_diff = ret_diff + diff


        # for difficulties in extract_difficulty_from_list(probs):
        #     ret.append(difficulties)
    return [ret_id, ret_diff]

def problems_ordered_all() -> dict:
    """
    Fetches all Kattis problems

    :param pages: number of problem pages, defaults to 1
    :rtype: list of problem objects
    """
    ret_id = []
    ret_diff = []
    #Capped to 100 in case of problems
    for page in range(100):
        print("Fetching page " + str(page) + "...")
        probs = Utils.html_page(requests.get(URL + "?order=difficulty_category" + "&page={}".format(page)))
        [id, diff] = extract_difficulty_from_list(probs)
        if len(id) < 1 or len(diff) < 1:
            print("Empty page found, stopping..")
            break
        if len(id) != len(diff):    
            print("Mismatch in amount of IDs and difficulties, quitting...")
            return [-1, -1]
        ret_id = ret_id + id
        ret_diff = ret_diff + diff


        # for difficulties in extract_difficulty_from_list(probs):
        #     ret.append(difficulties)
    return [ret_id, ret_diff]

def extract_difficulty_from_list(page):
    """
    Returns a list of difficulties:
    """
    #Extract problem difficultis
    problem_field = page.findAll("span", "difficulty_number")
    difficulties = [problem_field[i].text for i in range(len(problem_field))]

    #Return in case of not finding any elements
    if len(difficulties) < 1:
        return [[],[]]

    #problem = page.findAll("td", "bubble-container")
    link_entry = page.findAll("td")#, attrs={"class": " "})
    problem_id = []
    for i, p in enumerate(link_entry):
        if hasattr(p.contents[0], 'attrs') and 'href' in p.contents[0].attrs and 'title' in p.contents[0].attrs:
            problem_id.append(p.contents[0]['href'].split("/")[2])

    
    #problem = [problem[i].contents[1] for i in range(len(problem))]
    #problem_id = [problem[i]['href'].split("/")[2] for i in range(len(problem))]
    
    #problem_id = [problem_field[i].text for i in range(len(problem_field))]
    
    #Extract problem id
    #problems = page.findAll("a", recursive=True)[18:-4]
    #problem_id = [str(problems[i]).split("/")[2].split('"')[0] for i in range(0, len(problems), 3)]
            # obj = dict(
        #     date=submission_children[1].contents,
        #     runtime=submission_children[4].contents,
        #     lang=submission_children[5].contents
        # )
    # res = []
    # for i in range(0, len(problem_id)):
    #     res.append
    #     (
    #         dict
    #         (
    #             id = problem_id[i],
    #             diff = difficulties[i]
    #         )
    #     )
    
    #res = map(lambda "id", problem_id[i], diff:difficulties[i]) for i in range(0, len(problem_id))
    return [problem_id, difficulties]  
    

def problem(problem_id: str) -> dict:
    """
    Fetches information for a single Kattis problem

    :param problem_id: id of a Kattis problem
    :rtype: json object
    """
    obj = {
        "url": URL + problem_id,
        "stats_url": URL + problem_id + "/statistics",
    }

    problem_page = Utils.html_page(requests.get(obj["url"]))
    stats_page = Utils.html_page(requests.get(obj["stats_url"]))

    add_problem_information(problem_page, obj)
    add_problem_statistics(stats_page, obj)
    add_problem_title(problem_page, obj)

    return obj

def add_problem_title(problem_page, problem: dict) -> None:
    """
    Parses problem information and adds it
    to problem object

    """
    fields = ["title"]
    info = problem_page.find("h1", "book-page-heading")
    title = info.next.text
    #title = re.sub(r'[a-zA-Z]', '', title).strip()
    problem["title"] = title

def add_problem_information(problem_page, problem: dict) -> None:
    """
    Parses problem information and adds it
    to problem object

    """
    fields = ["time_limit", "memory_limit", "difficulty"]
    info = problem_page.findAll("div", "metadata_list-item")[:3]
    for i in range(len(info)):
        s = info[i].find('span').find_next_sibling().text.strip()
        info[i] = re.sub(r'[a-zA-Z]', '', s).strip()
    problem["info"] = {fields[i]: info[i] for i in range(min(len(info), len(fields)))}

def add_problem_statistics(stats_page, problem: dict) -> None:
    """
    Parses problem statistics and adds it
    to problem object

    """
    fields = [
        "submissions",
        "accepted_submissions",
        "submission_ratio",
        "authors",
        "accepted_authors",
        "author_ratio",
    ]

    stats = stats_page.find("table", class_="table2 condensed mt-5").findAll("tr")

    # Extract the numeric values from each <td> tag
    stats = [re.sub(r'<[^>]+>', '', str(td)).strip('\n%') for tr in stats for td in tr.findAll("td")[1:]]

    problem["stats"] = {
        fields[i]: stats[i] for i in range(min(len(stats), len(fields)))
    }


def problem_list(page):
    """
    Returns a list of problem ID's scraped from a
    Kattis problem page

    :param page: problem page
    """
    problems = page.findAll("a", recursive=True)[18:-4]
    return [
        str(problems[i]).split("/")[2].split('"')[0] for i in range(0, len(problems), 3)
    ]
