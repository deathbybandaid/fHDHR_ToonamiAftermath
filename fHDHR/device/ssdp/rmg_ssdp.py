

class RMG_SSDP():

    def __init__(self, fhdhr, broadcast_ip, max_age):
        self.fhdhr = fhdhr

        self.ssdp_content = None

        self.broadcast_ip = broadcast_ip
        self.device_xml_path = '/rmg/device.xml'

        self.cable_schema = "urn:schemas-opencable-com:service:Security:1"
        self.ota_schema = "urn:schemas-upnp-org:device-1-0"

        if self.fhdhr.config.dict["fhdhr"]["reporting_tuner_type"].lower() == "antenna":
            self.schema = self.ota_schema
        elif self.fhdhr.config.dict["fhdhr"]["reporting_tuner_type"].lower() == "cable":
            self.schema = self.cable_schema
        else:
            self.schema = self.ota_schema

        self.max_age = max_age

    def get(self):
        if self.ssdp_content:
            return self.ssdp_content.encode("utf-8")

        data = ''
        data_command = "NOTIFY * HTTP/1.1"

        data_dict = {
                    "HOST": "%s:%s" % ("239.255.255.250", 1900),
                    "NT": self.schema,
                    "NTS": "ssdp:alive",
                    "USN": 'uuid:%s::%s' % (self.fhdhr.config.dict["main"]["uuid"], self.schema),
                    "SERVER": 'fHDHR/%s UPnP/1.0' % self.fhdhr.version,
                    "LOCATION": "%s%s" % (self.fhdhr.api.base, self.device_xml_path),
                    "AL": "%s%s" % (self.fhdhr.api.base, self.device_xml_path),
                    "Cache-Control:max-age=": self.max_age
                    }

        data += "%s\r\n" % data_command
        for data_key in list(data_dict.keys()):
            data += "%s:%s\r\n" % (data_key, data_dict[data_key])
        data += "\r\n"

        self.ssdp_content = data
        return data.encode("utf-8")
