import PySimpleGUI as sg
from bs4 import BeautifulSoup as bs
import requests


def get_weather(location):
	USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
	url = f'https://www.google.com/search?q=weather+{location.replace(" ","")}'
	session = requests.Session()
	session.headers['User-Agent'] = USER_AGENT
	html = session.get(url)
	
	soup = bs(html.text, "html.parser")
	time = soup.find("div", attrs={'id': 'wob_dts'}).text
	weather = soup.find("span", attrs={'id': 'wob_dc'}).text
	temp = soup.find("span", attrs={'id': 'wob_tm'}).text
     
	return time, weather, temp


sg.theme("DarkBlack")
sg.set_options(font="Georgia 12")

layout = [
    [
        sg.Input(key="-INPUT-"),
        sg.Button("Search", key="-SEARCH-"),
        sg.Button("Clear", key="-CLEAR-")
    ],
    [
        sg.Text(
            "Temperature", 
            font="Georgia 30",
            key="-TEMP-", 
            visible=False, 
            expand_x=True, 
            justification="center", 
            pad=10
        )
    ],
    [
        sg.Text(
            "Weather", 
            font="Georgia 28", 
            key="-WEATHER-",
            visible=False, 
            expand_x=True, 
            justification="center", 
            pad=10
        )
    ],
    [
        sg.Text(
            "Time", 
            font="Georgia 20", 
            key="-TIME-", 
            visible=False, 
            expand_x=True, 
            justification="center", 
            pad=10
        )
    ]
]

window = sg.Window("Weather", layout, size=(630,300))

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == "-SEARCH-":
        time, weather, temp = get_weather(values["-INPUT-"])
        temp = f"{temp} °C"
        window["-TEMP-"].update(temp, visible=True)
        window["-WEATHER-"].update(weather, visible=True)
        window["-TIME-"].update(time, visible=True)
        
    
    if event == "-CLEAR-":
        window["-INPUT-"].update("")
        window["-TEMP-"].update(visible=False)
        window["-WEATHER-"].update(visible=False)
        window["-TIME-"].update(visible=False)
        
    
window.close()
