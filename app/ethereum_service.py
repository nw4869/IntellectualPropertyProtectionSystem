from time import sleep
from binascii import unhexlify
from app import web3, MyContract, my_contract
from config import Config
from app.errors import *


eth = web3.eth
web3.personal.unlockAccount(eth.accounts[0], '4869', 0)


def get_block(block_num):
    return eth.getBlock(block_num) if block_num is not None else None


def get_transaction(tx):
    transaction = eth.getTransaction(tx)
    transaction['is_confirmed'] = tx_is_confirmed(tx)
    transaction['confirm_num'] = get_tx_distance(tx)
    return transaction


def get_latest_block():
    return eth.getBlock('latest')


def get_latest_block_number():
    return get_latest_block()['number']


def get_block_by_tx(tx):
    transaction = get_transaction(tx)
    return None if transaction is None else get_block(transaction['blockNumber'])


def get_tx_distance(tx):
    tx = eth.getTransaction(tx)
    if tx['blockNumber'] is None:
        return None
    else:
        return get_latest_block_number() - tx['blockNumber']


def submit_file(user, file):
    address = user.wallets[0].address
    price = web3.toWei(file.price, "ether")
    file_hash = bytearray(unhexlify(file.hash))
    owner = "0x0000000000000000000000000000000000000000"

    # unlock
    web3.personal.unlockAccount(address, '4869', 0)

    gas_limit = web3.eth.getBlock('latest')['gasLimit']
    gas_estimate = my_contract.estimateGas({'from': address}).proof(file_hash, file.filename, file.description, file.for_sell, price, owner)

    if gas_estimate > gas_limit * 9 / 10:
        raise EthereumException()

    balance = get_balance(address)
    value = gas_estimate * eth.gasPrice
    if balance < value:
        raise BalanceException(to_ether(value), to_ether(balance))

    return my_contract.transact({'from': address}).proof(file_hash, file.filename, file.description, file.for_sell, price, owner)


def purchase(user, file):

    address = user.wallets[0].address
    price = to_wei(file.price)
    file_hash = bytearray(unhexlify(file.hash))

    # unlock
    web3.personal.unlockAccount(address, '4869', 0)

    gas_limit = web3.eth.getBlock('latest')['gasLimit']
    gas_estimate = my_contract.estimateGas({'from': address, 'value': price}).purchase(file_hash)

    if gas_estimate > gas_limit * 9 / 10:
        raise EthereumException()

    if get_balance(address) < gas_estimate * eth.gasPrice:
        raise BalanceException

    return my_contract.transact({'from': address, 'value': price}).purchase(file_hash)


def authorize(from_user, to_user, file):
    from_address = from_user.wallets[0].address
    to_address = to_user.wallets[0].address
    file_hash = bytearray(unhexlify(file.hash))

    # unlock
    web3.personal.unlockAccount(from_address, '4869', 0)

    gas_limit = web3.eth.getBlock('latest')['gasLimit']
    gas_estimate = my_contract.estimateGas({'from': from_address}).authorize(file_hash, to_address)

    if gas_estimate > gas_limit * 9 / 10:
        raise EthereumException()

    if get_balance(from_address) < gas_estimate * eth.gasPrice:
        raise BalanceException

    return my_contract.transact({'from': from_address}).authorize(file_hash, to_address)


def transfer(from_user, to_user, file):
    from_address = from_user.wallets[0].address
    to_address = to_user.wallets[0].address
    file_hash = bytearray(unhexlify(file.hash))

    # unlock
    web3.personal.unlockAccount(from_address, '4869', 0)

    gas_limit = web3.eth.getBlock('latest')['gasLimit']
    gas_estimate = my_contract.estimateGas({'from': from_address}).transfer(file_hash, to_address)

    if gas_estimate > gas_limit * 9 / 10:
        raise EthereumException()

    if get_balance(from_address) < gas_estimate * eth.gasPrice:
        raise BalanceException

    return my_contract.transact({'from': from_address}).transfer(file_hash, to_address)


