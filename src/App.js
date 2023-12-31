import './App.css';
import React from 'react';
import * as utils from "./utils.js"
import { SkillTooltip } from './SkillTooltip';
import { Text, Icon, FlairedCheckbox, Dropdown, DarkHR, Tooltip } from './genericComponents';
import * as miscData from "./miscData.js"

// todo:
// missing icons
// missing statuses

const axios = require('axios').default;
const RESOURCE_PREPPEND = "/skillviewer/"

var app;

export var data = {
  icons: {},
  mods: {},
  coreMods: { // todo define externally
    // "DOSEE": {
    //   addons: []
    // },
    // "EE1": {
    //   addons: []
    // },
    "EE_Core": {
      addons: [
        "Epip",
        "Derpy_Tweaks",
      ]
    },
    "Farandole": {
      addons: []
    },
  }
};

class App extends React.Component {
  constructor()
  {
    super()
    this.state = {
      initialized: false,
      currentSkill: null,
      game: "EE_Core",

      addons: [
        "Epip",
        "Derpy_Tweaks",
      ],

      schools: ["Warrior", "Water", "Earth", "Death", "Rogue", "Ranger", "Fire", "Summoning", "Air", "Polymorph", "Summoning"],
    }
    this.farandoleClasses = {} // Filled automatically while loading skills
  }

  isModActive(id) {
    return this.state.game == id || this.state.addons.includes(id)
  }

  setGame(id) {
    let schools = []
    if (id == "Farandole") { // Set all Farandole classes to be visible
      schools = schools.concat(Object.keys(this.farandoleClasses))
    }
    else { // Set vanilla schools to be visible
      schools = schools.concat(miscData.schools)
      schools.splice(schools.indexOf("Sourcery"))
      schools.splice(schools.indexOf("Special"))
    }
    this.setState({game: id, schools: schools})
  }

  isFarandole() {
    return this.state.game == "Farandole"
  }

  toggleMod(id) {
    this.setGame(id) // TODO! consider addons better
  }

  getAddons(modId) {
    let core = data.coreMods[modId]

    let addons = []
    for (let index in core.addons) {
      let id = core.addons[index]
      addons.push(data.mods[id])
    }

    return addons
  }

  loadSkills(skills, mod) {
    for (let skillId in mod.skills) {
      let skill = mod.skills[skillId]
      let ability = skill.Ability
      let canShow = this.state.schools.includes(ability)

      // Only load non-hidden skills for each ability and exclude classed Farandole ones
      if (canShow && !skill.Hidden && !skill.FarandoleClass && !this.isFarandole()) { // TODO show regular ability skills when using Farandole
        skills[ability][skillId] = skill
      }

      // Load Farandole skills per-class instead
      if (this.isFarandole() && skill.FarandoleClass) {
        // Initialize dict
        if (!skills[skill.FarandoleClass]) {
          skills[skill.FarandoleClass] = {}
          this.farandoleClasses[skill.FarandoleClass] = skill.FarandoleClass.replace(new RegExp("^Class_", "i"), "")
        }
        if (this.state.schools.includes(skill.FarandoleClass)) {
          skills[skill.FarandoleClass][skillId] = skill
        }
      }
    }
    return skills
  }

  getSkills() {
    let skills = {
      Warrior: {},
      Water: {},
      Earth: {},
      Death: {},
      Rogue: {},
      Ranger: {},
      Fire: {},
      Summoning: {},
      Air: {},
      Source: {},
      Polymorph: {},
      None: {},
    }

    let mod = data.mods[this.state.game]

    skills = this.loadSkills(skills, mod)

    for (let modId in data.coreMods[this.state.game].addons) {
      mod = data.mods[data.coreMods[this.state.game].addons[modId]]
      if (this.isModActive(mod.metadata.id)) {
        skills = this.loadSkills(skills, mod)
      }
    }

    return skills;
  }

  toggleSchool(school) {
    const state = this.state.schools

    if (state.includes(school)) {
      state.splice(state.indexOf(school), 1)
    }
    else {
      state.push(school)
    }

    this.setState({schools: state})
  }

  setSingleSchool(school) {
    this.setState({schools: [school]})
  }

