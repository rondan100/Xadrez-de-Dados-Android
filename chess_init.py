from re import compile

def pull_results(Bsoup):
        clean = []
        pull = Bsoup.findAll('span', attrs={'class': compile("icon(.*?)square")})

        # Clean to make useable 
        for i in pull:
            if 'minus' in str(i): 
                clean.append('loss')
            elif 'plus' in str(i): 
                clean.append('win')
            elif 'equal' in str(i):
                clean.append('draw')
            else:
                clean.append('error')
        
        return clean

def pull_moves(Bsoup):
    moves = []
    for i in Bsoup.findAll('td', attrs={'class': compile("table-text-center")}):
        if i.find('span'):
            moves.append(int(i.find('span').text))
    
    return moves

def pull_dates(Bsoup):
    dates = []
    for i in Bsoup.findAll('td', attrs={'class': compile("table-text-right archive-games-date-cell")}):
        dates.append(i.getText().strip())
    
    return dates

def pull_speed(Bsoup):
    times = []
    for i in Bsoup.findAll('span', attrs={'class': compile("archive-games-game-time")}):
        times.append((i.getText().strip()))
    
    return times

def remove_dups(duplicate): 
    final_list = [] 
    for num in duplicate: 
        if num not in final_list: 
            final_list.append(num) 
    return final_list

def pull_game_links(Bsoup):
    links = []
    for i in Bsoup.findAll('td', attrs={'class': compile("table-text-center archive-games-analyze-cell")}):
        for j in i.findAll('a'):
            links.append(j.get('href'))
            
    return remove_dups(links)

def find_color(text):
    if 'white' in str(text):
        return 'white'
    elif 'black' in str(text):
        return 'black'
    else:
        return 'error'

def pull_player_stats(Bsoup):
    my_elo_lst = []
    opponent_elo_lst = []
    opponent_country_lst = []
    opponent_name_lst = []
    my_color_lst = []
    for cell in Bsoup.findAll('td', {'class':'archive-games-user-cell'}):
        # Split the halves
        top_half = cell.findAll('div', {'class': 'post-view-meta-user'})[0]
        bottom_half = cell.findAll('div', {'class': 'post-view-meta-user'})[1]
        
        top_color = find_color(cell.findAll('span')[0])
        bottom_color = find_color(cell.findAll('span')[2])
        
        # Logic to see if I'm top player or bottom player
        if top_half.text.strip().split('\n')[0] == 'rondan1000':
            my_elo= top_half.find('span', {'class':'post-view-meta-rating'}).text
            my_color= top_color
            opponent_elo = bottom_half.find('span', {'class':'post-view-meta-rating'}).text
            opponent_country = bottom_half.find('div').get('v-tooltip')
            opponent_name = bottom_half.text.strip().split('\n')[0]
        else: 
            my_elo= bottom_half.find('span', {'class':'post-view-meta-rating'}).text
            my_color= bottom_color
            opponent_elo = top_half.find('span', {'class':'post-view-meta-rating'}).text
            opponent_country = top_half.find('div').get('v-tooltip')
            opponent_name = top_half.text.strip().split('\n')[0]        
        
        # Clean
        my_elo = int(my_elo.replace('(','').replace(')', ''))
        opponent_elo = int(opponent_elo.replace('(','').replace(')', ''))
        opponent_country = opponent_country.replace("'", "")
        
        # Gather data 
        my_elo_lst.append(my_elo)
        my_color_lst.append(my_color)
        opponent_elo_lst.append(opponent_elo)
        opponent_country_lst.append(opponent_country)
        opponent_name_lst.append(opponent_name)

    return(my_elo_lst, opponent_elo_lst, opponent_country_lst, opponent_name_lst, my_color_lst)

