from ast import For
from email import message
import email
from numbers import Integral
import string
from turtle import position
from dotenv import load_dotenv
load_dotenv()

import os
import discord
import requests
import sqlite3
connectionDB = sqlite3.connect("tutorial.db")
cur = connectionDB.cursor()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

#calculator
    if message.content.startswith('$calc'):
        operacion = message.content.split (' ')[1]

        def calc(op):
            if op.__contains__('+'):
                num1 = int(op.split('+')[0])
                num2 = int(op.split('+')[1])
                return num1 + num2;
            elif op.__contains__('-'):
                num1 = int(op.split('-')[0])
                num2 = int(op.split('-')[1])
                return num1 - num2;
            elif op.__contains__('x'):
                num1 = int(op.split('x')[0])
                num2 = int(op.split('x')[1])
                return num1 * num2;
            elif op.__contains__('/'):
                num1 = int(op.split('/')[0])
                num2 = int(op.split('/')[1])
                return num1 / num2;
            else:
                return 'Ha ocurrido un error'
        resultado = calc(operacion);
        if resultado == 'Ha ocurrido un error':   
            await message.channel.send(f'<@{message.author.id}> {resultado}')
        else:    
            await message.channel.send(f'Hola <@{message.author.id}> tu resultado es: {resultado}')

#cryptocurrency

    if message.content.startswith('$crypto'):
        moneda = message.content.split(' ')[1]
        divisa = message.content.split(' ')[2]
        info = requests.get(f'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={moneda}&tsyms={divisa}')

        response = info.json()
        price = response['DISPLAY'][moneda][divisa]['PRICE']
        high = response['DISPLAY'][moneda][divisa]['HIGH24HOUR']
        low = response['DISPLAY'][moneda][divisa]['LOW24HOUR']
        
        
        await message.channel.send(f'Hola <@{message.author.id}>')
        await message.channel.send(f'Moneda: {divisa}, Cryptomoneda: {moneda}')
        await message.channel.send(f'El precio: {price}')
        await message.channel.send(f'Precio más alto: {high}')
        await message.channel.send(f'Precio más bajo: {low}')


#weather

    if message.content.startswith('$clima'):
        ciudad = message.content.split(' ')[1]
        info = requests.get(f'https://goweather.herokuapp.com/weather/{ciudad}')
        response = info.json()
        todayTemp = response['temperature'] 
        tomorrowTemp = response['forecast'][0]['temperature']
        tomorrow2Temp = response['forecast'][1]['temperature']
        
        await message.channel.send(f'Hola <@{message.author.id}>')
        await message.channel.send(f'Temperatura en: {ciudad}')
        await message.channel.send(f'El dia de hoy es: {todayTemp}')
        await message.channel.send(f'El dia de mañana sera: {tomorrowTemp}')
        await message.channel.send(f'El dia de pasado mañana sera: {tomorrow2Temp}')

#search countries

    if message.content.startswith('$country'):
        if len(message.content) != 8:
            
            pais = message.content.split(' ')[1]
            info_temp = requests.get(f'https://goweather.herokuapp.com/weather/{pais}')
            response_temp = info_temp.json()
            temperatura = response_temp['temperature']
            clima = response_temp['description']
            info_pais = requests.get(f'https://restcountries.com/v3.1/name/{pais}')
            response_pais = info_pais.json()
            nombre = response_pais[0]['name']['common']
            capital = response_pais[0]['capital'][0]
            habitantes = response_pais[0]['population']
            region = response_pais[0]['region']
            bandera = response_pais[0]['flags']['png'] 

            await message.channel.send(f'Hi, <@{message.author.id}> your country is: {nombre}')
            await message.channel.send(f'Capital: {capital}')
            await message.channel.send(f'Inhabitants: {habitantes}')
            await message.channel.send(f'Region: {region}')
            await message.channel.send(f'Temperature: {temperatura}')
            await message.channel.send(f'Weather: {clima}')
            await message.channel.send(f'{bandera}')
            
        else:
            
            ip =  requests.get(f"{os.environ['LINK']}")
            response_ip = ip.json()
            pais_ip = response_ip['country']['names']['de']
            info_temp = requests.get(f'https://goweather.herokuapp.com/weather/{pais_ip}')
            response_temp = info_temp.json()
            temperatura = response_temp['temperature']
            clima = response_temp['description']
            info_pais = requests.get(f'https://restcountries.com/v3.1/name/{pais_ip}')
            response_pais = info_pais.json()
            nombre = response_pais[0]['name']['common']
            capital = response_pais[0]['capital'][0]
            habitantes = response_pais[0]['population']
            region = response_pais[0]['region']
            bandera = response_pais[0]['flags']['png']


            await message.channel.send(f'Hi, <@{message.author.id}> your country is: {nombre}')
            await message.channel.send(f'Capital: {capital}')
            await message.channel.send(f'Inhabitants: {habitantes}')
            await message.channel.send(f'Region: {region}')
            await message.channel.send(f'Temperature: {temperatura}')
            await message.channel.send(f'Weather: {clima}')
            await message.channel.send(f'{bandera}')
            
