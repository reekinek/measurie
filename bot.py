from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
from datetime import datetime
import math

import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix = '!', intents = intents, help_command=None)
bot.remove_command('help')



# this is made by chatgpt for the timezone thingy, idk what it does really I just adapted it a bit
def get_time_in_location(location):
    geolocator = Nominatim(user_agent="int_utils")
    timezone_finder = TimezoneFinder()
    
    try:
        location_data = geolocator.geocode(location)
        if location_data is None:
            return "Location not found. Please enter a valid city or country."

        latitude = location_data.latitude
        longitude = location_data.longitude
        timezone_str = timezone_finder.timezone_at(lat=latitude, lng=longitude)
        
        if timezone_str is None:
            return "Timezone not found for the specified location."

        timezone = pytz.timezone(timezone_str)
        local_time = datetime.now(timezone)
        return local_time.strftime('%H:%M:%S in 24h format and %I:%M:%S %p in 12h format')
    except Exception as e:
        return str(e)



# Syns the slash command on bootup
@bot.event
async def on_ready():
    print("on_ready() function called")
        
    try:
        synced = await bot.tree.sync()      
        print(f'Successfully synced {len(synced)} commands.')
    except Exception as e:
        print(f'Error syncing commands: {e}')



# /help slash command
@bot.tree.command(name="help", description="Shows you information on the bot and how to use it.")
async def help(interaction: discord.Interaction) -> None:
    await interaction.response.send_message("***Thanks for using International Utilities :)***\n\nCommands:\n***/help***\nShows all bot's commands\n***/temp value unit***\nConverts entered temperature into celsius, kelvin and fahrenheit.\n***/length value unit***\nConverts entered length into all commonly used length measurement units:\nmilimeters, centimeters, meters, kilometers, miles, yards, inches, feet, football stadiums, bananas.\n***/timezone city/country***\nChecks the current time in a city. If you enter a country,\nthe bot will use the country's capital city.\n***/speed value unit***\nConverts entered velocity into km/h, mph, m/s and fpm\n***/mass value unit***\nConverts entered mass into all commonly used mass units:\ngrams, decagrams, kilograms, tonnes (metric), ounces, pounds, stones, quarters, tons (american) and tons (british)\n***/volume value unit***\nConverts entered volume into all commonly used volume units:\nliters, milimeters, pints, quarts, gallons\n\n***If you need further help or want to report a bug, please contact ejtako_ or gaapcio***")


# /height slash command (yes this is a barely working spaghetti, it'll get a rework later)
@bot.tree.command(name="height", description="Converts height between imperial and metric units")
@app_commands.describe(value="Height value")
@app_commands.describe(unit="Height unit")
@app_commands.choices(unit=[
    app_commands.Choice(name="Centimeters", value="cm"),
    app_commands.Choice(name="Feet and inches", value="feet")
])
async def height(interaction: discord.Interaction, value: str, unit: str) -> None:
    if unit == "cm":
        feetvalue = math.floor(value / 30.48)
        inchesvalue = int(round((value / 30.48 - feetvalue) * 12, 0))
        await interaction.response.send_message(f'***{value}*** centimeters is ***{feetvalue}\'{inchesvalue}***')
    elif unit == "feet":
        if len(str(value)) == 3:
            try:
                feetvalue = value[0]
                inchesvalue = value[2]
                centimetersvalue = float(feetvalue) * 30.48 + float(inchesvalue) * 2.54
                await interaction.response.send_message(f'***{feetvalue}\'{inchesvalue}*** is ***{centimetersvalue}*** centimeters')
            except:
                await interaction.response.send_message(f'Please input a correct height in feet and inches. Examples: 5\'11, 6. You can either use a \' or a space.')
        elif len(str(value)) == 4:
            try:
                feetvalue = value[0]
                inchesvalue = value[2:4]
                centimetersvalue = float(feetvalue) * 30.48 + float(inchesvalue) * 2.54
                await interaction.response.send_message(f'***{feetvalue}\'{inchesvalue}*** is ***{centimetersvalue}*** centimeters')
            except:
                await interaction.response.send_message(f'Please input a correct height in feet and inches. Examples: 5\'11, 6. You can either use a \' or a space.')
        elif len(str(value)) == 1:
            try:
                feetvalue = value[0]
                inchesvalue = 0
                centimetersvalue = float(feetvalue) * 30.48 + float(inchesvalue) * 2.54
                await interaction.response.send_message(f'***{feetvalue}\'{inchesvalue}*** is ***{centimetersvalue}*** centimeters')
            except:
                await interaction.response.send_message(f'Please input a correct height in feet and inches. Examples: 5\'11, 6. You can either use a \' or a space.')
        else:
            await interaction.response.send_message(f'Please input a correct height in feet and inches. Examples: 5\'11, 6. You can either use a \' or a space.')


