class Player():
    def __init__(self):
        self.player_hand = list() 
        self.current_money = 100
        self.has_changed_hand = False
        
    def bet(self, money_to_bet):
        if money_to_bet < self.current_money:
            self.current_money -= money_to_bet
        else:
            self.current_money -= 1
            return 1
        
        return money_to_bet
    
    
    def change_card(self):
        if not self.has_changed_hand:
            self.player_hand = list()
            self.has_changed_hand = True
    
    
    def flop(self):
        for i in range(3):
            self.community_cards.append(self.deck.draw_card())

    def turn(self):
        self.community_cards.append(self.deck.draw_card())

    def river(self):
        self.community_cards.append(self.deck.draw_card())

    def player_fold(self):
        self.inactive_players.append(self.current_player)
        self.active_players.remove(self.current_player)
        self.current_player = self.get_next_player()

    def player_call(self):
        self.current_player.bet(self.current_bet - self.current_player.total_bet)
        self.pot += self.current_player.bet_amount
        self.current_player = self.get_next_player()

    def player_raise(self):
        amount_to_raise = self.current_player.on_player_raise()
        if amount_to_raise < self.minimum_bet:
            self.player_call()
            return

        total_bet = self.current_bet + amount_to_raise
        self.current_player.bet(total_bet - self.current_player.total_bet)
        self.pot += self.current_player.bet_amount
        self.current_bet = total_bet
        self.current_player = self.get_next_player()
    