from flask import Flask

app = Flask(__name__)
import codeitsuisse.routes.cryptoCollapz
import codeitsuisse.routes.rubiks
import codeitsuisse.routes.rubikstest
import codeitsuisse.routes.square
import codeitsuisse.routes.tickerStream
import codeitsuisse.routes.travellingSuisseRobot
import codeitsuisse.routes.quordleKeyboard
import codeitsuisse.routes.calendarDays
import codeitsuisse.routes.swizz
import codeitsuisse.routes.dns
