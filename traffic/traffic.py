def get_traffic():

    # Importing packages
    import pandas as pd
    from bs4 import BeautifulSoup as bs4
    import requests

    # Functions which will be used later on in the program
    def help(data): # This function cleans up our description, which initially has escape characters
        unwanted = ['\r', '\n', '\xa0'] # Escape character list
        for i in unwanted: # Cleaning for-loop, replacing escape characters with spaces
            data = data.replace(i, ' ')

        count = 0 # This will count the character 'list' position
        for i in data: # We will be removing unnecessary spaces in the description
            if i.isalnum() == True: # When this loop find it's first actual character,
                data = data[count:] # It will start the whole description from that position..
                break # and stop the loop from carrying on.
            else:
                count += 1 # If the above is not satisfied, it will add 1 to the count!
        return data # Returns the clean description!

    # (Spaces from the beginning are gone, spaces at the end are still there!)

    def clean_desc(data): # This funtion is the main cleaner
        return help(help(data)[::-1])[::-1] # first removes the spaces before the description and then reverses the string to remove the spaces at the back of the string.. then reverses it back to a readable state!

    # This is the final DataFrame we return!
    final = pd.DataFrame()

    # A dictionary of all provinces, without spaces.. compatible with our urls.
    province = {'1': 'Eastern_Cape', '2': 'Free_State', '3': 'Gauteng', '4': 'KwaZulu-Natal', '5': 'Limpopo', '6': 'Mpumalanga', '7': 'North_West', '8': 'Northern_Cape', '9': 'Western_Cape'}

    # A request for the user to input the province they want a traffic report on.
    prov = input('Choose a province..\n\n 1) Eastern Cape,\n 2) Free State,\n 3) Gauteng,\n 4) KwaZulu-Natal,\n 5) Limpopo,\n 6) Mpumalanga,\n 7) North West,\n 8) Northern Cape,\n 9) Western Cape')

    # Initial scraping of the webpage, mainly to get the number of pages available for the chosen province
    request = requests.get('https://m.news24.com/Traffic/'+province[prov])
    page = request.content
    soup = bs4(page)
    if len(soup.find_all('div', {"class": 'pageing_wrap'})) == 0:
        pages = 1
    else:
        pages = int(soup.find_all('div', {"class": 'pageing_wrap'})[0].find_all('div')[0].text.split(' ')[-1])

    # The cool part.. a for-loop that collects data from each page of a specific province. Adds Dataframe information of all pages to one Dataframe, (final)
    for i in range(1,pages+1):

        # The dataframe that feeds into the Dataframe above, final!
        df = pd.DataFrame()

        # Requesting the page's HTML and preparing it for BS$
        request = requests.get('https://m.news24.com/Traffic/'+province[prov]+'/'+str(1))
        page = request.content
        soup = bs4(page)

        # Finding all data needed to populate our DataFrame, features of high value.
        for i in range(len(soup.find_all('li', "item clr"))):
            # Creating a dictionary of gathered data.
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

        df.index = range(len(df)) # The DataFrame has an index of zeros, this line turns the index into 0, 1, 2, 3.. etc!

        # Finding unknown data and labeling it accordingly!
        for i in df.index:
            if len(df.direction[i].split(' ')) != 1:
                df.direction[i] = 'Direction Unknown'
            if df.situation[i] == df.description[i]:
                df.situation[i] = 'Situation Unknown'

        #  As commented above, Dataframe 'df' is fed into DataFrame 'final'
        final = final.append(df)

    # Fixing index of 'final'
    final.index = range(len(final))

    # Returning the appropriate output..
    if len(final) == 0:
        return print('No data available at this time!')
    else:
        return final

# Running the function
get_traffic()

# All data credited to News24 Traffic website.
