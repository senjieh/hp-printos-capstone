#this script will generate fake printer data to publish just as an example of real data a printer might send

import random as r

# 
# n = the number of pages requested to print
def get_job_results(n):
    result_list = []
    result_list.append("Recieved job to print "+ str(n) +" pages.")

    for _ in range(n):
        result_list.append(print_page())

    return result_list

def print_page():
    result = r.random()
    percent_fail = 10

    if result < percent_fail/100:
        return "The page failed to print correctly."
    else:
        return "the page has been printed"


if __name__ == "__main__":
    print(get_job_results(10))