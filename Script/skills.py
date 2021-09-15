import re
import json

REMOVE_HTML_FORMATTING = True
REMOVE_SOURCE_INFUSIONS_TEXT = False
SORT_BY_ABILITY = False
REMOVE_TIERED_EFFECT_HINT = True
CUSTOM_HIGHLIGHTING = True

# todo show applied effects

newDefRegex = re.compile('new entry "(.*)"')
paramRegex = re.compile('data "(.*)" "(.*)"')
usingSearch = re.compile('using "(.*)"')
cleanseRegex = re.compile("(Cleanses .*\.)")
descRegex = re.compile('<font size=(\'|\")19(\'|\")>(?P<FullText>.*)</font>') # 2 vanilla skills use " instead of '

potionTypes = [
    "Potion.txt",
    "Status_ACTIVE_DEFENSE.txt",
    "Status_BLIND.txt",
    "Status_CHALLENGE.txt",
    "Status_CHARMED.txt",
    "Status_CONSUME.txt",
    "Status_DAMAGE.txt",
    "Status_DAMAGE_ON_MOVE.txt",
    "Status_DEACTIVATED.txt",
    "Status_DECAYING_TOUCH.txt",
    "Status_DEMONIC_BARGAIN.txt",
    "Status_DISARMED.txt",
    "Status_EFFECT.txt",
    "Status_EXTRA_TURN.txt",
    "Status_FEAR.txt",
    "Status_FLOATING.txt",
    "Status_GUARDIAN_ANGEL.txt",
    "Status_HEAL.txt",
    "Status_HEAL_SHARING.txt",
    "Status_HEAL_SHARING_CASTER.txt",
    "Status_HEALING.txt",
    "Status_INCAPACITATED.txt",
    "Status_INVISIBLE.txt",
    "Status_KNOCKED_DOWN.txt",
    "Status_MUTED.txt",
    "Status_PLAY_DEAD.txt",
    "Status_POLYMORPHED.txt",
    "Status_SPARK.txt",
    "Status_STANCE.txt",
    "Status_THROWN.txt",
    "Weapon.txt",
]
tieredStatuses = {
    "AMER_DECAYING_APPLY": re.compile("AMER_DECAYING_APPLY"),
    "AMER_WEAKENED_APPLY": re.compile("AMER_WEAKENED_APPLY"),
    "AMER_ENTHRALLED_APPLY": re.compile("AMER_ENTHRALLED_APPLY"),
    "AMER_ATAXIA_APPLY": re.compile("AMER_ATAXIA_APPLY"),

    "AMER_SQUELCHED_APPLY": re.compile("AMER_SQUELCHED_APPLY"),
    "AMER_TERRIFIED_APPLY": re.compile("AMER_TERRIFIED_APPLY"),
    "AMER_SLOWED_APPLY": re.compile("AMER_SLOWED_APPLY"),
    "AMER_BLIND_APPLY": re.compile("AMER_BLIND_APPLY"),
}
relevantParams = {
    "id": "",
    "SkillType": "",
    "Ability": "None",
    "ActionPoints": 0,
    "Cooldown": "0",
    "Icon": "",
    "DisplayNameRef": "NO NAME",
    "DescriptionRef": "NO DESC",
    "MemorizationRequirements": "",
    "Stealth": "No",
    "UseWeaponDamage": "No",
    "UseWeaponProperties": "No",
    "Damage Multiplier": "100",
    "Damage Range": "10",
    "DamageType": "None",
    "Memory Cost": "0",
    "Magic Cost": 0,
    "SkillProperties": [],

    # manually-added properties
    "TieredStatuses": {},
    "Hidden": False,

    "IsEnemySkill": "No",

    # debug
    "StatsDescriptionParams": "",
    "ExplodeRadius": 0, # for some reason removing this breaks a few spell descs ???
}
# these parameters will have a "m" added at the end of their value in skill descriptions
parametersWithDistance = [
    "Range", "AreaRadius", "ExplodeRadius", "HitRadius", "MaxDistance", "TargetRadius"
]
skillTypes = [
    "Skill_Cone.txt",
    "Skill_Dome.txt",
    "Skill_Jump.txt",
    "Skill_MultiStrike.txt",
    "Skill_Projectile.txt",
    "Skill_ProjectileStrike.txt",
    "Skill_Quake.txt",
    "Skill_Rain.txt",
    "Skill_Rush.txt",
    "Skill_Shout.txt",
    "Skill_Storm.txt",
    "Skill_Summon.txt",
    "Skill_Target.txt",
    "Skill_Teleportation.txt",
    "Skill_Tornado.txt",
    "Skill_Wall.txt",
    "Skill_Zone.txt",
]
# special skills, like the lizards's flame breath. You can use this tag to hide them in skillbook selection for example
hiddenSkills = [
    # "Shout_InspireStart",
    # "Shout_FleshSacrifice",
    # "Cone_Flamebreath",
    # "Target_AMER_VampiricTouch",

    # "Dome_CircleOfProtection",
    # "Target_DemonicStare",
    # "Shout_BreakTheShackles",
    # "Target_MaddeningSong",
    # "Summon_SoulWolf",
    # "Target_Squall",
    # "Target_TimeWarp",
    # "Target_PetrifyingTouch",

    "Storm_Ethereal",
    "Target_BloatedCorpse_TheSupplicant",
    "Shout_AcclimateElectricFence",
    "Shout_ElectricFence_NEW",
    "Shout_MassCleanseWounds",
    "Shout_VampiricHungerAura",
    "Projectile_DustBlast",
    "Shout_VenomousAura",
    "Shout_MassOilyCarapace",
    "Projectile_PyroclasticEruption",
    "Target_Quest_PermanentSoulMate",
    "Target_AMER_Artifact_Deck",
    "Projectile_Grenade_ArmorPiercing_BoneHand",

    # DERPY
    "Cone_AcclimateShatter",
    "Target_AcclimateFireWhip",
    "Target_AcclimateWormTremor",
    "ProjectileStrike_MalleusMaleficarum_DazingBolt",
    "Projectile_Multishot_SI1",
    "Projectile_DimensionalBolt_SI1",


    
    # "Shout_AMER_Core_GenerateSource",

    # "Target_DemonicBargain_Wealth",
    # "Summon_Cat",
    # "Summon_Condor",
    # "Summon_AMER_BoneshapedSkitterer",
    # "Summon_AMER_BoneshapedCrusher",
    # "Summon_Quest_SummonNewt",
    # "Shout_Ignition_Splendor",
    # "Summon_AMER_AccursedVessel",
    # "Target_BloatedCorpse_TheSupplicant",
    # "Target_AMER_CorpseMastery",
    # "Projectile_BouncingShield_TheArena",

    # todo handle this properly. we cannot filter this one out the normal way because the Amer version of this spell has the same string in its name

]

