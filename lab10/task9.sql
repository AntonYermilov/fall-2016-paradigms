--9--
select First.Year, Second.Year, Country.Name, ((Second.Rate - First.Rate) / (Second.Year - First.Year))
    from Country
    inner join LiteracyRate First on Country.Code = First.CountryCode
    inner join LiteracyRate Second on Country.Code = Second.CountryCode
    where First.Year < Second.Year and First.Year = (select max(LiteracyRate.Year)
                                                         from LiteracyRate
                                                         where LiteracyRate.CountryCode = Country.Code
                                                               and First.Year <= LiteracyRate.Year
                                                               and LiteracyRate.Year < Second.Year)
    order by ((Second.Rate - First.Rate) / (Second.Year - First.Year)) desc;

