--9--
select First.Year, Second.Year, Country.Name, ((Second.Rate - First.Rate) / (Second.Year - First.Year))
    from Country
    inner join LiteracyRate First on Country.Code = First.CountryCode
    inner join LiteracyRate Second on Country.Code = Second.CountryCode
    inner join LiteracyRate Mid on Country.Code = Mid.CountryCode
    where First.Year <= Mid.Year and Mid.Year < Second.Year
    group by Country.Name, First.Year, Second.Year
    having max(Mid.Year) = First.Year
    order by ((Second.Rate - First.Rate) / (Second.Year - First.Year)) desc;
    --order by Country.Name, First.Year, Second.Year, Mid.Year;

