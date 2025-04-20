class KachelmannWetterCard extends HTMLElement {
  set hass(hass) {
    const entityTemp = this.config.entity_temperature;
    const entityCond = this.config.entity_condition;
    const entityRain = this.config.entity_rain;

    const temp = hass.states[entityTemp].state;
    const cond = hass.states[entityCond].state;
    const rain = hass.states[entityRain].state;

    const showRain = parseInt(rain) > 30;

    this.innerHTML = `
      <ha-card header="Kachelmannwetter">
        <div style="display:flex; align-items:center; justify-content:space-between; padding:1em">
          <div>
            <div style="font-size:2em;font-weight:bold">${temp} °C</div>
            <div>Zustand: ${cond}</div>
            <div>Regen: ${rain} %</div>
          </div>
          <div style="display:flex; align-items:center">
            <img src="/local/community/kachelmannwetter/logo.png" style="height:48px;opacity:0.7; margin-right:0.5em"/>
            ${showRain ? '<img src="/local/community/kachelmannwetter/rain.gif" style="height:64px;border-radius:8px"/>' : ''}
          </div>
        </div>
      </ha-card>
    `;
  }

  setConfig(config) {
    this.config = config;
  }

  getCardSize() {
    return 3;
  }
}

customElements.define('kachelmannwetter-card', KachelmannWetterCard);
