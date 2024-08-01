from web3 import Web3
import random
import time
from loguru import logger
from sys import stderr

#--------------------------------        НАСТРОЙКИ          ------------------------------------------------------------
# Определение диапазона суммы перевода и времени задержки
min_transfer = 0.16  # минимальная сумма перевода в токене
max_transfer = 0.18  # максимальная сумма перевода в токене
min_delay = 2  # минимальное время задержки в секундах между кошельками
max_delay = 5  # максимальное время
GWEI_CONTROL = 7

# Инициализация Web3
web3 = Web3(Web3.HTTPProvider('https://ethereum.publicnode.com')) #если потребуется отправить токен из другой EVM сети (не ERC20), просто вставьте RPC нужной EVM сети

# Адрес токена и его ABI
TOKEN_abi = '[{"inputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"symbol","type":"string"},{"internalType":"uint256","name":"totalSupply_","type":"uint256"},{"internalType":"address","name":"treasury","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"InvalidShortString","type":"error"},{"inputs":[{"internalType":"string","name":"str","type":"string"}],"name":"StringTooLong","type":"error"},{"inputs":[],"name":"Unauthorized","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[],"name":"EIP712DomainChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"tokenPool","type":"address"}],"name":"TokenPoolUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"eip712Domain","outputs":[{"internalType":"bytes1","name":"fields","type":"bytes1"},{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"version","type":"string"},{"internalType":"uint256","name":"chainId","type":"uint256"},{"internalType":"address","name":"verifyingContract","type":"address"},{"internalType":"bytes32","name":"salt","type":"bytes32"},{"internalType":"uint256[]","name":"extensions","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_tokenPool","type":"address"}],"name":"setTokenPool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"tokenPool","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
TOKEN_address = Web3.to_checksum_address('АДРЕС_ТОКЕНА') #Вставь сюда адрес токена для трансфера

# Логирование
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <3}</level> | <level>{message}</level>")

# Чтение приватных ключей
with open('private_keys.txt', 'r') as file:
    private_keys = file.read().splitlines()

# Подготовка контракта
TOKEN_contract = web3.eth.contract(address=TOKEN_address, abi=TOKEN_abi)

# Чтение списка кошельков
with open('addresses.txt', 'r') as file:
    wallets = file.read().splitlines()
    wallets = [Web3.to_checksum_address(wallet) for wallet in wallets]
def cheker_gwei():
    max_gwei = GWEI_CONTROL * 10 ** 9
    if web3.eth.gas_price > max_gwei:
        logger.info('Газ слишком большой, ждем')
        while web3.eth.gas_price > max_gwei:
            time.sleep(60)
        logger.info('Газ норм, продолжаю работу')

# Основной цикл отправки токенов
from_address = web3.eth.account.from_key(private_keys[0]).address
for wallet in wallets:
    cheker_gwei()

    amount_to_send = web3.to_wei(random.uniform(min_transfer, max_transfer), 'ether')
    try:
        # Подготовка данных для транзакции
        tx = TOKEN_contract.functions.transfer(wallet, amount_to_send).build_transaction({
            'from': from_address,
            'chainId': web3.eth.chain_id,
            'gasPrice': int(web3.eth.gas_price * 1.1),
            'nonce': web3.eth.get_transaction_count(from_address),
        })
        gasLimit = web3.eth.estimate_gas(tx)
        tx['gas'] = int(gasLimit * 1.2)

        signed_tx = web3.eth.account.sign_transaction(tx, private_keys[0])
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        status = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=360).status
        if status == 1:
            logger.info(f"send to {wallet} : {amount_to_send / 10 ** 18} tokens https://etherscan.io/tx/{tx_hash.hex()}")
        else:
            logger.error(f'[{from_address}] transaction failed!')
    except Exception as err:
        print(err)

    time.sleep(random.randint(min_delay, max_delay))
