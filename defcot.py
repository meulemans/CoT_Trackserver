import re
import datetime as dt
from decimal import *
import xml.etree.ElementTree as ET

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
			"lon":  str(f"{self.lon:.6f}"),
			"hae": str(f"{self.hae:.0f}"),
			"ce":  str(f"{self.ce:.0f}"),
			"le": str(f"{self.le:.0f}")
			}
			
			cot = ET.Element('point', attrib=pt_attr)
			return cot
		
		@property
		def lat(self):
			getcontext().prec = 8
			return Decimal(self.__lat)*1

		@lat.setter
		def lat(self, lat):
			getcontext().prec = 8
			if lat <= 90 and lat >= -90:
				self.__lat = Decimal(lat)*1
			else:
				raise Exception("Latitude based on WGS-84 ellipsoid in signed degree-decimal format (e.g. -33.350000). Range -90 -> +90.")

		@property
		def lon(self):
			getcontext().prec = 8
			return Decimal(self.__lon)*1

		@lon.setter
		def lon(self, lon):
			if lon <= 180 and lon >= -180:
				getcontext().prec = 8
				self.__lon = Decimal(lon)*1
			else:
				raise Exception("Longitude based on WGS-84 ellipsoid in signed degree-decimal format (e.g. 44.383333). Range -180 -> +180.")

		@property
		def hae(self):
			getcontext().prec = 3
			return Decimal(self.__hae)*1

		@hae.setter
		def hae(self, hae):
			getcontext().prec = 3
			self.__hae = Decimal(hae)*1

		@property
		def ce(self):
			getcontext().prec = 3
			return Decimal(self.__ce)*1

		@ce.setter
		def ce(self, ce):
			getcontext().prec = 3
			self.__ce = Decimal(ce)*1

		@property
		def le(self):
			getcontext().prec = 3
			return Decimal(self.__le)*1

		@le.setter
		def le(self, le):
			getcontext().prec = 3
			self.__le = Decimal(le)*1
			
	class Detail:

		class Remark:
			def __init__(self,text):
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
				return str(self.__source)

			@source.setter
			def source(self, source):
				self.__source = str(source)

			@property
			def time(self):
				return self.__time

			@time.setter
			def time(self, time):
				self.__time = time.strftime(DATETIME_FMT)

			@property
			def to(self):
				return str(self.__to)

			@to.setter
			def to(self, to):
				self.__to = str(to)

			@property
			def keywords(self):
				return str(self.__keywords)

			@keywords.setter
			def keywords(self, keywords):
				p=re.compile('[\w\- ]+(,[\w\- ]+)*')
				if p.match(keywords):
					self.__keywords = str(keywords)
				else:
					raise Exception("Keywords format needs to comply with [\w\- ]+(,[\w\- ]+)*")

			@property
			def version(self):
				getcontext().prec = 2
				return Decimal(self.__version)

			@version.setter
			def version(self, version):
				getcontext().prec = 2
				self.__version = Decimal(version)

			@property
			def text(self):
				return str(self.__text)

			@text.setter
			def text(self, text):
				self.__text = text
	
		class Track:
				def __init__(self,course,speed):
					self.course = course
					self.speed = speed

				def generate_cot(self):
					trck_attr = {
					"course":str(self.course),
					"speed":str(f"{self.speed:.1f}")
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
					return int(self.__course)

				@course.setter
				def course(self, course):
					if (int(course) <= 360) or (int(course)>=0):
						self.__course = int(course)
					else:
						raise Exception("Course needs to be between 0 and 360")
	
				@property
				def Speed(self):
					getcontext().prec = 1
					return Decimal(self.__Speed)*1

				@Speed.setter
				def Speed(self, Speed):
					getcontext().prec = 1
					self.__Speed = Decimal(Speed)*1
			
				@property
				def slope(self):
					return int(self.__slope)

				@slope.setter
				def slope(self, slope):
					if (int(slope) <= 90) or (int(slope)>=-90):
						self.__slope = int(slope)
					else:
						raise Exception("slope needs to be between -90 and 90")

				@property
				def eCourse(self):
					getcontext().prec = 2
					return Decimal(self.__eCourse)*1

				@eCourse.setter
				def eCourse(self, eCourse):
					getcontext().prec = 2
					self.__eCourse = Decimal(eCourse)*1

				@property
				def eSpeed(self):
					getcontext().prec = 2
					return Decimal(self.__eSpeed)*1

				@eSpeed.setter
				def eSpeed(self, eSpeed):
					getcontext().prec = 2
					self.__eSpeed = Decimal(eSpeed)*1

				@property
				def eSlope(self):
					getcontext().prec = 2
					return Decimal(self.__eSlope)*1

				@eSlope.setter
				def eSlope(self, eSlope):
					getcontext().prec = 2
					self.__eSlope = Decimal(eSlope)*1		
		
				@property
				def version(self):
					getcontext().prec = 2
					return Decimal(self.__version)*1

				@version.setter
				def version(self, version):
					getcontext().prec = 2
					self.__version = Decimal(version)*1

		class Flow_Tags:
			def __init__(self,version):
				self.version=version
						
			@property
			def version(self):
				getcontext().prec = 2
				return Decimal(self.__version)*1

			@version.setter
			def version(self, version):
				getcontext().prec = 2
				self.__version = Decimal(version)*1
	
			@property
			def innerXML(self):
				return self.__innerXML

			@innerXML.setter
			def innerXML(self, innerXML):
				self.__innerXML = ET.fromstring(innerXML)

			def generate_cot(self):
				fltgs_attr = {
				"version":str(f"{self.version:.2f}")
				}
				cot = ET.Element('_flow-tags_', attrib=fltgs_attr)
				cot.text=self.innerXML
				return cot

		class Uid:
			def __init__(self,version):
				self.version=version
		
			@property
			def version(self):
				getcontext().prec = 2
				return Decimal(self.__version)*1

			@version.setter
			def version(self, version):
				getcontext().prec = 2
				self.__version = Decimal(version)*1
		
			@property
			def attributes(self):
				return self.__Attributes

			@attributes.setter
			def attributes(self, Attributes):
				self.__Attributes = Attributes
	
			def generate_cot(self):
				uid_attr = {
				"version":str(f"{self.version:.2f}")
				}
				try:
					for key, value in self.attributes:
						uid_attr[key]=str(value)
				except AttributeError:
					pass
				cot = ET.Element('uid', attrib=uid_attr)
				return cot

		class Status:
			def __init__(self, battery):
				self.battery = battery

			@property
			def battery(self):
				return int(self.__battery)

			@battery.setter
			def battery(self, battery):
				self.__battery = int(battery)

			@property
			def readiness(self):
				return bool(self.__readiness)

			@readiness.setter
			def readiness(self, readiness):
				self.__readiness = bool(readiness)

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

		def generate_cot(self):
			cot = ET.Element('detail')
			if isinstance(self.remark,Event.Detail.Remark):
				try:
					cot.append(self.remark.generate_cot())
				except AttributeError:
					pass
			if isinstance(self.track,Event.Detail.Track):
				try:
					cot.append(self.track.generate_cot())
				except AttributeError:
					pass
			if isinstance(self.flow_tags,Event.Detail.Flow_Tags):
				try:
					cot.append(self.flow_tags.generate_cot())
				except AttributeError:
					pass
			if isinstance(self.uid,Event.Detail.Uid):
				try:
					cot.append(self.uid.generate_cot())
				except AttributeError:
					pass
			if isinstance(self.status,Event.Detail.Status):
				try:
					cot.append(self.status.generate_cot())
				except AttributeError:
					pass
			return cot

		@property
		def remark(self):
			try:
				return self.__Remark
			except Exception:
				pass

		@remark.setter
		def remark(self, Remark):
			if isinstance(Remark,Event.Detail.Remark):
				self.__Remark = Remark
			else:
				raise Exception("Remark must be an instance of Event.Detail.Remark")

		@property
		def track(self):
			try:
				return self.__Track
			except Exception:
				pass

		@track.setter
		def track(self, Track):
			if isinstance(Track,Event.Detail.Track):
				self.__Track = Track
			else:
				raise Exception("Track must be an instance of Event.Detail.Track")

		@property
		def flow_tags(self):
			try:
				return self.__Flow_Tags
			except Exception:
				pass

		@flow_tags.setter
		def flow_tags(self, Flow_Tags):
			if isinstance(Flow_Tags,Event.Detail.Flow_Tags):
				self.__Flow_Tags = Flow_Tags
			else:
				raise Exception("Flow_Tags must be an instance of Event.Detail.Flow_Tags")

		@property
		def uid(self):
			try:
				return self.__uid
			except Exception:
				pass

		@uid.setter
		def uid(self, Uid):
			if isinstance(Uid,Event.Detail.Uid):
				self.__uid = Uid
			else:
				raise Exception("Uid must be an instance of Event.Detail.Uid")

		@property
		def status(self):
			try:
				return self.__status
			except Exception:
				pass

		@status.setter
		def status(self, status):
			if isinstance(status,Event.Detail.Status):
				self.__status = status
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
			"uid": str(self.uid),
			"time": str(self.time),
			"start": str(self.start),
			"stale": str(self.stale),
			"type": str(self.type),
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
		if hasattr(self,'detail'):
			try:
				cot.append(self.detail.generate_cot())
			except AttributeError:
				pass
		return cot

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
	def type(self, type):
		self.__type = str(type)

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
		if isinstance(time,str):
			self.__time = dt.datetime.strptime(time,'%Y-%m-%d %H:%M:%S').strftime(DATETIME_FMT)
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