# /temp slash command
@bot.tree.command(name="temp", description="Converts given temperature into other units")
@app_commands.describe(value="Temperature value")
@app_commands.describe(unit="Temperature unit")
@app_commands.choices(unit=[
    app_commands.Choice(name="Celsius", value="C"),
    app_commands.Choice(name="Fahrenheit", value="F"),
    app_commands.Choice(name="Kelvin", value="K")
])
async def temp(interaction: discord.Interaction, value: float, unit: str) -> None:
    unit = unit.upper()
    if unit == "C":
        fahrenheit = (value *9/5) +32
        kelvin = value +273.15
        print(f"/temp command ran")
        await interaction.response.send_message(f'***{round(value, 2)}*** Celsius is ***{round(fahrenheit, 2)}*** Fahrenheit and ***{round(kelvin, 2)}*** Kelvin.')
    elif unit == "K":
        celsius = value - 273.15
        fahrenheit = (value - 273.15) * 9/5 + 32
        print(f"/temp command ran")
        await interaction.response.send_message(f'***{round(value, 2)}*** Kelvin is ***{round(celsius, 2)}*** Celsius and ***{round(fahrenheit, 2)}*** Fahrenheit.')
    elif unit == "F":
        celsius = (value - 32) * 5/9
        kelvin = (value - 32) * 5/9 + 273.15
        print(f"/temp command ran")
        await interaction.response.send_message(f'***{round(value, 2)}*** Fahrenheit is ***{round(celsius, 2)}*** Celsius and ***{round(kelvin, 2)}*** Kelvin.')
    else:
        await interaction.response.send_message("Unkown parameters. Please use numbers for the value and choose an unit.")
        print(f"/temp command ran")



# /length slash command
@bot.tree.command(name="length", description="Converts given length into other units")
@app_commands.describe(value="Length value")
@app_commands.describe(unit="Length unit")
@app_commands.choices(unit=[
    app_commands.Choice(name="Milimeters", value="milimeters"),
    app_commands.Choice(name="Centimeters", value="centimeters"),
    app_commands.Choice(name="Meters", value="meters"),
    app_commands.Choice(name="Kilometers", value="kilometers"),
    app_commands.Choice(name="Inches", value="inches"),
    app_commands.Choice(name="Feet", value="feet"),
    app_commands.Choice(name="Yards", value="yards"),
    app_commands.Choice(name="Miles", value="miles"),
    app_commands.Choice(name="Football Fields", value="football fields"),
    app_commands.Choice(name="Bananas", value="bananas")
])
@app_commands.describe(to_unit="Unit to conver to(optional)")
@app_commands.choices(to_unit=[
    app_commands.Choice(name="Milimeters", value="milimeters"),
    app_commands.Choice(name="Centimeters", value="centimeters"),
    app_commands.Choice(name="Meters", value="meters"),
    app_commands.Choice(name="Kilometers", value="kilometers"),
    app_commands.Choice(name="Inches", value="inches"),
    app_commands.Choice(name="Feet", value="feet"),
    app_commands.Choice(name="Yards", value="yards"),
    app_commands.Choice(name="Miles", value="miles"),
    app_commands.Choice(name="Football Fields", value="football fields"),
    app_commands.Choice(name="Bananas", value="bananas")
])
async def length(interaction: discord.Interaction, value: float, unit: str, to_unit: str = None) -> None:

    # Table of units
    conversion = {
        'meters': 1,
        'kilometers': 1000,
        'centimeters': 0.01,
        'milimeters': 0.001,
        'inches': 0.0254,
        'feet': 0.3048,
        'yards': 0.9144,
        'miles': 1609.344,
        'football fields': 91.44,
        'bananas': 0.1778
    }

    if to_unit:

        #Converts given value to meters
        print("/length command ran")
        value_meters = value * conversion[unit]
        #Converts value from meters to 2nd given unit
        converted_value = value_meters / conversion[to_unit]
        await interaction.response.send_message(f"***{value}*** {unit} is ***{round (converted_value, 2)}*** {to_unit}")
    else:
        #Converts given value to meters
        print("/length command ran")
        value_meters = value * conversion[unit]
        await interaction.response.send_message(f"***{value}*** {unit} is: ***{round (value_meters / conversion['meters'], 2)}*** meters, ***{round (value_meters / conversion['kilometers'], 2)}*** kilometers, ***{round (value_meters / conversion['centimeters'], 2)}*** centimeters, ***{round (value_meters / conversion['milimeters'], 2)}*** milimeters, ***{round (value_meters / conversion['inches'], 2)}*** inches, ***{round(value_meters / conversion['feet'], 2)}*** feet, ***{round (value_meters / conversion['yards'], 2)}*** yards, ***{round (value_meters / conversion['miles'], 2)}*** miles, ***{round (value_meters / conversion['football fields'], 2)}*** football fields, ***{round (value_meters / conversion['bananas'], 2)}*** bananas.")


