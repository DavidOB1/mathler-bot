import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

possible_keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "+", "-", "/", "*"]
possible_first_key = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-"]
operations = []
cannot_have = []
must_have = []
value = ["A", "A", "A", "A", "A", "A"]
not_value = ["", "", "", "", "", ""]


def input_keys(keys):
    for key in keys:
        page.send_keys(key)
        page.send_keys(Keys.RETURN)


def get_info(row):
    for i in range(6):
        symbol = op[i]
        xpath = '//*[@id="root"]/div/div[4]/div[' + str(row) + ']/div[' + str(i+1) + ']'
        stat = driver.find_element(By.XPATH, xpath).get_attribute("class")[100:110]
        if "green" in stat:
            if not symbol in must_have:
                must_have.append(symbol)
            value[i] = symbol
        elif "yellow" in stat:
            if not symbol in must_have:
                must_have.append(symbol)
            not_value[i] += symbol
        elif "slate" in stat:
            if not ((symbol in must_have) or (symbol in value) or (symbol in cannot_have)):
                cannot_have.append(symbol)


def try_op(op):
    try:
        x = eval(op)
        doubles = (("//" in op) or ("--" in op) or ("++" in op) or ("**" in op) or ("00" in op))
        if (x == num) and not doubles:
            operations.append(op)
    except:
        pass


def loop(n, s):
    if len(operations) < 1:
        if n == 5:
            if value[5] != "A":
                try_op(s+value[5])
            else:
                for i in range(y1):
                    if possible_keys[i] != not_value[n]:
                        try_op(s+possible_keys[i])
                        if not len(operations) < 1:
                            break
        elif value[n] != "A":
            loop(n+1, s+value[n])
        else:
            for i in range(y1):
                if possible_keys[i] != not_value[n]:
                    loop(n+1, s+possible_keys[i])


def loop2(n, s):
    if n == 5:
        if value[5] != "A":
            try_op(s+value[5])
        else:
            for i in range(y1):
                if possible_keys[i] != not_value[n]:
                    try_op(s+possible_keys[i])
    elif value[n] != "A":
        loop2(n+1, s+value[n])
    else:
        for i in range(y1):
            if possible_keys[i] != not_value[n]:
                loop2(n+1, s+possible_keys[i])


driver = webdriver.Chrome()
driver.get("https://www.mathler.com/")
wait = WebDriverWait(driver, 10)
wait.until(expected_conditions.title_is("Mathler - A daily math game"))
page = driver.find_element(By.TAG_NAME, "html")


daily = driver.find_element(By.CLASS_NAME, "text-xl")
num = int(daily.text[30:32])


if num <= 65:
    op = "-" + str(75 - num) + "+75"
else:
    op = "123-" + str(123 - num)


input_keys(op)
get_info(1)


for thing in cannot_have:
    if thing in possible_keys:
        possible_keys.remove(thing)
    if thing in possible_first_key:
        possible_first_key.remove(thing)
y1 = len(possible_keys)


if value[0] != "A":
    loop(1, value[0])
else:
    if not_value[0] != "":
        possible_first_key.remove(not_value[0])
    for i in range(len(possible_first_key)):
        if len(operations) < 1:
            loop(1, possible_first_key[i])


op = operations[0]
input_keys(op)
operations.remove(op)
get_info(2)


for thing in cannot_have:
    if thing in possible_keys:
        possible_keys.remove(thing)
    if thing in possible_first_key:
        possible_first_key.remove(thing)
y1 = len(possible_keys)


if value[0] != "A":
    loop2(1, value[0])
else:
    if (not_value[0] != "") and (not_value[0] in possible_first_key):
        possible_first_key.remove(not_value[0])
    for i in range(len(possible_first_key)):
        if not possible_first_key[i] in not_value[0]:
            loop2(1, possible_first_key[i])


op = random.choice(operations)
input_keys(op)

for j in range(3):
    for i in range(6):
        dont_have_this = []
        tally = 0
        xpath = '//*[@id="root"]/div/div[4]/div[' + str(j+3) + ']/div[' + str(i+1) + ']'
        stat = driver.find_element(By.XPATH, xpath).get_attribute("class")[100:110]
        if "green" in stat:
            operations = [x for x in operations if x[i] == op[i]]
            if op[i] not in must_have:
                must_have.append(op[i])
            if op[i] in dont_have_this:
                dont_have_this.remove(op[i])
            tally += 1
        elif "yellow" in stat:
            operations = [x for x in operations if (op[i] in x) and (op[i] != x[i])]
            if op[i] not in must_have:
                must_have.append(op[i])
        elif "slate" in stat:
            if not ((op[i] in must_have) or (op[i] in dont_have_this)):
                dont_have_this.append(op[i])
        for something in dont_have_this:
            operations = [x for x in operations if not something in x]
    if tally == 5:
        quit()
    op = random.choice(operations)
    input_keys(op)
