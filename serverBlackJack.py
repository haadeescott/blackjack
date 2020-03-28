# server for multithreaded TCP chat application
import os
import random
import socket
from socket import AF_INET, SOCK_STREAM
from threading import Thread


# BlackJack functions
# calculate total sum of all cards in hand
def calc_hand(hand):
    non_aces = [c for c in hand if c != 'A']
    aces = [c for c in hand if c == 'A']

    sum = 0

    for card in non_aces:
        if card in 'JQK':
            sum += 10
        else:
            sum += int(card)

    for card in aces:
        if sum <= 10:
            sum += 11
        else:
            sum += 1

    return sum


def startGame(players):

    p1StillPlaying = True
    p2StillPlaying = True

    while True:
        cards = [
            '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
            '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
            '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
            '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A',
        ]

        random.shuffle(cards)

        dealer = []
        player1 = []
        player2 = []
        player_score1 = []
        player_score2 = []

        if p1StillPlaying:
            player1.append(cards.pop())
        if p2StillPlaying:
            player2.append(cards.pop())
        dealer.append(cards.pop())
        if p1StillPlaying:
            player1.append(cards.pop())
        if p2StillPlaying:
            player2.append(cards.pop())
        dealer.append(cards.pop())

        first_hand = True
        dealerReveal = False
        player1Reply = '1'
        player2Reply = '1'
        choice1 = '0'
        choice2 = '0'
        newline = "dgdfgdfgdsfgdshfhdgdfgdfhgfhgfdjfghdhfg"


        while True:
            os.system('cls' if os.name == 'nt' else 'clear')

            #Dealer
            dealer_score = calc_hand(dealer)

            if dealerReveal:
                print('Dealer Cards: [{}] ({})'.format(']['.join(dealer), dealer_score))
            else:
                print('Dealer Cards: [{}][?]'.format(dealer[0]))
                broadcast(bytes('Dealer Cards: [{}][?]'.format(dealer[0]), "utf8"))



            #Player 1
            if p1StillPlaying:
                player_score1 = calc_hand(player1)


                if first_hand and player_score1 == 21:
                    players[0].send(bytes('Blackjack! Nice!\n', "utf8"))
                    broadcast(bytes("%s's got a blackjack!" %clients[players[0]], "utf8"))
                    # print('Blackjack! Nice!')
                    # print('')

                while choice1 != bytes('2', "utf8"):
                    # print('Your Cards:   [{}] ({})'.format(']['.join(player1), player_score1))
                    # print('')
                    # print('Player 1: What would you like to do?')
                    # print(' [1] Hit')
                    # print(' [2] Stand')
                    # print('')
                    # choice1 = input('Your choice: ')
                    # print('')

                    # players[0].send(bytes('Player 1 Cards:   [{}] ({})'.format(']['.join(player1), player_score1), "utf8"))
                    # players[0].send(bytes(" Player 1: What would you like to do?\n\n", "utf8"))
                    # players[0].send(bytes(" [1] Hit", "utf8"))
                    # players[0].send(bytes(" [2] Stand", "utf8"))
                    # players[0].send(bytes(" Your choice: ", "utf8"))
                    broadcast(bytes("%s's Cards:   [{}] ({})".format(']['.join(player1), player_score1) %clients[players[0]], "utf8"))
                    broadcast(bytes(" %s, What would you like to do?" %clients[players[0]], "utf8"))
                    broadcast(bytes(" [1] Hit", "utf8"))
                    broadcast(bytes(" [2] Stand", "utf8"))
                    broadcast(bytes(" Your choice: ", "utf8"))
                    while True:
                        choice1 = players[0].recv(BUFFSIZE)
                        broadcast(choice1, clients[players[0]] + ": ")
                        if choice1 == bytes('1', "utf8"):
                            player1.append(cards.pop())
                            player_score1 = calc_hand(player1)
                            break
                        elif choice1 == bytes('2', "utf8"):
                            break



                    first_hand = False

                    if player_score1 > 21:
                        choice1 = bytes('2', "utf8")
                        # players[0].send(bytes('Player 1 Cards:   [{}] ({})'.format(']['.join(player1), player_score1), "utf8"))
                        # players[0].send(bytes('Player 1 busted!', "utf8"))
                        broadcast(bytes("%s's Cards:   [{}] ({})".format(']['.join(player1), player_score1) %clients[players[0]], "utf8"))
                        broadcast(bytes('%s busted!' %clients[player[0]], "utf8"))




            first_hand = True

            #Player 2
            if p2StillPlaying:
                player_score2 = calc_hand(player2)

                if first_hand and player_score2 == 21:
                    # print('Blackjack! Nice!')
                    # print('')
                    players[1].send(bytes('Blackjack! Nice!\n', "utf8"))
                    broadcast(bytes('%s got a blackjack!' %clients[players[1]], "utf8"))



                while choice2 != bytes('2', "utf8"):
                    # print('Your Cards:   [{}] ({})'.format(']['.join(player2), player_score2))
                    # print('')
                    # print('Player 2: What would you like to do?')
                    # print(' [1] Hit')
                    # print(' [2] Stand')
                    # print('')
                    #
                    # choice2 = input('Your choice: ')
                    # print('')
                    #
                    # first_hand = False
                    #
                    # if choice2 == '1':
                    #     player2.append(cards.pop())
                    #     player_score2 = calc_hand(player2)
                    # players[1].send(bytes('Your Cards:   [{}] ({})'.format(']['.join(player2), player_score2), "utf8"))
                    # players[1].send(bytes(' Player 2: What would you like to do?', "utf8"))
                    # players[1].send(bytes(' [1] Hit', "utf8"))
                    # players[1].send(bytes(' [2] Stand', "utf8"))
                    # players[1].send(bytes(' Your choice: ', "utf8"))
                    broadcast(bytes("%s's Cards:   [{}] ({})".format(']['.join(player2), player_score2) %clients[players[1]], "utf8"))
                    broadcast(bytes(' %s, What would you like to do?' %clients[players[1]], "utf8"))
                    broadcast(bytes(' [1] Hit', "utf8"))
                    broadcast(bytes(' [2] Stand', "utf8"))
                    broadcast(bytes(' Your choice: ', "utf8"))
                    while True:
                        choice2 = players[1].recv(BUFFSIZE)
                        broadcast(choice2, clients[players[1]] + ": ")
                        if choice2 == bytes('1', "utf8"):
                            player2.append(cards.pop())
                            player_score2 = calc_hand(player2)
                            break
                        if choice2 == bytes('2', "utf8"):
                            break


                    if player_score2 > 21:
                        # print('Your Cards:   [{}] ({})'.format(']['.join(player2), player_score2))
                        # print('You busted!')
                        # print('')
                        choice2 = bytes('2', "utf8")
                        #players[1].send(bytes('Your Cards:   [{}] ({})'.format(']['.join(player2), player_score2), "utf8"))
                        #players[1].send(bytes(' You busted!', "utf8"))
                        broadcast(bytes(" %s's Cards:   [{}] ({})".format(']['.join(player2), player_score2) %clients[players[1]], "utf8"))
                        broadcast(bytes(' %s busted!' %clients[player[1]], "utf8"))



            while calc_hand(dealer) <= 16:
                dealer.append(cards.pop())
            dealer_score = calc_hand(dealer)
            print('Dealer Cards: [{}] ({})'.format(']['.join(dealer), dealer_score))
            broadcast(bytes(' Dealer Cards: [{}] ({})'.format(']['.join(dealer), dealer_score), "utf8"))


            if dealer_score > 21:
                print('Dealer busted, all players win!')
                broadcast(bytes(' Dealer busted, all players win!\n', "utf8"))

            if p1StillPlaying:
                if player_score1 < 22:
                    if player_score1 == dealer_score:
                        print('Player 1 draw with dealer')
                        broadcast(bytes(' %s draw with dealer' %clients[players[0]], "utf8"))
                    elif player_score1 > dealer_score:
                        print('player 1 beat the dealer, you win!')
                        broadcast(bytes(' %s beat the dealer, you win!' %clients[players[0]], "utf8"))
                    elif dealer_score <= 21:
                        print('Dealer win player 1 :(')
                        broadcast(bytes(' Dealer win %s :(' %clients[players[0]], "utf8"))

            if p2StillPlaying:
                if player_score2 < 22:
                    if player_score2 == dealer_score:
                        print('Player 2 draw with dealer')
                        broadcast(bytes(' %s draw with dealer' %clients[players[1]], "utf8"))
                    elif player_score2 > dealer_score:
                        print('player 2 beat the dealer, you win!')
                        broadcast(bytes(' %s beat the dealer, you win!' %clients[players[1]], "utf8"))
                    elif dealer_score <= 21:
                        print('Dealer win player 2 :(')
                        broadcast(bytes('Dealer win %s :(' %clients[players[1]], "utf8"))

            print('')

            if p1StillPlaying:
                #player1Reply = input('Player 1: Play again? Enter 1 if yes, enter 2 if no')
                #players[0].send(bytes('Player 1: Play again? Enter 1 if yes, enter 2 if no', "utf8"))
                broadcast(bytes(' %s, Do you want to play again? Enter 1 if yes, enter 2 if no' %clients[players[0]], "utf8"))
                player1Reply = players[0].recv(BUFFSIZE)
                broadcast(player1Reply)
                while player1Reply != bytes('1', "utf8") and player1Reply != bytes('2', "utf8"):
                   # player1Reply = input('Player 1: Play again? Enter 1 if yes, enter 2 if no')
                    #players[0].send(bytes('Player 1: Play again? Enter 1 if yes, enter 2 if no', "utf8"))
                    #player1Reply = players[0].recv(BUFFSIZE)
                    broadcast(bytes(' %s, Do you want to play again? Enter 1 if yes, enter 2 if no' %clients[players[0]], "utf8"))
                    player1Reply = players[0].recv(BUFFSIZE)
                    broadcast(player1Reply)

            if p2StillPlaying:
                #player2Reply = input('Player 2: Play again? Enter 1 if yes, enter 2 if no')
                #players[1].send(bytes('Player 2: Play again? Enter 1 if yes, enter 2 if no', "utf8"))
                broadcast(bytes(' %s, Do you want to play again? Enter 1 if yes, enter 2 if no' %clients[players[1]], "utf8"))
                player2Reply = players[1].recv(BUFFSIZE)
                broadcast(player2Reply)
                while player2Reply != bytes('1', "utf8") and player2Reply != bytes('2', "utf8"):
                    #player2Reply = input('Player 2: Play again? Enter 1 if yes, enter 2 if no')
                    #players[1].send(bytes('Player 2: Play again? Enter 1 if yes, enter 2 if no', "utf8"))
                    broadcast(bytes(' %s, Do you want to play again? Enter 1 if yes, enter 2 if no' %clients[players[1]], "utf8"))
                    player2Reply = players[1].recv(BUFFSIZE)
                    broadcast(player2Reply)





            if player1Reply == bytes('2', "utf8"):
                p1StillPlaying = False

            if player2Reply == bytes('2', "utf8"):
                p2StillPlaying = False

            if not p1StillPlaying and not p2StillPlaying:
                print("Exiting game...")
                broadcast(bytes("Exiting game...", "utf8"))
                break
            else:
                print("restarting game...")
                broadcast(bytes("restarting game...", "utf8"))
                break






        if not p1StillPlaying and not p2StillPlaying:
            print("Game Exited")
            broadcast(bytes("Games Exited", "utf8"))
            break




