from .models import *


class NationDB(object):
    """国家"""
    def query_nation_list(self):
        result_db = Nation.objects.filter().all()
        return result_db

    def query_nation_by_id(self, nid):
        result_db = Nation.objects.filter(nid=nid).first()
        return result_db

    def update_nation(self, modify_info):
        is_exist = Nation.objects.filter(nation=modify_info['nation']).first()
        if is_exist:
            raise Exception("该国家已存在")
        Nation.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_nation(self, modify_info):
        is_exist = Nation.objects.filter(nation=modify_info['nation']).first()
        if is_exist:
            raise Exception("该国家已存在")
        Nation.objects.create(**modify_info)


class ProvinceDB(object):
    """省份"""
    def __init__(self):
        pass

    def query_province_list(self):
        result_db = Province.objects.filter().all()
        return result_db

    def query_province_by_nation(self,nation_id):
        result_db = Province.objects.filter(nation_id=nation_id).all()
        return result_db

    def query_province_by_id(self, nid):
        result_db = Province.objects.filter(nid=nid).first()
        return result_db

    def update_province(self, modify_info):
        is_exist = self.is_exist(modify_info["province"], modify_info["nation_id"])
        if is_exist:
            raise Exception("该省份已存在")
        Province.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_province(self, modify_info):
        is_exist = self.is_exist(modify_info["province"],modify_info["nation_id"])
        if is_exist:
            raise Exception("该省份已存在")
        Province.objects.create(**modify_info)

    def is_exist(self,province,nation):
        result_db = Province.objects.filter(province=province, nation_id=nation).first()
        return result_db


class CityDB(object):
    """城市"""
    def __init__(self):
        pass

    def query_city_list(self):
        result_db = City.objects.filter().all()
        return result_db

    def query_city_by_id(self, nid):
        result_db = City.objects.filter(nid=nid).first()
        return result_db

    def query_city_by_province(self, province_id):
        result_db = City.objects.filter(province_id=province_id).all()
        return result_db

    def update_city(self, modify_info):
        is_exist = self.is_exist(modify_info["province_id"], modify_info["city"])
        if is_exist:
            raise Exception("该城市已存在")
        City.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_city(self, modify_info):
        is_exist = self.is_exist(modify_info["province_id"],modify_info["city"])
        if is_exist:
            raise Exception("该城市已存在")
        City.objects.create(**modify_info)

    def is_exist(self,province,city):
        result_db = City.objects.filter(province_id=province, city=city).first()
        return result_db


class CountryDB(object):
    """县区"""
    def __init__(self):
        pass

    def query_country_list(self):
        result_db = Country.objects.filter().all()
        return result_db

    def query_country_by_id(self, nid):
        result_db = Country.objects.filter(nid=nid).first()
        return result_db

    def query_country_by_city(self, city_id):
        result_db = Country.objects.filter(city_id=city_id).all()
        return result_db

    def update_country(self, modify_info):
        is_exist = self.is_exist(modify_info["country"], modify_info["city_id"])
        if is_exist:
            raise Exception("该县区已存在")
        Country.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_country(self, modify_info):
        is_exist = self.is_exist(modify_info["country"],modify_info["city_id"])
        if is_exist:
            raise Exception("该县区已存在")
        Country.objects.create(**modify_info)

    def is_exist(self,country,city_id):
        result_db = Country.objects.filter(country=country, city_id=city_id).first()
        return result_db


class TownDB(object):
    """县区"""
    def __init__(self):
        pass

    def query_town_list(self):
        result_db = Town.objects.filter().all()
        return result_db

    def query_town_by_id(self, nid):
        result_db = Town.objects.filter(nid=nid).first()
        return result_db

    def query_town_by_country(self, country_id):
        result_db = Town.objects.filter(country_id=country_id).all()
        return result_db

    def update_town(self, modify_info):
        is_exist = self.is_exist( modify_info["town"],modify_info["country_id"])
        if is_exist:
            raise Exception("该镇已存在")
        Town.objects.filter(nid=modify_info['nid']).update(**modify_info)

    def insert_town(self, modify_info):
        is_exist = self.is_exist(modify_info["town"],modify_info["country_id"])
        if is_exist:
            raise Exception("该镇已存在")
        Town.objects.create(**modify_info)

    def is_exist(self,town,country_id):
        result_db = Town.objects.filter(town=town, country_id=country_id).first()
        return result_db

nation_db = NationDB()
province_db = ProvinceDB()
city_db = CityDB()
country_db = CountryDB()
town_db = TownDB()