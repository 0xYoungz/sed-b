import requests
from colorama import init, Fore, Style
import os
import sys
import time
import datetime

init(autoreset=True)


def msg():
    print(r"""

███████╗███████╗███████╗██████╗               ██████╗  ██████╗ ████████╗
██╔════╝██╔════╝██╔════╝██╔══██╗              ██╔══██╗██╔═══██╗╚══██╔══╝
███████╗█████╗  █████╗  ██║  ██║    █████╗    ██████╔╝██║   ██║   ██║   
╚════██║██╔══╝  ██╔══╝  ██║  ██║    ╚════╝    ██╔══██╗██║   ██║   ██║   
███████║███████╗███████╗██████╔╝              ██████╔╝╚██████╔╝   ██║   
╚══════╝╚══════╝╚══════╝╚═════╝               ╚═════╝  ╚═════╝    ╚═╝   
                                                                        
""")

garis = "×" * 20
garis2 = "•" * 27


def msg2():
    print(f"{Fore.CYAN+Style.BRIGHT} {garis2}\n By : 0xYoungz\n {garis2}\n auto claim ✅\n auto clear tasks ✅\n {garis2}")


# URLs
url_get_profile = 'https://elb.seeddao.org/api/v1/profile'
url_balance = 'https://elb.seeddao.org/api/v1/profile/balance'
url_bonus = 'https://elb.seeddao.org/api/v1/login-bonuses'
url_claim = 'https://elb.seeddao.org/api/v1/seed/claim'

# Headers
headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-ID,en-US;q=0.9,en;q=0.8,id;q=0.7',
    'content-length': '0',
    'dnt': '1',
    'origin': 'https://cf.seeddao.org',
    'priority': 'u=1, i',
    'referer': 'https://cf.seeddao.org/',
    'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'telegram-data': 'tokens',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

def load_credentials():
    # Read tokens from file and return as a list
    try:
        with open('query.txt', 'r') as file:
            tokens = file.read().strip().split('\n')
        return tokens
    except FileNotFoundError:
        print("File tokens.txt tidak ditemukan.")
        return []
    except Exception as e:
        print("Terjadi kesalahan saat memuat token:", str(e))
        return []

def get_profile():
    response = requests.get(url_get_profile, headers=headers)
    if response.status_code == 200:
        data_profil = response.json()
        name = data_profil['data']['name']
        print(f"{Fore.GREEN+Style.BRIGHT}{garis} Login Akun : {name} {garis}\n")
        return data_profil
    else:
        print(f"{Fore.RED+Style.BRIGHT}Failed to get profile : {response.status_code}")
        return None

def balance():
    response = requests.get(url_balance, headers=headers)
    if response.status_code == 200:
        data_balance = response.json()
        print(f"{Fore.YELLOW+Style.BRIGHT}Akun Balance : {data_balance['data'] / 1000000000}")
        return True
    else:
        print(f"{Fore.RED+Style.BRIGHT}Error : {response.json()}")
        return False

def bonus_login():
    response = requests.get(url_bonus, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data.get('data'), list) and data['data']:
            day = data['data'][0].get('no', '')
            print(f"{Fore.CYAN+Style.BRIGHT}claim bonus daily : Berhasil claim | day {day}")
        else:
            print("Data format not expected")
    else:
        data = response.json()
        if data.get('message') == 'already claimed for today':
            print("bonus login sudah diclaim")
        else:
            print(f"Gagal claim : {data}")

def tugas():
    response = requests.get('https://elb.seeddao.org/api/v1/tasks/progresses', headers=headers)
    tasks = response.json()['data']
    
    for task in tasks:
        if task['task_user'] is None or not task['task_user']['completed']:
            complete_task(task['id'], task['name'])

def complete_task(task_id, task_name):
    response = requests.post(f'https://elb.seeddao.org/api/v1/tasks/{task_id}', headers=headers)
    if response.status_code == 200:
        print(f"{Fore.GREEN+Style.BRIGHT}Tugas : {task_name} berhasil..")
    else:
        print(f"Failed : Gagal Menyelesaikan Tugas {task_name} | code | {response.status_code}")


def countdown_timer(seconds):
    animation = "....."
    for i in range(seconds, 0, -1):
        sys.stdout.write(f"\r{Fore.YELLOW+Style.BRIGHT}Done. Tunggu {i} detik {animation[:i % len(animation)]}   ")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\r" + " " * 50)


def main():
    tokens = load_credentials()
    
    confirm_tugas = input("Ingin Auto Clear Taks (y/n) : ")
    
    
    os.system('clear')
    msg()
    msg2()
    
    while True:
        
        for index, token in enumerate(tokens):
            headers['telegram-data'] = token
            info = get_profile()
            if info:
                print(f"{Fore.GREEN+Style.BRIGHT}Memuat akun {info['data']['name']}")
                
            if balance():
                response = requests.post(url_claim, headers=headers)
                
                if response.status_code == 200:
                    print(f"Claim : Berhasil claim mining..")
                elif response.status_code == 400:
                    response_data = response.json()
                    print(f"{Fore.MAGENTA+Style.BRIGHT}Claim : Belum waktunya claim!!")
                else:
                    print(f"[-] Error | code | {response.status_code}")
                
                bonus_login()
                
                if confirm_tugas.lower() == 'y':
                    tugas()
                
                
                countdown_timer(30)
                print()

if __name__ == "__main__":
    main()