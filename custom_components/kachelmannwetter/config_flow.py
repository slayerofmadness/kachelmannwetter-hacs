import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from .const import DOMAIN, CONF_API_KEY, CONF_LOCATION_NAME

class KachelmannConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=user_input[CONF_LOCATION_NAME], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_API_KEY): str,
                vol.Required(CONF_LOCATION_NAME): str,
                vol.Required(CONF_LATITUDE): float,
                vol.Required(CONF_LONGITUDE): float
            })
        )
