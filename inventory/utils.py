from .server import country_db,city_db,province_db,nation_db

def build_region(country_id):
    if country_id:
        country_obj=country_db.query_country_by_id(country_id)
        city_obj=city_db.query_city_by_id(country_obj.city_id)
        province_obj=province_db.query_province_by_id(city_obj.province_id)
        nation_obj=nation_db.query_nation_by_id(province_obj.nation_id)
    return "{0}/{1}/{2}/{3}".format(nation_obj.nation,province_obj.province,city_obj.city,country_obj.country)