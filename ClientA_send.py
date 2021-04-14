from socket import *
import hashlib


def client_transaction(message1):
    serverName = 'localhost'
    serverPortF1 = 12000
    client_port_a = 30000
    clientSocketA = socket(AF_INET, SOCK_DGRAM)
    clientSocketA.bind((serverName, client_port_a))
    message = message1
    clientSocketA.sendto(message.encode(), (serverName, serverPortF1))
    clientSocketA.close()

def transaction():
    payee = ''
    payer_account = ''

    def payer():
        print("Select the Payer:")
        print("1. A0000001")
        print("2. A0000002")
        choice_payer_number = input("Choice: ")
        choice_payer_account = ''
        while (choice_payer_number != '1') and (choice_payer_number != '2'):
            print("Wrong choice, choose again")
            choice_payer_number = input("Choice: ")

        if choice_payer_number == '1':
            choice_payer_account = "A0000001"
        else:
            choice_payer_account = "A0000002"

        return choice_payer_account


    def payee():
        print("Select the Payee:")
        print("1. B0000001")
        print("2. B0000002")
        choice_payee_number = input("Choice: ")
        choice_payee_account = ''
        while (choice_payee_number != '1') and (choice_payee_number != '2'):
            print("Wrong choice, choose again")
            choice_payee_number = input("Choice: ")

        if choice_payee_number == '1':
            choice_payee_account = "B0000001"
        else:
            choice_payee_account = "B0000002"
        return choice_payee_account


    def amount_transfer():
        amount = int(input("Enter the amount of payment in decimal.\n"))
        amount_hex = '{:08x}'.format(amount)
        return amount, amount_hex


    payer_account = payer()
    payee_account = payee()
    amount_t, amount_h = amount_transfer()
    print(f"Tx: {payer_account} pays {payee_account} the amount of {amount_t}BC")
    Tx = payer_account+payee_account+amount_h
    c_balance, confirmed_balance = current_balance(payer_account)
    new_balance = c_balance - amount_t - 2
    if new_balance >= 0:
        with open('Unconfirmed_TA.txt', 'a') as U:
            U.write(Tx + '\n')
        client_transaction(Tx)
        amount_hex = '{:08x}'.format(new_balance)
        update_balance(payer_account, amount_hex, confirmed_balance)
    else:
        print("Not enough fonds.")


def update_balance(account, new_balance, confirmed_balance):
    update_amount = account+' '+new_balance.upper()+' '+confirmed_balance
    with open('BalanceA.txt', 'r+') as f:
        if account == 'A0000001':
            f.seek(0)
            f.write(update_amount)
        elif account == 'A0000002':
            f.seek(26)
            f.write('\n'+update_amount)


def current_balance(account):
    number_n_hex = 0
    confirmed_balance = ''
    with open('BalanceA.txt', 'r') as f:
        for line in f:
            count = 0
            for word in line.split():
                if account == word:
                    count = 1
                elif count == 1:
                    str_hex = "0x"+ word
                    number_n_hex = int(str_hex, 16)
                    count = 2
                elif count == 2:
                    confirmed_balance = word
                    break
                else:
                    pass
    return number_n_hex, confirmed_balance


def print_current_balance():
    num_hex, confirmed_balance = current_balance('A0000001')
    print(f'A0000001 current balance is {num_hex}')
    num_hex, confirmed_balance = current_balance('A0000002')
    print(f'A0000002 current balance is {num_hex}')


def print_unconfirmed_transactions():
    with open('Unconfirmed_TA.txt') as f:
        for line in f:
            count = 0
            for word in line.split():
                print(word)


def print_confirmed_transactions():
    count = int(input("How many last confirmed transactions: "))
    print(f'Printing the last {count} number of confirmed transactions')
    index = 0
    for line in reversed(list(open('Confirmed_TA.txt'))):
        if index < count:
            print(line.rstrip())
            index = index + 1
        else:
            break


def print_block_function(x, y):
    header_nonce = x[0:8]
    header_nonce_int = int(header_nonce, 16)
    header_last_block_header_hash = x[8:72]
    header_hash = x[8:136]
    hash_handler = hashlib.sha256()
    hash_block = str(header_nonce_int)+header_hash
    hash_handler.update(hash_block.encode("utf-8"))
    hash_of_header = hash_handler.hexdigest()
    header_merkle = x[72:136]
    body_1 = x[136:160]
    body_2 = x[160:184]
    body_3 = x[184:208]
    body_4 = x[208:232]
    print(f'Block {y}:')
    print(x)
    print(f'Header: 1. Nonce {header_nonce} = {header_nonce_int} ;                \n'
          f'        2. Last header block hash: {header_last_block_header_hash};    \n'
          f'        3. Merkle root: {header_merkle};                               \n'
          f'        4. Hash of the header: {hash_of_header}')
    print(f' --------------------------------------------------------------------------------------------------------\n'
          f'Body:   {body_1};                                                     \n'
          f'        {body_2};                                                     \n'
          f'        {body_3};                                                     \n'
          f'        {body_4}                                                      \n'
          f'---------------------------------------------------------------------------------------------------------\n')


def printing_block_chain():
    print(f'Printing the chain of blocks')
    counter = 1
    client_transaction("print")
    client_port_a = 30000
    clientSocketA = socket(AF_INET, SOCK_DGRAM)
    clientSocketA.bind(('', client_port_a))
    modifiedMessage, serverAddress = clientSocketA.recvfrom(8192)
    block_chain = modifiedMessage.decode()
    while block_chain != "done":
        print_block_function(block_chain, counter)
        counter = counter + 1
        modifiedMessage, serverAddress = clientSocketA.recvfrom(8192)
        block_chain = modifiedMessage.decode()
    clientSocketA.close()


def main():
    true = True
    while true:
        print("-----------------------------------MENU------------------------------------------")
        print("                               | ACCOUNT A |                                     ")
        print("---------------------------------------------------------------------------------")
        print("1. Enter a new transaction.")
        print("2. The current balance for each account.")
        print("3. Print the unconfirmed transactions.")
        print("4. Print the last X number of confirmed transactions (either as a Payee or Payer.")
        print("5. Print the blockchain.")
        print("6. Exit!")
        choice = input("Choose from the MENU: ")
        if choice == '1':
            transaction()
        elif choice == '2':
            print("2. Current balances for each account A.")
            print_current_balance()
        elif choice == '3':
            print("3. Unconfirmed transactions.")
            print_unconfirmed_transactions()
        elif choice == '4':
            print_confirmed_transactions()
        elif choice == '5':
            printing_block_chain()
        else:
            true = False


