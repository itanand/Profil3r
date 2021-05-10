import requests
from bs4 import BeautifulSoup
import time

class Pastebin:

    def __init__(self, config, permutations_list):
        # 1000 ms
        self.delay = config['plateform']['pastebin']['rate_limit'] / 1000
        # https://pastebin.com/u/{username}
        self.format = config['plateform']['pastebin']['format']
        self.permutations_list = permutations_list
        # programming
        self.type = config['plateform']['pastebin']['type']

    # Generate all potential pastebin usernames
    def possible_usernames(self):
        possible_usernames = []

        for permutation in self.permutations_list:
            possible_usernames.append(self.format.format(
                permutation = permutation,
            ))
        return possible_usernames

    def search(self):
        pastebin_usernames = {
            "type": self.type,
            "accounts": []
        }
        possible_usernames_list = self.possible_usernames()

        for username in possible_usernames_list:
            try:
                r = requests.get(username)
            except requests.ConnectionError:
                print("failed to connect to pastebin")
            
            # If the account exists
            if r.status_code == 200: 
                # Parse HTML response content with beautiful soup 
                soup = BeautifulSoup(r.text, 'html.parser')
                
                # Scrape the user informations
                try:
                    user_profile_views = str(soup.find_all(class_='views')[0].get_text()) or None
                    user_pastes_views = str(soup.find_all(class_='views')[1].get_text()) or None
                    user_profile_creation_date = str(soup.find_all(class_='date-text')[0].get_text()) or None
                except:
                    pass

                # Scrape the user pastes
                user_pastes = []

                try:
                    pastes = soup.find_all(class_='maintable')[0].find_all('tr')

                    for paste in pastes[1:]:
                        columns = paste.find_all('td')

                        user_pastes.append({
                            "name": str(columns[0].get_text().strip()),
                            "added": str(columns[1].get_text().strip()),
                            "expires": str(columns[2].get_text().strip()),
                            "hits": str(columns[3].get_text().strip()),
                            "syntax": str(columns[4].get_text().strip())
                        })
                except:
                    pass
                
                # Append all the informations to the account table
                pastebin_usernames["accounts"].append({"value": username, 
                                                       "profile_views": user_profile_views,
                                                       "pastes_views" : user_pastes_views,
                                                       "profile_creation_date": user_profile_creation_date,
                                                       "user_pastes": user_pastes
                                                      })
            time.sleep(self.delay)
        
        return pastebin_usernames