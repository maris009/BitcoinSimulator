from socket import *
import hashlib
import os

block_hash_zero = '{:064x}'.format(0)
last_block_hash = block_hash_zero


def hash_nonce_function():
    nonce = 0
    merkle_root = str(merkle_function())
    while True:
        block_header = str(nonce) + last_block_hash + merkle_root
        hashValue = hash_function(block_header)
        nonceFound = True
        for i in range(4):
            if hashValue[i] != '0':
                nonceFound = False
        if nonceFound:
            break
        else:
            nonce = nonce + 1
    print(hashValue)
    print(nonce)
    return hashValue, nonce


def hash_function(variable):
    m = hashlib.sha256()
    m.update(variable.encode("utf-8"))
    hash_message = m.hexdigest()
    return hash_message


def mining_function():
    last_header_hash, nonce_block = hash_nonce_function()
    merkle_root = merkle_function()
    with open('Temp_TF2.txt', 'r') as rg:
        body = ''
        for line in rg:
            body = body + line.strip()
    block = '{:08x}'.format(nonce_block)+last_block_hash+merkle_root+body
    serverSocketF2.sendto(block.encode(), (serverName, serverPortF1))
    serverSocketF2.sendto(block.encode(), (serverName, clientPortB))
    with open('BlockchainF2.txt', 'a') as bf:
        bf.write(block+'\n')
    print(block)



def merkle_function():
    hashA = ''
    hashB = ''
    hashC = ''
    hashD = ''
    with open('Temp_TF2.txt','r') as rm:
        num = 1
        for line in rm:
            if num == 1:
                A = rm.readline()
                hashA = hash_function(A)
                num = num + 1
            elif num == 2:
                B = rm.read()
                hashB = hash_function(B)
                num = num + 1

            elif num == 3:
                C = rm.read()
                hashC = hash_function(C)
                num = num + 1
            elif num == 4:
                D = rm.read()
                hashD = hash_function(D)
                break
    hashCD = hash_function(hashC + hashD)
    hashAB = hash_function(hashA + hashB)
    hashABCD = hash_function(hashAB+hashCD)
    return hashABCD


turn = 2
balance_F2 = 0
mining_fee = 30
tx_fee = 8
count = 0

while 1:
    serverPortF2 = 12500
    serverPortF1 = 12000
    clientPortB = 40000
    client_port_b = 35000
    serverName = 'localhost'

    serverSocketF2 = socket(AF_INET, SOCK_DGRAM)
    serverSocketF2.bind(('', serverPortF2))
    print('The server is ready to receive')
    message, clientAddress = serverSocketF2.recvfrom(2048)
    str_client_address = str(clientAddress)
    modifiedMessage = message.decode()
    if str_client_address == "('127.0.0.1', 35000)" and modifiedMessage != "print":
        with open('Temp_TF2.txt', 'a') as f:
            f.write(modifiedMessage+'\n')
        f.close()
        count = count + 1
        serverSocketF2.sendto(modifiedMessage.encode(), (serverName, serverPortF1))
        if count == 4:
            if turn % 2 == 1:
                balance_F2 = balance_F2 + mining_fee + tx_fee
                print(balance_F2)
                turn = turn + 1
                mining_function()
                last_block_hash, nonce_back = hash_nonce_function()
                count = 0
                with open('Temp_TF2.txt', 'a') as f:
                    f.seek(0)
                    f.truncate()
                f.close()
            else:
                count = 0
                turn = turn + 1

        else:
            pass
    elif modifiedMessage == "print":
        print("made it here")
        with open("BlockchainF2.txt", "r") as bcf:
            for line in bcf:
                block_message = line.strip()
                print(block_message)
                serverSocketF2.sendto(block_message.encode(), (serverName, client_port_b))
        bcf.close()
        serverSocketF2.sendto("done".encode(), (serverName, client_port_b))

    else:
        str_message = str(modifiedMessage)
        if len(str_message) < 30:
            with open('Temp_TF2.txt', 'a') as f:
                f.write(modifiedMessage + '\n')
            f.close()
            count = count + 1
            if count == 4:
                if turn % 2 == 1:
                    balance_F2 = balance_F2 + mining_fee + tx_fee
                    print(balance_F2)
                    turn = turn + 1
                    mining_function()
                    last_block_hash, nonce_back = hash_nonce_function()
                    count = 0
                    with open('Temp_TF2.txt', 'a') as f:
                        f.seek(0)
                        f.truncate()
                    f.close()
                else:
                    count = 0
                    turn = turn + 1

            else:
                pass
        else:
            serverSocketF2.sendto(modifiedMessage.encode(), (serverName, clientPortB))
            hash_handler = hashlib.sha256()
            message_nonce = modifiedMessage[0:8]
            nonce_int = int(message_nonce, 16)
            message_body = modifiedMessage[8:136]
            block_header = str(nonce_int)+message_body
            hash_handler.update(block_header.encode("utf-8"))
            last_block_hash = hash_handler.hexdigest()
            print(last_block_hash)
            with open('BlockchainF2.txt', 'a') as b:
                b.write(modifiedMessage + '\n')
            b.close()
            count = 0
            with open('Temp_TF2.txt', 'a') as f:
                f.seek(0)
                f.truncate()
            f.close()
    serverSocketF2.close()