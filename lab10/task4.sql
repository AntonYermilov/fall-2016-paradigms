--4--
select Country.Name, sum(Country.Code = City.CountryCode and City.Population >= 1000000)
    from Country, City
    group by Country.Name
    order by sum(Country.Code = City.CountryCode and City.Population >= 1000000) desc, Country.Name;

