
import json
from skills import Parse

mods = {
    "DOSEE": {
        "folders": ["DOSEE"],
        "path": "Output/Data/Mods/DOSEE/skills.json",
        "descriptionOverride": {},
    },
    "EE_Core": {
        "folders": ["Larian", "Amer"],
        "path": "Output/Data/Mods/EE_Core/skills.json",
        "descriptionOverride": {},
    },
    "EE1": {
        "folders": ["DOSEE", "EE1"],
        "path": "Output/Data/Mods/EE1/skills.json",
        "descriptionOverride": {},
    },
    "Derpy_Tweaks": {
        "folders": ["Larian", "Amer", "Derpy"],
        "path": "Output/Data/Mods/Derpy_Tweaks/skills.json",
        "descriptionOverride": json.load(open("derpy_output.json", "r")),
    },
    "Epip": {
        "folders": ["Larian", "Amer", "Epip"],
        "path": "Output/Data/Mods/Epip/skills.json",
        "descriptionOverride": {
            "Shout_AMER_Core_GenerateSource": {
                "Description": "<font size='19'>Tap the well of Source within you to generate an additional Source point, consuming 2 turns of Source Generation to do so. If you do not have enough turns of Source Generation or if you are already at maximum Source, extend the duration of your Source Generation by 1 turn instead.</font>",
            },
            "Target_ReactionShot": {
                "Description": "<font size='19'>Ready yourself to fire upon the first three enemies that enter target [1] radius, for the next 2 rounds. Reactive attacks performed with this skill deal damage equivalent to your basic weapon attacks.</font><br><br><font color='46b195'>Source Infusions:</font><font size='17'><br><font color='46b195'>1: </font>Gain +15% damage (+4% per Huntsman) while performing a Predator or Centurion reaction for 2 turns.<br><font color='46b195'>2 (requires 5 Huntsman): </font>For 2 turns, your Predator and Centurion reactions cost 0 AP.<br><font color='46b195'>3 (requires 9 Huntsman): </font>Apply the effect of this spell's second Source Infusion to all allies within 13m. Recover 1SP.<br> </font>",
            },
            "Cone_GroundSmash": {
                "Description": "<font size='19'>Fissure the earth, dealing [1] to enemies in a [3] degree, [2] long cone, and clearing non-cursed surfaces and clouds.<br><br><font color='b823cb'>Vulnerable III</font> consumes 7 Battered:<br>Target is easier to Batter or Harry, and suffers damage from healing.</font><br><br><font color='46b195'>Source Infusions:</font><font size='17'><br><font color='46b195'>1: </font>+5% accuracy (+1% per Warfare) and +20% damage (+4% per Warfare) while casting.<br><font color='46b195'>2 (requires 5 Warfare): </font>+40% damage (+8% per Warfare) while casting.<br><font color='46b195'>3 (requires 9 Warfare): </font>Cast on all visible enemies within 10m.<br><font color='858580' size='18' face=\"Averia Serif\"><br>Tiered statuses apply up to tier 3 and reduce resistances; see your journal for a full description.</font></font>",
            },
            "Shout_VenomCoating": {
                "Description": "<font size='19'>Coat your weapon with ill intent, adding [3] to your weapon. Additionally, consume poison surfaces and clouds within [2] radius of you, gaining up to [1], based on the size of the surface consumed.</font><br><br><font color='46b195'>Source Infusions:</font><font size='17'><br><font color='46b195'>1: </font>Grants Immunity to Poisoned, +15% Poison resistance (+2% per Geomancer), and you Poison those who attack you, for 3 turns.<br><font color='46b195'>2 (requires 5 Geomancer): </font>Create an 8m solid circle of Poison around yourself before casting.<br><font color='46b195'>3 (requires 9 Geomancer): </font>Recover 2AP and 1SP.<br> </font>",
            },
            "Projectile_Ricochet": {
                "Description": "<font size='19'>Loose an arcane arrow at target character that chains to up to [3] enemies in [2] radius, dealing [1] to each target.</font><br><br><font color='46b195'>Source Infusions:</font><font size='17'><br><font color='46b195'>1: </font>+5% accuracy (+1% per Huntsman) and +20% (+4% per Huntsman) damage while casting.<br><font color='46b195'>2 (requires 5 Huntsman): </font>Repeat 1 time, targeting a random enemy within 5m of target.<br><font color='46b195'>3 (requires 9 Huntsman): </font>Repeat 2 more times, targeting a random enemy within 5m of target.<br> </font>",
            },
            "Shout_Apotheosis": {
                "Description": "<font size='19'>Apply Apotheosis to yourself for 2 turns, allowing you to continue Source Generation while active.</font><br><br><font color='46b195'>Source Infusions:</font><font size='17'><br><font color='46b195'>1: </font>+1 turn duration (+0.1 per Polymorph). Recover 1AP.<br><font color='46b195'>2 (requires 5 Polymorph): </font>+1 turn duration (+0.2 per Polymorph). Recover 1AP.<br><font color='46b195'>3 (requires 9 Polymorph): </font>Instead of previous Source Infusion effects: Source generation produces +1 SP each turn, until it is depleted.<br> </font>"
            },
        },
    },
}

for modId in mods:
    mod = mods[modId]

    result = Parse(mod["folders"], mod["descriptionOverride"])

    output = json.dumps(result, indent=2)
    with open(mod["path"], "w") as f:
        f.write(output)