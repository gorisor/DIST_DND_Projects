# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 12:31:17 2020

@author: GORISOR
"""

import random

# Roll dice (Num is number of dice, d is number of sides, mod is single addition modifier)
def rolld(num,d,mod):
    value = mod
    for i in range(num):
        value += random.randint(1,d)
    return value

# Roll the 6 cardinal stats of a character (4d6, choose highest 3)
def rollStats():
    stats = [0]*6
    for i in range(6):
        rolls = [rolld(1,6,0),rolld(1,6,0),rolld(1,6,0),rolld(1,6,0)]     
        rolls.remove(min(rolls))
        stats[i] = rolls[0] + rolls[1] + rolls[2]
    return stats

# Return the modifier for a stat
def getMOD(stat):
    return (stat-10)//2


# General Character
class basicCharacter:
    def __init__(self,name,stats):
        # Set Stats
        self.strength = int(stats[0])       
        self.dexterity = int(stats[1])        
        self.constitution = int(stats[2])        
        self.intelligence = int(stats[3])     
        self.wisdom = int(stats[4])     
        self.charisma = int(stats[5])
        
        # Set Mods
        self.STR = getMOD(self.strength)
        self.DEX = getMOD(self.dexterity)
        self.CON = getMOD(self.constitution)
        self.INT = getMOD(self.intelligence)
        self.WIS = getMOD(self.wisdom)
        self.CHA = getMOD(self.charisma) 
        
        # Set other values
        self.name = name
        self.Class = "None"
        self.AtkMOD = getMOD(self.strength)     
        self.AC = 10 + self.DEX
        self.HP = rolld(1,6,self.CON)
        self.INIT = self.DEX        

    # No longer necessary
    def getInitiative(self):
        rolld20 = rolld(1,20,0)
        return rolld20
    
    # Gather all information from character
    # Returns string
    def printChar(self):
        charInfo = "Name: "+self.name+"  Class: "+self.Class
        # STR
        temp = "\nSTR: " + str(self.strength) + "+" + str(self.STR)
        if self.STR < 0:
            temp = temp.replace("+","")
        charInfo += temp
        
        # DEX
        temp = " DEX: " + str(self.dexterity) + "+" + str(self.DEX)
        if self.DEX < 0:
            temp = temp.replace("+","")
        charInfo += temp
        
        # CON
        temp = "\nCON: " + str(self.constitution) + "+" + str(self.CON)
        if self.CON < 0:
            temp = temp.replace("+","")
        charInfo += temp
        
        # INT
        temp = " INT: " + str(self.intelligence) + "+" + str(self.INT)
        if self.INT < 0:
            temp = temp.replace("+","")
        charInfo += temp
        
        # WIS
        temp = "\nWIS: " + str(self.wisdom) + "+" + str(self.WIS)
        if self.WIS < 0:
            temp = temp.replace("+","")
        charInfo += temp
        
        # CHA
        temp = " CHA: " + str(self.charisma) + "+" + str(self.CHA)
        if self.CHA < 0:
            temp = temp.replace("+","")
        charInfo += temp
        
        charInfo += "\nAC: " + str(self.AC)
        return str(charInfo)
    
    # Prints all character info to command line
    def DEBUG_printChar(self):
        print(self.printChar())
     
    # Returns string of key character values
    def fastPrint(self):
        charInfo = "Name: " + self.name + "\nAC: " + str(self.AC)
        return str(charInfo)
    
    # Prints key character values to command line    
    def DEBUG_fastPrint(self):
        print(self.fastPrint())


# Player Character class    
class playerCharacter(basicCharacter):
    def __init__(self,characterInfo):
        playerName = characterInfo[0]
        name = characterInfo[1]
        Class = characterInfo[2]
        level = int(characterInfo[3])
        stats = characterInfo[4:10]
        ACMod = int(characterInfo[10])
        INIT = int(characterInfo[11])
        Perc = int(characterInfo[12])
        super().__init__(name,stats)
        self.ACMod = ACMod
        self.AC += ACMod
        self.playerName = playerName
        self.Class = Class
        self.Level = level
        self.INIT = INIT
        self.Perc = Perc
    
    # Returns string of all key character values
    def fastPrint(self):
        charInfo = "Player Name: "+ self.playerName + "\nName: " + self.name
        charInfo += "\nAC: " + str(self.AC) + "\nPassive Perception: " 
        charInfo += str(self.Perc) + "\nClass: " + self.Class
        return str(charInfo)
    
    # Prints key character values to command line    
    def DEBUG_fastPrint(self):
        print(self.fastPrint())
 
    
# Randomly generated character class       
class randomCharacter(basicCharacter):
    def __init__(self,name):
        # Roll Random Stats and generate character
        stats = rollStats()
        tokenName = "Token " + str(name)
        super().__init__(tokenName,stats)
        
        # Select generic type and update
        classType = ["Warrior","Archer","Adept"]
        classSet = random.randint(1,100)
        
        # Warrior
        if classSet < 60:
            self.Class = classType[0]
            self.strength += 2
            self.constitution += 2
            self.intelligence -= 2
            self.AtkMOD = getMOD(self.strength)
        
        # Archer
        elif classSet < 90:
            self.Class = classType[1]
            self.dexterity += 2
            self.constitution -= 2
            self.AtkMOD = getMOD(self.dexterity)
            
        # Adept
        else:
            self.Class = classType[2]
            self.constitution -= 2
            self.intelligence += 2
            self.AtkMOD = getMOD(self.strength)
        
        # Set Mods
        self.STR = getMOD(self.strength)
        self.DEX = getMOD(self.dexterity)
        self.CON = getMOD(self.constitution)
        self.INT = getMOD(self.intelligence)
        self.WIS = getMOD(self.wisdom)
        self.CHA = getMOD(self.charisma) 
        
        # Update Other Values
        self.AC = 14 + self.DEX
        self.HP = 4+self.CON+ rolld(1,8,-3)
        self.MaxHP = self.HP
        self.INIT = self.DEX        
        self.Attack = "Attack: (+" + str(self.AtkMOD) + ") 1d6+" + str(self.AtkMOD)
        if self.AtkMOD < 0:
            self.Attack = self.Attack.replace("+","")
        
        # Archer Specific Changes
        if self.Class == classType[1]:
            self.Attack += "\nRange: 70 ft"
            self.AC -= 2
        
        # Adept Specific Changes
        if self.Class == classType[2]:
            self.AC -= 5
            self.Attack = self.Attack.replace("1d6","1d4")
            self.Attack += "\nSpells: (2x) Cure Wounds [1d8+3], (at will) Vicious Mockery [WIS 14, 1d4 + Disadvantage]"
    
    # Returns string of all values for character
    def printChar(self):
        charInfo = super().printChar()
        charInfo += " HP: " + str(self.HP) + "/" + str(self.MaxHP)
        charInfo += "Attack: " + self.Attack
        return str(charInfo)
    
    # Prints string of all character values to command line
    def DEBUG_printChar(self):
        print(self.printChar())
    
    # Returns string of key values for character
    def fastPrint(self):
        charInfo = super().fastPrint()
        charInfo += " HP: " + str(self.HP) + "/" + str(self.MaxHP)
        charInfo += "\n" + self.Attack
        return str(charInfo)
    
    # Prints key values for character to command line
    def DEBUG_fastPrint(self):
        print(self.fastPrint())


# Class for importing enemy characters
class importedEnemy(randomCharacter):
    def __init__(self,charInfo):
        # Roll Random Stats and generate character
        self.name = charInfo[0]
        self.HP = int(charInfo[1])
        self.MaxHP = self.HP
        self.ACMod = int(charInfo[2])
        self.AC = 10 + self.ACMod
        self.INIT = int(charInfo[3]) 
        self.Attack = "Attack: " + charInfo[4]
       
    # Returns string of all enemy values
    def printChar(self):
        charInfo = super().printChar()
        charInfo += " HP: " + str(self.HP) + "/" + str(self.MaxHP)
        charInfo += "Attack: " + self.Attack
        return str(charInfo)
    
    # Prints enemy values to command line
    def DEBUG_printChar(self):
        print(self.printChar())
    
    # Returns string of key enemy values
    def fastPrint(self):
        charInfo = "Name: " + self.name 
        charInfo += "\nAC: " + str(self.AC) + " HP: " + str(self.HP) + "/" 
        charInfo += str(self.MaxHP) + "\n" + self.Attack
        return str(charInfo)
    
    # Prints key enemy values to command line
    def DEBUG_fastPrint(self):
        print(self.fastPrint())


# Battle Manager        
class manager:
    # The Party
    playerCharacters = []
    def __init__(self):
        self.combatants = []
        self.criticalInits = []
    
    # Remove all combatants
    def clearEnemies(self):
        self.combatants = []
    
    # Add a number of random enemies
    def addEnemies(self,numEnemies):
        for i in range(numEnemies):
            newEnemy = randomCharacter(str(i))
            self.combatants.append((newEnemy,newEnemy.getInitiative()+newEnemy.INIT))
    
    # Return string of all critical rolls
    def returnCrits(self):
        info = ""
        for i in range(len(self.criticalInits)):
            info += str(self.criticalInits[i][0]) + " " + str(self.criticalInits[i][1]) + "\n"
        return info
    
    # Begin combat, sorts Initiatives, gathers criticals
    # Ensure that each character (by name) is only added once
    def startCombat(self):
        self.criticalInits = []
        for characters in manager.playerCharacters:
            addChar = True
            for combatant in self.combatants:
                if combatant[0].name == characters.name:
                    addChar = False
            if addChar:
                self.combatants.append((characters,characters.getInitiative()+characters.INIT))
        self.sortINIT()
    
    # sorts combatants according to initiative rolls
    def sortINIT(self):
        # Simple sort of combatants by init
        for i in range(len(self.combatants)):
            maxINIT = self.combatants[i][1]
            maxIndex = i
            for j in range(i,len(self.combatants)):
                if maxINIT < self.combatants[j][1]:
                    maxINIT = self.combatants[j][1]
                    maxIndex = j
            temp = self.combatants[i]
            self.combatants[i] = self.combatants[maxIndex]
            self.combatants[maxIndex] = temp
        
        # Check for critical success and failure and build string of names
        for i in range(len(self.combatants)):
            roll = self.combatants[i][1] - self.combatants[i][0].INIT
            if roll == 20:
                self.criticalInits.append((self.combatants[i][0].name,"Critical Success!"))
            elif roll == 1:
                self.criticalInits.append((self.combatants[i][0].name,"Critical Failure!"))
    
    # Return the list of combatants
    def getINITs(self):
        return self.combatants
    
    # [no longure used] Return string of ALL players and player values
    def printPlayers(self):
        chars = ""
        for character in manager.playerCharacters:
            chars += character.fastPrint()
            chars += "\n\n"
        return chars
    
    # [no longer used] Return string of ALL combatants and values
    def printCombatants(self):
        chars = ""
        for character in self.combatants:
            chars += character[0].fastPrint()
            chars += "\n\n"
        return chars

    # Return long run of all combatant information
    def printCombatantsLong(self):
        chars = ""
        for character in self.combatants:
            chars += character[0].printChar()
            chars += "\n\n"
        return chars
    
    # Return player list
    def returnPlayers(self):
        return manager.playerCharacters
    
    # Move combatant list forward by one step
    def nextCombatant(self):
        tempCharacter = self.combatants.pop(0)
        self.combatants.append(tempCharacter)
    
    # Move combatant list backward by one step
    def lastCombatant(self):
        tempCharacter = self.combatants.pop(-1)
        self.combatants.insert(0,tempCharacter)
    
    # Remove combatant from combatant list (by index)
    def killCombatant(self,index):
        self.combatants.pop(index)
    
    # Increment or decrement HP of combatant in combat
    # Remove dead combatant from combat
    def damageCombatant(self,name,e):
        for character in self.combatants:
            if character[0].name == name:
                try:
                    damage = int(e.get())
                except:
                    damage = 0
                character[0].HP -= damage
                # Remove combatant from combat if they die
                if character[0].HP <= 0:
                    self.removeCombatant(character[0].name)
    
    # Remove combatant from combat list (by name)
    def removeCombatant(self,name):
        for character in self.combatants:
            if character[0].name == name:
                self.combatants.remove(character)
                break        
    
    # Sort the playerCharacters by playerName
    def sortPCs():
        for i in range(len(manager.playerCharacters)):
            minVal = manager.playerCharacters[i].playerName.lower()
            minIndx = i
            for j in range(i,len(manager.playerCharacters)):
                if minVal > manager.playerCharacters[j].playerName.lower():
                    minVal = manager.playerCharacters[j].playerName.lower()
                    minIndx = j
            temp = manager.playerCharacters[i]
            manager.playerCharacters[i] = manager.playerCharacters[minIndx]
            manager.playerCharacters[minIndx] = temp
    
    # Add character to master list
    def addPlayerCharacter(self,character):
        addChar = True
        for chars in manager.playerCharacters:
            if chars.name == character.name:
                addChar = False
        if addChar:
            manager.playerCharacters.append(character)
            manager.sortPCs()
    
    # Read in enemies from fileName (text file)
    # See example text file for layout
    def importEnemy(self,fileName):        
        characterFile = open(fileName)
        characterInfo = []
        value = 0
        starts = [6,4,7,6,5]
        # Read file by line
        for line in characterFile:
            if line == "#EndCharacters\n":
                break
            elif line == "#Character\n":
                characterInfo = []
                value = 0
            else:
                if value >= len(starts):
                    # Add combatant
                    self.combatants.append((importedEnemy(characterInfo),rolld(1,20,int(characterInfo[3]))))
                else:
                    characterInfo.append(line[starts[value]:len(line)-1])
                    value += 1        
        characterFile.close()
    
    # Read in pary from fileName (text file)
    # See example text file for layout
    def importParty(self,fileName):        
        characterFile = open(fileName)
        characterInfo = []
        value = 0
        starts = [12,6,7,7,5,5,5,5,5,5,7,6,6]
        # Read file by line
        for line in characterFile:
            if line == "#EndCharacters\n":
                break
            elif line == "#Character\n":
                characterInfo = []
                value = 0
            else:
                if value >= len(starts):
                    # Add combatant
                    self.addPlayerCharacter(playerCharacter(characterInfo))
                else:
                    characterInfo.append(line[starts[value]:len(line)-1])
                    value += 1        
        characterFile.close()
        manager.sortPCs()
    
    # Save party to fileName (text file)
    # Follows same style guide as import for useage in both directions
    def exportParty(self,fileName):
        characterFile = open(fileName,"w+")
        for char in manager.playerCharacters:
            cI = "#Character\nPlayerName: " + char.playerName + "\nName: "
            cI += char.name + "\nClass: " + char.Class + "\nLevel: "
            cI += str(char.Level) + "\nSTR: " + str(char.strength) + "\nDEX: " 
            cI += str(char.dexterity) + "\nCON: " + str(char.constitution)
            cI += "\nINT: " + str(char.intelligence) + "\nWIS: " 
            cI += str(char.wisdom) + "\nCHA: " + str(char.charisma)
            cI += "\nACMod: " + str(char.ACMod) + "\nINIT: " + str(char.INIT) 
            cI += "\nPerc: " + str(char.Perc) + "\n\n"
            characterFile.write(cI)
        characterFile.write("#EndCharacters\n")
        characterFile.close()
    
    # Remove all characters from party list
    def clearParty(self):
        manager.playerCharacters = []
        self.combatants = []
        
    # Remove specific party member by name
    def removePartyMember(self,name):
        for character in manager.playerCharacters:
            if character.name == name:
                manager.playerCharacters.remove(character)
                manager.sortPCs()
                break
    
    # Return array of character values
    # Designed for addCharacter function in BattleManager
    def getPartyMember(self,name):
        for ch in manager.playerCharacters:
            if ch.name == name:
                return [ch.playerName,ch.name,ch.Class,ch.Level,ch.strength,
                        ch.dexterity,ch.constitution,ch.intelligence,ch.wisdom,
                        ch.charisma,ch.ACMod,ch.INIT,ch.Perc]
