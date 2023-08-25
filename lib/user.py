import requests
import re
from .utils import Utils
from .problems import problem

URL = "https://open.kattis.com/problems/"
URL_SUBMISSION = "https://open.kattis.com/submissions/"


class KattisUser:
    """
    An authenticated Kattis User

    :param username: kattis username
    :param password: kattis password
    :param cookies: user login cookies
    """

    def __init__(self, username, password, cookies):
        self.username = username
        self.__password = password
        self.__cookies = cookies
        self.__submission_url = "https://open.kattis.com/users/"
        self.__problem_url = "https://open.kattis.com/problems?show_solved=on&show_partial=off&show_tried=off&show_untried=off"

    def problem(self, problem_id: str) -> dict:
        """
        Gets a users solved problem.

        """
        #problem_page = Utils.html_page(requests.get(URL + problem_id + "?tab=submissions"))
        problem_page = Utils.html_page(
            requests.get(
                URL + problem_id + "?tab=submissions",
                data={"script": "true"},
                cookies=self.__cookies,
            )
        )

        #print(problem_page)
        # file = open("./test_page.txt", "w")
        # file.write(str(problem_page))
        # file.close()

        solution = problem_page.find("div", "status is-status-accepted")
        
        if(solution == None):
            return [False, None, None, None]

        submission = solution.findParent("tr")
        submission_id = submission["data-submission-id"]

        submission_page = Utils.html_page(
            requests.get(
                URL_SUBMISSION + submission_id,
                data={"script": "true"},
                cookies=self.__cookies,
            )
        )

        #print(problem_page)
        # file = open("./test_page.txt", "w")
        # file.write(str(submission_page))
        # file.close()

        submission_fields = submission_page.find(attrs={"data-submission-id": submission_id})
        if(submission_fields == None):
            return [False, None, None, None]
        submission_children = submission_fields.findChildren("td")
        if(submission_children == None):
            return [False, None, None, None]
        # print(submission_children[1].next)
        # print(submission_children[4].next)
        # print(submission_children[5].next)

        # obj = dict(
        #     date=submission_children[1].contents,
        #     runtime=submission_children[4].contents,
        #     lang=submission_children[5].contents
        # )
        date = submission_children[1].text
        runtime = submission_children[4].text
        lang = submission_children[5].text
        return [True, date, runtime, lang]

    def problems(self, pages=1) -> dict:
        """
        Gets a users solved problems.

        """
        obj, data, count = {}, {"script": "true"}, 0

        for page in range(pages):
            problem_page = Utils.html_page(
                requests.get(
                    self.__problem_url + "&page={}".format(page),
                    data=data,
                    cookies=self.__cookies,
                )
            )

            problem_list = problem_page.find("table", "table2").find_all("tr")
            for prob in problem_list[1:]: # skip table header
                children = prob.findChildren("a")
                problem_id = children[0]["href"].split("/")[2]
                obj[problem_id] = problem(problem_id) # can take very long if there are many solved problems
                count += 1

        obj["count"] = count
        return obj

    def stats(self) -> dict:
        """
        Gets a users stats (score, rank)

        """
        fields, data = ["rank", "score"], {"script": "true"}

        stats_page = Utils.html_page(
            requests.get(
                self.__submission_url + self.username,
                data=data,
                cookies=self.__cookies,
            )
        )

        # Parse score and rank
        user_stats = stats_page.findAll("div", "divider_list-item")
        for i in range(len(user_stats)):
            s = re.compile(r"[^\d.]+")
            user_stats[i] = s.sub("", str(user_stats[i]))

        return {
            fields[i]: user_stats[i] for i in range(min(len(user_stats), len(fields)))
        }

    def data(self) -> dict:
        """
        Combined solved problems and user stats

        """
        pages = 28
        return {
            "username": self.username,
            "stats": self.stats(),
            "problems": self.problems(pages)
        }
