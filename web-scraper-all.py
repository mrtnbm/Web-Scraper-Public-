import os
import sys
import time

import PySimpleGUI as sg  # code convention, see PySimpleGUI docs
import requests
from bs4 import BeautifulSoup, SoupStrainer

CURRENT_WORKING_DIR = os.path.abspath(os.getcwd())
MAX_RETRIES_REQ = 10
print = sg.Print


def parse_save_website(website_page, sel_lang=""):
    """
    Parses HTML with lxml (faster than html.parser,
    see https://www.crummy.com/software/BeautifulSoup/bs4/doc/#improving-performance) and only saves a tags into a
    list
    :param sel_lang: selected language if not all get scraped
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
            sg.SystemTray.notify("Language not listed on website", "Closing program...", display_duration_in_ms=1000,
                                 fade_in_duration=200)


def write_csv(string, path):
    """
    Writes string to csv file in root directory
    :param path: Desired file-path
    :param string: String containing all numerals in csv style
    :return: None
    """
    filename = 'dataset.csv'
    full_path = os.path.join(path, filename)
    with open(full_path, 'w', newline='', encoding='utf-8-sig') as f:  # utf-8-sig forces Excel to open file with uft-8
        f.write("lang;number;numeral\n")  # header
        f.write(string)


def find_lang_short(list_item):
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


def progress_bar(counter):
    """
    [Not used, headless mode only]
    Prints out progress bar in cmd.
    :param counter: Amount of links already processed
    :return: String
    """
    return print(end="\r" + "░" * 81 + "┃\r┃" + "█" * int(80 * counter / (len(lst_of_links) - 1)) + "%6.2f %%" % (
            counter / (len(lst_of_links) - 1) * 100))


def collapse(layout, key, visible):
    """
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
    :param layout: The layout for the section
    :param key: Key used to make this section visible / invisible
    :param visible: visible determines if section is rendered visible or invisible on initialization
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
                  [sg.InputText(default_text="German", text_color="lightgray",
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
              [sg.InputText(default_text=os.path.join('C', 'users', os.getlogin(), 'Documents'), text_color="lightgray",
                            tooltip="Enter desired path for the csv-file!", border_width=0), sg.FolderBrowse()],
              [collapse(hidden_sec, 'hidden_sec', True)],
              [sg.Checkbox(text="Scrape all languages", default=False, key='-CB-', enable_events=True)],
              [sg.Button("OK", font=("Helvetica", "10", "bold"), border_width=0), sg.Button("Exit", border_width=0)]]

    window = sg.Window('Web-Scraper', layout, finalize=True, resizable=True, auto_size_text=True,
                       auto_size_buttons=True, no_titlebar=True, grab_anywhere=True, keep_on_top=True)

    toggle_sec1 = True

    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            window.close()
            sys.exit(1)
        if event == "-CB-":
            toggle_sec1 = not toggle_sec1
            window['hidden_sec'].update(visible=toggle_sec1)
        if event == "OK":
            window.close()
            while True:
                try:
                    int(values[0])
                    int(values[1])
                    int(values[2])
                except ValueError as eval:
                    print("Values contains non integer values.:", eval)
                    sg.theme('Dark Gray 13')
                    alt_values = sg.popup_get_text(
                        "Error: Values contains non integer values. Please enter integer values:", default_text="1,2,1",
                        no_titlebar=True, keep_on_top=True, grab_anywhere=True)
                    if (values[0] or values[1] or values[2] or (
                            not is_alllang and values["inputtxt"])) is None or "" or alt_values is None:
                        sg.SystemTray.notify("Cancelled", "Closing program...", display_duration_in_ms=1000,
                                             fade_in_duration=200)
                        sys.exit(1)

                    try:
                        alt_values_split = alt_values.split(",")
                        values[0] = alt_values_split[0]
                        values[1] = alt_values_split[1]
                        values[2] = alt_values_split[2]
                        if not is_alllang:
                            values[4] = alt_values_split[4]
                    except IndexError as erri:
                        sg.SystemTray.notify("Too many retries", "Closing program...", display_duration_in_ms=1000,
                                             fade_in_duration=200)
                        print("Index error:", erri)
                        sys.exit(1)
                else:
                    break

            return event, values


def progress_bar_meter(counter):
    sg.theme('Dark Gray 13')
    if selected_lang == "":
        return sg.one_line_progress_meter('Scraping numerals...', counter + 1, len(lst_of_links), 'Scraping numerals...',
                                      key='key', no_button=True, orientation='h', no_titlebar=True, grab_anywhere=True,
                                      keep_on_top=True)
    else:
        return sg.one_line_progress_meter('Scraping numerals...', counter + 1, len(range(start, end, step)), 'Scraping numerals...',
                                          key='key', no_button=True, orientation='h', no_titlebar=True,
                                          grab_anywhere=True,
                                          keep_on_top=True)


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

    while True:
        if retries > MAX_RETRIES_REQ:
            sg.SystemTray.notify("Too many retries", "Closing program...", display_duration_in_ms=1000,
                                 fade_in_duration=200)
            sys.exit(1)
        try:
            # 3.05 because of TCP retransmission windows https://2.python-requests.org/en/master/user/advanced/#timeouts
            page = requests.get('https://www.languagesandnumbers.com/site-map/en/', timeout=3.05)
            page.raise_for_status()  # raises error if status code is between 400-600
        except requests.exceptions.HTTPError as errh:  # handling server error codes
            print("HTTP error: ", errh)
            print("Trying again...")
            retries += 1
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting: ", errc)
            print("Trying again...")
            retries += 1
        except requests.exceptions.Timeout as errt:
            print("Timeout Error: ", errt)
            print("Trying again...")
            retries += 1
        except requests.exceptions.RequestException as err:  # safety-net for any unspecified exception
            print("Unspecified error: ", err)
            print("Trying again...")
            retries += 1
        else:
            break

    main_link = 'https://www.languagesandnumbers.com/'

    sg.SystemTray.notify('Started Script', 'Scraping languagesandnumbers.com...', display_duration_in_ms=1000,
                         fade_in_duration=0)

    lst_of_links = []
    lst_of_words = ""

    parse_save_website(page, sel_lang=selected_lang)

    count = 0
    count_inner = 0
    retries = 0
    for link in lst_of_links:
        if selected_lang == "":
            progress_bar_meter(count)
        lang = find_lang_short(link)

        for i in range(start, end, step):
            if not selected_lang == "":
                progress_bar_meter(count_inner)
            # requests.Session uses single TCP-connection for sending/receiving HTTP multi reqs/resps
            # saves time over opening a new connection for every single req/resp pair, see
            # https://en.wikipedia.org/wiki/HTTP_persistent_connection
            with requests.Session() as session:
                if lang == "kor":  # korean is not supported
                    continue
                else:
                    while True:
                        if retries > MAX_RETRIES_REQ:
                            sg.SystemTray.notify("Too many retries", "Closing program...", display_duration_in_ms=1000,
                                                 fade_in_duration=200)
                            sys.exit(1)
                        try:
                            # post to server with params for language and number and extract response
                            response = session.post('https://www.languagesandnumbers.com/ajax/en', timeout=3.05,
                                                    data={"numberz": i, "lang": lang})
                            response.raise_for_status()
                        except requests.exceptions.HTTPError as errh:
                            print("HTTP error: ", errh)
                            print("Trying again...")
                            retries += 1
                        except requests.exceptions.ConnectionError as errc:
                            print("Error Connecting: ", errc)
                            print("Trying again...")
                            retries += 1
                            time.sleep(3)  # replugging ethernet cable is slow
                        except requests.exceptions.Timeout as errt:
                            print("Timeout Error: ", errt)
                            print("Trying again...")
                            retries += 1
                        except requests.exceptions.RequestException as err:
                            print("Unspecified error: ", err)
                            print("Trying again...")
                            retries += 1
                        else:
                            break

                    # parse response
                    soup = BeautifulSoup(response.content, "lxml", from_encoding="utf-8")

                    # if number is not supported by server, mark row with XYZ for later filtering (dirty)
                    if soup.get_text().split(':')[-1] == "This number is too big":
                        lst_of_words = lst_of_words + find_lang_long(link) + ";" + str(i) + ";" + "XYZ\n"
                    else:
                        lst_of_words = lst_of_words + find_lang_long(link) + ";" + str(i) + ";" + \
                                       soup.get_text(separator=" ", strip=True).split(':')[-1] + "\n"
            count_inner += 1
        count += 1
    alt_path = ""
    retries = 0
    while True:
        try:
            if retries >= 1:
                write_csv(lst_of_words, alt_path)
            elif retries == 0:
                write_csv(lst_of_words, file_path)
            elif retries > MAX_RETRIES_REQ:
                sg.SystemTray.notify("Max retries reached", "Closing program...", display_duration_in_ms=1000,
                                     fade_in_duration=200)
                sys.exit(1)
        except OSError as erro:
            print("Couldn't write to file: ", erro)

            sg.theme('Dark Gray 13')
            alt_path = sg.popup_get_folder("Error: Please enter a different folder name", no_titlebar=True,
                                           grab_anywhere=True, keep_on_top=True)
            print("Trying again...")
            retries += 1

            if alt_path is None or "":
                sg.SystemTray.notify("Cancel", "Closing program...", display_duration_in_ms=1000, fade_in_duration=200)
                sys.exit(1)
        else:
            break

    seconds = time.time() - start_time

    sg.SystemTray.notify("Finished",
                         str("Program executed in " + time.strftime("%H:%M:%S (hh:mm:ss)", time.gmtime(seconds))))
