import random
import smtplib
import mysql.connector as myconn
from email.message import EmailMessage
from datetime import datetime

mydb = myconn.connect(
    host="localhost",
    user="root",
    password="A@y@n#786",
    database="atm"
)

cursor=mydb.cursor()

def generate_slip(card, txn_type, amount, balance):
    txn_id = random.randint(100000, 999999)
    txn_time = datetime.now()

    slip = f"""
-------- ATM TRANSACTION SLIP --------
Transaction ID : {txn_id}
Card Number    : {card}
Transaction    : {txn_type}
Amount         : {amount}
Balance        : {balance}
Date & Time    : {txn_time}
-------------------------------------
"""

    print(slip)

    file_name = f"transaction_{txn_id}.txt"
    U= open(file_name, "w") 
    U.write(slip)
    U.close()

def login ():
    card=input("Enter Card No :")
    pin=input("Enter Pin :")
    cursor.execute("SELECT name, balance FROM users WHERE card_no=%s AND pin=%s",(card, pin))
    result=cursor.fetchone()
    
    if result:
        print(f"\nWelcome, {result[0]}!")
        atm_menu(card)
    else:
        print("Invalid Card Number or PIN!")

        
        
def atm_menu(card):
    while True:
        print("\n1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Exit")       
           
        choice=int(input("Enter your Choice :"))
        
        if choice==1:
            cursor.execute("select balance from users where card_no=%s", (card,) )  
            balance=cursor.fetchone()[0] 
            print ("YOUR BALANCE IS ",balance)
            
        elif choice==2:
            amount = float(input("Enter amount :"))

            cursor.execute( "SELECT balance FROM users WHERE card_no=%s",(card,) )
            bal = cursor.fetchone()[0]
            new_balance = bal + amount

            cursor.execute( "UPDATE users SET balance=%s WHERE card_no=%s", (new_balance, card))
            mydb.commit()

            print("AMOUNT DEPOSITED SUCCESSFULLY")

            generate_slip(card, "Deposit", amount, new_balance)

            
        elif choice==3:
            otp = random.randint(100000, 999999)
            # Email details
            sender_email = "shanchaudhary11oo@gmail.com"
            app_password = "xtgq efof tdim efge"   # 16-digit app password
            receiver_email = "ayanchaudhart@gmail.com"
            # Create email
            msg = EmailMessage()
            msg.set_content(f"Your OTP is: {otp}")
            msg["Subject"] = "Your OTP Verification Code"
            msg["From"] = sender_email
            msg["To"] = receiver_email
            # Send email
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:  # (SMTP)Simple Mail Transfer Protocol with SSL
                server.login(sender_email, app_password)
                server.send_message(msg)
                print("OTP sent successfully!")
                
            user_otp=int(input("Enter OTP :"))  
            if user_otp == otp:
                amt = float(input("Enter amount to withdraw: "))

                cursor.execute( "SELECT balance FROM users WHERE card_no=%s", (card,) )
                bal = cursor.fetchone()[0]

                if amt <= bal:
                    new_balance = bal - amt

                    cursor.execute("UPDATE users SET balance=%s WHERE card_no=%s", (new_balance, card) )
                    mydb.commit()

                    print("Please collect your cash.")

                    generate_slip(card, "Withdraw", amt, new_balance)
                else:
                    print("Insufficient Balance!")

                
        elif choice==4:        
            print("Thank you for using ATM!")
            break
        
        else:
            print("Invalid choice!")
            
login()            