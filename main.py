import discord
from discord.ui import View, Select
import random, traceback, os, sys
from discord.ext import commands
import pyppeteer
from pyppeteer import launch
import asyncio
import pytz
from discord import app_commands

token = "Your bot token"
channels = [1279547345473765399]


if sys.platform.startswith("win"):  
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
elif sys.platform.startswith("darwin"):  
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
elif sys.platform.startswith("linux"):  
    chrome_path = "/usr/bin/chromium-browser"
else:
    chrome_path = None 

class Client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.tree = app_commands.CommandTree(self)

async def on_ready(self):
    print(f"{self.user} ({self.user.id}) is ready!")
    await client.tree.sync()

client = Client()

class Bloxfruitspage:
    def __init__(self, fruit, receiver):
        self.fruit = fruit
        self.receiver = receiver

    def get_proof(self):
        filename = "assets/bloxfruitproof.html"
        try:
            with open(filename, 'r', encoding="utf-8") as file:
                html_content = file.read()
                html_content = html_content.replace('FRUIT', self.fruit)
                html_content = html_content.replace('RECEIVER', self.receiver)
            return html_content
        except FileNotFoundError:
            raise Exception("HTML template file not found.")
        except Exception as e:
            raise Exception(f"Error generating proof: {e}")

class bloxfruitModal(discord.ui.Modal, title='Blox fruit proof generator'):
    gifter = discord.ui.TextInput(
        label="Receiver Name",
        placeholder="Enter receiver Roblox username",
        style=discord.TextStyle.short,
        required=True,
    )

    nitro_fruit = discord.ui.TextInput(
        label='Fruit',
        placeholder='Enter the fruit name or value',
        style=discord.TextStyle.short,
        required=True,
        max_length=32,
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=False, thinking=True)

            proof = Bloxfruitspage(self.nitro_fruit.value, self.gifter.value).get_proof()
            temp_html = "assets/temp.html"
            
            with open(temp_html, "w", encoding="utf-8") as f:
                f.write(proof)


            browser = await launch(
                executablePath=chrome_path,
                headless=True,
            )
            page = await browser.newPage()
            absolute_path = f'file://{os.path.abspath(temp_html)}'
            await page.setViewport({'width': 1280, 'height': 1024})
            await page.goto(absolute_path)
            await page.screenshot({'path': 'proof.png', 'fullPage': True})
            await browser.close()

            embed = discord.Embed(color=0x717CDA, title="Success", description="> :white_check_mark: **Please check your DMs!**")
            embed.set_image(url="attachment://proof.png")
            embed.set_footer(text="Ternw")
            await interaction.user.send(file=discord.File('proof.png'))

        except Exception as e:
            traceback.print_exc()

@client.tree.command(description='Generate proof of a Blox Fruit proof.')
async def bloxfruitproof(interaction: discord.Interaction):
    if interaction.channel.id not in channels:
        embed = discord.Embed(
            color=0x717CDA,
            title="Error",
            description=">:x: **Oops! You can't use this command here. Please go to <#1279547345473765399>.**",
        )
        embed.set_footer(text="Ternw")
        return

    try:
        await interaction.response.send_modal(bloxfruitModal())
    except Exception as e:
        print(f"Error sending modal: {e}")

class Robuxpage:
    def __init__(self, amount, robloxuser):
        self.amount = amount
        self.robloxuser = robloxuser

    def get_proof(self):
        filename = "assets/robloxproof.html"
        try:
            with open(filename, 'r', encoding="utf-8") as file:
                html_content = file.read()
                html_content = html_content.replace('ROBUXAMOUNT', self.amount)
                html_content = html_content.replace('ROBLOXUSER', self.robloxuser)
            return html_content
        except FileNotFoundError:
            raise Exception("HTML template file not found.")
        except Exception as e:
            raise Exception(f"Error generating proof: {e}")

class RobuxModal(discord.ui.Modal, title='Robux amount proof'):
    robloxuser = discord.ui.TextInput(
        label="Enter your Roblox username",
        placeholder="Enter your username",
        style=discord.TextStyle.short,
        required=True,
    )

    amount = discord.ui.TextInput(
        label='Amount of Robux',
        placeholder='Enter amount (e.g., 10)',
        style=discord.TextStyle.short,
        required=True,
        max_length=32,
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=False, thinking=True)

            proof = Robuxpage(self.amount.value, self.robloxuser.value).get_proof()
            temp_html = "assets/temp.html"

            with open(temp_html, "w", encoding="utf-8") as f:
                f.write(proof)

            browser = await launch(
                executablePath=chrome_path,
                headless=True,
            )
            page = await browser.newPage()
            absolute_path = f'file://{os.path.abspath(temp_html)}'
            await page.goto(absolute_path)
            bounding_box = await page.evaluate(
                """() => {
                    const body = document.body;
                    return {
                        width: body.scrollWidth,
                        height: body.scrollHeight,
                    };
                }"""
            )
            await page.setViewport({'width': bounding_box['width'], 'height': bounding_box['height']})
            await page.screenshot({'path': 'proof.png'})
            await browser.close()

            embed = discord.Embed(color=0x717CDA, title="Success", description="> :white_check_mark: **Please check your DMs!**")
            embed.set_image(url="attachment://proof.png")
            embed.set_footer(text="Ternw")
            await interaction.user.send(file=discord.File('proof.png'))

        except Exception as e:
            traceback.print_exc()

@client.tree.command(name="robloxproof", description="Generate Robux amount.")
async def robloxproof(interaction: discord.Interaction):
    if interaction.channel.id not in channels:
        embed = discord.Embed(
            color=0x717CDA,
            title="Error",
            description=">:x: **Oops! You can't use this command here. Please go to <#1279547345473765399>.**",
        )
        embed.set_footer(text="Ternw")
        return

    try:
        await interaction.response.send_modal(RobuxModal())
    except Exception as e:
        print(f"Error sending modal: {e}")

client.run(token)