def new_account(password):
    return web3.personal.newAccount(password)


def get_balance(address):
    return web3.eth.getBalance(address)


def to_ether(wei):
    return web3.fromWei(wei, 'ether')


def to_wei(ether):
    return web3.toWei(ether, 'ether')


def transfer_wei(_from, to, value):
    return web3.eth.sendTransaction({'from': _from, 'to': to, 'value': int(value)})


def is_address(address):
    return web3.isAddress(address)


def estimate_tx_wei(tx):
    return eth.estimateGas(tx) * eth.gasPrice


def tx_is_confirmed(tx):
    distance = get_tx_distance(tx)
    return distance is not None and distance >= Config.CONFIRM_BLOCK_NUM


def file_is_confirmed(file):
    return tx_is_confirmed(file.txhash) if file and file.txhash else None


def traversal_all_contract():
    for i in range(0, eth.blockNumber + 1):
        if eth.getBlockTransactionCount(i) > 0:
            block = eth.getBlock(i)
            for transaction in block['transactions']:
                contractAddress = eth.getTransactionReceipt(transaction)['contractAddress']
                print(i, block['hash'], transaction, contractAddress)


def deploy_contract():
    return MyContract.deploy()


def test_load_contract(address):
    print('contract:', address)
    # contract_factory = contract.construct_contract_factory(web3, contract_data['abi'])
    # my_contract = contract_factory(address=address)
    result = my_contract.call().add(1, 2)
    print('add result:', result)

    print('proof timestamp:', my_contract.call().getProofName("aaaaa"))

    gas_limit = int(eth.getBlock('latest')['gasLimit'])
    # tx = my_contract.transact().proof("aaa", "bb", "cc")
    tx = my_contract.transact({'gas': int(gas_limit*0.9)}).proof("aaaaa", "bbb", "cc")
    print(tx)

    while True:
        receipt = eth.getTransactionReceipt(tx)
        if receipt is not None:
            break
        sleep(1)
    print('receipt:', receipt)

    from datetime import datetime

    now = datetime.now()
    print(now)
    new_data = str(now)
    print('try to set new data:', new_data)
    tx_list = []
    for i in range(1):
        tx = my_contract.transact().setData(new_data)
        # tx = my_contract.transact({'gas': 210000}).setData(new_data)
        tx_list.append(tx)
        print('tx hash:', tx)
    while len(tx_list) > 0:
        for tx in tx_list:
            receipt = eth.getTransactionReceipt(tx)
            if receipt is not None:
                tx_list.remove(tx)
                # print('tx receive:', receipt)
                print('tx %s receipt: blockNumber: %s, transactionIndex: %s' % (tx, receipt['blockNumber'], receipt['transactionIndex']))
        data = my_contract.call().getData()
        print('contract data:', data)

        if len(tx_list) > 0:
            sleep(2)
    print(datetime.now())


def deploy():
    print('depolying contract')
    tx_hash = deploy_contract()
    print('tx_hash:', tx_hash)
    print('waiting', end='', flush=True)
    while True:
        receipt = eth.getTransactionReceipt(tx_hash)
        if receipt is not None:
            break
        print('.', end='', flush=True)
        sleep(2)
    print()
    # print('receipt:', receipt)
    address_ = receipt['contractAddress']
    MyContract.address = address_
    my_contract.address = address_
    print('deploy success, contract address:', address_)
    print('updating contract config')
    Config.contract_data['address'] = address_
    Config.update_contract_config(Config.contract_data)
    print('done.')


if __name__ == '__main__':
    print('blockNum', eth.blockNumber)

    # unlock
    print('unlock', web3.personal.unlockAccount(eth.coinbase, '4869'), 0)

    # traversal_all_contract()

    # test_deploy()

    # load_contract("0x0b02516fdb53cd5f06547d5dda0b0bfe8d0ba1c6")
    # test_load_contract("0x76ab884bbe0252f490a557c4117b6c6d1ce533af")
    # deploy()
