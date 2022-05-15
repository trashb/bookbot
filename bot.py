#imports
import discord
from libgen_api import LibgenSearch
#import discord_ui
#import Paginator

client = discord.Client()

def error(type):
    if type == "command":
        return discord.Embed(title = "Error!", description = "Command does not exist! Use !help for a list of commands with proper formatting.", color = discord.Color.red())
    elif type == "result":
        return discord.Embed(title = "Error!", description = "No Results! Why don't you check your spelling, or try a different book?", color = discord.Color.red())

def removeBlank(d):
    for key in d:
        if d[key] == '':
            d[key] = "N/A"
    return d

def createEmbed(title, res):
    output = discord.Embed(title = f"Results for {title}", color = discord.Color.blue())
    output.add_field(name= "Title", value=res["Title"])
    output.add_field(name= "Author", value=res["Author"])
    output.add_field(name = "Year", value = res["Year"])
    output.add_field(name = "Language", value = res["Language"])
    output.add_field(name = "Extension", value = res["Extension"])
    output.add_field(name= "Link", value= LibgenSearch().resolve_download_links(res)["Cloudflare"])
    return output
'''
#scroll between top entries using emoji reactions
@client.event
async def embedpages(botChannel, results):        #list of embeds (outputs) 
    m = await botChannel.send(embed = results[0])
    await m.add_reaction('◀')
    await m.add_reaction('▶')
    i=0
    emoji = ""
    while True:
        if emoji == '▶' and i<9:
            i += 1
        elif emoji == '◀' and i>0:
            i -= 1
        await m.edit(embed=results[i])
        r = await m.wait_for_reaction(message = message, timeout = 30.0)
        if r == None:
            break
    await m.clear_reactions(m)
'''
#####################################EVENTS#####################################
@client.event
async def on_ready():
    print("logged in")
    return

@client.event
async def on_message(msg):
    if msg.content[:1]=="!":
        errored = False
        message = msg.content.lower().split(" ",2)
        print(message)
        botChannel = client.get_channel(msg.channel.id)
        cmd = message[0]    #command 
        #pg = message[-1][-1:2]    # the number of pages; always the last index
        

