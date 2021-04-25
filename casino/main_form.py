import sqlite3
import sys
from random import randint
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QButtonGroup
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

db = sqlite3.connect('casino.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
    login TEXT,
    password TEXT,
    cash BIGINT,
    nickname TEXT,
    game INTEGER,
    win INTEGER,
    lose INTEGER,
    secret TEXT
)""")  # Создаю новую БД
db.commit()


class Enterance(QMainWindow):

    def __init__(self):
        super(Enterance, self).__init__()
        uic.loadUi('enter_ds.ui', self)
        self.pushButton_enter.clicked.connect(self.next)
        self.pushButton_exit.clicked.connect(self.exi)
        self.pushButton_reg.clicked.connect(self.reg)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.next()
        if event.key() == Qt.Key_Escape:
            self.close()

    def next(self):
        global user_login
        user_login = self.lineEdit_login.text()
        user_password = self.lineEdit_passw.text()
        sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'")
        if user_login == '' or user_password == '':
            self.statusBar().showMessage('Заполните все поля')
        elif sql.fetchone() is None:
            self.lineEdit_login.setText('')
            self.lineEdit_passw.setText('')
            self.statusBar().showMessage('Такого логина не существует')
        else:
            password = sql.execute(f"SELECT password FROM users WHERE login = '{user_login}'").fetchone()[0]
            if user_password == password:
                self.close()
                self.chose = Choose()
                self.chose.show()
            else:
                self.lineEdit_passw.setText('')
                self.statusBar().showMessage('Неверный пароль')

    def exi(self):
        self.close()

    def reg(self):
        self.close()
        self.reg = Registr()
        self.reg.show()


class Registr(QMainWindow):

    def __init__(self):
        super().__init__()
        self.mn = Enterance()
        uic.loadUi('reg_ds.ui', self)
        self.pushButton_back.clicked.connect(self.back)
        self.pushButton_registr.clicked.connect(self.nextt)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.nextt()
        if event.key() == Qt.Key_Escape:
            self.back()

    def nextt(self):
        user_login = self.lineEdit_login.text()
        user_password = self.lineEdit_passw.text()
        user_nickname = self.lineEdit_nn.text()
        user_word = self.lineEdit_word.text()
        sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'")
        if user_login == '' or user_password == '' or user_word == '' or user_nickname == '':
            self.statusBar().showMessage('Заполните все поля')

        elif sql.fetchone() is None:
            self.mn.show()
            sql.execute(f"INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (user_login, user_password,
                                                                               0, user_nickname, 0, 0, 0, user_word))
            db.commit()
            self.close()

        else:
            self.statusBar().showMessage('Пользователь с таким логином уже зарегистрирован')
            self.lineEdit_login.setText('')
            self.lineEdit_passw.setText('')
            self.lineEdit_nn.setText('')
            self.lineEdit_word.setText('')

    def back(self):
        self.close()
        self.mn = Enterance()
        self.mn.show()


class Choose(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('choose_ds.ui', self)
        pixmap1 = QPixmap('squers_game.jpg')
        pixmap2 = QPixmap('twenty-one.jpg')
        self.lbl_cubes.setPixmap(pixmap1)
        self.lbl_apples.setPixmap(pixmap2)
        self.pushButton_game1.clicked.connect(self.game1)
        self.pushButton_game2.clicked.connect(self.game2)
        self.pushButton_statistic.clicked.connect(self.statistic)
        self.pushButton_exit.clicked.connect(self.exitt)
        self.pushButton_addCash.clicked.connect(self.add_balance)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def statistic(self):
        self.close()
        self.stat = Statistic()
        self.stat.show()

    def game1(self):
        self.close()
        self.game1 = Game1()
        self.game1.show()

    def game2(self):
        self.close()
        self.game2 = Game2()
        self.game2.show()

    def add_balance(self):
        self.close()
        self.blnc = Balance()
        self.blnc.show()

    def exitt(self):
        self.close()


class Statistic(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('statistic_ds.ui', self)
        self.pushButton_back.clicked.connect(self.back)

        sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
        self.label_balance_2.setText(str(sql.fetchone()[0]))
        sql.execute(f'SELECT game FROM users WHERE login = "{user_login}"')
        self.label_games_2.setText(str(sql.fetchone()[0]))
        sql.execute(f'SELECT win FROM users WHERE login = "{user_login}"')
        self.label_wins_2.setText(str(sql.fetchone()[0]))
        sql.execute(f'SELECT lose FROM users WHERE login = "{user_login}"')
        self.label_loses_2.setText(str(sql.fetchone()[0]))
        sql.execute(f'SELECT nickname FROM users WHERE login = "{user_login}"')
        self.label_nn_2.setText(str(sql.fetchone()[0]))
        sql.execute(f'SELECT secret FROM users WHERE login = "{user_login}"')
        self.label_word_2.setText(str(sql.fetchone()[0]))
        self.label_name_2.setText(str(user_login))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.back()

    def back(self):
        self.close()
        self.chose = Choose()
        self.chose.show()


class Balance(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('add_balance.ui', self)
        sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
        self.statusBar().showMessage('Баланс: ' + str(sql.fetchone()[0]))
        sql.execute(f"SELECT secret FROM users WHERE login = '{user_login}'")
        self.user_word = sql.fetchone()[0]
        self.pushButton_back.clicked.connect(self.back)
        self.pushButton_cash.clicked.connect(self.plus_balance)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.plus_balance()
        if event.key() == Qt.Key_Escape:
            self.back()

    def back(self):
        self.close()
        self.chose = Choose()
        self.chose.show()

    def plus_balance(self):

        summa = self.lineEdit_cash.text()
        word = self.lineEdit_cash_word.text()
        if summa == '':
            self.statusBar().showMessage('Укажите на сколько хотите пополнить баланс')
        elif summa.isalpha() or int(summa) < 1:
            self.statusBar().showMessage('Введите корректное число')
            self.lineEdit_cash.setText('')
        else:
            if word == str(self.user_word):
                sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
                balance = sql.fetchone()[0]
                sql.execute(f'UPDATE users SET cash = {balance + int(summa)} WHERE login = "{user_login}"')
                db.commit()
                sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
                self.statusBar().showMessage('Ваш баланс успешно пополнен и состовляет: ' + str(sql.fetchone()[0]))
                self.lineEdit_cash.setText('')
                self.lineEdit_cash_word.setText('')
            elif word == '':
                self.statusBar().showMessage('Введите кодовое слово')
            else:
                self.statusBar().showMessage('Неправильное кодовое слово')
                self.lineEdit_cash_word.setText('')


class Game2(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('game2_ds.ui', self)
        self.count = 0
        self.fl = 0
        self.pushButton_strt.clicked.connect(self.begin)
        self.pushButton_end_game.clicked.connect(self.end_game)
        self.pushButton_back.clicked.connect(self.back)
        self.pushButton_still.clicked.connect(self.still)
        sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
        self.lbl_balance.setText(f'Ваш баланс: {str(sql.fetchone()[0])}')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.begin()
        if event.key() == Qt.Key_Escape:
            self.back()

    def back(self):
        if self.fl == 0:
            self.close()
            self.chose = Choose()
            self.chose.show()
        else:
            self.statusBar().showMessage('Невозможно выйти в меню')

    def begin(self):
        if self.fl == 0:
            self.user_stavka = self.lineEdit_stavka.text()
            sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
            balance = sql.fetchone()[0]
            if self.user_stavka == '':
                self.statusBar().showMessage('Укажите вашу ставку')
            elif self.user_stavka.isalpha():
                self.statusBar().showMessage('Введите корректную ставку')
                self.lineEdit_stavka.setText('')
                self.fl = 0
            elif int(self.user_stavka) < 1:
                self.statusBar().showMessage('Введите ставку больше 0')
                self.lineEdit_stavka.setText('')
                self.fl = 0
            elif int(self.user_stavka) > balance:
                self.statusBar().showMessage('У вас недостаточно средств на балансе')
                self.lineEdit_stavka.setText('')
            else:
                self.fl = 1
                score = randint(1, 7)
                self.count += score
                self.statusBar().showMessage('')
                self.label_result.setText(f'Лесник подарил вам: {score}, в корзине: {self.count}')
        else:
            self.statusBar().showMessage('Невозможно сделать ставку во время игры')

    def end_game(self):
        if self.fl == 1:
            self.fl = 0
            self.label_result.setText('')
            sql.execute(f'SELECT game FROM users WHERE login = "{user_login}"')
            game = sql.fetchone()[0]
            sql.execute(f'SELECT win FROM users WHERE login = "{user_login}"')
            win = sql.fetchone()[0]
            sql.execute(f'SELECT lose FROM users WHERE login = "{user_login}"')
            lose = sql.fetchone()[0]
            if int(self.count) == 18:
                self.count = 0
                sql.execute(f'UPDATE users SET lose = {int(win) + 1} WHERE login = "{user_login}"')
                db.commit()
                sql.execute(f'UPDATE users SET game = {int(game) + 1} WHERE login = "{user_login}"')
                db.commit()
                sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
                balance = sql.fetchone()[0]
                sql.execute(f'UPDATE users SET cash = {int(balance) + int(int(self.user_stavka) * 0.3)} '
                            f'WHERE login = "{user_login}"')
                db.commit()
                self.label_result.setText('Поздравляем, вы набрали 18 яблок')
                sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
                balance = sql.fetchone()[0]
                self.lbl_balance.setText(f'Ваш баланс: {str(balance)}')
                self.statusBar().showMessage('Ваш выигрыш составил: ' + str(int(int(self.user_stavka) * 0.3)))
            elif int(self.count) == 19:
                self.count = 0
                sql.execute(f'UPDATE users SET lose = {int(win) + 1} WHERE login = "{user_login}"')
                db.commit()
                sql.execute(f'UPDATE users SET game = {int(game) + 1} WHERE login = "{user_login}"')
                db.commit()
                sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
                balance = sql.fetchone()[0]
                sql.execute(f'UPDATE users SET cash = {int(balance) + int(int(self.user_stavka) * 0.5)} '
                            f'WHERE login = "{user_login}"')
                db.commit()
                self.label_result.setText('Поздравляем, вы набрали 19 яблок')
                sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
                balance = sql.fetchone()[0]
                self.lbl_balance.setText(f'Ваш баланс: {str(balance)}')
                self.statusBar().showMessage('Ваш выигрыш составил: ' + str(int(int(self.user_stavka) * 0.5)))
            elif int(self.count) == 20:
                self.count = 0
                sql.execute(f'UPDATE users SET lose = {int(win) + 1} WHERE login = "{user_login}"')
                db.commit()
                sql.execute(f'UPDATE users SET game = {int(game) + 1} WHERE login = "{user_login}"')
                db.commit()
                sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
                balance = sql.fetchone()[0]
                sql.execute(f'UPDATE users SET cash = {int(balance) + int(int(self.user_stavka) * 0.7)} '
                            f'WHERE login = "{user_login}"')
                db.commit()
                self.label_result.setText('Поздравляем, вы набрали 20 яблок')
                sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
                balance = sql.fetchone()[0]
                self.lbl_balance.setText(f'Ваш баланс: {str(balance)}')
                self.statusBar().showMessage('Ваш выигрыш составил: ' + str(int(int(self.user_stavka) * 0.7)))
            elif int(self.count) == 17:
                self.count = 0
                sql.execute(f'UPDATE users SET lose = {int(win) + 1} WHERE login = "{user_login}"')
                db.commit()
                sql.execute(f'UPDATE users SET game = {int(game) + 1} WHERE login = "{user_login}"')
                db.commit()
                self.label_result.setText('Поздравляем, вы набрали 17 яблок')
                sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
                balance = sql.fetchone()[0]
                self.lbl_balance.setText(f'Ваш баланс: {str(balance)}')
                self.statusBar().showMessage('Ваш выигрыш составил: 0')
            elif int(self.count) < 17:
                sql.execute(f'UPDATE users SET lose = {int(lose) + 1} WHERE login = "{user_login}"')
                db.commit()
                sql.execute(f'UPDATE users SET game = {int(game) + 1} WHERE login = "{user_login}"')
                db.commit()
                sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
                balance = sql.fetchone()[0]
                sql.execute(f'UPDATE users SET cash = {int(balance) - int(self.user_stavka)} '
                            f'WHERE login = "{user_login}"')
                db.commit()
                self.label_result.setText('Вы набрали: ' + str(self.count) + ' и это меньше чем нужно')
                sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
                balance = sql.fetchone()[0]
                self.lbl_balance.setText(f'Ваш баланс: {str(balance)}')
                self.statusBar().showMessage('Вы проиграли: ' + str(self.user_stavka))
                self.count = 0
        else:
            self.statusBar().showMessage('Вам необходимо сделать ставку')

    def still(self):
        if self.fl == 1:
            score = randint(1, 7)
            self.count += score
            sql.execute(f'SELECT game FROM users WHERE login = "{user_login}"')
            game = sql.fetchone()[0]
            sql.execute(f'SELECT win FROM users WHERE login = "{user_login}"')
            win = sql.fetchone()[0]
            sql.execute(f'SELECT lose FROM users WHERE login = "{user_login}"')
            lose = sql.fetchone()[0]
            if self.count == 21:
                self.count = 0
                self.fl = 0
                self.label_result.setText('')
                sql.execute(f'UPDATE users SET lose = {int(win) + 1} WHERE login = "{user_login}"')
                db.commit()
                sql.execute(f'UPDATE users SET game = {int(game) + 1} WHERE login = "{user_login}"')
                db.commit()
                sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
                balance = sql.fetchone()[0]
                sql.execute(f'UPDATE users SET cash = {int(balance) + int(self.user_stavka)} '
                            f'WHERE login = "{user_login}"')
                db.commit()
                self.label_result.setText('Поздравляем, вы набрали 21 яблок')
                sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
                balance = sql.fetchone()[0]
                self.lbl_balance.setText(f'Ваш баланс: {str(balance)}')
                self.statusBar().showMessage('Ваш выигрыш составил: ' + str(self.user_stavka))
            elif self.count > 21:
                self.fl = 0
                self.label_result.setText('')
                sql.execute(f'UPDATE users SET lose = {lose + 1} WHERE login = "{user_login}"')
                db.commit()
                sql.execute(f'UPDATE users SET game = {game + 1} WHERE login = "{user_login}"')
                db.commit()
                sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
                balance = sql.fetchone()[0]
                sql.execute(f'UPDATE users SET cash = {int(balance) - int(self.user_stavka)} '
                            f'WHERE login = "{user_login}"')
                db.commit()
                self.label_result.setText('Вы набрали больше чем нужно: ' + str(self.count))
                sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
                balance = sql.fetchone()[0]
                self.lbl_balance.setText(f'Ваш баланс: {str(balance)}')
                self.statusBar().showMessage('Вы проиграли: ' + str(self.user_stavka))
                self.count = 0
            else:
                self.label_result.setText(f'Лесник подарил вам: {score}, в корзине: {self.count}')
                self.statusBar().showMessage('')
        else:
            self.statusBar().showMessage('Вам необходимо сделать ставку')


class Game1(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('game1_ds.ui', self)
        self.fl = 0
        self.result = 'ЧЕТНОЕ'
        sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
        self.lbl_balance.setText(f'Ваш баланс: {str(sql.fetchone()[0])}')
        self.pushButton_strt.clicked.connect(self.begin)
        self.pushButton_back.clicked.connect(self.back)
        self.pushButton_throw.clicked.connect(self.game)
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radioButton_even)
        self.button_group.addButton(self.radioButton_odd)
        self.button_group.buttonClicked.connect(self.run2)

    def begin(self):
        if self.fl == 0 or self.fl == 2:
            self.user_stavka = self.lineEdit_stavka.text()
            sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
            balance = sql.fetchone()[0]
            if self.user_stavka == '':
                self.statusBar().showMessage('Укажите вашу ставку')
                self.fl = 0
            elif self.user_stavka.isalpha():
                self.statusBar().showMessage('Введите корректную ставку')
                self.lineEdit_stavka.setText('')
                self.fl = 0
            elif int(self.user_stavka) < 1:
                self.statusBar().showMessage('Введите ставку больше 0')
                self.lineEdit_stavka.setText('')
                self.fl = 0
            elif int(self.user_stavka) > balance:
                self.statusBar().showMessage('У вас недостаточно средств на балансе')
                self.lineEdit_stavka.setText('')
                self.fl = 0
            else:
                self.fl = 1
                self.statusBar().showMessage(f'Ваша ставка: {self.user_stavka}')
        else:
            self.statusBar().showMessage('Ваша ставка уже сделана: ' + str(self.user_stavka))

    def game(self):
        sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
        balance = sql.fetchone()[0]
        if self.fl != 0:
            if int(self.user_stavka) > balance:
                self.statusBar().showMessage('У вас недостаточно средств на балансе')
                self.lineEdit_stavka.setText('')
                self.fl = 0
            else:
                self.fl = 2
                self.statusBar().showMessage(f'Ваша ставка: {self.user_stavka}')
                number = randint(1, 12)
                even = range(2, 13, 2)
                odd = range(1, 13, 2)
                if self.result == 'ЧЕТНОЕ':
                    if number in even:
                        self.win_game()
                    else:
                        self.lose_game()
                else:
                    if number in odd:
                        self.win_game()
                    else:
                        self.lose_game()
        else:
            self.statusBar().showMessage('Вам необходимо сделать ставку')

    def run2(self, button):
        self.result = button.text()

    def win_game(self):
        sql.execute(f'SELECT game FROM users WHERE login = "{user_login}"')
        game = sql.fetchone()[0]
        sql.execute(f'SELECT win FROM users WHERE login = "{user_login}"')
        win = sql.fetchone()[0]
        sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
        balance = sql.fetchone()[0]
        sql.execute(f'UPDATE users SET cash = {balance + int(self.user_stavka)} WHERE login = "{user_login}"')
        db.commit()
        self.label_result.setText('Поздравляем, вы выиграли: ' + str(self.user_stavka))
        sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
        self.lbl_balance.setText(f'Ваш баланс: {str(sql.fetchone()[0])}')
        sql.execute(f'UPDATE users SET win = {int(win) + 1} WHERE login = "{user_login}"')
        db.commit()
        sql.execute(f'UPDATE users SET game = {int(game) + 1} WHERE login = "{user_login}"')
        db.commit()

    def lose_game(self):
        sql.execute(f'SELECT game FROM users WHERE login = "{user_login}"')
        game = sql.fetchone()[0]
        sql.execute(f'SELECT lose FROM users WHERE login = "{user_login}"')
        lose = sql.fetchone()[0]
        sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
        balance = sql.fetchone()[0]
        sql.execute(f'UPDATE users SET cash = {balance - int(self.user_stavka)} WHERE login = "{user_login}"')
        db.commit()
        self.label_result.setText('К сожалению, вы проиграли: ' + str(self.user_stavka))
        sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
        self.lbl_balance.setText(f'Ваш баланс: {str(sql.fetchone()[0])}')
        sql.execute(f'UPDATE users SET lose = {int(lose) + 1} WHERE login = "{user_login}"')
        db.commit()
        sql.execute(f'UPDATE users SET game = {int(game) + 1} WHERE login = "{user_login}"')
        db.commit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            if self.fl == 2:
                if self.user_stavka == self.lineEdit_stavka.text():
                    self.game()
                else:
                    self.begin()
            elif self.fl == 1:
                self.game()
            else:
                self.begin()

        if event.key() == Qt.Key_Escape:
            self.back()

    def back(self):
        if self.fl == 0 or self.fl == 2:
            self.close()
            self.chose = Choose()
            self.chose.show()
        else:
            self.statusBar().showMessage('Невозможно выйти в меню')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Enterance()
    ex.show()
    sys.exit(app.exec_())
