from socket import *


def receive_message(x):
    C = open('Confirmed_TB.txt', 'a')
    if len(x) > 30:
        print("hello receiving the message from F1")
        tx_1 = x[136:160]
        C.write(tx_1+'\n')
        process_tx(tx_1)
        tx_2 = x[160:184]
        C.write(tx_2+'\n')
        process_tx(tx_2)
        tx_3 = x[184:208]
        C.write(tx_3+'\n')
        process_tx(tx_3)
        tx_4 = x[208:232]
        C.write(tx_4+'\n')
        process_tx(tx_4)
        with open('Unconfirmed_TB.txt', 'a') as f:
            f.seek(0)
            f.truncate()
    else:
        print("message small")


def process_tx(x):
    x_payer = x[0:8]
    x_payee = x[8:16]
    x_payed = x[16:24]
    account_balance(x_payer,x_payee,x_payed)


def account_balance(payer, payee, payed):
    if payer == "B0000001" or payer == "B0000002":
        with open("BalanceB.txt", "r+") as af:
            words = af.read().split()
            if payer == "B0000001":
                a = words[1]
                b = words[2]
                print("hello account_balance")
                new_confirmed_balance = sub_hex(b, payed)
                update_amount = "B0000001" + ' ' + a.upper() + ' ' + new_confirmed_balance.upper()
                af.seek(0)
                af.write(update_amount)

            elif payer == "B0000002":
                a = words[4]
                b = words[5]
                new_confirmed_balance = sub_hex(b, payed)
                update_amount = "B0000002" + ' ' + a.upper() + ' ' + new_confirmed_balance.upper()
                af.seek(26)
                af.write('\n'+update_amount)
        af.close()

    elif payer == "A0000001" or payer == "A0000002":
        with open("BalanceB.txt", "r+") as bf:
            words = bf.read().split()
            if payee == "B0000001":
                a = words[1]
                b = words[2]
                new_unconfirmed_balance = add_hex(a, payed)
                new_confirmed_balance = add_hex(b, payed)
                update_amount = "B0000001" + ' ' + new_unconfirmed_balance.upper() + ' ' + new_confirmed_balance.upper()
                bf.seek(0)
                bf.write(update_amount)

            elif payee == "B0000002":
                a = words[4]
                b = words[5]
                new_unconfirmed_balance = add_hex(a, payed)
                new_confirmed_balance = add_hex(b, payed)
                update_amount = "B0000002" + ' ' + new_unconfirmed_balance.upper() + ' ' + new_confirmed_balance.upper()
                bf.seek(26)
                bf.write('\n'+update_amount)
        bf.close()


def add_hex(x,y):
    a = int(x,16)
    b = int(y,16)
    sum_hex = a+b
    amount_hex = '{:08x}'.format(sum_hex)
    return amount_hex


def sub_hex(x,y):
    a = int(x,16)
    b = int(y,16)
    minus_hex = a-b-2
    amount_hex = '{:08x}'.format(minus_hex)
    return amount_hex


while 1:
    serverName = 'localhost'
    clientPortB = 40000
    clientSocketB = socket(AF_INET, SOCK_DGRAM)
    clientSocketB.bind(('', clientPortB))
    print('The server is ready to receive')
    modifiedMessage, serverAddress = clientSocketB.recvfrom(8192)
    confirmed_tx = modifiedMessage.decode()
    receive_message(confirmed_tx)
    clientSocketB.close()


