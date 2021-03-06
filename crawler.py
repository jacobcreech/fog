import urllib2
import json
import Queue
import time
import random
import sys

api_key = open('api_key.txt')
key = api_key.read()
api_key.close()
getSummaries = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='
getOwnedGames = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='
#getFriendsList = 'http://api.steampowered.com/ISteamUser/GetFriendList/v0001/?key='
queue = Queue.Queue()
counter = 0


def get_games():
    global counter
    while not queue.empty():
        current_user = str(queue.get())
        try:
            summaries = json.loads(urllib2.urlopen(getSummaries + key + '&steamids=' + current_user + '&format=json', timeout = 10).read())
        except urllib2.URLError, e:
            print "URLError(getSummaries): ", e.reason
            print "User ID:", current_user
            queue.put(current_user)
            continue
        except urllib2.HTTPError, e:
            print "HTTPError(getSummaries): ", e.code
            print "User ID:", current_user
            queue.put(current_user)
            continue
        except:
            e = sys.exc_info()[0]
            print 'getSummaries:', e
            print "User ID:", current_user
            queue.put(current_user)
            continue

        if 'response' in summaries and 'players' in summaries['response'] and len(summaries['response']['players']) > 0 and 'communityvisibilitystate' in summaries['response']['players'][0]:
            if summaries['response']['players'][0]['communityvisibilitystate'] == 3:
                try:
                    owned_games = json.loads(urllib2.urlopen(getOwnedGames + key + '&steamid=' + current_user + '&include_played_free_games=1&format=json', timeout = 10).read())
                except urllib2.URLError, e:
                    print "URLError(getOwnedGames): ", e.reason
                    print "User ID:", current_user
                    queue.put(current_user)
                    continue
                except urllib2.HTTPError, e:
                    print "HTTPError(getOwnedGames): ", e.code
                    print "User ID:", current_user
                    queue.put(current_user)
                    continue
                except:
                    e = sys.exc_info()[0]
                    print 'getOwnedGames:', e
                    print "User ID:", current_user
                    queue.put(current_user)
                    continue

                #user_owned_games[current_user] = owned_games
                dictionary_file = open('dictionary.txt', 'a')
                dictionary_file.write(str(current_user) + ' ' + str(owned_games) + '\n')
                dictionary_file.close()
                counter += 1
                print current_user, counter

                '''try:
                    friend_list = json.loads(urllib2.urlopen(getFriendsList + key + '&steamid=' + current_user + '&format=json', timeout = 10).read())
                except urllib2.URLError, e:
                    print "URLError: ", e.reason
                    print "User ID:", current_user
                    queue.put(current_user)
                    continue

                except urllib2.HTTPError, e:
                    print "HTTPError: ", e.code
                    print "User ID:", current_user
                    queue.put(current_user)
                    continue

                except:
                    e = sys.exc_info()[0]
                    print e
                    print "User ID:", current_user
                    queue.put(current_user)
                    continue

                for friend in friend_list['friendslist']['friends']:
                    friend_id = friend['steamid']
                    if friend_id not in user_set:
                        queue.put(friend_id)
                        user_set.append(friend_id)'''
        #while not temp_queue.empty():
         #   queue_file.write(temp_queue.get() + '\n')
        queue_file = open('queue.txt', 'w')
        for elem in list(queue.queue):
            queue_file.write(str(elem) + '\n')
        queue_file.close()
        time.sleep(random.randint(1, 2))


def main():
    try:
        queue_file = open('queue.txt', 'r')
        for line in queue_file:
            queue.put(line[:17])
        queue_file.close()

        global counter
        dict_file = open('dictionary.txt', 'r')
        for line in dict_file:
            counter += 1
        dict_file.close()
    except IOError, e:
        pass
    get_games()

main()