# manually-overwritten properties, mostly for skills used from items.
propertyOverrides = {
    "Projectile_Grenade_WaterBlessedBalloon": {"Icon": "Item_GRN_WaterBalloon_Blessed"},
    "Projectile_Grenade_BlessedOilFlask": {"Icon": "Item_GRN_OilFlask_Blessed"},
    "Projectile_Grenade_BlessedIce": {"Icon": "Item_GRN_Ice_Blessed"},
    "Projectile_Grenade_CursedMolotov": {"Icon": "Item_GRN_Molotov_Cursed"},
    "ProjectileStrike_Grenade_CursedClusterBomb": {"Icon": "Item_GRN_ClusterBomb_Cursed"},
}
apCostOverrides = {
    "Projectile_Grenade_ArmorPiercing": 3,
    "Projectile_Grenade_Nailbomb": 3,
    "Projectile_Grenade_Flashbang": 3,
    "Projectile_Grenade_Molotov": 3,
    "Projectile_Grenade_CursedMolotov": 3,
    "Projectile_Grenade_Love": 3,
    "Projectile_Grenade_MindMaggot": 3,
    "Projectile_Grenade_ChemicalWarfare": 3,
    "Projectile_Grenade_Terror": 3,
    "Projectile_Grenade_Ice": 3,
    "Projectile_Grenade_BlessedIce": 3,
    "Projectile_Grenade_Holy": 3,
    "Projectile_Grenade_Tremor": 3,
    "Projectile_Grenade_Taser": 3,
    "Projectile_Grenade_WaterBalloon": 3,
    "Projectile_Grenade_WaterBlessedBalloon": 3,
    "Projectile_Grenade_SmokeBomb": 3,
    "Projectile_Grenade_MustardGas": 3,
    "Projectile_Grenade_OilFlask": 3,
    "Projectile_Grenade_BlessedOilFlask": 3,
    "Projectile_Grenade_PoisonFlask": 3,
    "Projectile_Grenade_CursedPoisonFlask": 3,
    "ProjectileStrike_Grenade_ClusterBomb": 3,
    "ProjectileStrike_Grenade_CursedClusterBomb": 3,
}
for i in apCostOverrides:
    if i not in propertyOverrides:
        propertyOverrides[i] = {}
    propertyOverrides[i]["ActionPoints"] = apCostOverrides[i]

