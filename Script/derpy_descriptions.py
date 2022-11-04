import re
import json
from collections import defaultdict

statRegex = re.compile('local .* = Ext\.GetStat\("(.*)"\)')
descriptionRegex = re.compile('.*\.Description = "(.*)"')

statRegex2 = re.compile('    (.*) = {')

PROPERTIES = {
    "Description": re.compile('Description = "(.*)"'),
    "DisplayName": re.compile('DisplayName = "(.*)"'),
}

currentStat = None

patchedProperties = defaultdict(dict)

with open("SkillTextPatching.lua", "r") as f:
    for line in f.readlines():
        match = statRegex.search(line)
        descMatch = descriptionRegex.search(line)

        if match:
            stat = match.groups()[0]
            currentStat = stat
        elif descMatch:
            desc = descMatch.groups()[0]
            patchedProperties[currentStat]["Description"] = desc

# parse new file
with open("SkillTextPatchingPartTwo.lua", "r") as f:
    for line in f.readlines():
        match = statRegex2.search(line)

        if match:
            stat = match.groups()[0]
            currentStat = stat
        elif currentStat:
            for prop,regex in PROPERTIES.items():
                match = regex.search(line)

                if match:
                    patchedProperties[currentStat][prop] = match.groups()[0]

print(patchedProperties)

with open("derpy_output.json", "w") as f:
    f.write(json.dumps(patchedProperties, indent=2))