# Function to display hostname and
# IP address
def getHostnameIP():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print("Hostname :  ", host_name)
        print("Server IP : ", host_ip)
    except:
        print("Unable to get hostname and ip")


def acceptIncomingConnections():
    # sets up method to handle Incoming clients
    while True:
        client, client_address = SERVER.accept()
        print("Received connection from %s (%s)" % client_address)
        # print("test - %s" % client)
        if len(clients) > 5:
            client.send(bytes("full", "utf8"))
        else:
            client.send(bytes("Welcome, type your username at the textbox below and press enter!", "utf8"))
            addresses[client] = client_address
            Thread(target=handle_client, args=(client,)).start()
            players.append(client)
            if len(addresses) > 1:
                print("entering game")
                startGame(players)


def handle_client(client):  # Takes client socket as argument.
    # handles 1 client connection
    username = client.recv(BUFFSIZE).decode("utf8")
    message = ""
    if bool(clients):
        for x in clients:
            message = message + clients[x] + ", "
        message = message + "is currently in the chat!"
    welcome = 'Hello %s! Welcome to the chat group.' % username
    welcome = welcome + message + ' To quit, type exit.'
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % username
    broadcast(bytes(msg, "utf8"))
    clients[client] = username

    # while True:
    #
    #     msg = client.recv(BUFFSIZE)
    #     if msg == bytes("exit", "utf8"):
    #     #     broadcast(msg, username + ": ")
    #     # else:
    #         # client.send(bytes("exit", "utf8"))
    #         client.close()
    #         del clients[client]
    #         broadcast(bytes("%s has left the chat." % username, "utf8"))
    #         print("%s (%s) has disconnected from chat room" % addresses[client])
    #         break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    # broadcast message to all clients to simulate group chat
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}
players = []
# HOST = socket.gethostbyname('0.0.0.0')
listeningPort = input("Hello, this is CSC1010 Chat server, please enter the listening port\n")
list = listeningPort.split()
# PORT = 1234
HOST = list[0]
PORT = int(list[1])
BUFFSIZE = 1024
address = (HOST, PORT)

# Create a TCP/IP socket
SERVER = socket.socket(AF_INET, SOCK_STREAM)
# Bind socket to port
SERVER.bind(address)

if __name__ == "__main__":
    SERVER.listen(5)
    # getHostnameIP()
    # print("Port: ", PORT)
    print("Waiting for incoming connections...")
    ACCEPT_THREAD = Thread(target=acceptIncomingConnections)
    # create thread for each client/incoming connection
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
