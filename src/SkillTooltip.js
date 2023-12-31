import * as utils from "./utils.js"
import './App.css';
import React from 'react';
import * as miscData from "./miscData.js"

import { DarkHR, Icon, Text, Tooltip } from "./genericComponents.js"
import HTMLReactParser from "html-react-parser";

const parse = HTMLReactParser

export function SkillTooltip(props) {
	let skill = props.data

	let tooltip = <div className="flex-vertical tooltip">
		<SkillHeader skill={skill} />

		<SkillDescription skill={skill} />

		<SkillFooter skill={skill} />

		<Cooldown skill={skill} />

	</div>

	return (
		<Tooltip content={tooltip} placement="right" classOverride={"skill-tooltip"}>
			{props.children}
		</Tooltip>
	)
}

function ActionPoint(props) {
	return (
		<div className="action-point">
			<Icon img={"action_point"} />
		</div>
	)
}

function SourcePoint(props) {
	return (
		<div className="action-point">
			<Icon img={"source_point"} />
		</div>
	)
}

function SkillHeader(props) {
	let skill = props.skill
	let apCost = skill["ActionPoints"]
	let spCost = skill["Magic Cost"]

	let apOrbs = []

	// add SP indicators
	for (let x = 0; x < spCost; x++) {
		apOrbs.push(<SourcePoint key={-x - 1} />)
	}

	// add AP indicators
	for (let x = 0; x < apCost; x++) {
		apOrbs.push(<ActionPoint key={x} />)
	}

	return (
		<div className="flex-horizontal tooltip-header-bg flex-centered">
			<div className="tooltip-header flex-horizontal-small">
				<Text text={skill.DisplayNameRef} className="tooltip-header-title"/>

				{/* <Text text={skill.id}/>	 */}

				<div className="flex-horizontal-small flex-centered">
					{apOrbs}
				</div>
			</div>
		</div>
	)
}

function SkillDescription(props) {
	let skill = props.skill

	let baseDescription = skill.BaseDescription
	baseDescription = parse("<p key='" + -1 + "'>" + baseDescription + "</p>")

	let infusionText = []
	let prefixes = [
		"<span class='text-si-symbol'>♦</span>: ",
		"<span class='text-si-symbol'>♦♦</span>: ",
		"<span class='text-si-symbol'>♦♦♦</span>: "
	]
	for (let level in skill.SourceInfusions) {
		infusionText.push(parse("<p key='" + level + "'>" + prefixes[level-1] + skill.SourceInfusions[level] + "</p>"))
	}

	// statuses
	let statuses = []
	for (let x in skill.TieredStatuses) {
		let status = skill.TieredStatuses[x]
		if (status in miscData.statusNames) {
			let text = parse(utils.format("<p class='compact-text' key='" + status + "'>Applies up to <span class='{0}'>{1}</span></p>", miscData.mappings.statusCSS[status], miscData.statusNames[status]))

			statuses.push(text)
		}
	}

	for (let action in skill.SkillProperties) {
		let data = skill.SkillProperties[action]

		// for tier 3 statuses, use the custom "Apply up to X" string. TODO move
		if (action in miscData.statusNames) {
			continue
		}

		let text = parse(utils.format("<p class='compact-text' key='" + action + "'><span class='{0}'>{1}</span></p>", "", CreateSkillPropertyLine(action, data)))

		statuses.push(text)
	}

	let statusesDisplay = null
	if (statuses.length > 0) {
		statusesDisplay = <div className="flex-vertical">

			{statuses}

		</div>
	}

	let elements = [baseDescription]
	if (Object.keys(skill.SourceInfusions).length > 0) {
		elements.push(<DarkHR key={-10}/>)
		elements.push(infusionText)
		elements.push(<DarkHR key={-20}/>)
	}

	return (
		<div className="text-left tooltip-middle">

			{elements}
			
			<div className="flex-vertical">
				{statusesDisplay}
				<Requirements skill={skill} />
			</div>
			
		</div>
	)
}

function SkillFooter(props) {
	let skill = props.skill

	let memoryCost = null
	// es-lint-disable-next-line
	if (skill["Memory Cost"] && skill["Memory Cost"] != "0") {
		memoryCost = <div className="">
			{/* <Icon size="14px" img="memory_white"/> */}
			<Text text={utils.format("{0} Memory Slot{1}", skill["Memory Cost"], parseInt(skill["Memory Cost"]) > 1 ? "s" : "")}/>
		</div>
	}
	
	// For footer, use the Farandole class, or ability name otherwise
	let abilityName = miscData.mappings.abilityNames[skill.Ability]
	let schoolName;
	if (skill.FarandoleClass) {
		schoolName = skill.FarandoleClass.replace(new RegExp("^Class_", "i"), "")
	}
	else {
		schoolName = abilityName
	}

	return (
		<div className="tooltip-bottom flex-horizontal flex-align-centered">
			<div className="tooltip-bottom-text flex-horizontal-small">
				<Text overrideColor className={miscData.colorHighlighting[abilityName]} text={schoolName}/>
				{memoryCost}
			</div>
		</div>
	)
}