bannedStrings = [
    # Derpy
    "Derpy_StatusDamage",

    "Empowered",
    "Polymorph",
    "_Move",
    "Bane",
    "Enemy",
    
    # vanilla leftovers
    "SmokeCover",
    "MassCorpseExplosion",
    "MassCleanseWounds",
    "MassCryotherapy",
    "SpiritForm",
    "MassBreathingBubbles",
    "FlamingSkin",
    "IceSkin",
    "JellyfishSkin",
    "PoisonousSkin",
    "DeployMassTraps",
    "BlessedSmokeCloud",
    "MasterOfSparks",
    "Target_Enrage",
    "Shout_Cryotherapy",
    "ProjectileStrike_HailAttack",
    "Projectile_PyroclasticEruption",
    "EvasiveAura",
    "Shout_BreathingBubble",
    "Target_MassSabotage",

    # incarnate / summon
    "IncarnateVault",
    "IncarnateFreeFall",
    "IncarnateNetherswap",
    "IncarnateTerrifyingCruelty",
    "IncarnateGagOrder",
    "SlugSparkingSwings",

    # hmm why are these not tagged as enemy?
    "Summon_EnemyShamblingMound_Caster",
    "Summon_EnemyShamblingMound_Ranger",
    "Summon_EnemyShamblingMound_Melee",

    "InsectShockingTouch",


    # technical
    "NexusMeditate",
    "META",
    "TEST",
    "Infus_",
    "Infus",
    "Infusion",
    "SCRIPT",
    "Debug",
    "Dummy",
    "NULLSKILL",
]
enemySkillExclude = [
    "Projectile_Grenade_ArmorPiercing",
    "Projectile_Grenade_Nailbomb",
    "Projectile_Grenade_Flashbang",
    "Projectile_Grenade_Molotov",
    "Projectile_Grenade_CursedMolotov",
    "Projectile_Grenade_Love",
    "Projectile_Grenade_MindMaggot",
    "Projectile_Grenade_ChemicalWarfare",
    "Projectile_Grenade_Terror",
    "Projectile_Grenade_Ice",
    "Projectile_Grenade_BlessedIce",
    "Projectile_Grenade_Holy",
    "Projectile_Grenade_Tremor",
    "Projectile_Grenade_Taser",
    "Projectile_Grenade_WaterBalloon",
    "Projectile_Grenade_WaterBlessedBalloon",
    "Projectile_Grenade_SmokeBomb",
    "Projectile_Grenade_MustardGas",
    "Projectile_Grenade_OilFlask",
    "Projectile_Grenade_BlessedOilFlask",
    "Projectile_Grenade_PoisonFlask",
    "Projectile_Grenade_CursedPoisonFlask",
    "Projectile_Grenade_ArmorPiercing_BoneHand",

]

def ParsePotions(folders):
    potions = {}
    potion = None

    for folder in folders:
        for doc in potionTypes:
            try:
                d = open("Data/" + folder + "/" + doc)
            except:
                print(folder + " has no file " + doc)
                continue

            potionId = None
            for line in d.readlines():
                if newDefRegex.search(line):
                    search = newDefRegex.search(line).groups()

                    potions[search[0]] = {"id": search[0]}
                    potionId = search[0]
                elif paramRegex.search(line):
                    search = paramRegex.search(line).groups()
                    potions[potionId][search[0]] = search[1]
                elif usingSearch.search(line):
                    search = usingSearch.search(line).groups()
                    potions[potionId]["parent"] = search[0]

                    if search[0] in potions: # ?? 
                        for key in potions[search[0]]:
                            if key != "id":
                                potions[potionId][key] = potions[search[0]][key]
    
    return potions

def format(string, params):
    ind = 1
    for x in params:
        if x == None:
            x = "[REPLACE]"
        string = string.replace("[" + str(ind) + "]", x)
        ind += 1
    return string

def hasBannedString(string):
    for x in bannedStrings:
        if x in string:
            return True
    return False

