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

