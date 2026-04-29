from django.shortcuts import render, redirect
import random
from . models import Score

def home(request):
    context = {
        'player_name': 'hero',
        'player_health': 100,
        'enemies':["Goblin","Orc","Dragon"]
    }
    return render(request, 'battle/home.html',context)

def game(request):

    # request.session.flush()
    player_max_health = request.session.get('player_max_health', 35)
    enemy_health = request.session.get('enemy_health', 30)
    enemy_stats = request.session.get('enemy_stats', {'Goblin':30,'Orc':60,'Dragon':100})
    enemy_name= request.session.get('enemy_name', 'Goblin')
    max_hp = enemy_stats.get(enemy_name, 30)
    context ={
        'player_name': request.session.get('player_name', 'Hero'),
        'player_health': request.session.get('player_health', 35),
        'enemy_name': enemy_name,
        'enemy_health': enemy_health,
        
        'enemy_max_health':max_hp,
        'enemy_health_percent':(enemy_health/max_hp) * 100,
        'player_max_health': player_max_health,
        'player_health_percent': (35 / player_max_health) * 100,
        'potion':request.session.get('potion', 0),
        'score': request.session.get('score', 0),
        'difficulty': request.session.get('difficulty', 'normal'),

    }
    return render(request, 'battle/game.html',context)

def attack(request):
    player_health=request.session.get('player_health', 35)
    enemy_health=request.session.get('enemy_health', 30)
    enemy_name = request.session.get('enemy_name','Goblin')
    player_max_health = request.session.get('player_max_health', 35)
    enemy_damage_max = request.session.get('enemy_damage_max', 15)
    
    enemy_stats = request.session.get('enemy_stats', {'Goblin': 30,'Orc': 60,'Dragon':100})
    max_hp = enemy_stats.get(enemy_name, 30)
    
    
    message=''

    player_damage = random.randint(1,20)
    enemy_health -= player_damage
    request.session['enemy_health']=enemy_health
    request.session['score'] = request.session.get('score', 0) + player_damage
    enemy_health = max(0, enemy_health)
    
    
    enemy_damage = random.randint(1, enemy_damage_max)
    player_health -= enemy_damage
    player_health = max(0, player_health)
    request.session['player_health']= player_health
    message = f'You hit {enemy_name} for {player_damage} damage! {enemy_name} hits you for {enemy_damage} damage!'

    if enemy_health <= 0:
        if enemy_name == 'Goblin':
            player_health += 35
            if player_health > 70:
                player_health = 70

            request.session['player_max_health'] = 70
            player_max_health = 70
            message = 'You defeated Goblin! Level Up! HP: 70 💪 Next enemy: Orc ⚔️'
            request.session['enemy_health'] = enemy_stats['Orc']
            request.session['enemy_name'] = 'Orc'
            request.session['player_health'] = player_health
            context = {
                'player_name': request.session.get('player_name', 'Hero'),
                'player_health': player_health,
                'enemy_name': 'Orc',
                'enemy_health': enemy_stats['Orc'],
                'enemy_max_health': enemy_stats['Orc'],  # ← correct max!
                'enemy_health_percent': 100,              # ← full health!
                'player_max_health': player_max_health,
                'player_health_percent': (player_health / player_max_health) * 100,
                'message': message,
                'game_over': False,
                'potion': request.session.get('potion', 0),
                'score':request.session.get('score', 0),
                'difficulty': request.session.get('difficulty', 'normal'),
            }
            return render(request, 'battle/game.html', context)
        
        elif enemy_name == 'Orc':
            player_health += 50
            if player_health > 120:
                player_health = 120

            request.session['player_max_health'] = 120
            player_max_health = 120
            message = 'You defeated Orc! Level Up! HP: 120 💪 Next enemy: Dragon 🐉'
            request.session['enemy_health'] = enemy_stats['Dragon']
            request.session['enemy_name'] = 'Dragon'
            request.session['player_health'] = player_health
            context = {
                'player_name': request.session.get('player_name', 'Hero'),
                'player_health': player_health,
                'enemy_name': 'Dragon',
                'enemy_health': enemy_stats['Dragon'],
                'enemy_max_health': enemy_stats['Dragon'],  # ← correct max!
                'enemy_health_percent': 100,                # ← full health!
                'player_max_health': player_max_health,
                'player_health_percent': (player_health / player_max_health) * 100,
                'message': message,
                'game_over': False,
                'potion': request.session.get('potion', 0),
                'score':request.session.get('score', 0),
                'difficulty': request.session.get('difficulty', 'normal'),
            }
            return render(request, 'battle/game.html', context)
        
        elif enemy_name == 'Dragon':
            message = 'You defeated Dragon! YOU WIN! 🎉👑'
            request.session['game_over'] = True
            Score.objects.create(
                name = request.session.get('player_name', 'Hero'),
                score = request.session.get('score', 0),
                
            )
    request.session['player_health'] = player_health
    # else:
    #     message = f'You hit {enemy_name} for {player_damage} damage!'
    if player_health <= 0:
        message = 'You were defeat... Game Over! 💀'
        request.session['game_over']= True
    
    context ={
        'player_name': request.session.get('player_name', 'Hero'),
        'player_health':player_health,
        'enemy_name':request.session.get('enemy_name','Goblin'),
        'enemy_health':max(0, enemy_health),
        'message':message,
        'game_over': request.session.get('game_over', False),
        
        'enemy_max_health':max_hp,
        'enemy_health_percent': max(0, enemy_health / max_hp) *100,
        'player_max_health': player_max_health,
        'player_health_percent': (player_health / player_max_health) * 100,
        'potion':request.session.get('potion', 0),
        'score': request.session.get('score', 0),
        'difficulty': request.session.get('difficulty', 'normal'),
    }
    return render(request, 'battle/game.html', context)