function Cooldown(props) {
	let cooldown = props.skill.Cooldown == -1 ? "-" : props.skill.Cooldown
	return (
		<div className="cooldown">
			<Text text={cooldown}/>
		</div>
	)
}

function Requirements(props) {
	
	let skill = props.skill

	// memorization requirements
	let parsedReqs = []
	for (let ability in skill.ParsedMemorizationRequirements) {
		let amount = skill.ParsedMemorizationRequirements[ability]
		let abilityName = miscData.mappings.abilityNames[ability]

		let text = parse(utils.format("<p class='compact-text' key='" + ability + "'>Requires <span class='{0}'>{1} {2}</span></p>", miscData.colorHighlighting[abilityName], amount, abilityName))

		parsedReqs.push(text)
	}
	// if (skill.MemorizationRequirements) {
	// 	let reqs = skill.MemorizationRequirements.split("; ")
	// 	for (let x in reqs) {
	// 		let stat = miscData.mappings.abilityNames[reqs[x].split(" ")[0]]
	// 		let amount = reqs[x].split(" ")[1]

	// 		let text = parse(utils.format("<p class='compact-text' key='" + x + "'>Requires <span class='{0}'>{1} {2}</span></p>", miscData.colorHighlighting[stat], amount, stat))

	// 		parsedReqs.push(text)
	// 	}
	// }

	return (
		<div className="flex-vertical">
			{parsedReqs}
		</div>
	);
}

// TODO fix IF surface conditions
// create a string out of a SkillProperties entry
function CreateSkillPropertyLine(id, data) {
	let types = {
		"Curse": "Curses surfaces.",
		"Bless": "Blesses surfaces.",
		"Bloodify": "Turns surfaces bloody.",
		"Freeze": "Freezes surfaces.",
		"Douse": "Douses surfaces.",
		"Condense": "Condenses surfaces.",
		"Contaminate": "Contaminates surfaces.",
		"Electrify": "Electrifies surfaces.",
		"Ignite": "Ignites surfaces.",
		"Vaporize": "Vaporizes surfaces.",
		"Melt": "Melts surfaces.",
		"Oilify": "Contaminates surfaces to oil.",
		"Shatter": "Shatters surfaces.",

		"Force": "Pushes the target {0}cm away from caster.",
		"AlwaysBackstab": "Always backstabs.",
		"Summon": "Summons a summon.",
		"SwapPlaces": "Swaps places of caster and target.",
		"Pickup": "Picks items up.",
		"Equalize": "Equalizes health.",
		"EXPLODE": "Explodes the target.",
		"CanBackstab": "Can backstab.",
		"ADRENALINE": "Instantly gain {3} AP, and lose {4} AP next turn.",
		"AlwaysHighGround": "Is always cast from high ground.",
		"SHACKLES_OF_PAIN": "Applies Shackles of Pain for {1} turn(s).", // hardcoded status.

		"Sabotage": "Explodes {0} random grenade(s)/arrow(s) of the target.",
		"CreateSurface": "{3}% chance to create a {0}m {2} surface for {1} turn(s)",
		"TargetCreateSurface": "{3}% chance to create a {0}m {2} surface for {1} turn(s)",
		"CreateConeSurface": "Creates a {0}m {2} surface for {1} turn(s).",
		"DAMAGE_ON_MOVE": "{0}% chance to receive damage every {3}cm moved.", // TODO
	}

	let str = "Applies " +  data.name

	if (id == "CreateSurface" || id == "TargetCreateSurface") {

		let surfaceName = data.params[2] + " surface";
		let surfaceData = miscData.SURFACES[data.params[2]]

		if (surfaceData) {
			surfaceName = surfaceData.name
		}
		else
		{
			console.log(data.params[2])
		}

		let params = [...data.params]
		params[2] = surfaceName
		
		// removing surfaces
		if (surfaceName == "None") {
			return "Clears surfaces in a {0}m radius."
		}

		// if there is no chance param, or 100% chance - don't show chance
		if (params.length == 3 || params[3] == "100") {
			return utils.format("Creates a {0}m {2} for {1} turn(s).", ...params)
		}
	}

	// TODO
	if (str.includes("Arrows")) {
		return ""
	}

	if (types[id]) {
		return utils.format(types[id], ...data.params)
	}

	// status length
	if (data.params.length > 0 && data.params[1] != "0") {
		str += utils.format(" for {0} turn{1}", data.params[1], data.params[1] != "1" ? "s" : "")
	}

	for (let i in data.prefixes) {
		let prefix = data.prefixes[i]

		// TODO consider skills with multiple conditions (&)
		if (typeof prefix == "object") {
			prefix = prefix.condition
		}

		if (prefix == "SELF") {
			str += " on self"
		}
		else if (prefix == "TARGET") {
			str += " on target"
		}
		else if (prefix == "Enemy") {
			str += " on enemy"
		}
		else if (prefix.includes("SURFACEBOOST(")) {
			str += ", receives bonuses from consumed surfaces"
		}
	}

	str += "."

	return str
}