def prettifySkillDescription(string):
    if not REMOVE_HTML_FORMATTING:
        return string

    TIERED_STATUS_STRINGS = [
        "Tiered statuses apply up to tier 3 and reduce resistances; see your journal for a full description.",

        "<font color='c80030'>Ataxia III</font> consumes 7 Battered:<br>Target slowed and is Disarmed.</font>",
        "<font color='7f25d4'>Subjugated III</font> consumes 7 Battered:<br>Target suffers damage when attacking this status' owner, making it less likely to do so; reduces AP recovery.</font>",
        "<font color='b823cb'>Vulnerable III</font> consumes 7 Battered:<br>Target is easier to Batter or Harry, and suffers damage from healing.</font>",
        "<font color='b823cb'>Terrified III</font> consumes 7 Harried:<br>Target loses attack of opportunity and spends AP fleeing.</font>",
        "<font color='797980'>Dazzled III</font> consumes 7 Harried:<br>Target has reduced accuracy, dodge, and is Blinded.</font>",
        "<font color='c80030'>Slowed III</font> consumes 7 Harried:<br>Target has reduced movement and AP recovery.</font>",
        "<font color='797980'>Squelched III</font> consumes 7 Harried:<br>Target loses AP when using movement skills and is Silenced.</font>",
        "<font color='639594'>Weakened III</font> consumes 7 Battered:<br>Target's damage is reduced.</font>",
    ]

    if REMOVE_TIERED_EFFECT_HINT:
        for entry in TIERED_STATUS_STRINGS:
            string = string.replace(entry, "")
    
    # filter out the initial formatting tag, and replace the br ones with newline character
    string = string.replace("<br>", "\n")
    string = string.replace("size='18'", "")
    string = string.replace("size=\"18\"", "")
    string = string.replace("size=\"12\"", "size=\"1\"")
    string = string.replace("<img src='Icon_BulletPoint'>", "")

    HTMLRegex = re.compile("(</*?font(.*?>)?)")

    # AHHHH THIS INCONSISTENCY IS KILLING ME
    string = string.replace("Aerothurge", "Aerotheurge")

    if REMOVE_SOURCE_INFUSIONS_TEXT:
        string = string.split("\n\nSource Infusions:")[0]

    # next, filter out inner formatting tags
    search = HTMLRegex.search(string)
    if search:
        for match in search.groups():
            string = string.replace(match, "")

    return (string)

def highlightKeywords(string):

    colorHighlighting = {
        "Pyrokinetic": "text-pyro",
        "Geomancer": "text-geo",
        "Aerotheurge": "text-aero",
        "Hydrosophist": "text-water",
        "Warfare": "text-warfare",
        "Huntsman": "text-huntsman",
        "Polymorph": "text-poly",
        "Summoning": "text-summon",
        "Scoundrel": "text-rogue",
        "Necromancer": "text-necro",

        "Earth Damage": "text-dmg-earth",
        "Fire Damage": "text-dmg-fire",
        "Water Damage": "text-dmg-water",
        "Air Damage": "text-dmg-air",
        "Physical Damage": "text-dmg-phys",
        "Piercing Damage": "text-dmg-pierce",
        "Physical Armor": "text-dmg-armor-phys",
        "Magic Armor": "text-dmg-armor-magic",
        "Weapon Damage": "text-dmg-phys",

        "Battered": "text-battered",
        "Harried": "text-harried",

        "AP": "text-ap",

        "Ataxia III": "text-ataxia",
        "Vulnerable III": "text-vulnerable",
        "Weakened III": "text-weakened",
        "Subjugated III": "text-subjugated",

        "Squelched III": "text-squelched",
        "Slowed III": "text-slowed",
        "Dazzled III": "text-dazzled",
        "Terrified III": "text-terrified",
    }

    newString = string

    for key in colorHighlighting:
        newString = newString.replace(key, "<span class='" + colorHighlighting[key] + "'>" + key + "</span>")

    search = cleanseRegex.search(newString)
    if search:
        newString = newString.replace(search.groups()[0], "<span class='text-cleanse'>" + search.groups()[0] + "</span>")

    return newString

