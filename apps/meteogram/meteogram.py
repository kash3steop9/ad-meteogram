import appdaemon.plugins.hass.hassapi as hass
import os.path
import requests
import json
import datetime

class MeteogramService(hass.Hass):
    BASE_URL = "https://nodeserver.cloud3squared.com/getMeteogram/"

    def initialize(self):
        config = self.get_plugin_config()

        self.meteogram_config = {
            "token": self.args["token"],
            "chartWidth": self.args.get("width") or "1350",
            "chartHeight": self.args.get("height") or "360",
            "placeName": self.args["name"],
            "longPlaceName": self.args["name"],
            "latitude": str(self.args.get("lat") or config["latitude"]),
            "longitude": str(self.args.get("lng") or config["longitude"]),
            "countryCode": self.args.get("countryCode") or "US",
            "countryCodeLang": self.args.get("countryCode") or "US",
            "appLocale": "auto",
            "theme": self.args.get("theme") or "fully-transparent",
            "chartFont": {
                "group": "Noto",
                "family": "Noto Sans",
                "size": "11"
            },
            "chartSpacing": {
                "": "20"
            },
            "hierarchical": "true",
            "daylightBandsWeekendColorDiff": "true",
            "provider": {
                "": "met.no",
                "b": "none",
                "keyKnmi": "-",
                "keyPirate": "-",
                "averaging": "false",
                "transition": "0"
            },
            "hoursToDisplay": "162",
            "hoursAvailable": "162",
            "headerLocation": "false",
            "headerTemperature": "false",
            "headerMoonPhase": "false",
            "headerUpdateTime": "false",
            "precipitationSeries": "expected",
            "precipitationAxisMin": "0",
            "precipitationAxisMax": "30",
            "precipitationAxisScale": "fixed",
            "pressure": "false",
            "cloudLayers": "true",
            "cloudLayersSharedColor": "true",
            "windSpeed": "true",
            "windSpeedMinMaxLabels": "false",
            "windSpeedUnit": self.args.get("windSpeedUnit") or "m/s",
            "windSpeedColor": "#ddc0c0c0",
            "windSpeedAxisMin": "0",
            "windSpeedAxisMax": "40",
            "windSpeedAxisScale": "fixed",
            "windArrows": "false",
            "compressionQuality": "90.0"
        }

        self.meteogram_url = self.BASE_URL + requests.utils.quote(json.dumps(self.meteogram_config).replace(" ", ""), safe='')

        self.output_path = self.args.get('outputPath') or "/config/www/meteograms/meteogram.png"

        self.run_daily(self.load_meteogram, datetime.time(4, 40, 20))

        # run immediately if no current output
        if not os.path.exists(self.output_path):
            self.load_meteogram(None)

    def load_meteogram(self, kwargs):
        try:
            r = requests.get(self.url_meteograms, allow_redirects=True)
        except Exception as err:
            # catch connection error - r does not get a status code then
            self.log("Unable to fetch meteogram: %s", err, stack_info=True)
            
            # try again in 2 minutes
            self.run_in(self.load_meteogram, 120)
        else:
            if r.status_code == 200:
                with open(self.output_path, 'wb') as fp:
                    fp.write(r.content)
            else:
                self.log("Unable to fetch meteogram: HTTP %s", r.status_code)
                # try again in 2 minutes
                self.run_in(self.load_meteogram, 120)