# # Initialize
# def chess_initt():
#     results = []
#     moves = []
#     dates = []
#     speed = []
#     games = []
#     my_elo = []
#     my_color = []
#     opponent_elo = []
#     opponent_country = []
#     opponent_name = []
#     # self.nick = nick
#     nick = """heru007"""
#     chesscom = """https://www.chess.com/games/archive/"""+nick+"""?
#                     gameOwner=other_game&gameTypes%5B0%5D=chess960
#                     &gameTypes%5B1%5D=daily&gameType=live&page={}"""

#     for i in range(1,33):
#         # Get the page
#         text = requests.get(chesscom.format(i)).text
#         # Soupify
#         b = BeautifulSoup(text, 'html.parser')
        
#         # Collect results
#         results += pull_results(b)
#         moves += pull_moves(b)
#         dates += pull_dates(b)
#         speed += pull_speed(b)
#         games += pull_game_links(b)
#         my_elo += pull_player_stats(b)[0]
#         opponent_elo += pull_player_stats(b)[1]
#         opponent_country += pull_player_stats(b)[2]
#         opponent_name += pull_player_stats(b)[3]
#         my_color += pull_player_stats(b)[4]
        
#         # Check progress
#         print(i)
        
#     # Make Df
#     d = {'date': dates,
#         'result': results,
#         'moves': moves,
#         'speed': speed,
#         'link': games,
#         'my_elo': my_elo,
#         'opponent_elo': opponent_elo,
#         'opponent_country': opponent_country,
#         'opponent_name': opponent_name,
#         'color': my_color
#     }

#     games_df = pd.DataFrame(d)

#     # Escreve as partidas em arquivo .csv
#     games_df.to_csv(path_or_buf='chess_games.csv')

# # def matrix(importar,plot):
# #     if importar == 1:
# #         chess_initt()

# #     if plot == 0:
#     games_df = pd.read_csv('chess_games.csv', index_col=0)

#     games_df.set_index(games_df.index[::-1], drop=True, inplace=True)
#     games_df['date'] = pd.to_datetime(games_df['date'])

#     speed_games = games_df[games_df.speed=='10 min']
#     speed_games.reset_index(drop=True, inplace=True)
#     speed_games.set_index(speed_games.index[::-1], drop=True, inplace=True)

#     speed_games['my_elo_ma'] = speed_games['my_elo'][::-1].rolling(window=30).mean()
#     speed_games['result'] = pd.Series(np.where(speed_games.result.values == 'win', 1, 0), speed_games.index)

# # def graph_1():
# #     from matrix import 
#     sns.set_style("whitegrid")
#     plt.figure(figsize=(13, 7))

#     sns.lineplot(y='my_elo', 
#                 x=speed_games.index,
#                 data=speed_games, 
#                 color='darkslategray')

#     sns.lineplot(y='my_elo_ma', 
#                 x=speed_games.index,
#                 data=speed_games, 
#                 color='red')

#     plt.xlabel('Number of Games', fontsize=11)
#     plt.ylabel('My Elo', fontsize=13)
#     plt.title('My Elo Over Time', fontsize=13)
#     plt.xlim(-20)
#     # plt.xlim(right=2000)
#     # print(games_df)
#     # print(speed_games["date"])
#     plt.legend(['elo', '30-day MA'])
#     plt.subplots_adjust(bottom=0.12)

#     # plt.show()
# # elif plot == 1:
#     board = np.zeros((8,8,3))
#     board += 0.5 # "Black" color
#     board[::2, ::2] = 1 # "White" color
#     board[1::2, 1::2] = 1 # "White" color

#     positions = [1, 5, 7, 2, 0, 3, 6, 4]

#     fig, ax = plt.subplots()
#     ax.imshow(board, interpolation='nearest')

#     queen = plt.imread('town.png')
#     extent = np.array([-0.4, 0.4, -0.4, 0.4]) # (0.5 would be the full cell)
#     for y, x in enumerate(positions):
#         ax.imshow(queen, extent=extent + [x, x, y, y])

#     ax.set(xticks=[], yticks=[])
#     ax.axis('image')

# # matrix(0)

