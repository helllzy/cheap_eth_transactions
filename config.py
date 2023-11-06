# all transactions will be processed below this gas
MAX_GWEI = 55

ACCS_DELAY = [200, 400]

# delay between each module
ACTIONS_DELAY = [30, 100]

RANDOMIZE_WALLETS = True

# True if you added proxies in proxies.txt
USE_PROXY = True

# how many retries do you want for each module
# works only if transaction was rejected
RETRIES_COUNT = 1

# if wallet nonce > exact_nonce_count: skip wallet
EXACT_NONCE = True
EXACT_NONCE_COUNT = [10, 15]

'''
-----------------|available modules|-----------------|
"bungee",                                            |
"zerion_dna",                                        |
"transfer",                                          |
"blur"                                               |
-----------------------------------------------------|
you can customize bungee chains and amount in `modules/modules.py`, bungee function
'''

MODULES = [
    'bungee',
    'zerion_dna',
    'transfer',
    'blur'
]

# True if you want to do extra transactions,
# going to do after main modules
EXTRA = True

EXTRA_MODULES = [
    'bungee',
    'bungee',
    'bungee',
    'bungee',
    'bungee',
    'transfer',
    'transfer',
    'transfer',
]

# how many extra modules do you want
EXTRA_MODS_COUNT = [1, 2]


RPC = ['https://ethereum.publicnode.com',
       'https://1rpc.io/eth',
       'https://rpc.ankr.com/eth'
       ]

# only if you chose transfer and added addresses in trans_addresses.txt
ETH_FOR_TRANSFER = [0.0001, 0.0003]

# only if you chose blur
ETH_FOR_BLUR = [0.00001, 0.0001]