# /mass slash command
@bot.tree.command(name="mass", description="Converts given mass into other units")
@app_commands.describe(value="Mass value")
@app_commands.describe(unit="Mass unit")
@app_commands.choices(unit=[
    app_commands.Choice(name="Grams", value="grams"),
    app_commands.Choice(name="Dekagrams", value="dekagrams"),
    app_commands.Choice(name="Kilograms", value="kilograms"),
    app_commands.Choice(name="Tonnes", value="tonnes"),
    app_commands.Choice(name="Ounces", value="ounces"),
    app_commands.Choice(name="Pounds", value="pounds"),
    app_commands.Choice(name="Stones", value="stones"),
    app_commands.Choice(name="Quarters", value="Quarters"),
    app_commands.Choice(name="Long ton(UK ton)", value="long ton"),
    app_commands.Choice(name="Short ton(US ton)", value="short ton")
])
@app_commands.describe(to_unit="Unit to conver to(optional)")
@app_commands.choices(to_unit=[
    app_commands.Choice(name="Grams", value="grams"),
    app_commands.Choice(name="Dekagrams", value="dekagrams"),
    app_commands.Choice(name="Kilograms", value="kilograms"),
    app_commands.Choice(name="Tonnes", value="tonnes"),
    app_commands.Choice(name="Ounces", value="ounces"),
    app_commands.Choice(name="Pounds", value="pounds"),
    app_commands.Choice(name="Stones", value="stones"),
    app_commands.Choice(name="Quarters", value="quarters"),
    app_commands.Choice(name="Long tons(UK)", value="long tons"),
    app_commands.Choice(name="Short(US) tons", value="short tons")
])
async def mass(interaction: discord.Interaction, value: float, unit: str, to_unit: str = None) -> None:

    # Table of units
    conversion = {
        'kilograms': 1,
        'grams': 1000,
        'dekagrams': 100,
        'tonnes': 0.001,
        'ounces': 35.27396,
        'pounds': 2.204623,
        'stones': 0.157473,
        'quarters': 0.088184904873951,
        'long tons': 0.0009842065,
        'short tons': 0.001102311
    }

    if to_unit:

        #Converts given value to kilograms
        value_kg = value * conversion[unit]
        #Converts value from kilograms to 2nd given unit
        converted_value = value_kg * conversion[to_unit]
        await interaction.response.send_message(f"{value} {unit} is {round (converted_value, 3)} {to_unit}")
        print("/mass command ran")
    else:
        #Converts given value to meters
        value_kg = value * conversion[unit]
        print("/mass command ran")
        await interaction.response.send_message(f"{value} {unit} is: {round (value_kg * conversion['kilograms'], 2)} kilograms, {round (value_kg * conversion['grams'], 3)} grams, {round (value_kg * conversion['dekagrams'], 2)} dekagrams, {round (value_kg * conversion['tonnes'], 3)} tonnes, {round (value_kg * conversion['ounces'], 2)} ounces, {round(value_kg * conversion['pounds'], 2)} pounds, {round (value_kg * conversion['stones'], 2)} stones, {round (value_kg * conversion['quarters'], 2)} quarters, {round (value_kg * conversion['long tons'], 2)} Long (UK) tons, {round (value_kg * conversion['short tons'], 2)} short (US) tons.")