def start(request):
    player_name = request.POST.get('player_name', 'Hero')
    difficulty = request.POST.get('difficulty', 'normal')

    if difficulty == "easy":
        enemies = {'Goblin': 20, 'Orc':40,'Dragon':70}
        enemy_damage_max=10
    elif difficulty == 'hard':
        enemies = {'Goblin': 50, 'Orc':90,'Dragon':150}
        enemy_damage_max=20
    else:
        enemies = {'Goblin': 30, 'Orc':60,'Dragon':100}
        enemy_damage_max=15

    request.session.flush()
    request.session['enemy_stats'] = enemies
    request.session['enemy_damage_max'] = enemy_damage_max
    request.session['player_name'] = player_name
    request.session['player_health'] = 35
    request.session['enemy_health'] = enemies['Goblin']
    request.session['enemy_name'] = 'Goblin'
    request.session['game_over'] = False
    request.session['player_max_health'] = 35
    request.session['potion'] = 1
    request.session['score'] = 0
    request.session['difficulty'] = difficulty

    return redirect('/game/')


    
def potion(request):
    player_health=request.session.get('player_health', 35)
    player_max_health=request.session.get('player_max_health', 35)

    player_health+=30

    if player_health > player_max_health:
        player_health = player_max_health

    request.session['player_health']=player_health
    request.session['potion']=0

    return redirect('/battle/')  

def leaderboard(request):
    scores = Score.objects.all().order_by('-score')
    context = {
        'scores':scores,
    }
    return render(request, 'battle/leaderboard.html', context)

def battle(request):
    player_health = request.session.get('player_health', 35)
    player_max_health = request.session.get('player_max_health', 35)
    enemy_health = request.session.get('enemy_health', 30)
    enemy_name = request.session.get('enemy_name', 'Goblin')
    enemy_stats = request.session.get('enemy_stats', {'Goblin': 30, 'Orc': 60, 'Dragon': 100})
    max_hp = enemy_stats.get(enemy_name, 30)

    context = {
        'player_name': request.session.get('player_name', 'Hero'),
        'player_health': player_health,
        'player_max_health': player_max_health,
        'player_health_percent': (player_health / player_max_health) * 100,
        'enemy_name': enemy_name,
        'enemy_health': enemy_health,
        'enemy_max_health': max_hp,
        'enemy_health_percent': (enemy_health / max_hp) * 100,
        'message': '🧪 Potion used! +30 HP!',
        'game_over': request.session.get('game_over', False),
        'potion': request.session.get('potion', 0),
        
    }
    return render(request, 'battle/game.html', context)