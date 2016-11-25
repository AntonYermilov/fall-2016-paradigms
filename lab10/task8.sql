--8--
select Country.Name, Country.Population, Country.SurfaceArea
    from Country
    inner join City on Country.Code = City.CountryCode
    inner join Capital on Country.Code = Capital.CountryCode
    where City.Id = Capital.CityId and City.Population < (select City.Population
                                                              from City
                                                              where City.CountryCode = Country.Code)
    order by (1.0 * Country.Population / Country.SurfaceArea) desc, Country.Name;

