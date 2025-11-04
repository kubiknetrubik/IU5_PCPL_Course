import json
import sys
from print_result import print_result
from cm_timer import cm_timer_1
from gen_random import gen_random_inf
from unique import Unique
with open("lab_python_fp/data_light.json", encoding="utf-8") as file:
        data = json.load(file)
@print_result
def f1(arg)-> list[str]:
    return sorted(Unique([User["job-name"] for User in arg],ignore_case=True))


@print_result
def f2(arg):
    return list(filter(lambda job: job.startswith("программист"), arg))


@print_result
def f3(arg):
    return list(map(lambda x: x + ' с опытом Python', arg))


@print_result
def f4(arg):
    salaries = gen_random_inf(len(arg), 100000, 200000)
    return [f"{profession}, зарплата {salary} руб." for profession, salary in zip(arg, salaries)]


if __name__ == '__main__':
    with cm_timer_1():
        f4(f3(f2(f1(data))))