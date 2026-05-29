import discord
import random
import os
from discord import app_commands
import json
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()


client = commands.Bot(command_prefix="!" , intents = discord.Intents.all())
tree = client.tree

TOKEN = os.getenv("TOKEN")

if not TOKEN : 
    print("Please set the .env file with token")
    exit(69)

map_emojis = {
    "1" : "🧱" ,
    "0" : "⬛" ,
    "P" : "🤓" ,
    "E" : "🥩" 
}


@client.event
async def on_ready():
    synced = await tree.sync()
    print(f"client logged as {client.user}")
    print(f"synced {len(synced)} command(s)")


def get_data() : 

    with open('./levels.json' , "r" , encoding='utf-8') as f:
        data = json.load(f)  

    return data


data = get_data()


class ControlButtons(discord.ui.View):
    def __init__(self , author , maze , level):
        super().__init__()
        self.steps = {
           "U" : [-1 , 0],
           "D" : [1 , 0],
           "R" : [0 , 1],
           "L" : [0 , -1]
        }
        self.r = 1
        self.c = 1
        self.maze = maze
        self.author = author
        self.level = level

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.author:
            await interaction.response.send_message("you are not the author", ephemeral=True)
            return False  
        return True  


    def boundary_check(self , direction : str):
        row_size = len(self.maze)
        col_size = len(self.maze[0])

        dr, dc = self.steps[direction]
        new_r = self.r + dr
        new_c = self.c + dc

        if new_r < 0 or new_c < 0 or new_c >= col_size or new_r >= row_size or self.maze[new_r][new_c] == "1":
            return True

                
        return False        


    def handle_movement(self , direction : str) -> bool:
        dr, dc = self.steps[direction]
        new_r = self.r + dr
        new_c = self.c + dc

        if self.maze[new_r][new_c] == "E":
            return True 
            
        self.maze[self.r][self.c] , self.maze[new_r][new_c] =  self.maze[new_r][new_c] , self.maze[self.r][self.c] 


        self.r = new_r
        self.c = new_c

        return False

    def build_msg(self):
        maze_string = ""

        for row in self.maze: 
            for col in row:
                maze_string += map_emojis[col]
            maze_string += '\n'


        msg = f'```{maze_string}```'

        return msg


    
    @discord.ui.button(label = "" , emoji = "🔐" , row = 0 , style = discord.ButtonStyle.gray , disabled=True)
    async def _btn_disable(self , interaction : discord.Interaction , button : discord.ui.Button) -> None:
        pass
        


    

    @discord.ui.button(label = "" , emoji = "🔼" , row = 0 , style = discord.ButtonStyle.blurple)
    async def _btn_up(self , interaction : discord.Interaction , button : discord.ui.Button) -> None:
        if self.boundary_check("U"):
            await interaction.response.send_message("out of maze" , ephemeral=True)
            return 

        
        result = self.handle_movement("U")
        if result == True:
            await interaction.message.edit(content = "YOU WON" , view = None)
            return 
        


        msg = self.build_msg()


        await interaction.response.defer()
        await interaction.message.edit(content = msg , view = self)






    @discord.ui.button(label = "" , emoji = "🔐" , row = 0 , style = discord.ButtonStyle.gray , disabled=True)
    async def _btn_disable_2(self , interaction : discord.Interaction , button : discord.ui.Button) -> None:
        pass


    
    


    
    @discord.ui.button(label = "" , emoji = "⬅️" , row = 1 , style = discord.ButtonStyle.blurple)
    async def _btn_left(self , interaction : discord.Interaction , button : discord.ui.Button) -> None:
        if self.boundary_check("L"):
            await interaction.response.send_message("out of maze" , ephemeral=True)
            return 

        
        result = self.handle_movement("L")
        if result == True:
            await interaction.message.edit(content = "YOU WON" , view = None)
            return

        msg = self.build_msg()


        await interaction.response.defer()
        await interaction.message.edit(content = msg , view = self)

    @discord.ui.button(label = "" , emoji = "🔐" , row = 1 , style = discord.ButtonStyle.gray , disabled=True)
    async def _btn_disable_3(self , interaction : discord.Interaction , button : discord.ui.Button) -> None:
        pass


    @discord.ui.button(label = "" , emoji = "➡️" , row = 1 , style = discord.ButtonStyle.blurple)
    async def _btn_right(self , interaction : discord.Interaction , button : discord.ui.Button) -> None:
        if self.boundary_check("R"):
            await interaction.response.send_message("out of maze" , ephemeral=True)
            return 

        
        result = self.handle_movement("R")
        if result == True:
            await interaction.message.edit(content = "YOU WON" , view = None)
            return

        msg = self.build_msg()

        await interaction.response.defer()

        await interaction.message.edit(content = msg , view = self)





    
    @discord.ui.button(label = "" , emoji = "🔐" , row = 2 , style = discord.ButtonStyle.gray , disabled=True)
    async def _btn_disable_4(self , interaction : discord.Interaction , button : discord.ui.Button) -> None:
        pass
        


    

    @discord.ui.button(label = "" , emoji = "🔽" , row = 2 , style = discord.ButtonStyle.blurple)
    async def _btn_down(self , interaction : discord.Interaction , button : discord.ui.Button) -> None:
        if self.boundary_check("D"):
            await interaction.response.send_message("out of maze" , ephemeral=True)
            return 

        
        result = self.handle_movement("D")
        if result == True:
            await interaction.message.edit(content = "YOU WON" , view = None)
            return

        msg = self.build_msg()


        await interaction.response.defer()
        await interaction.message.edit(content = msg , view = self)



    @discord.ui.button(label = "" , emoji = "🔐" , row = 2 , style = discord.ButtonStyle.gray , disabled=True)
    async def _btn_disable_5(self , interaction : discord.Interaction , button : discord.ui.Button) -> None:
        pass


    



@tree.command(name = "play" , description="play maze game")
@app_commands.describe(level = "the level you wanna play we the level number increases the diffculty increases too if None select random")
async def _play(interaction : discord.Interaction , level : app_commands.Range[int , 1 , len(data)] | None = None):
    if not level :
        level = random.randrange(1 , len(data))

    maze_string = ""
    maze_list = data[f"level{level}"]["maze"]

    for row in maze_list: 
        for col in row:
            maze_string += map_emojis[col]
        maze_string += '\n'

    view = ControlButtons(interaction.user , data[f"level{level}"]["maze"] , level)

    await interaction.response.send_message(f"```{maze_string}```" , view = view)


client.run(TOKEN)
