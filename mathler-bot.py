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
skip_good_guess = True
## if you set skip_good_guess to False, it can sometimes solve the puzzles
## in less turns, but there will be longer pauses since it has to do
## more computation
keep_off = False


driver = webdriver.Chrome()
driver.get("https://www.mathler.com/")
wait = WebDriverWait(driver, 10)
wait.until(expected_conditions.title_contains("Mathler - A daily math"))
page = driver.find_element(By.TAG_NAME, "html")
num = int(driver.find_element(By.CLASS_NAME, "text-md").text[40:])


def get_first_guess():
    if num <= 65:
        operations.append(f"-{75 - num}+75")
    else:
        operations.append(f"123-{123 - num}")


def input_keys(keys):
    for key in keys:
        page.send_keys(key)
    page.send_keys(Keys.RETURN)


def get_info(row):
    tally = 0
    for i in range(6):
        symbol = op[i]
        xpath = f'//*[@id="root"]/div/div[3]/div[{row}]/div[{i+1}]'
        stat = driver.find_element(By.XPATH, xpath).get_attribute("class")[100:110]
        if "green" in stat:
            if not symbol in must_have:
                must_have.append(symbol)
            value[i] = symbol
            tally += 1
        elif "yellow" in stat:
            if not symbol in must_have:
                must_have.append(symbol)
            not_value[i] += symbol
        elif "slate" in stat:
            if not ((symbol in must_have) or (symbol in value) or (symbol in cannot_have)):
                cannot_have.append(symbol)
    if tally == 6:
        quit()
    return tally


def try_op(op):
    try:
        x = eval(op)
        if (x == num):
            doubles = (("//" in op) or ("--" in op) or ("++" in op) or ("**" in op) or ("00" in op))
            if (not doubles) and (skip_good_guess or (good_guess(op))):
                for item in must_have:
                    if not item in op:
                        return
                operations.append(op)
    except:
        return


def good_guess(op):
    for value in op:
        if op.count(value) > 1:
            return False
    return True


def loop(n, s):
    if len(operations) < 1:
        if n == 5:
            if value[5] != "A":
                try_op(s+value[5])
            else:
                for item in possible_keys:
                    if item != not_value[n]:
                        try_op(s+item)
                        if len(operations) > 0:
                            break
        elif value[n] != "A":
            loop(n+1, s+value[n])
        else:
            for item in possible_keys:
                if item != not_value[n]:
                    loop(n+1, s+item)


def get_guess():
    if value[0] != "A":
        loop(1, value[0])
    else:
        if not_value[0] != "":
            possible_first_key.remove(not_value[0])
            not_value[0] = ""
        for first_value in possible_first_key:
            if len(operations) > 0:
                break
            else:
                loop(1, first_value)


def eliminate_keys():
    for thing in cannot_have:
        if thing in possible_keys:
            possible_keys.remove(thing)
        if thing in possible_first_key:
            possible_first_key.remove(thing)


get_first_guess()

for i in range(6):
    op = operations[0]
    input_keys(op)
    operations.remove(op)
    y = get_info(i+1)
    if y > 1:
        if not keep_off:
            skip_good_guess = False
    eliminate_keys()
    get_guess()
    if len(operations) == 0:
        skip_good_guess = True
        keep_off = True
        get_guess()
