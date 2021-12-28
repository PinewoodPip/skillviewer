import re
import json

patchedDescriptions = {}

statRegex = re.compile('local .* = Ext\.GetStat\("(.*)"\)')
descriptionRegex = re.compile('.*\.Description = "(.*)"')

statRegex2 = re.compile('    (.*) = {')
descriptionRegex2 = re.compile('Description = "(.*)"')

currentStat = None

with open("SkillTextPatching.lua", "r") as f:
    for line in f.readlines():
        match = statRegex.search(line)
        descMatch = descriptionRegex.search(line)

        if match:
            stat = match.groups()[0]
            currentStat = stat
            patchedDescriptions[stat] = {}
        elif descMatch:
            desc = descMatch.groups()[0]
            patchedDescriptions[currentStat] = desc

# parse new file
with open("SkillTextPatchingPartTwo.lua", "r") as f:
    for line in f.readlines():
        match = statRegex2.search(line)
        descMatch = descriptionRegex2.search(line)

        if match:
            stat = match.groups()[0]
            currentStat = stat
            patchedDescriptions[stat] = {}
        elif descMatch:
            desc = descMatch.groups()[0]
            patchedDescriptions[currentStat] = desc

print(patchedDescriptions)

with open("derpy_output.json", "w") as f:
    f.write(json.dumps(patchedDescriptions, indent=2))