#Mlb players app
    
    def playerid(name):
                datos_jugador = requests.get(f"http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code=&name_part='{name}'")
                response_id = datos_jugador.json()
                player_id = response_id['search_player_all']['queryResults']['row']['player_id']
                return player_id
    
    if message.content.startswith('$jugador'): 
        #Player id
        nombre = message.content.split(' ')[1]
        apellido = message.content.split(' ')[2]
        full_name = f'{nombre} {apellido}'
        result_id = playerid(full_name)
        p = f"https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/{result_id}/headshot/67/current"   
        #player details
        details = requests.get(f"http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code='mlb'&player_id='{result_id}'")
        response_details = details.json()
        name = response_details['player_info']['queryResults']['row']['name_display_first_last']
        birthday = response_details['player_info']['queryResults']['row']['birth_date']
        country = response_details['player_info']['queryResults']['row']['birth_country']
        city = response_details['player_info']['queryResults']['row']['birth_city']
        team = response_details['player_info']['queryResults']['row']['team_name']
        debut = response_details['player_info']['queryResults']['row']['pro_debut_date']
        position = response_details['player_info']['queryResults']['row']['primary_position_txt']
        height = response_details['player_info']['queryResults']['row']['height_feet']
        age = response_details['player_info']['queryResults']['row']['age']
        weight = response_details['player_info']['queryResults']['row']['weight']

        #date and debut
        date = birthday.split('T')[0]
        date_debut = debut.split('T')[0]
        #weight in kg
        weight_kg = int(weight) / 2.205
        kg_round = round(weight_kg, 2)
        #height in m
        height_m = int(height) / 3.281
        m_round = round(height_m, 2)

        await message.channel.send(f'{p}')
        await message.channel.send(f'Nombre: {name}')
        await message.channel.send(f'Nacimiento: {date}, {city}, {country}')
        await message.channel.send(f'Edad: {age} años')
        await message.channel.send(f'Equipo: {team}')
        await message.channel.send(f'Posición: {position}')
        await message.channel.send(f'Debut: {date_debut}')
        await message.channel.send(f'Estatura: {m_round} m Peso: {kg_round} kg')