  componentDidMount() {
    // load game data
    let requests = [
      RESOURCE_PREPPEND + "Script/Output/Data/Mods/EE_Core/mod.json",
      RESOURCE_PREPPEND + "Script/Output/Data/Mods/EE_Core/skills.json",
      RESOURCE_PREPPEND + "Script/Output/Data/Mods/Derpy_Tweaks/mod.json",
      RESOURCE_PREPPEND + "Script/Output/Data/Mods/Derpy_Tweaks/skills.json",
      RESOURCE_PREPPEND + "Script/Output/Data/Mods/Epip/mod.json",
      RESOURCE_PREPPEND + "Script/Output/Data/Mods/Epip/skills.json",
      RESOURCE_PREPPEND + "Script/Output/Data/Mods/DOSEE/mod.json",
      RESOURCE_PREPPEND + "Script/Output/Data/Mods/DOSEE/skills.json",
      RESOURCE_PREPPEND + "Script/Output/Data/Mods/EE1/mod.json",
      RESOURCE_PREPPEND + "Script/Output/Data/Mods/EE1/skills.json",
      RESOURCE_PREPPEND + "Script/Output/Data/Mods/Farandole/mod.json",
      RESOURCE_PREPPEND + "Script/Output/Data/Mods/Farandole/skills.json",
    ]
    let promises = []

    app = this;

    data.icons = {
      ...utils.importAll(require.context("./images/skills", false, /\.(gif|jpe?g|svg|png)$/)),
      ...utils.importAll(require.context("./images/UI", false, /\.(gif|jpe?g|svg|png)$/)),
    }

    for (let x = 0; x < requests.length; x++) {
      promises.push(axios.get(requests[x]))
    }
    
    axios.all(promises)
      .then(async function(responses) {

        // todo cleanup
        data.mods["EE_Core"] = {}
        data.mods["EE_Core"].metadata = responses[0].data
        data.mods["EE_Core"].skills = responses[1].data

        data.mods["Derpy_Tweaks"] = {}
        data.mods["Derpy_Tweaks"].metadata = responses[2].data
        data.mods["Derpy_Tweaks"].skills = responses[3].data

        data.mods["Epip"] = {}
        data.mods["Epip"].metadata = responses[4].data
        data.mods["Epip"].skills = responses[5].data

        data.mods["DOSEE"] = {}
        data.mods["DOSEE"].metadata = responses[6].data
        data.mods["DOSEE"].skills = responses[7].data

        data.mods["EE1"] = {}
        data.mods["EE1"].metadata = responses[8].data
        data.mods["EE1"].skills = responses[9].data

        data.mods["Farandole"] = {}
        data.mods["Farandole"].metadata = responses[10].data
        data.mods["Farandole"].skills = responses[11].data

        this.setState({initialized: true})
        
        let urlParams = new URLSearchParams(window.location.search)
        const gameType = urlParams.get("game")
        if (gameType) {
          // Needs to be done twice to load Farandole classes... TODO improve
          app.setGame(gameType)
          app.loadSkills({}, data.mods[gameType])
          app.setGame(gameType)
        }
      }.bind(this))
      .catch((error) => {
        alert("The app did not load properly. Try refreshing.")
        throw error;
    });

  }

  render() {
    if (!this.state.initialized) {
      return <div className="flex-horizontal flex-vertical"><p>Loading...</p></div>
    }

    let skills = this.getSkills()

    return (
      <div className="main-container">
        <Sidebar app={this}/>
        <SkillGrid skills={skills}/>
      </div>
    );
  }
  
}

class Sidebar extends React.Component {

  render() {

    let checkboxes = []

    if (app.isFarandole()) {
      let classes = []
      for (let id in app.farandoleClasses) {
        classes.push({id: id, name: app.farandoleClasses[id]})
      }
      classes.sort(function name(a, b) {
        return a.name < b.name
      })
      for (let index in classes) {
        let farandoleClass = classes[index]
        let id = farandoleClass.id
  
        checkboxes.push(<Tooltip content={"Right-click to show only this class."} placement={"right"} key={index}>
          <FlairedCheckbox text={farandoleClass.name} ticked={this.props.app.state.schools.includes(id)} onChange={() => {this.props.app.toggleSchool(id)}} onContextMenu={() => {this.props.app.setSingleSchool(id)}}/>
        </Tooltip>)
      }
    }
    else {
      for (let index in miscData.schools) {
        let school = miscData.schools[index]
  
        checkboxes.push(<Tooltip content={"Right-click to show only this school."} placement={"right"} key={index}>
          <FlairedCheckbox text={miscData.mappings.abilityNames[school]} ticked={this.props.app.state.schools.includes(school)} onChange={() => {this.props.app.toggleSchool(school)}} onContextMenu={() => {this.props.app.setSingleSchool(school)}}/>
        </Tooltip>)
      }
    }

    let options = {}
    for (let id in data.coreMods) {
      options[id] = "Game: " + data.mods[id].metadata.name
    }

    let addons = []
    let addonData = app.getAddons(app.state.game)
    for (let index in addonData) {
      let addon = addonData[index]

      addons.push(<FlairedCheckbox text={addon.metadata.name} key={index} ticked={app.isModActive(addon.metadata.id)} onChange={() => {app.toggleMod(addon.metadata.id)}}/>)
    }

    let onGameChanged = function(ev) {
      this.props.app.setGame(ev.target.value)
    }.bind(this)

    return (
      <div className="sidebar">
        <Text text="Mods"/>

        <Dropdown options={options} selected={this.props.app.state.game} onChange={onGameChanged}/>

        <div className="checkboxes-container">
          {addons}
        </div>

        <DarkHR/>

        <Text text="Schools"/>

        <div className="checkboxes-container">
          {checkboxes}
        </div>
        
      </div>
    )
  }
}

class SkillGrid extends React.Component {

  render() {
    let elements = []

    for (let school in this.props.skills) {
      for (let skillId in this.props.skills[school]) {
        let skill = this.props.skills[school][skillId]
        elements.push(<SkillButton data={skill} key={skillId}/>)
      }
    }

    return (
      <div className="flex-horizontal-list skill-grid">
        {elements}
      </div>
    );
  }
}

class SkillButton extends React.Component {

  render() {
    let data = this.props.data
    return (
      <SkillTooltip data={data}>
        <div className="skill-button unselectable" onClick={() => {console.log(data)}}>
          <Icon img={data.Icon}/>
        </div>
      </SkillTooltip>
        // <div className="skill-button">
        //   <Icon img={data.Icon}/>
        // </div>
    )
  }
}

export default App;
