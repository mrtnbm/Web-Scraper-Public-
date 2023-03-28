import logging
import os
import pathlib
import random
import sys
import time
from datetime import datetime

import PySimpleGUI as sg  # code convention, see PySimpleGUI docs
import requests
from bs4 import BeautifulSoup, SoupStrainer

now: datetime = datetime.now()
dt_string: str = now.strftime("%d%m%Y-%H%M%S")

logging.basicConfig(filename=dt_string + '.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

CURRENT_WORKING_DIR: str = os.path.abspath(os.getcwd())
MAX_RETRIES_REQ = 164
HEADERS: dict[str, str] = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'}
REQ_TIMEOUT = 3.05

ICON_CANCEL = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA7EAAAOxAGVKw4bAAACCklEQVRYhb2Xz0obURTGfwkhS' \
              b'CgiWQRXUvIAJfQBxEX7Dn2KLoovUIIElyW46rpI8QFEWwldhZKWVLoSEdylRUqooGIX/VzMDJmMd+aeySS5cDYzZ873zfl3zylhPI' \
              b'Iq8AJ4CTwHmsAT4B9wC/wCvgEnwHEpeFb8CBqCXcEfgYzyV9AVbBQBrgi2Q2NW4KTcCXYEK3nB1wVfCgAnZaggZCbwpuBijuCR/Ba' \
              b'0fOCNBYHHSbg9ISgLThYIHsmpMycEr5cAHsluErwuGHs+OhN8MhjvC757dO6nQiFoez74GpIsK6jvNL2PgqqgJjj02HwfgVcEowzF' \
              b'C0E9RhbBO4feB0ElplfzeOJGsIpgy8N0oKANk0FiCjyW1D4vvLK4X4IDB0BEwgWOJ1STMBhYRrKfAlSeEVyCAYKfRmUniQLgElyh/' \
              b'J3PSWIGcAnGZeB/2h+lnCz9vLbIG4JHCZewlVaimSGwJmFatruS0EpiYC3DtAroet6ZynDTx1LuRtT1EDQ3ollasevvpkjI2opD5b' \
              b'cGL0SX0V6G3oEml9GR1/0xtpbr+Fy2gaWvYAbM0pm+jkMSyxxIOq4aXtZINlTamK5gKD1fIPjokesdJJ4uiMRI8CwTPOGJ3pzdblt' \
              b'MEjnxRsVXs7YSjSwvkYagI7jKAWxeTks5iFSBLYL1vEXg0rXw9TVwCfwAesBn63r+AFBlaRT3w8ejAAAAAElFTkSuQmCC '
ICON_WARNING = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAACXBIWXMAAA7EAAAOxAGVKw4bAAACDUlEQVRYhcXXz0sVURQH8M8M' \
               b'D5EIERdhISIuokUrg2gRBZUS1Z8hEW2iTbSPEKJ/IFr0w3/BiqiEdi0SFWtdWdFCCKHCkuq0mPfwNVjvzlPf+8JhmDtzzvd7zj1z' \
               b'751MIqK4HMYJHMII+uuPV/EWc5jFy4zfqbFbEfcFV4I3QSTau+Bq0LcVYsFksFKBuGwrwfkgr0reHzzYAnHZHgUDqeR7gqVtJG/Y' \
               b'UjBY5stK5AN4joMtdC7jRWnsCIZb+L3C8YzPm2WeB48Ts5nexH860fdJc080N8cFTLTIYDtwChf/ElAv/fUOkDdwrdGUjQpcsrGo' \
               b'dAL9uEwx7zVMdpC8gcmgluMo9nVBwCCO5RjvAnkD4znGuihgLMdoFwWM5lLX6J3BQLVdageQKw4T3cJqrthYuoXlGhYUx6wq2BUM' \
               b'lcfaELAgOLMDe3+qncuCXnzS2b2Aovf25hnfcbeNALM4W7enbfjfr3MTDAVrFUr3OuhpRApqwWIF/7Won55yyPiAGxXUz2SsN24y' \
               b'fmKmgv/NrPz1BT3BXGIG98oRgzuJvvPN1SsHGQ7eJwT5EZxu8puoj7Xy+xjFH9W/EexPFBH1eV8MfiWSH0iaoHol5rfxe59vmfkm' \
               b'InqDqcTS/m+qpqJYa9pDMBrcDr5VIP4S3ErJOmv1QpOQ3YrGO6k4RY3Y6OZ1xe/5Ap7hYcbXlLh/AHcmXTfceSpqAAAAAElFTkSu' \
               b'QmCC '

print = sg.Print


def parse_save_website(website_page, lst_of_links, sel_lang="") -> None:
    """
    Parses HTML with lxml (faster than html.parser,
    see https://www.crummy.com/software/BeautifulSoup/bs4/doc/#improving-performance) and only saves a tags into a
    list
    :param sel_lang: selected language if not all should be scraped
    :param website_page: Response of server request :returns: None
    """
    if sel_lang == "":
        for link_el in BeautifulSoup(website_page.content, features="lxml", parse_only=SoupStrainer('a')):
            if hasattr(link_el, "href") and 'how-to-count-in' in link_el['href']:
                # "aczu savnecze" is the first artificial language which we do not want to scrape
                if 'aczu-savnecze' in link_el['href']:
                    break
                lst_of_links.append(link_el['href'])

        # the first link_el is for a random entry
        lst_of_links.pop(0)
    else:
        for link_el in BeautifulSoup(website_page.content, features="lxml", parse_only=SoupStrainer('a')):
            if hasattr(link_el, "href") and 'how-to-count-in' in link_el['href']:
                if sel_lang.lower() in link_el['href']:
                    lst_of_links.append(link_el['href'])
                    break
        if len(lst_of_links) == 0:
            sg.SystemTray.notify("Language not listed on website", "Closing program...", display_duration_in_ms=750,
                                 fade_in_duration=100, icon=ICON_WARNING)
            sys.exit(1)


def write_csv(string, path) -> None:
    """
    Writes string to csv file in root directory
    :param path: Desired file-path
    :param string: String containing all numerals in csv style
    :return: None
    """
    filename = 'dataset.csv'
    full_path = os.path.join(path, filename)
    # utf-8-sig forces Excel to open file with uft-8
    with open(full_path, 'w', newline='', encoding='utf-8-sig') as f:
        f.write("Language;Number;Numeral\n")  # header
        f.write(string)


def find_lang_short(list_item) -> str:
    """
    Returns last suffix without "/" of the given website, which is used for posting requests to the server.
    :param list_item: List item of lst_of_links
    :return: String
    """
    return str(list_item).removesuffix('/').split("/")[-1]


def find_lang_long(list_item):
    """
    Returns language of the given website in uppercase.
    :param list_item: List item of lst_of_links
    :return: String
    """
    return list_item.split('how-to-count-in-')[1].split('/', 1)[0].title()

# def progress_bar(counter):
#     """
#     [Not used, headless mode only]
#     Prints out progress bar in cmd.
#     :param counter: Amount of links already processed
#     :return: String
#     """
#     return print(end="\r" + "░" * 81 + "┃\r┃" + "█" * int(80 * counter / (len(lst_of_links) - 1)) + "%6.2f %%" % (
#             counter / (len(lst_of_links) - 1) * 100))


def collapse(layout, key, visible):
    """
    See https://stackoverflow.com/a/63471167
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed".
    The purpose of this function is to create a collapsible section in a GUI using the PySimpleGUI library. By default, all sections created using PySimpleGUI are visible. However, this function allows the user to create a section that is initially hidden and can be made visible later by setting the visible attribute of the section to True.

    The pin method is used to ensure that the column is not resized or moved by the user when it is visible. This ensures that the collapsed section always occupies the same space in the layout, whether it is visible or not.
    :param layout: The layout for the section
    :param key: Key used to make this section visible / invisible
    :param visible: A boolean value that determines if the section is initially visible or not.
    :return: A pinned column that can be placed directly into your layout
    :rtype: sg.pin
    """
    return sg.pin(sg.Column(layout, key=key, visible=visible, pad=(0, 0)))


def create_main_window():
    """
    Creates a GUI window in which the user can define the csv path and the numbers which should be extracted. The
    window then closes and the script starts.
    :return: (event, values) User input from the text fields and the fired events (events).
    """

    sg.theme('Dark Gray 13')

    hidden_sec = [[sg.Text("Specific language that should be scraped:", border_width=0)],
                  [sg.InputText(default_text="", text_color="lightgray",
                                tooltip="Enter the language which should be scraped.", key="inputtxt", border_width=0)]]

    layout = [[sg.Text("Start number for each language:", border_width=0)],
              [sg.InputText(default_text=1, text_color="lightgray",
                            tooltip="Enter the start number (int) which should be used for scraping.", border_width=0)],
              [sg.Text("End number for each language", border_width=0)],
              [sg.InputText(default_text=2, text_color="lightgray",
                            tooltip="Enter the end number (int) which should be used for scraping.", border_width=0)],
              [sg.Text("Steps between numbers", border_width=0)],
              [sg.InputText(default_text=1, text_color="lightgray",
                            tooltip="Enter in what steps numbers should be scraped between Start-End", border_width=0)],
              [sg.Text("Path to csv file:", border_width=0)],
              [sg.InputText(default_text=CURRENT_WORKING_DIR, text_color="lightgray",
                            tooltip="Enter desired path for the csv-file!", border_width=0), sg.FolderBrowse()],
              [collapse(hidden_sec, 'hidden_sec', True)],
              [sg.Checkbox(text="Scrape all languages",
                           default=False, key='-CB-', enable_events=True)],
              [sg.Button("OK", font=("Helvetica", "10", "bold"), border_width=0), sg.Button("Exit", border_width=0)]]

    window = sg.Window('Web-Scraper', layout, finalize=True, resizable=True, auto_size_text=True,
                       auto_size_buttons=True, no_titlebar=False, grab_anywhere=True, keep_on_top=False)

    toggle_sec1 = True

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            window.close()
            # sys.exit(0)
            return "", {}
        if event == "-CB-":
            toggle_sec1 = not toggle_sec1
            window['hidden_sec'].update(visible=toggle_sec1)
        if event == "OK":
            try:
                int(values[0])
                int(values[1])
                int(values[2])
                path = pathlib.Path(values[3])
                if not (path.is_dir() and path.exists()):
                    logging.error("Path is not a directory or does not exist.")
                    create_pop_up_window(mode="path")
                    continue
            except ValueError as valerr:
                logging.error(
                    "Values 0-2 contains non integer values.: %s", valerr)
                create_pop_up_window()
                continue
            window.close()
            break
    return event, values


def create_pop_up_window(mode=""):
    """
    Creates a pop-up window in case the user has entered non integer values in the text fields for the number intervalls and steps or an invalid path for saving the csv file.
    :return: None
    """
    if mode == "path":
        text = "Please enter a valid path to a directory!"
    else:
        text = "Please enter only integer values in the text fields!"
    sg.theme('Dark Gray 13')
    layout_col = [[sg.Text(text, font=("Helvetica", "10", "bold"), text_color="red", justification="center")],
                  [sg.Button("OK", font=("Helvetica", "10", "bold"), border_width=0)]]
    layout = [[sg.Column(layout_col, element_justification="center")]]
    window = sg.Window('Error', layout, finalize=True, resizable=True, auto_size_text=True,
                       auto_size_buttons=True, no_titlebar=True, grab_anywhere=True, keep_on_top=True)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'OK'):
            window.close()
            break
    return event, values