def replaceParamsInDescription(skills, skill, potions):
    if "DescriptionRef" not in skill.keys():
        return "None"

    desc = skill["DescriptionRef"]

    # params = skill["allParams"]
    params = skill

    if "StatsDescriptionParams" in params.keys():
        paramDefs = params["StatsDescriptionParams"]
        paramList = []
        p = {"sourceType": "", "source": "", "param": "", "temp": ""}

        # todo nested references
        # might be easier to just go in reverse?
        for char in paramDefs:
            if char == ":":
                if p["source"] != "":
                    p["sourceType"] = p["source"]
                    p["source"] = p["temp"]
                    p["temp"] = ""
                else:
                    p["source"] = p["temp"]
                    p["temp"] = ""
            elif char == ";":
                p["param"] = p["temp"]
                if p["sourceType"] == "":
                    p["sourceType"] = "Skill"
                paramList.append(p)
                p = {"sourceType": "", "source": "", "param": "", "temp": ""}
            else:
                p["temp"] += char
        if p["temp"] != "":
            p["param"] = p["temp"]
            paramList.append(p)

        print(paramList)
        realValues = []
        for x in paramList:
            source = x["source"]
            sourceType = x["sourceType"]
            realSource = None
            param = x["param"]
            valid = False

            if x["sourceType"] == "Skill" or x["sourceType"] == "":
                if source == "":
                    realSource = skill
                    valid = True
                else:
                    if source in skills.keys():
                        realSource = skills[source]
                        valid = True
            elif sourceType == "StatusData" or sourceType == "Potion" or sourceType == "Weapon":
                realSource = potions[source]
                valid = True

            if valid:
                # remove spaces. property entries have spaces but formatting params do not
                param = param.replace(" ", "")
                # wtf does this do kamil ^, isnt this useless

                # special cases
                if param == "Damage":
                    # todo dmg range
                    damage = ""

                    if "Damage Multiplier" in realSource.keys():
                        damage += realSource["Damage Multiplier"]
                    elif "Damage" in realSource.keys(): # used in weapon boosts
                        damage += "(Level-based) "
                    else:
                        damage += "(UNKNOWN)"

                    # if skill uses weapon damage it wont have damagetype
                    if ("DamageType" in realSource.keys() and (realSource["DamageType"] == "Magic" or realSource["DamageType"] == "Corrosive")):
                        if realSource["DamageType"] == "Magic":
                            damage = "(" + realSource["Damage Multiplier"] + "% Damage) Magic Armor"
                        else:
                            damage = "(" + realSource["Damage Multiplier"] + "% Damage) Physical Armor"
                    elif "UseWeaponDamage" in realSource.keys() and realSource["UseWeaponDamage"] == "Yes":
                        damage += "% Weapon Damage"
                    else:
                        if "DamageType" in realSource.keys():
                            if realSource["DamageType"] == "Chaos":
                                damage += "% "
                            else:
                                damage += "% " + realSource["DamageType"] + " Damage"
                        elif "Damage Type" in realSource.keys():
                            if realSource["Damage Type"] == "Chaos":
                                damage += "% "
                            else:
                                damage += realSource["Damage Type"] + " Damage"
                        else:
                            damage += "UNKNOWN DAMAGE TYPE"
                    realValues.append(damage)
                elif param == "HealAmount":
                    if realSource["HealType"] == "Percentage":
                        baseString = "[1]% [2]"
                    else:
                        baseString = "([1] Qualifier) [2]"
                    
                    healType = realSource["HealStat"]
                    if healType == "PhysicalArmor":
                        healType = "Physical Armor"
                    elif healType == "MagicArmor":
                        healType = "Magic Armor"

                    baseString = format(baseString, [realSource["HealValue"], healType])
                    realValues.append(baseString)

                elif param in parametersWithDistance and param in realSource.keys():
                    realValues.append(realSource[param] + "m")

                elif param == "Armor":
                    realValues.append("(" + realSource[param] + " Qualifier) Armor")
                elif param == "StealthDamageMultiplier":
                    realValues.append(realSource["Stealth Damage Multiplier"])
                elif param == "DistanceDamageMultiplier":
                    realValues.append(realSource["Distance Damage Multiplier"])
                else:
                    if param in realSource.keys():
                        realValues.append(realSource[param])
            else:
                # firebrand etc doesnt work
                realValues.append(None)

        print(realValues)
        return highlightKeywords(format(desc, realValues))
    return highlightKeywords(desc)

