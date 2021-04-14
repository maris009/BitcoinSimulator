import ClientA_send
import ClientB_send


true = True
while true:
    print("---------MENU---------------")
    print("1. Account Client A.")
    print("2. Account Client B.")
    print("3. Exit!")
    choice = input("Choose your account: ")
    if choice == '1':
        ClientA_send.main()
    elif choice == '2':
        ClientB_send.main()
    else:
        true = False































"""
payee = ''
payer_account = ''


def payer():
    print("Select the Payer:")
    print("1. A0000001")
    print("2. A0000002")
    print("3. B0000001")
    print("4. B0000002")
    choice_payer_number = input("Choice: ")
    choice_payer_account = ''
    while (choice_payer_number != '1') and (choice_payer_number != '2') and (choice_payer_number != '3') and (choice_payer_number != '4'):
        print("Wrong choice, choose again")
        choice_payer_number = input("Choice: ")

    if choice_payer_number == '1' or choice_payer_number == '2':
        if choice_payer_number == '1':
            choice_payer_account = "A0000001"
            choice_payee_account = payeeB()

        else:
            choice_payer_account = "A0000002"
            choice_payee_account = payeeB()
    else:
        if choice_payer_number == '3':
            choice_payer_account = "B0000001"
            choice_payee_account = payeeA()

        else:
            choice_payer_account = "B0000002"
            choice_payee_account = payeeA()
    return choice_payer_account, choice_payee_account


def payeeB():
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


def payeeA():
    print("Select the Payee:")
    print("1. A0000001")
    print("2. A0000002")
    choice_payee_number = input("Choice: ")
    choice_payee_account = ''
    while (choice_payee_number != '1') and (choice_payee_number != '2'):
        print("Wrong choice, choose again")
        choice_payee_number = input("Choice: ")

    if choice_payee_number == '1':
        choice_payee_account = "A0000001"
    else:
        choice_payee_account = "A0000002"
    return choice_payee_account


def amount_transfer():
    amount = int(input("Enter the amount of payment in decimal.\n"))
    amount_hex = '{:08x}'.format(amount)
    return amount, amount_hex


payer_account, payee_account = payer()
amount_t, amount_h = amount_transfer()
print(f"Tx: {payer_account} pays {payee_account} the amount of {amount_t}BC")
Tx = payer_account+payee_account+amount_h

payer_account, payee_account = payer()
amount_t, amount_h = amount_transfer()
print(f"Tx: {payer_account} pays {payee_account} the amount of {amount_t}BC")
Tx = payer_account+payee_account+amount_h


"""
