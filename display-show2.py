import time
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector

#LCD Display
LCD_RS = 26
LCD_E = 20
LCD_D4 = 5
LCD_D5 = 6
LCD_D6 = 13
LCD_D7 = 19
lcd_backlight = 2

lcd_columns = 16
lcd_rows = 2

lcd = LCD.Adafruit_CharLCD(LCD_RS,LCD_E,LCD_D4,LCD_D5,LCD_D6,LCD_D7, lcd_columns, lcd_rows, lcd_backlight)

#SQL Connection

connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Elefant12!",
        database="rfid_login"
)

def dbLoginEntry(ID):
    today = getDateTime()
    checkEntrys = "SELECT ID FROM login WHERE USERID = %s AND DATE = %s AND Type = 'Kommen' ORDER BY Date"
    cursor.execute(checkEntrys, (id, today))
    existing_entry = cursor.fetchone()

    if existing_entry:
        insert_query = "INSERT INTO login (UserID,Type,Date) VALUES (%s,'GEHEN',%s)"
        current_time = datetime.datetime.now()
        insert_values = (ID,current_time)
        cursor.execute(insert_query, insert_values)
        displayMessage(f"Sie wurden ausgelogt um:\n{today} ")

    else:
        insert_query = "INSERT INTO login (UserID,Type,Date) VALUES (%s,'KOMMEN',%s)"
        insert_values = (ID,today)
        cursor.execute(insert_query, insert_values)
        displayMessage(f"Sie wurden eingelogt um:\n{today}")

def dbShowLoginTime():


def displayMessage(message):
    displayWidth = 16
    lcd.clear()
    message_line = message.split('\n')

    if len(message_line) == 2:
        line1 = message_line[0]
        line2 = message_line[1]
        if len(line1) > displayWidth:
            while len(line1) > displayWidth:
                lcd.clear()
                lcd.message(line1[:displayWidth] + '\n' + line2)
                time.sleep(1)
                line1 = line1[1:]
            time.sleep(2)
            lcd.clear()
        elif len(line2) > displayWidth:
            while len(line2) > displayWidth:
                lcd.clear()
                lcd.message(line1 + '\n' + line2[:displayWidth])
                time.sleep(1)
                line2 = line2[1:]
            time.sleep(2)
            lcd.clear()
        elif len(line1) > displayWidth and len(line2) > displayWidth:
            lcd.message(message)
            for i in range(len(message)):
                time.sleep(0.5)
                lcd.move_left()
            time.sleep(2)
            lcd.clear()
        else:
            lcd.message(message)
            time.sleep(5)
            lcd.clear()
    elif len(message_line) == 1 and len(message) > displayWidth:
        lcd.message(message)
        for i in range(len(message)):
            time.sleep(0.5)
            lcd.move_left()
        time.sleep(2)
        lcd.clear()
    else:
        lcd.message(message)
        time.sleep(5)
        lcd.clear

def getDateTime():
    datetime_format="%Y-%m-%d %H:%M:%S"
    formatierte_zeit = time.strftime(datetime_format)
    
    return formatierte_zeit


cursor = connection.cursor()


#RFID READER
reader = SimpleMFRC522()


try:
    while True:
        id, _  = reader.read()
        print(id,)
        check_user_Query = "SELECT ID,Name FROM user WHERE UID= %s"
        
        cursor.execute(check_user_Query, (id,))

        results = cursor.fetchall()

        if results:
            userID = results[0][0]
            userName = results[0][1]
            
            message = f"Willkommen Benutzer:\n{userName}"
            displayMessage(message)
        else:
            message = "Sie wurden leider nicht gefunden"

            displayMessage(message)

            time.sleep(5.0)
            lcd.clear()

except KeyboardInterrupt:
    lcd.clear()
    pass

finally:
    cursor.close()
    connection.close()
    GPIO.cleanup()

