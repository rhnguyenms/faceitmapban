import requests
import concurrent.futures

def fetch_match_details(match_id, api_key):
    url = f"https://open.faceit.com/data/v4/matches/{match_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_player_stats(player_id, game_id, api_key):
    url = f"https://open.faceit.com/data/v4/players/{player_id}/stats/{game_id}"
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_all_player_stats(players, game_id, api_key):
    def fetch_stats(player):
        return fetch_player_stats(player['player_id'], game_id, api_key)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_stats, players))
    return results

def calculate_weighted_winrate(match_details, api_key):
    game_id = match_details['game']
    teams_info = {'faction1': {'total_matches': 0, 'maps': {}}, 'faction2': {'total_matches': 0, 'maps': {}}}

    for faction in ['faction1', 'faction2']:
        players = match_details['teams'][faction]['roster']
        faction_total_matches = sum([int(player['game_skill_level']) for player in players])

        player_stats_list = fetch_all_player_stats(players, game_id, api_key)

        for player_stats in player_stats_list:
            for segment in player_stats.get('segments', []):
                if segment['mode'] == '5v5' and segment['type'] == 'Map':
                    map_name = segment['label']
                    matches = int(segment['stats']['Matches'])
                    win_rate = float(segment['stats'].get('Win Rate %', 0))

                    if map_name not in teams_info[faction]['maps']:
                        teams_info[faction]['maps'][map_name] = {'win_rate_sum': 0, 'weighted_matches': 0, 'confidence_score_sum': 0}

                    confidence_score = matches / faction_total_matches
                    teams_info[faction]['maps'][map_name]['confidence_score_sum'] += confidence_score
                    teams_info[faction]['maps'][map_name]['win_rate_sum'] += win_rate * confidence_score
                    teams_info[faction]['maps'][map_name]['weighted_matches'] += matches

    for faction, info in teams_info.items():
        for map_name, data in info['maps'].items():
            adjusted_win_rate = (data['win_rate_sum'] / data['confidence_score_sum']) if data['confidence_score_sum'] > 0 else 0
            info['maps'][map_name]['win_rate'] = adjusted_win_rate

    return teams_info

def recommend_map_bans(teams_info):
    recommendations = {'ban_against_faction1': [], 'ban_against_faction2': []}

    for faction, info in teams_info.items():
        sorted_maps = sorted(info['maps'].items(), key=lambda x: x[1]['win_rate'], reverse=True)
        recommendations[f'ban_against_{faction}'] = [map_name for map_name, _ in sorted_maps[:3]]

    return recommendations

if __name__ == "__main__":
    api_key = "88579df0-eb57-4232-bc56-044f9f35ecaf"
    print("Please enter a match ID:")
    match_id = input().strip()
    match_details = fetch_match_details(match_id, api_key)
    teams_info = calculate_weighted_winrate(match_details, api_key)
    recommendations = recommend_map_bans(teams_info)

    team_name_1 = match_details['teams']['faction1']['name']
    team_name_2 = match_details['teams']['faction2']['name']

    print(f"Recommended Map Bans Against {team_name_1}:", recommendations['ban_against_faction1'])
    print(f"Recommended Map Bans Against {team_name_2}:", recommendations['ban_against_faction2'])