def Parse(folders, descriptionOverrides):
    potions = ParsePotions(folders)
    skills = {}
    currentSkill = None

    for folder in folders:
        for skillType in skillTypes:
            try:
                data = open("Data/" + folder + "/" + skillType)
            except:
                print(folder + " has no file " + skillType)
                continue
            lineCount = 1
            for line in data.readlines():
                if (newDefRegex.search(line)):
                    search = newDefRegex.search(line).groups()

                    if currentSkill != None:
                        skills[currentSkill["id"]] = currentSkill

                    currentSkill = {"id": search[0], "allParams": {}}
                    
                elif usingSearch.search(line):
                    search = usingSearch.search(line)
                    baseSkillId = search.groups()[0]

                    for key in skills[baseSkillId]:
                        if key != "id":
                            currentSkill[key] = skills[baseSkillId][key]

                elif (paramRegex.search(line)):
                    paramSearch = paramRegex.search(line)
                    param = paramSearch.groups()[0]
                    value = paramSearch.groups()[1]

                    # filter out formatting from descriptions
                    if param == "DescriptionRef":
                        if currentSkill["id"] in descriptionOverrides:
                            value = descriptionOverrides[currentSkill["id"]]
                        if descRegex.search(value) != None:
                            value = prettifySkillDescription(value)
                    
                    # status effect applications, surfaces actions, etc.
                    if param == "SkillProperties":
                        statuses = []
                        print(line)
                        for key in tieredStatuses:
                            if tieredStatuses[key].search(line):
                                statuses.append(key)
                        
                        # clean up the SkillProperties line
                        line = line.replace('data "SkillProperties" ', "")
                        line = line.replace("\n", "")
                        line = line.strip("\"")
                        props = line.split(";")

                        parsedProps = {}
                        for prop in props:
                            if prop == "":
                                continue
                            params = prop.split(",")
                            currentProp = params[0]
                            prefixes = []

                            # prefixes like "SELF:"
                            propPrefixes = currentProp.split(":")
                            currentProp = propPrefixes[len(propPrefixes)-1]

                            if len(propPrefixes) > 1:
                                prefixes = propPrefixes[:1]

                                for i in range(len(prefixes)):
                                    pref = prefixes[i]
                                    if "IF(" in pref:
                                        prefixes[i] = {"condition": pref[3:len(pref)-1]}


                            name = currentProp
                            if currentProp in potions and "DisplayNameRef" in potions[currentProp]: # todo
                                name = potions[currentProp]["DisplayNameRef"]
                                pass

                            propParams = []
                            for i in range(1, len(params)):
                                propParams.append(params[i])

                            parsedProps[currentProp] = {"params": propParams, "name": name, "prefixes": prefixes}

                        currentSkill["SkillProperties"] = parsedProps
                        currentSkill["TieredStatuses"] = statuses

                    if param != "SkillProperties": # todo
                        currentSkill[param] = value

                lineCount += 1

    # remove irrelevant skills and params
    skills = FilterSkills(skills, potions)

    # parse requirements
    ParseRequirements(skills)

    # cast to integer/bool in appropriate fields
    CastFields(skills)

    ParseSourceInfusions(skills)

    for skillId in skills:
        if skillId in propertyOverrides:
            skill = skills[skillId]
            for prop in propertyOverrides[skillId]:
                skill[prop] = propertyOverrides[skillId][prop]

    return skills

colorHighlighting = {"Pyrokinetic": "text-pyro",
	"Geomancer": "text-geo",
	"Aerotheurge": "text-aero",
	"Hydrosophist": "text-water",
    "Sourcery": "text-water",
	"Warfare": "text-warfare",
	"Huntsman": "text-huntsman",
	"Polymorph": "text-poly",
	"Summoning": "text-summon",
	"Scoundrel": "text-rogue",
	"Necromancer": "text-necro",
    "Special": "text-necro"}
abilityNames = {"None": "Special", "WarriorLore": "Warfare",
		"Warrior": "Warfare",
		"WaterSpecialist": "Hydrosophist",
		"Water": "Hydrosophist",
		"EarthSpecialist": "Geomancer",
		"Earth": "Geomancer",
		"Necromancy": "Necromancer",
		"Death": "Necromancer",
		"RogueLore": "Scoundrel",
		"Rogue": "Scoundrel",
		"RangerLore": "Huntsman",
		"Ranger": "Huntsman",
		"FireSpecialist": "Pyrokinetic",
		"Fire": "Pyrokinetic",
		"Summoning": "Summoning",
		"AirSpecialist": "Aerotheurge",
		"Air": "Aerotheurge",
		"Source": "Sourcery",
		"Polymorph": "Polymorph",
		"DualWielding": "Dual Wielding",
		"Ranged": "Ranged",
		"SingleHanded": "Single Handed",
		"TwoHanded": "Two Handed",
		"Leadership": "Leadership",
		"Perseverance": "Perseverance",
		"PainReflection": "Retribution",}

