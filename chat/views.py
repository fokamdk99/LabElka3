from django.shortcuts import render
from django.contrib.auth import get_user_model
User = get_user_model()
from chat.models import Conversation, Message

# Create your views here.
def conversation(request):
    return render(request, "chat/conversation.html")

def chat_index(request, friend_username):
    print("wchodze w chat_index")
    context = {}
    usr = request.user
    context['user'] = usr
    friend = User.objects.get(username=friend_username)
    context['friend'] = friend
    
    usernames = []
    usernames.append(usr)
    usernames.append(friend.username)
    #konwersacje = Conversation.objects.filter(related_users__username__in=usernames)
    '''tmp = get_recent_conversations(usr)
    if tmp is None:
        print('nic nie ma w konwersacjach')
    else:
        context['konwersacje'] = tmp'''
    
    conversation_data = get_messages(usr.username, friend.username)
    if(conversation_data is not None):
        konwersacja = conversation_data[0]
        messages=conversation_data[1]
        context = {
            'konwersacja':konwersacja,
            #'konwersacje': konfy,   #konwersacje.order_by('-last_spoken_with'),
            #'user':usr,
            'messages':messages
    }
    else:
        context = {}
    context['konwersacje']=get_recent_conversations(usr)

    '''print('zaczynam zbierac recent conversations')
    recent_konwersacje = Conversation.objects.filter(related_users__username__contains=usr.username)
    print("tu juz zaczynam od poczatku")
    konfy = []
    for konfa in recent_konwersacje:
        friends = konfa.related_users.all().values('username')
        tmp = friends[0]
        tmp = tmp['username']
        if (tmp!=usr.username):
            friend=friends[0]
        else:
            friend=friends[1]
        
        if(konfa.messages.all().exists()):
            najnowsza_wiadomosc=konfa.messages.order_by('-timestamp')[0]
            print(f"chat_index: friend to {friend['username']}, new info to: {najnowsza_wiadomosc.content}")
            results = {'friend':friend['username'], 'konwersacja':konfa, 'najnowsza_wiadomosc':najnowsza_wiadomosc.content}
        else:
            najnowsza_wiadomosc='Napisz wiadomosc!'
        #najnowsza_wiadomosc=konfa.messages.order_by('-timestamp')[0]
        #print(f"chat_index: friend to {friend['username']}, new info to: {najnowsza_wiadomosc.content}")
            results = {'friend':friend['username'], 'konwersacja':konfa, 'najnowsza_wiadomosc':najnowsza_wiadomosc}
        konfy.append(results)
        context['konwersacje'] = konfy'''
    

    
    #konwersacje = usr.konwersacja_set.all()
    #print(f"chat_index: friend to {context['friend'].username}")
    context['friend']=friend_username
    return render(request, 'chat/conversation.html', context)

def get_messages(username, friend): #znajdz wiadomosci dotyczace danej konwersacji
    print("wchodze w get_messages")
    konwersacje = Conversation.objects.filter(related_users__username__contains=username).filter(related_users__username__contains=friend)
    print(f"get_messages: usernames: {username} oraz {friend}")
    for konfa in konwersacje:
        print(f"konfa: {konfa}")
        if(konfa.related_users.count() == 2):
            konwersacja = konfa
    if konwersacja is not None:
        messages = konwersacja.messages.all()
        for ms in messages:
            print(f"wiadomosc: {ms.content}")

        results = []
        results.append(konwersacja)    
        results.append(messages)
        return results

def get_recent_conversations(user):
    print("wchodze w get_recent_conversations")
    recent_konwersacje = Conversation.objects.filter(related_users__username__contains=user.username)

    konfy = []
    for konfa in recent_konwersacje:
        friends = konfa.related_users.all().values('username')
        tmp = friends[0]
        tmp = tmp['username']
        if (tmp!=user.username):
            friend=friends[0]
        else:
            friend=friends[1]
        
        if(konfa.messages.all().exists()):
            najnowsza_wiadomosc=konfa.messages.order_by('-timestamp')[0]
            print(f"get_recent_conversations: friend to {friend['username']}, new info to: {najnowsza_wiadomosc.content}")
            results = {'friend':friend['username'], 'konwersacja':konfa, 'najnowsza_wiadomosc':najnowsza_wiadomosc.content}
        else:
            najnowsza_wiadomosc='Napisz wiadomosc!'
        #najnowsza_wiadomosc=konfa.messages.order_by('-timestamp')[0]
        #print(f"chat_index: friend to {friend['username']}, new info to: {najnowsza_wiadomosc.content}")
            results = {'friend':friend['username'], 'konwersacja':konfa, 'najnowsza_wiadomosc':najnowsza_wiadomosc}
        konfy.append(results)
    return konfy