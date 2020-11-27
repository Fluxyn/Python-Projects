from time import sleep
player_health = 5
enemy_health = 5

def print_health():
        print("Player =" , player_health)
        print("Enemy =" , enemy_health)

print("You engaged battle with a Enemy!")
def turn():
        print("Choose an attack")
        answer = input("1. Uppercut\n2: Punch\n3. Kick\n")
        if answer == '1':
                print("Player uppercutted Enemy")
                enemy_health =- 2
        if answer == '2':
                print("Player punched Enemy")
                enemy_health - 4
        if answer == '3':
                print("Player kicked Enemy")
                enemy_health -= 3
        print("Enemy attacked Player")
        player_health - 3
        print_health()
        sleep(2)
        turn()
turn()
