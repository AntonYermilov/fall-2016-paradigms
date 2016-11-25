--3--
select City.Name
    from Country 
    inner join City on Country.Code = City.CountryCode
    inner join Capital on Country.Code = Capital.CountryCode
    where Country.Name like "Malaysia" and Capital.CityId = City.Id;

