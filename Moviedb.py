import requests
import json
import telepot
import locale
import datetime

bot = telepot.Bot('1682510966:AAHLZWvkjvV90g3q9CvSKM5IygkAB5z0RNA')
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def requisicao(titulo):

    try:
        req = requests.get('https://api.themoviedb.org/3/search/movie?&language=pt-BR&api_key=b3a156870abcdcfc2c7515e1950f5fea&query=' + titulo)
        dicionario = json.loads(req.text)
        return dicionario
    except:
        print('Erro na conexão')
        return None

def printar_detalhe(msg):

    bot.sendMessage(msg['chat']['id'], "Olá " + msg['chat']['first_name']+
                    ", seja bem vindo ao BOT Oráculo do Cinema!\nDigite o Título do Filme que deseja informação:")

    movie = requisicao(msg['text'])
    bot.sendMessage(msg['chat']['id'], "Encontrei alguns resultados para o título \""+ msg['text']+"\" \U0001f9D0")
    timenow = datetime.datetime.now().strftime("%A %d/%m/%Y às %H:%M")
    log = "\n=================================\n"+timenow+"\nRemetente: "+ msg['chat']['first_name']+"\nFilme pesquisado: "+msg['text']
    arquivo = open('log.txt', 'a+')
    arquivo.write(str(log))
    arquivo.close()
    if movie['total_results'] > 200:
        bot.sendMessage(msg['chat']['id'],
                        "Puxa "+ msg['chat']['first_name']+"!!! \U0001F614 Que pena meu dono não me permite enviar tantas mensagens, tente refinar um pouco mais a sua busca!  \U0001F61C")
        return None
    else:
        for x in range(0,movie['total_pages']):
            #bot.sendMessage(msg['chat']['id'], movie['results'][i])
            movie2 = requisicao(msg['text']+"&page="+str(x + 1))
            for y in range(0,20):
                linha = y + 1

                if (movie2['results'][y]['poster_path'] is not None) and  movie2['results'][y]['overview'] != "":
                    bot.sendMessage(msg['chat']['id'], "Título: " + str(movie2['results'][y]['title'])+
                                    "\nLançamento: " + str(movie2['results'][y]['release_date'])+
                                    "\nNota: " + str(movie2['results'][y]['vote_average'])+
                                    "\nSinopse:\n" + movie2['results'][y]['overview'])
                    bot.sendPhoto(msg['chat']['id'],
                              "https://image.tmdb.org/t/p/original" + movie2['results'][y]['poster_path'])
                    #bot.sendMessage(msg['chat']['id'], "=========================================")


bot.message_loop(printar_detalhe, 5)
while True:
    pass