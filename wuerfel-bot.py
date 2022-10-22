import numpy

class Game:
    def __init__(self, player_count):
        self.player_count = player_count
        self.current_player = 0
        self.player_health = numpy.arange(player_count, dtype=int)
        self.player_health.fill(25)
        self.players = array([f"{i}" for i in range(player_count)])

def check_for_winner(self):
    dead_players = 0
    for player_health in self.player_health:
        if player_health <= 0:
            dead_players += 1
    if dead_players == self.player_count - 1:
        return True
    return False

def determine_next_player(self):
    if check_for_winner(self):
        return -1
    
    self.current_player = (self.current_player + 1) % self.player_count
    while self.player_health[self.current_player] <= 0:
        self.current_player += 1
        if self.current_player >= self.player_count:
            self.current_player = 0

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, filters, MessageHandler, Updater

token = ""

PLAYER_COUNT, GAME_MOVE, DECREASE_HEALTH = range(3)

currentGames = {}

def read_token() -> str:
    token_file = open("token.txt")
    token = token_file.read()
    token_file.close()
    return token

def read_files():
    global token
    token = read_token()

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Servas {update.effective_user.first_name}!')

async def new_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f'Wövü Spiela sansn?')
    return PLAYER_COUNT

async def player_count(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currentGames[update.message.chat_id] = Game(int(update.message.text))
    current_player = currentGames[update.message.chat_id].current_player
    await update.message.reply_text(
        "Nice dann gemmas au\n"
        f"Spieler {current_player}, wövü host di den obgwürflt?\n"
        "(wennst mehr wie 25 gwürflt host, gibst 0 ein)"
    )
    return GAME_MOVE

async def game_move(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currentGame = currentGames[update.message.chat_id]
    if int(update.message.text) > 0:
        currentGame.player_health[currentGame.current_player] -= int(update.message.text)
        if currentGame.player_health[currentGame.current_player] <= 0:
            await update.message.reply_text(f"Spieler {currentGame.current_player} is vareckt")
    elif int(update.message.text) == 0:
        await update.message.reply_text("Wövü hostn in nächstn obagwürflt?")
        return DECREASE_HEALTH

    if determine_next_player(currentGame) == -1:
        await update.message.reply_text(f"Spieler {currentGame.current_player} hod gwunna")
        return ConversationHandler.END

    await update.message.reply_text(f"Spieler {currentGame.current_player}, wövü hostn di obagwürflt?")

    return GAME_MOVE

async def decrease_health(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currentGame = currentGames[update.message.chat_id]
    determine_next_player(currentGame)
    currentGame.player_health[currentGame.current_player] -= int(update.message.text)

    if currentGame.player_health[currentGame.current_player] <= 0:
        await update.message.reply_text(f"Spieler {currentGame.current_player} is vareckt")
        
        if determine_next_player(currentGame) == -1:
            await update.message.reply_text(f"Spieler {currentGame.current_player} hod gwunna")
            return ConversationHandler.END 

    await update.message.reply_text(f"Spieler {currentGame.current_player}, wövü hostn di obagwürflt?")

    return GAME_MOVE


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    player_count = update.message.from_user
    await update.message.reply_text("Jo dann hoid doch ned")

    return ConversationHandler.END

def main():
    read_files()
    application = ApplicationBuilder().token(token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('new_game', new_game)],
        states={
            PLAYER_COUNT: [MessageHandler(filters.Regex("^\\d+$"), player_count)],
            GAME_MOVE: [MessageHandler(filters.Regex("^\\d+$"), game_move)],
            DECREASE_HEALTH: [MessageHandler(filters.Regex("^\\d+$"), decrease_health)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    application.add_handler(CommandHandler("hello", hello))
    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == '__main__':
    main()