#/volume slash command
@bot.tree.command(name="volume", description="Converts given volume into other units")
@app_commands.describe(value="Volume value")
@app_commands.describe(unit="Volume unit")
@app_commands.choices(unit=[
    app_commands.Choice(name="Liters", value="liters"),
    app_commands.Choice(name="Milliliters", value="mililiters"),
    app_commands.Choice(name="Pints(UK)", value="UK pints"),
    app_commands.Choice(name="Pints (US)", value="US pints"),
    app_commands.Choice(name="Gills (UK)", value="UK gills"),
    app_commands.Choice(name="Gills (US)", value="US gills"),
    app_commands.Choice(name="Quarts (UK)", value="UK quarts"),
    app_commands.Choice(name="Quarts (US)", value="US quarts"),
    app_commands.Choice(name="Gallons (UK)", value="UK gallons"),
    app_commands.Choice(name="Gallons (US)", value="US gallons")


])
@app_commands.describe(to_unit="Unit to conver to(optional)")
@app_commands.choices(to_unit=[
    app_commands.Choice(name="Liters", value="liters"),
    app_commands.Choice(name="Milliliters", value="mililiters"),
    app_commands.Choice(name="Pints(UK)", value="UK pints"),
    app_commands.Choice(name="Pints (US)", value="US pints"),
    app_commands.Choice(name="Gills (UK)", value="UK gills"),
    app_commands.Choice(name="Gills (US)", value="US gills"),
    app_commands.Choice(name="Quarts (UK)", value="UK quarts"),
    app_commands.Choice(name="Quarts (US)", value="US quarts"),
    app_commands.Choice(name="Gallons (UK)", value="UK gallons"),
    app_commands.Choice(name="Gallons (US)", value="US gallons")

])
async def mass(interaction: discord.Interaction, value: float, unit: str, to_unit: str = None) -> None:

    # Table of units
    conversion = {
        'liters': 1,
        'milliliters': 1000,
        'UK pints': 1.7597539864,
        'US pints': 2.1133764189,
        'UK gills': 7.0390159456,
        'US gills': 8.4535056755,
        'UK quarts': 0.8798771,
        'US quarts': 1.056688,
        'UK gallons': 0.2199693,
        'US gallons': 0.264172

    }

    if to_unit:

        #Converts given value to liters
        value_l = value * conversion[unit]
        #Converts value from liters to 2nd given unit
        converted_value = value_l * conversion[to_unit]
        await interaction.response.send_message(f"{value} {unit} is {round (converted_value, 3)} {to_unit}")
    else:
        #Converts given value to meters
        value_l = value * conversion[unit]
        await interaction.response.send_message(f"{value} {unit} is: {round (value_l * conversion['liters'], 2)} liters, {round (value_l * conversion['milliliters'], 3)} milliliters, {round (value_l * conversion['UK pints'], 2)} UK pints, {round (value_l * conversion['US pints'], 2)} US pints, {round (value_l * conversion['UK gills'], 2)} UK gills, {round(value_l * conversion['US gills'], 2)} US gills, {round (value_l * conversion['UK quarts'], 2)} UK quarts, {round (value_l * conversion['US quarts'], 2)} US quarts, {round (value_l * conversion['UK gallons'], 2)} UK gallons, {round (value_l * conversion['US gallons'], 2)} US gallons.")



# /time slash command
@bot.tree.command(name="time", description="Gives information about the time in the specified place.")
@app_commands.describe(location="Place of which you want to check the time")
async def time(interaction: discord.Interaction, location: str) -> None:
    current_time = get_time_in_location(location)
    if current_time[0] == "L":
        print(f"/time command ran")
        await interaction.response.send_message("Location not found. Examples of a correct use of the !time command: /time berlin, /time finland \nAfter /time write a city or a country name. Note that it'll only display a single timezone, even if a country has many.")
    else:
        print(f"/time command ran")
        await interaction.response.send_message(f'The current time in {location.title()} is ***{current_time}***')



# /speed slash command
@bot.tree.command(name="speed", description="Converts given velocity units into other units")
@app_commands.describe(value="Velocity value")
@app_commands.describe(unit="Velocity unit")
@app_commands.choices(unit=[
    app_commands.Choice(name="Kilometers per hour", value="km/h"),
    app_commands.Choice(name="Miles per hour", value="mph"),
    app_commands.Choice(name="Meters per second", value="m/s"),
    app_commands.Choice(name="Feet per minute", value="fpm")
])
async def speed(interaction: discord.Interaction, value: float, unit: str) -> None:
    unit = unit.lower()
    if unit == "km/h":
        mph = value * 0.621371192
        mps = value * 0.277777778
        fpm = value * 54.680664916
        print(f"/speed command ran")
        await interaction.response.send_message(f'***{round(value, 2)}*** km/h is ***{round(mph, 2)}*** mph, ***{round(mps, 2)}*** m/s and ***{round(fpm, 2)}*** fpm.')
    elif unit == "mph":
        kmph = value * 1.609344
        mps = value * 0.44704
        fpm = value * 88
        print(f"/speed command ran")
        await interaction.response.send_message(f'***{round(value, 2)}*** mph is ***{round(kmph, 2)}*** km/h, ***{round(mps, 2)}*** m/s and ***{round(fpm, 2)}*** fpm.')
    elif unit == "m/s":
        mph = value * 2.23693629
        kmph = value * 3.6
        fpm = value * 196.85039370079
        print(f"/speed command ran")
        await interaction.response.send_message(f'***{round(value, 2)}*** m/s is ***{round(mph, 2)}*** km/h, ***{round(kmph, 2)}*** m/s and ***{round(fpm, 2)}*** fpm.')
    elif unit == "fpm":
        mph = value * 0.0113636
        mps = value * 0.00508
        kmph = value * 0.018287941478400002
        print(f"/speed command ran")
        await interaction.response.send_message(f'***{round(value, 2)}*** fpm is ***{round(mph, 2)}*** mph, ***{round(mps, 2)}*** m/s and ***{round(kmph, 2)}*** km/h.')
    else:
        await interaction.response.send_message("Unkown parameters. Please use numbers for the value and choose an unit.")
        print(f"/speed command ran")


# runs the bot with the token, not visible in commits
bot.run("")