def ParseSourceInfusions(skills):
    for key in skills:
        skill = skills[key]

        desc = skill["DescriptionRef"].split("Source Infusions:")
        ability = abilityNames[skill["Ability"]]

        baseDescription = desc[0]
        infusions = {}

        SIReq2 = "2 " + "(requires 5 <span class='{param1}'>{param2}</span>):".format(param1=colorHighlighting[ability], param2=ability)
        SIReq3 = "3 " + "(requires 9 <span class='{param1}'>{param2}</span>):".format(param1=colorHighlighting[ability], param2=ability)

        if (len(desc) > 1):
            infus1 = desc[1].split("1:")
            if (len(infus1) > 1):
                infusions[1] = infus1[1]

            infus2 = desc[1].split(SIReq2)
            if (len(infus2) > 1):
                infusions[2] = infus2[1]

                if 1 in infusions:
                    infusions[1] = infusions[1].replace(SIReq2 + infus2[1], "")

            infus3 = desc[1].split(SIReq3)
            if (len(infus3) > 1):
                infusions[3] = infus3[1]

                if 1 in infusions:
                    infusions[1] = infusions[1].replace(SIReq3 + infus3[1], "")
                if 2 in infusions:
                    infusions[2] = infusions[2].replace(SIReq3 + infus3[1], "")

        skill["BaseDescription"] = baseDescription
        skill["SourceInfusions"] = infusions



def FilterSkills(allSkills, potions):

    relevantSkills = {}

    for x in allSkills:
        allSkills[x]["DescriptionRef"] = replaceParamsInDescription(allSkills, allSkills[x], potions)

        allSkills[x]["Hidden"] = allSkills[x]["id"] in hiddenSkills

        if not hasBannedString(x) and ("IsEnemySkill" not in allSkills[x].keys() or allSkills[x]["IsEnemySkill"] != "Yes" or allSkills[x]["id"] == "Dome_CircleOfProtection" or x in enemySkillExclude):
            relevantSkills[x] = allSkills[x]

            keysToPop = []
            for key in relevantSkills[x]:
                if key not in relevantParams:
                    keysToPop.append(key)
            for z in keysToPop:
                relevantSkills[x].pop(z)

            for key in relevantParams:
                if key not in relevantSkills[x]:
                    relevantSkills[x][key] = relevantParams[key]
    return relevantSkills

def ParseRequirements(relevantSkills):

    for key in relevantSkills:
        skill = relevantSkills[key]

        skill["ParsedMemorizationRequirements"] = {}

        if skill["MemorizationRequirements"] == "":
            continue

        reqs = skill["MemorizationRequirements"].split("; ")

        for reqString in reqs:
            splitReqs = reqString.split(" ")
            ability = splitReqs[0]
            amount = splitReqs[1]

            skill["ParsedMemorizationRequirements"][ability] = int(amount)

def CastFields(relevantSkills):

    for key in relevantSkills:
        skill = relevantSkills[key]

        skill["ActionPoints"] = int(skill["ActionPoints"])
        skill["Cooldown"] = int(skill["Cooldown"])
        skill["UseWeaponDamage"] = True if skill["UseWeaponDamage"] == "Yes" else False

        if ("Ability" not in skill):
            skill["Ability"] = "None"


# if SORT_BY_ABILITY:
#     sort = {}
#     for x in relevantSkills:
#         skill = relevantSkills[x]
#         if "Ability" in skill.keys() and skill["Ability"] != "None":
#             if skill["Ability"] in sort.keys():
#                 sort[skill["Ability"]][skill["id"]] = skill
#             else:
#                 sort[skill["Ability"]] = {skill["id"]: skill}
#     relevantSkills["sorted"] = sort


# -------------------------

# result = Parse(["Larian", "Amer", "Derpy"], json.load(open("derpy_output.json", "r")))

# output = json.dumps(result, indent=2)
# with open("Output/skills.json", "w") as f:
    # f.write(output)

if __name__ == "__main__":
    Parse(["Larian", "Amer", "Derpy"], {})