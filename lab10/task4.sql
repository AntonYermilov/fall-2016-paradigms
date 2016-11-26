--4--
select Country.Name, sum(Country.Code = City.CountryCode and City.Population >= 1000000) CNT
    from Country, City
    group by Country.Name
    order by CNT desc, Country.Name;

