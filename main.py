import PySimpleGUI as sg
from bs4 import BeautifulSoup as bs
import requests


def get_weather(location):
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    url = f'https://www.google.com/search?q=weather+{location.replace(" ","")}'
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    
    try:
        html = session.get(url)
        soup = bs(html.text, "html.parser")        
        loc = soup.find("span", attrs={'class': 'BBwThe'}).text
        time = soup.find("div", attrs={'id': 'wob_dts'}).text
        weather = soup.find("span", attrs={'id': 'wob_dc'}).text
        temp = soup.find("span", attrs={'id': 'wob_tm'}).text
        return loc, time, weather, temp

    except:
        return None, None, None, None  


def clear():
    window["-INPUT-"].update("")
    window["-LOC-"].update(visible=False)
    window["-TEMP-"].update(visible=False)
    window["-WEATHER-"].update(visible=False)
    window["-TIME-"].update(visible=False)


sg.theme("DarkBlack")
sg.set_options(font="Georgia 12")

layout = [
    [
        sg.Input(key="-INPUT-", pad=(20,10)),
        sg.Button("Search", key="-SEARCH-", pad=(5,10), expand_x=True),
        sg.Button("Clear", key="-CLEAR-", pad=(5,10), expand_x=True)
    ],
    [
        sg.Text(
            "", 
            font="Georgia 30",
            key="-LOC-", 
            visible=False, 
            expand_x=True, 
            justification="center", 
            pad=10
        )
    ],
    [
        sg.Text(
            "", 
            font="Georgia 28",
            key="-TEMP-", 
            visible=False, 
            expand_x=True, 
            justification="center", 
            pad=10
        )
    ],
    [
        sg.Text(
            "", 
            font="Georgia 26", 
            key="-WEATHER-",
            visible=False, 
            expand_x=True, 
            justification="center", 
            pad=10
        )
    ],
    [
        sg.Text(
            "", 
            font="Georgia 20", 
            key="-TIME-", 
            visible=False, 
            expand_x=True, 
            justification="center", 
            pad=10
        )
    ]
]

window = sg.Window("Weather", layout, size=(700,370))

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == "-SEARCH-":
        loc, time, weather, temp = get_weather(values["-INPUT-"])

        if loc != None and time != None and weather != None and temp != None:
            temp = f"{temp} °C"
            window["-LOC-"].update(loc, visible=True)
            window["-TEMP-"].update(temp, visible=True)
            window["-WEATHER-"].update(weather, visible=True)
            window["-TIME-"].update(time, visible=True)
        else:
            clear()

    if event == "-CLEAR-":
        clear()
        
window.close()