#player's career
    if message.content.startswith('$stats'):
        
        #stats career by year
        if message.content.__contains__('2') | message.content.__contains__('1'):
            #Player id
            year = message.content.split(' ')[3]
            nombre = message.content.split(' ')[1]
            apellido = message.content.split(' ')[2]
            full_name = f'{nombre} {apellido}'
            result_id = playerid(full_name)
            p = f"https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/{result_id}/headshot/67/current"   
            details = requests.get(f"http://lookup-service-prod.mlb.com/json/named.sport_hitting_tm.bam?league_list_id='mlb'&game_type='R'&season='{year}'&player_id='{result_id}'")
            response_career = details.json()
            hits = response_career['sport_hitting_tm']['queryResults']['row']['h']
            hr = response_career['sport_hitting_tm']['queryResults']['row']['hr']
            carreras = response_career['sport_hitting_tm']['queryResults']['row']['r']
            ponches = response_career['sport_hitting_tm']['queryResults']['row']['so']
            Bb = response_career['sport_hitting_tm']['queryResults']['row']['bb']
            Avg = response_career['sport_hitting_tm']['queryResults']['row']['avg']
            Vb  = response_career['sport_hitting_tm']['queryResults']['row']['ab']
            jjugados = response_career['sport_hitting_tm']['queryResults']['row']['g']
            cp = response_career['sport_hitting_tm']['queryResults']['row']['rbi'] 
            season = response_career['sport_hitting_tm']['queryResults']['row']['season']

            await message.channel.send(f'{p}')
            await message.channel.send(f'Temporada: {season}')
            await message.channel.send(f'JJ: {jjugados} ')
            await message.channel.send(f'AB: {Vb}')
            await message.channel.send(f'C: {carreras}')
            await message.channel.send(f'H: {hits}')
            await message.channel.send(f'CP: {cp}')
            await message.channel.send(f'BB: {Bb}')
            await message.channel.send(f'P: {ponches}')
            await message.channel.send(f'J: {hr}')
            await message.channel.send(f'PRO: {Avg}') 
        
        #stats career
        else:
            nombre = message.content.split(' ')[1]
            apellido = message.content.split(' ')[2]
            full_name = f'{nombre} {apellido}'
            result_id = playerid(full_name)
            p = f"https://img.mlbstatic.com/mlb-photos/image/upload/d_people:generic:headshot:67:current.png/w_213,q_auto:best/v1/people/{result_id}/headshot/67/current"   
            details = requests.get(f"http://lookup-service-prod.mlb.com/json/named.sport_career_hitting.bam?league_list_id='mlb'&game_type='R'&player_id='{result_id}'")
            response_career = details.json()
            hits = response_career['sport_career_hitting']['queryResults']['row']['h']
            hr = response_career['sport_career_hitting']['queryResults']['row']['hr']
            carreras = response_career['sport_career_hitting']['queryResults']['row']['r']
            ponches = response_career['sport_career_hitting']['queryResults']['row']['so']
            Bb = response_career['sport_career_hitting']['queryResults']['row']['bb']
            Avg = response_career['sport_career_hitting']['queryResults']['row']['avg']
            Vb  = response_career['sport_career_hitting']['queryResults']['row']['ab']
            jjugados = response_career['sport_career_hitting']['queryResults']['row']['g']
            cp = response_career['sport_career_hitting']['queryResults']['row']['rbi']

            await message.channel.send(f'{p}')
            await message.channel.send(f'JJ: {jjugados} ')
            await message.channel.send(f'AB: {Vb}')
            await message.channel.send(f'C: {carreras}')
            await message.channel.send(f'H: {hits}')
            await message.channel.send(f'CP: {cp}')
            await message.channel.send(f'BB: {Bb}')
            await message.channel.send(f'P: {ponches}')
            await message.channel.send(f'J: {hr}')
            await message.channel.send(f'PRO: {Avg}')     



client.run(os.environ['TOKEN'])












    # if message.content.startswith('$crear'):
    #     first_name = message.content.split(' ')[1]
    #     last_name = message.content.split(' ')[2]
    #     full_name = f'{first_name} {last_name}'
    #     email = message.content.split(' ')[3]
    #     password = message.content.split(' ')[4]
    #     confirm_pass = message.content.split(' ')[5]
    #     response = requests.post('http://api.cup2022.ir/api/v1/user',
    #     data = {'name': full_name, 'email': email, 'password': password, 'confirmar pass': confirm_pass})
    #     cur.execute('INSERT INTO users (discord_id, name, email, password) VALUES (?, ?, ?, ?)', [message.author.id, full_name, email, password])
    #     connectionDB.commit()
    #     await message.channel.send('usario creado')

    # if message.content.startswith('!BorrarUsuario'):
    #     cur.execute('DELETE FROM users WHERE discord_id = ?', [message.author.id])
    #     connectionDB.commit()
    #     await message.channel.send('Usuario Eliminado!')