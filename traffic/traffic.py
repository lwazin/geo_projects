# Function to clean up the code

def get_traffic():
    # Importing packages
    import pandas as pd
    from bs4 import BeautifulSoup as bs4
    import requests

    def help(data):
        unwanted = ['\r', '\n', '\xa0']
        for i in unwanted:
            data = data.replace(i, ' ')

        count = 0
        for i in data:
            if i.isalnum() == True:
                data = data[count:]
                break
            else:
                count += 1
        return data

    def clean_desc(data):
        return help(help(data)[::-1])[::-1]

    prov = input('Choose a province..\n\n 1) Eastern Cape,\n 2) Free State,\n 3) Gauteng,\n 4) KwaZulu-Natal,\n 5) Limpopo,\n 6) Mpumalanga,\n 7) North West,\n 8) Northern Cape,\n 9) Western Cape')
    province = {'1': 'Eastern_Cape', '2': 'Free_State', '3': 'Gauteng', '4': 'KwaZulu-Natal', '5': 'Limpopo', '6': 'Mpumalanga', '7': 'North_West', '8': 'Northern_Cape', '9': 'Western_Cape'}

    request = requests.get('https://m.news24.com/Traffic/'+province[prov])
    page = request.content
    soup = bs4(page)
    len(soup.find_all('li', "item clr"))

    df = pd.DataFrame()
    for i in range(len(soup.find_all('li', "item clr"))):
        data = {'location':soup.find_all('li', "item clr")[i].find_all('span', 'location_name')[0].text,
        'timestamp':soup.find_all('li', "item clr")[i].find_all('span', 'timestamp')[0].text,
        'description':clean_desc(soup.find_all('li', "item clr")[i].find_all('span', 'description')[0].text).split(' : ')[-1].split(' - ')[1],
        'reason':clean_desc(soup.find_all('li', "item clr")[i].find_all('span', 'description')[0].text).split(' : ')[-1].split(' - ')[0],
        'situation':clean_desc(soup.find_all('li', "item clr")[i].find_all('span', 'description')[0].text).split(' : ')[-1].split(' - ')[-1],
        'area':clean_desc(soup.find_all('li', "item clr")[i].find_all('span', 'description')[0].text).split(' : ')[0],
        'direction': clean_desc(soup.find_all('li', "item clr")[i].find_all('span', 'description')[0].text).split(' : ')[1]}
        if len(df) == 0:
            df = pd.DataFrame([data])
        else:
            df = df.append(pd.DataFrame([data]))

    df.index = range(len(df))
    for i in df.index:
        if len(df.direction[i].split(' ')) != 1:
            df.direction[i] = 'Direction Unknown'
        if df.situation[i] == df.description[i]:
            df.situation[i] = 'Situation Unknown'

    if len(df) == 0:
        return print('No data available at this time!')
    else:
        return df


get_traffic()