def progress_bar_meter(counter):
    """
    Standard build-in progress meter from PySimpleGUI package customized in order to change the appearance a bit.
    :param counter: The current iteration in the loop
    :return: True/False
    """
    sg.theme('Dark Gray 13')

    if selected_lang == "":
        return sg.one_line_progress_meter('Scraping numerals...', counter + 1, len(lst_of_links),
                                          'Scraping numerals...', orientation='h', no_titlebar=False,
                                          grab_anywhere=True, border_width=0)
    else:
        return sg.one_line_progress_meter('Scraping numerals...', counter + 1, len(range(start, end, step)),
                                          'Scraping numerals...', orientation='h', no_titlebar=False,
                                          grab_anywhere=True, border_width=0)


if __name__ == '__main__':
    events, values = create_main_window()
    start = int(values[0])
    end = int(values[1])
    step = int(values[2])
    file_path = values[3]
    selected_lang = str(values["inputtxt"])
    is_alllang = values["-CB-"]
    retries = 0

    start_time = time.time()  # log execution time of script

    while retries < MAX_RETRIES_REQ:
        try:
            # 3.05 because of TCP retransmission windows https://2.python-requests.org/en/master/user/advanced/#timeouts
            page = requests.get('https://www.languagesandnumbers.com/site-map/en/', headers=HEADERS,
                                timeout=REQ_TIMEOUT)
            page.raise_for_status()  # raises error if status code is between 400-600
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout,
                requests.exceptions.RequestException) as e:
            logging.error('1 Error: %s', e)
            logging.info("Trying again...")
            retries += 1
            if isinstance(e, requests.exceptions.ConnectionError):
                time.sleep(3)  # replugging ethernet cable is slow
        else:
            break
    else:
        sg.SystemTray.notify("Too many retries", "Closing program...", display_duration_in_ms=750,
                             fade_in_duration=100, icon=ICON_WARNING)
        logging.info('Reached max retries, closing program.')
        sys.exit(1)

    main_link = 'https://www.languagesandnumbers.com/'

    sg.SystemTray.notify('Started Script', 'Scraping languagesandnumbers.com...', display_duration_in_ms=750,
                         fade_in_duration=0)

    lst_of_links = []
    lst_of_words = ""

    parse_save_website(page, lst_of_links, sel_lang=selected_lang)

    count = 0
    count_inner = 0
    retries = 0

    for link in lst_of_links:
        page = requests.get(main_link + link, headers=HEADERS)
        soup = BeautifulSoup(page.content, features="lxml",
                             parse_only=SoupStrainer(id='number-form'))
        form = soup.find_all(id='number-form')

        lang = find_lang_short(link)
        if not form:
            logging.warning(
                'No form available for %s (%s): Skipping invisible submit-form in order to avoid scrape detection.',
                str(lang), str(find_lang_long(link)))
            # lst_of_words = lst_of_words + find_lang_long(link) + ";" + '-1' + ";" + "Language not supported.\n"
            continue
        if selected_lang == "" and not progress_bar_meter(count):
            logging.info(
                'Process cancelled by clicking cancel button for link %s.', str(link))
            sg.SystemTray.notify("Cancelled", "Closing program...", display_duration_in_ms=750, fade_in_duration=50,
                                 icon=ICON_CANCEL)
            sys.exit(1)

        for i in range(start, end, step):
            # POST method is not working on the ajax server with numbers > 12
            if lang == 'pld' and i > 12:
                logging.warning("POSTING HTTP to ajax server is not supported for %s with values larger than 12.",
                                str(lang))
                continue
            if selected_lang != "" and not progress_bar_meter(count_inner):
                logging.info(
                    'Progress cancelled (inner) for i=%s and link=%s', str(i), str(link))
                sg.SystemTray.notify("Cancelled", "Closing program...", display_duration_in_ms=750,
                                     fade_in_duration=100, icon=ICON_CANCEL)
                sys.exit(1)
            # requests.Session uses single TCP-connection for sending/receiving HTTP multi reqs/resps
            # saves time over opening a new connection for every single req/resp pair, see
            # https://en.wikipedia.org/wiki/HTTP_persistent_connection
            with requests.Session() as session:
                while retries < MAX_RETRIES_REQ:
                    try:
                        # post to server with params for language and number and extract response
                        response = session.post('https://www.languagesandnumbers.com/ajax/en', headers=HEADERS,
                                                timeout=REQ_TIMEOUT,
                                                data={"numberz": i, "lang": lang})
                        logging.info('POST method - params: {numberz: %s, lang: %s (%s)}', str(i), str(lang),
                                     str(find_lang_long(link)))

                        # sleep between 1 and 3 seconds to avoid server timeouts
                        time.sleep(random.uniform(1, 3))

                        response.raise_for_status()
                    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout) as err:
                        logging.error(
                            "Error while retrieving response of %s: %s", str(lang), err)
                        logging.info("Trying again...")
                        retries += 1
                        if isinstance(err, requests.exceptions.ConnectionError):
                            time.sleep(3)  # replugging ethernet cable is slow
                    except requests.exceptions.RequestException as err:
                        logging.error(
                            "UnspecifiedError while retrieving response of %s: %s", str(lang), err)
                        logging.info("Trying again...")
                        retries += 1
                    else:
                        break
                else:
                    logging.info('Too many retries while trying to post query i=%s and link=%s', str(i),
                                 str(link))
                    sg.SystemTray.notify("Too many retries", "Closing program...", display_duration_in_ms=750,
                                         fade_in_duration=100, icon=ICON_WARNING)
                    sys.exit(1)

                # parse response
                soup = BeautifulSoup(
                    response.content, "lxml", from_encoding="utf-8")

                # if number is not supported by server, ignore it
                # soup.get_text().split(':')[-1].split('.')[0] == "This number is too big":
                if soup.get_text().split(':', 3)[-1].split('.')[0] == "This number is too big":
                    logging.warning("Not supported. This number is too big. (Lang: %s (%s))", str(lang),
                                    str(find_lang_long(link)))
                    # lst_of_words = lst_of_words + find_lang_long(link) + ";" + str(
                    #    i) + ";" + "Not supported, number too big.\n"
                    break
                else:
                    # soup.get_text(separator=" ", strip=True).split(':', 3)[-1]
                    lst_of_words = lst_of_words + find_lang_long(link) + ";" + str(i) + ";" + \
                        soup.get_text(separator=" ", strip=True).split(
                            ':', 3)[-1] + "\n"
            count_inner += 1
        count += 1
    alt_path = ""
    retries = 0
    while retries < MAX_RETRIES_REQ:
        try:
            if retries >= 1:
                write_csv(lst_of_words, alt_path)
            elif retries == 0:
                write_csv(lst_of_words, file_path)
        except OSError as erro:
            logging.error("Could not write to file: %s", erro)

            sg.theme('Dark Gray 13')
            alt_path = sg.popup_get_folder("Error: Please enter a different folder name", no_titlebar=False,
                                           grab_anywhere=True, keep_on_top=True)
            logging.info("Trying again...")
            retries += 1

            if alt_path is None or "":
                logging.info("Cancelled operation, closing program.")
                sg.SystemTray.notify("Cancelled", "Closing program...", display_duration_in_ms=750,
                                     fade_in_duration=100, icon=ICON_CANCEL)
                sys.exit(1)
        else:
            break
    else:
        logging.warning(
            "Max retries reached while trying to write .csv file, closing program.")
        sg.SystemTray.notify("Max retries reached", "Closing program...", display_duration_in_ms=750,
                             fade_in_duration=100, icon=ICON_WARNING)
        sys.exit(1)

    seconds = time.time() - start_time

    logging.info("Program executed in %s", time.strftime(
        "%H:%M:%S (hh:mm:ss)", time.gmtime(seconds)))
    sg.SystemTray.notify("Finished",
                         str("Program executed in " +
                             time.strftime("%H:%M:%S (hh:mm:ss)", time.gmtime(seconds))),
                         display_duration_in_ms=750, fade_in_duration=100)
