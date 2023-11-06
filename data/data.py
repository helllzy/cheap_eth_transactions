from json import load

from loguru import logger

from config import MODULES, EXTRA_MODULES, USE_PROXY


with open('data/priv.txt') as file:
    KEYS = [i.strip() for i in file.readlines()]

if len(KEYS) < 1:
    logger.critical("You didn`t add wallets in priv.txt!")
    exit()

with open('data/trans_addresses.txt') as file:
    TRANS_ADDRESSES = [i.strip() for i in file.readlines()]

WALLETS = {}

for _id in range(len(KEYS)):
    WALLETS[str(_id+1)] = {"private_key": KEYS[_id]}

    if USE_PROXY:
        with open('data/proxies.txt') as file:
            PROXIES = [i.strip() for i in file.readlines()]

        if len(KEYS) > len(PROXIES):
            logger.critical('Number of wallets isn`t equal to number of proxies')
            exit()

        WALLETS[str(_id+1)]["proxy"] = PROXIES[_id]

    if 'transfer' in MODULES+EXTRA_MODULES:
        WALLETS[str(_id+1)]["trans_addr"] = TRANS_ADDRESSES[_id]

with open('data/abi/blur.json') as file:
    BLUR_ABI = load(file)

with open('data/abi/bungee.json') as file:
    BUNGEE_ABI = load(file)

DNA_ADDRESS = 0x932261f9Fc8DA46C4a22e31B45c4De60623848bF
BLUR_ADDRESS = '0x0000000000A39bb272e79075ade125fd351887Ac'
BUNGEE_ADDRESS = 0xb584D4bE1A5470CA1a8778E9B86c81e165204599

HELZY = [
'''
 .----------------.  .----------------.  .----------------.  .----------------.  .----------------. 
| .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
| |  ____  ____  | || |  _________   | || |   _____      | || |   ________   | || |  ____  ____  | |
| | |_   ||   _| | || | |_   ___  |  | || |  |_   _|     | || |  |  __   _|  | || | |_  _||_  _| | |
| |   | |__| |   | || |   | |_  \_|  | || |    | |       | || |  |_/  / /    | || |   \ \  / /   | |
| |   |  __  |   | || |   |  _|  _   | || |    | |   _   | || |     .'.' _   | || |    \ \/ /    | |
| |  _| |  | |_  | || |  _| |___/ |  | || |   _| |__/ |  | || |   _/ /__/ |  | || |    _|  |_    | |
| | |____||____| | || | |_________|  | || |  |________|  | || |  |________|  | || |   |______|   | |
| |              | || |              | || |              | || |              | || |              | |
| '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
 '----------------'  '----------------'  '----------------'  '----------------'  '----------------' 
''',
'''
 █████   █████ ██████████ █████       ███████████ █████ █████
░░███   ░░███ ░░███░░░░░█░░███       ░█░░░░░░███ ░░███ ░░███ 
 ░███    ░███  ░███  █ ░  ░███       ░     ███░   ░░███ ███  
 ░███████████  ░██████    ░███            ███      ░░█████   
 ░███░░░░░███  ░███░░█    ░███           ███        ░░███    
 ░███    ░███  ░███ ░   █ ░███      █  ████     █    ░███    
 █████   █████ ██████████ ███████████ ███████████    █████   
░░░░░   ░░░░░ ░░░░░░░░░░ ░░░░░░░░░░░ ░░░░░░░░░░░    ░░░░░    
''',
]
