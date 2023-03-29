import random
from flaskr.Deck import Deck
from flaskr.Player import Player


class PokerGame:
    def __init__(self, number_of_players):
        self.deck = Deck()
        self.pot = 0
        self.players = list()
        for single_player in range(number_of_players):
            self.players.append(Player())
        self.table_cards = list()
        self.current_bet = 0
        self.minimum_bet = 10
        self.active_players = []
        self.inactive_players = []
        self.current_player = None
        self.round_count = 0
        
    def start_game(self):
        self.put_table_card()
        self.deal_cards()
        
        self.current_player = self.players[0]
        self.active_players = self.players.copy()
        self.inactive_players = []
        self.round_count = 0
        #self.ask_players_for_action()

    def deal_cards(self):
        #for player in self.players:
        for index in range(len(self.players)):
            self.players[index].hand = [self.deck.pick_cards(5)]
            print(self.players[index].hand, flush=True)

    def put_table_card(self):
        self.table_cards = self.deck.pick_cards(5)

    def place_bet(self, bet):
        self.pot += bet
    
    def place_small_blind(self):
        small_blind_player = self.players[(self.dealer_position + 1) % len(self.players)]
        small_blind_player.bet(self.minimum_bet // 2)
        self.pot += small_blind_player.bet_amount

    def place_big_blind(self):
        big_blind_player = self.players[(self.dealer_position + 2) % len(self.players)]
        big_blind_player.bet(self.minimum_bet)
        self.pot += big_blind_player.bet_amount

    def ask_players_for_action(self):
        self.round_count += 1
        if self.round_count == 1:
            self.burn_card()
            self.flop()
        elif self.round_count == 2:
            self.burn_card()
            self.turn()
        elif self.round_count == 3:
            self.burn_card()
            self.river()
        else:
            self.end_game()
            return
        
        for player in self.active_players:
            if player == self.current_player:
                continue
            player.on_player_turn()
            
        action = self.current_player.on_player_turn()
        if action == 'fold':
            self.player_fold()
        elif action == 'call':
            self.player_call()
        elif action == 'raise':
            self.player_raise()
        else:
            self.ask_players_for_action()

    def burn_card(self):
        self.deck.draw_card()

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

    def get_hand_score(hand):
        """
        Calcola lo score della mano del giocatore
        """
        # Estrae i valori e i semi delle carte
        ranks = [card.rank for card in hand]
        suits = [card.suit for card in hand]

        # Conta le occorrenze dei valori delle carte
        rank_counts = {rank: ranks.count(rank) for rank in ranks}

        # Controlla se ci sono coppie, tris, ecc.
        pair_ranks = [rank for rank, count in rank_counts.items() if count == 2]
        three_of_a_kind_ranks = [rank for rank, count in rank_counts.items() if count == 3]
        four_of_a_kind_ranks = [rank for rank, count in rank_counts.items() if count == 4]

        # Controlla se la mano contiene una scala
        is_straight = False
        unique_ranks = list(set(ranks))
        unique_ranks.sort()
        if len(unique_ranks) == 5 and (unique_ranks[-1] - unique_ranks[0] == 4):
            is_straight = True

        # Controlla se la mano contiene un colore
        is_flush = len(set(suits)) == 1

        # Controlla se la mano contiene una scala reale
        is_straight_flush = is_straight and is_flush and (ranks[0] == "10")

        # Calcola lo score della mano in base ai criteri sopra descritti
        if is_straight_flush:
            return 9
        elif four_of_a_kind_ranks:
            return 8
        elif three_of_a_kind_ranks and pair_ranks:
            return 7
        elif is_flush:
            return 6
        elif is_straight:
            return 5
        elif three_of_a_kind_ranks:
            return 4
        elif len(pair_ranks) == 2:
            return 3
        elif pair_ranks:
            return 2
        else:
            return 1