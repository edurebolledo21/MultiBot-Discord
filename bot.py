from numbers import Integral
import string
from dotenv import load_dotenv
load_dotenv()

import os
import discord
import requests

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

#Calculadora
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

#Criptomoneda

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


#Clima

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

#App de paises

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
            
            ip =  requests.get(f'https://api.geoapify.com/v1/ipinfo?&apiKey=66931cf4d4bd40259dafee5d6d898138')
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
            


client.run(os.environ['TOKEN'])