####################COMMANDS#####################
        if cmd == "!help":
            output = discord.Embed(title = "Help", description = "Available commands: ", color = discord.Color.blue())
            output.add_field(name="!search_title", value="Ex. !search_title harry-potter", inline = False)
            output.add_field(name="!search_author", value="Ex. !search_author j.k.-rowling", inline = False)
            output.add_field(name="!search_title_filtered", value="paramters: author, year, language, extension (0 for no filter)\n Ex. !search_filters_title percy-jackson rick-riordan 0 german pdf")
            output.add_field(name="!search_author_filtered", value="paramters: title, year, language, extension (0 for no filter)\n Ex. !search_filters_title rick-riordan 0 0 german epub")
            print("AAAAAAA")
            await botChannel.send(embed = output)
        ########
        else:
            try:
                title = message[1].replace("-"," ")         #title or author
            except:
                await botChannel.send(embed = error("command"))
                errored = True
            else:
                try:
                    filters = message[2].split()        #list
                except:
                    pass
                else:
                    if len(filters) != 4:
                        await botChannel.send(embed = error("command"))
                        errored = True
        ##########
            if not errored:
                if cmd == "!search_title":
                    '''
                    entries = LibgenSearch().search_title(title)
                    if len(entries)==0:
                        await botChannel.send(embed = error("result"))
                        errored = True
                                   #list of dicts (results)
                    else:
                        outputs = []
                        for i in range(len(entries)):
                            res = LibgenSearch().search_title(title)[i]
                            outputs.append(createEmbed(title, res))
                        
                        await Paginator.Simple().start(botChannel, pages=outputs)
                        #await embedpages(botChannel, outputs)
                    '''
                    output = discord.Embed(title = f"Results for {title}", color = discord.Color.blue())
                    try:
                        res = LibgenSearch().search_title(title)[0]
                        res = removeBlank(res)
                        output.add_field(name = "Title", value=res["Title"]) 
                    except:
                        await botChannel.send(embed = error("result"))
                        errored = True

                    else:
                        output.add_field(name= "Author", value=res["Author"])
                        output.add_field(name= "Year", value=res["Year"])
                        output.add_field(name= "Language", value=res["Language"])
                        output.add_field(name= "Extension", value=res["Extension"])
                        output.add_field(name= "Link", value= LibgenSearch().resolve_download_links(res)["Cloudflare"])
                    
                        await botChannel.send(embed = output)
            #########    
                elif cmd == "!search_author":
                    output = discord.Embed(title = f"Results for {title}", color = discord.Color.blue())
                    try:
                        res = LibgenSearch().search_author(title)[0]
                        res = removeBlank(res)
                        output.add_field(name = "Title", value=res["Title"]) 
                    except:
                        await botChannel.send(embed = error("result"))
                        errored = True

                    else:
                        output.add_field(name= "Author", value=res["Author"])
                        output.add_field(name= "Year", value=res["Year"])
                        output.add_field(name= "Language", value=res["Language"])
                        output.add_field(name= "Extension", value=res["Extension"])
                        output.add_field(name= "Link", value= LibgenSearch().resolve_download_links(res)["Cloudflare"])
                    
                        await botChannel.send(embed = output)
            #########
                elif cmd == "!search_title_filtered":
                    title_filters = {}
                    for i in range(len(filters)):
                        if filters[i] != "0":
                            if i == 0:
                                title_filters["Author"] = filters[i].replace("-"," ")
                            elif i == 1:
                                title_filters["Year"] = filters[i]
                            elif i == 2:
                                title_filters["Language"] = filters[i]
                            elif i == 3:
                                title_filters["Extension"] = filters[i]    
                    output = discord.Embed(title = f"Results for {title}", color = discord.Color.blue())
                    try:
                        res = LibgenSearch().search_title_filtered(title, title_filters, exact_match=False)[0]
                        res = removeBlank(res)
                        output.add_field(name = "Title", value=res["Title"])
                    except:
                        await botChannel.send(embed = error("result"))
                        errored = True
                    else:
                        output.add_field(name = "Author", value=res["Author"])
                        output.add_field(name= "Year", value=res["Year"])
                        output.add_field(name= "Language", value=res["Language"])
                        output.add_field(name= "Extension", value=res["Extension"])
                        output.add_field(name= "Link", value= LibgenSearch().resolve_download_links(res)["Cloudflare"])
                        await botChannel.send(embed = output)
            #########
                elif cmd == "!search_author_filtered":
                    title_filters = {}
                    for i in range(len(filters)):
                        if filters[i] != "0":
                            if i == 0:
                                title_filters["Title"] = filters[i].replace("-"," ")
                            elif i == 1:
                                title_filters["Year"] = filters[i]
                            elif i == 2:
                                title_filters["Language"] = filters[i] 
                            elif i == 3:
                                title_filters["Extension"] = filters[i]    
                    output = discord.Embed(title = f"Results for {title}", color = discord.Color.blue())
                    try:
                        res = LibgenSearch().search_author_filtered(title, title_filters, exact_match=False)[0]
                        res = removeBlank(res)
                        output.add_field(name = "Title", value=res["Title"])
                    except:
                        await botChannel.send(embed = error("result"))
                        errored = True
                    else:
                        output.add_field(name = "Author", value=res["Author"])
                        output.add_field(name= "Year", value=res["Year"])
                        output.add_field(name= "Language", value=res["Language"])
                        output.add_field(name= "Extension", value=res["Extension"])
                        output.add_field(name= "Link", value= LibgenSearch().resolve_download_links(res)["Cloudflare"])
                        await botChannel.send(embed = output)

                elif cmd[0]=="!":
                    await botChannel.send(embed = error("command"))
                    errored = True

#run
client.run('OTc1MDc3OTkwOTczMjAyNTMy.G0x7Eh.v1Aq1IqwWZmJyXksbtLHNHhEKl0wOemEJqUVUQ')
