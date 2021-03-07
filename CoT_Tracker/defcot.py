import datetime as dt
import re
import xml.etree.ElementTree as ET
from decimal import *

DATETIME_FMT = "%Y-%m-%dT%H:%M:%SZ"


class Event:
    class Point:
        def __init__(self, lat, lon, hae, ce, le):
            self.lat = lat
            self.lon = lon
            self.hae = hae
            self.ce = ce
            self.le = le

        def generate_cot(self):
            pt_attr = {
                "lat": str(f"{self.lat:.6f}"),
                "lon": str(f"{self.lon:.6f}"),
                "hae": str(f"{self.hae:.0f}"),
                "ce": str(f"{self.ce:.0f}"),
                "le": str(f"{self.le:.0f}")
            }

            cot = ET.Element('point', attrib=pt_attr)
            return cot

        @property
        def lat(self):
            return Decimal(self._lat)

        @lat.setter
        def lat(self, value):
            if 90 >= value >= -90:
                self._lat = Decimal(value)
            else:
                raise Exception(
                    "Latitude based on WGS-84 ellipsoid in signed degree-decimal format (e.g. -33.350000). Range -90 -> +90.")

        @property
        def lon(self):
            return Decimal(self._lon)

        @lon.setter
        def lon(self, value):
            if 180 >= value >= -180:
                self._lon = Decimal(value)
            else:
                raise Exception(
                    "Longitude based on WGS-84 ellipsoid in signed degree-decimal format (e.g. 44.383333). Range -180 -> +180.")

        @property
        def hae(self):
            return Decimal(self._hae)

        @hae.setter
        def hae(self, value):
            self._hae = Decimal(value)

        @property
        def ce(self):
            return Decimal(self._ce)

        @ce.setter
        def ce(self, value):
            self._ce = Decimal(value)

        @property
        def le(self):
            return Decimal(self._le)

        @le.setter
        def le(self, value):
            self._le = Decimal(value)

    class Detail:

        class Remark:
            def __init__(self, text):
                self.text = text

            def generate_cot(self):
                rmrks_attr = {}
                try:
                    rmrks_attr["source"] = str(self.source)
                except AttributeError:
                    pass
                try:
                    rmrks_attr["time"] = str(self.time)
                except AttributeError:
                    pass
                try:
                    rmrks_attr["to"] = str(self.to)
                except AttributeError:
                    pass
                try:
                    rmrks_attr["keywords"] = str(self.keywords)
                except AttributeError:
                    pass
                try:
                    rmrks_attr["version"] = str(self.version)
                except AttributeError:
                    pass
                cot = ET.Element('remarks', attrib=rmrks_attr)
                cot.text = self.text
                return cot

            @property
            def source(self):
                return str(self._source)

            @source.setter
            def source(self, value):
                self._source = str(value)

            @property
            def time(self):
                return self._time

            @time.setter
            def time(self, value):
                self._time = value.strftime(DATETIME_FMT)

            @property
            def to(self):
                return str(self._to)

            @to.setter
            def to(self, value):
                self._to = str(value)

            @property
            def keywords(self):
                return str(self._keywords)

            @keywords.setter
            def keywords(self, value):
                p = re.compile('[\w\- ]+(,[\w\- ]+)*')
                if p.match(value):
                    self._keywords = str(value)
                else:
                    raise Exception("Keywords format needs to comply with [\w\- ]+(,[\w\- ]+)*")

            @property
            def version(self):
                getcontext().prec = 2
                return Decimal(self._version)

            @version.setter
            def version(self, value):
                getcontext().prec = 2
                self._version = Decimal(value)

            @property
            def text(self):
                return str(self._text)

            @text.setter
            def text(self, value):
                self._text = value

        class Track:
            def __init__(self, course, speed):
                self.course = course
                self.speed = speed

            def generate_cot(self):
                trck_attr = {
                    "course": str(self.course),
                    "speed": str(f"{self.speed:.1f}")
                }
                try:
                    trck_attr["slope"] = str(self.slope)
                except AttributeError:
                    pass
                try:
                    trck_attr["eCourse"] = str(f"{self.eCourse:.2f}")
                except AttributeError:
                    pass
                try:
                    trck_attr["eSpeed"] = str(f"{self.eSpeed:.2f}")
                except AttributeError:
                    pass
                try:
                    trck_attr["eslope"] = str(f"{self.eSlope:.2f}")
                except AttributeError:
                    pass
                try:
                    trck_attr["version"] = str(f"{self.version:.2f}")
                except AttributeError:
                    pass
                cot = ET.Element('track', attrib=trck_attr)
                return cot

            @property
            def course(self):
                return int(self._course)

            @course.setter
            def course(self, value):
                if (int(value) <= 360) or (int(value) >= 0):
                    self._course = int(value)
                else:
                    raise Exception("Course needs to be between 0 and 360")

            @property
            def Speed(self):
                getcontext().prec = 1
                return Decimal(self._Speed) * 1

            @Speed.setter
            def Speed(self, value):
                getcontext().prec = 1
                self._Speed = Decimal(value) * 1

            @property
            def slope(self):
                return int(self._slope)

            @slope.setter
            def slope(self, value):
                if (int(value) <= 90) or (int(value) >= -90):
                    self._slope = int(value)
                else:
                    raise Exception("slope needs to be between -90 and 90")

            @property
            def eCourse(self):
                getcontext().prec = 2
                return Decimal(self._eCourse) * 1

            @eCourse.setter
            def eCourse(self, value):
                getcontext().prec = 2
                self._eCourse = Decimal(value) * 1

            @property
            def eSpeed(self):
                getcontext().prec = 2
                return Decimal(self._eSpeed) * 1

            @eSpeed.setter
            def eSpeed(self, value):
                getcontext().prec = 2
                self._eSpeed = Decimal(value) * 1

            @property
            def eSlope(self):
                getcontext().prec = 2
                return Decimal(self._eSlope) * 1

            @eSlope.setter
            def eSlope(self, value):
                getcontext().prec = 2
                self._eSlope = Decimal(value) * 1

            @property
            def version(self):
                getcontext().prec = 2
                return Decimal(self._version) * 1

            @version.setter
            def version(self, value):
                getcontext().prec = 2
                self._version = Decimal(value) * 1

        class Flow_Tags:
            def __init__(self, version):
                self.version = version

            @property
            def version(self):
                getcontext().prec = 2
                return Decimal(self._version) * 1

            @version.setter
            def version(self, value):
                getcontext().prec = 2
                self._version = Decimal(value) * 1

            @property
            def innerXML(self):
                return self._innerXML

            @innerXML.setter
            def innerXML(self, value):
                self._innerXML = ET.fromstring(value)

            def generate_cot(self):
                fltgs_attr = {
                    "version": str(f"{self.version:.2f}")
                }
                cot = ET.Element('_flow-tags_', attrib=fltgs_attr)
                cot.text = self.innerXML
                return cot

        class Uid:

            @property
            def version(self):
                return Decimal(self._version)

            @version.setter
            def version(self, value):
                self._version = Decimal(value)

            @property
            def attributes(self):
                return self._attributes

            @attributes.setter
            def attributes(self, value):
                self._attributes = value

            def generate_cot(self):
                uid_attr = {}
                try:
                    uid_attr = {
                        "version": str(f"{self.version:.1f}")
                    }
                except AttributeError:
                    pass
                try:
                    for key, value in self.attributes.items():
                        uid_attr[key] = str(value)
                except AttributeError:
                    pass
                cot = ET.Element('uid', attrib=uid_attr)
                return cot

        class Status:
            def __init__(self, battery):
                self.battery = battery

            @property
            def battery(self):
                return int(self._battery)

            @battery.setter
            def battery(self, value):
                self._battery = int(value)

            @property
            def readiness(self):
                return bool(self._readiness)

            @readiness.setter
            def readiness(self, value):
                self._readiness = bool(value)

            def generate_cot(self):
                sts_attr = {
                    "battery": str(self.battery)
                }
                try:
                    sts_attr["readiness"] = str(self.readiness)
                except AttributeError:
                    pass
                cot = ET.Element('Status', attrib=sts_attr)
                return cot

        class Contact:
            def __init__(self, value):
                self.callsign = value

            @property
            def callsign(self):
                return str(self._callsign)

            @callsign.setter
            def callsign(self, value):
                self._callsign = str(value)

            @property
            def freq(self):
                return Decimal(self._freq)

            @freq.setter
            def freq(self, value):
                self._freq = Decimal(value)

            @property
            def email(self):
                return str(self._email)

            @email.setter
            def email(self, value):
                self._email = str(value)

            @property
            def dsn(self):
                return str(self._dsn)

            @dsn.setter
            def dsn(self, value):
                self._dsn = str(value)

            @property
            def phone(self):
                return str(self._phone)

            @phone.setter
            def phone(self, value):
                self._phone = str(value)

            @property
            def modulation(self):
                return str(self._modulation)

            @modulation.setter
            def modulation(self, value):
                self._modulation = str(value)

            @property
            def hostname(self):
                return str(self._hostname)

            @hostname.setter
            def hostname(self, value):
                self._hostname = str(value)

            @property
            def version(self):
                getcontext().prec = 2
                return Decimal(self._version) * 1

            @version.setter
            def version(self, value):
                getcontext().prec = 2
                self._version = Decimal(value) * 1

            def generate_cot(self):
                ct_attr = {
                    "callsign": str(self.callsign)
                }
                try:
                    ct_attr["freq"] = str(f"{self.freq:.2f}")
                except AttributeError:
                    pass
                try:
                    ct_attr["email"] = str(self.email)
                except AttributeError:
                    pass
                try:
                    ct_attr["dsn"] = str(self.dsn)
                except AttributeError:
                    pass
                try:
                    ct_attr["phone"] = str(self.phone)
                except AttributeError:
                    pass
                try:
                    ct_attr["modulation"] = str(self.modulation)
                except AttributeError:
                    pass
                try:
                    ct_attr["hostname"] = str(self.hostname)
                except AttributeError:
                    pass
                try:
                    ct_attr["version"] = str(f"{self.version:.2f}")
                except AttributeError:
                    pass
                cot = ET.Element('contact', attrib=ct_attr)
                return cot

        def generate_cot(self):
            cot = ET.Element('detail')
            if isinstance(self.remark, Event.Detail.Remark):
                try:
                    cot.append(self.remark.generate_cot())
                except AttributeError:
                    pass
            if isinstance(self.track, Event.Detail.Track):
                try:
                    cot.append(self.track.generate_cot())
                except AttributeError:
                    pass
            if isinstance(self.flow_tags, Event.Detail.Flow_Tags):
                try:
                    cot.append(self.flow_tags.generate_cot())
                except AttributeError:
                    pass
            if isinstance(self.uid, Event.Detail.Uid):
                try:
                    cot.append(self.uid.generate_cot())
                except AttributeError:
                    pass
            if isinstance(self.status, Event.Detail.Status):
                try:
                    cot.append(self.status.generate_cot())
                except AttributeError:
                    pass
            if isinstance(self.contact, Event.Detail.Contact):
                try:
                    cot.append(self.contact.generate_cot())
                except AttributeError:
                    pass
            return cot

        @property
        def remark(self):
            try:
                return self._remark
            except Exception:
                pass

        @remark.setter
        def remark(self, value):
            if isinstance(value, Event.Detail.Remark):
                self._remark = value
            else:
                raise Exception("Remark must be an instance of Event.Detail.Remark")

        @property
        def track(self):
            try:
                return self._track
            except Exception:
                pass

        @track.setter
        def track(self, value):
            if isinstance(value, Event.Detail.Track):
                self._track = value
            else:
                raise Exception("Track must be an instance of Event.Detail.Track")

        @property
        def flow_tags(self):
            try:
                return self._flow_Tags
            except Exception:
                pass

        @flow_tags.setter
        def flow_tags(self, value):
            if isinstance(value, Event.Detail.Flow_Tags):
                self._flow_Tags = value
            else:
                raise Exception("Flow_Tags must be an instance of Event.Detail.Flow_Tags")

        @property
        def uid(self):
            try:
                return self._uid
            except Exception:
                pass

        @uid.setter
        def uid(self, value):
            if isinstance(value, Event.Detail.Uid):
                self._uid = value
            else:
                raise Exception("Uid must be an instance of Event.Detail.Uid")

        @property
        def status(self):
            try:
                return self._status
            except Exception:
                pass

        @status.setter
        def status(self, value):
            if isinstance(value, Event.Detail.Status):
                self._status = value
            else:
                raise Exception("Status must be an instance of Event.Detail.Status")

        @property
        def contact(self):
            try:
                return self._contact
            except Exception:
                pass

        @contact.setter
        def contact(self, value):
            if isinstance(value, Event.Detail.Contact):
                self._contact = value
            else:
                raise Exception("Status must be an instance of Event.Detail.Status")

    def __init__(self, version, event_type, uid, time, start, stale, how):
        self.version = version
        self.type = event_type
        self.uid = uid
        self.time = time
        self.start = start
        self.stale = stale
        self.how = how

    def generate_cot(self):
        evt_attr = {
            "version": str(f"{self.version:.1f}"),
            "type": str(self.type),
            "uid": str(self.uid),
            "time": str(self.time),
            "start": str(self.start),
            "stale": str(self.stale),
            "how": str(self.how)
        }
        try:
            evt_attr["access"] = str(self.access)
        except AttributeError:
            pass
        try:
            evt_attr["qos"] = str(self.qos)
        except AttributeError:
            pass
        try:
            evt_attr["opex"] = str(self.opex)
        except AttributeError:
            pass
        cot = ET.Element('event', attrib=evt_attr)
        try:
            cot.append(self.point.generate_cot())
        except Exception:
            pass
        if hasattr(self, 'detail'):
            try:
                cot.append(self.detail.generate_cot())
            except AttributeError:
                pass
        final_cot = ('<?xml version="1.0"  encoding="UTF-8" standalone="yes"?>' + ET.tostring(cot, encoding="unicode")).encode('utf-8')
        return final_cot

    @property
    def version(self):
        getcontext().prec = 2
        return Decimal(self.__version) * 1

    @version.setter
    def version(self, version):
        getcontext().prec = 2
        self.__version = Decimal(version) * 1

    @property
    def type(self):
        return str(self.__type)

    @type.setter
    def type(self, value):
        self.__type = str(value)

    @property
    def access(self):
        return str(self.__access)

    @access.setter
    def access(self, access):
        self.__access = str(access)

    @property
    def qos(self):
        return str(self.__qos)

    @qos.setter
    def qos(self, qos):
        p = re.compile('\d-\w-\w')
        if p.match(qos):
            self.__qos = str(qos)
        else:
            raise Exception("qos format needs to comply with \d-\w-\w")

    @property
    def opex(self):
        return str(self.__opex)

    @opex.setter
    def opex(self, opex):
        p = re.compile("^[oes].*")
        if p.match(opex):
            self.__opex = str(opex)
        else:
            raise Exception("opex format needs to comply with ^[o,e,s].*")

    @property
    def uid(self):
        return str(self.__uid)

    @uid.setter
    def uid(self, uid):
        self.__uid = str(uid)

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, time):
        if isinstance(time, str):
            self.__time = dt.datetime.strptime(time, '%Y-%m-%d %H:%M:%S').strftime(DATETIME_FMT)
        else:
            self.__time = time.strftime(DATETIME_FMT)

    @property
    def start(self):
        return self.__start

    @start.setter
    def start(self, start):
        if isinstance(start, str):
            self.__start = dt.datetime.strptime(start, '%Y-%m-%d %H:%M:%S').strftime(DATETIME_FMT)
        else:
            self.__start = start.strftime(DATETIME_FMT)

    @property
    def stale(self):
        return self.__stale

    @stale.setter
    def stale(self, stale):
        if isinstance(stale, str):
            self.__stale = dt.datetime.strptime(stale, '%Y-%m-%d %H:%M:%S').strftime(DATETIME_FMT)
        else:
            self.__stale = stale.strftime(DATETIME_FMT)

    @property
    def how(self):
        return str(self.__how)

    @how.setter
    def how(self, how):
        p = re.compile('\w(-\w+)*')
        if p.match(how):
            self.__how = str(how)
        else:
            raise Exception("how format needs to comply with \w(-\w+)*")

    @property
    def point(self):
        return self.__Point

    @point.setter
    def point(self, Point):
        if isinstance(Point, Event.Point):
            self.__Point = Point
        else:
            raise Exception("Point must be an instance of Event.Point")

    @property
    def detail(self):
        return self.__Detail

    @detail.setter
    def detail(self, Detail):
        if isinstance(Detail, Event.Detail):
            self.__Detail = Detail
        else:
            raise Exception("Detail must be an instance of Event.Detail")
