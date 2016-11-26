--8--
select Country.Name, Country.Population, Country.SurfaceArea
    from Country
    inner join City JustCity on Country.Code = JustCity.CountryCode
    inner join Capital on Country.Code = Capital.CountryCode
    inner join City CapitalCity on Capital.CityId = CapitalCity.Id
    group by Country.Name
    having max(JustCity.Population) and JustCity.Id <> CapitalCity.Id
    order by (1.0 * Country.Population / Country.SurfaceArea) desc, Country.Name;

