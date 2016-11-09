head' :: [a] -> a
head' (a : b) = a

tail' :: [a] -> [a]
tail' (a : b) = b

take' :: Int -> [a] -> [a]
take' 0 a = []
take' n [] = []
take' n (a : b) = a : (take' (n - 1) b)

drop' :: Int -> [a] -> [a]
drop' 0 a = a
drop' n [] = []
drop' n (a : b) = drop' (n - 1) b

filter' :: (a -> Bool) -> [a] -> [a]
filter' f [] = []
filter' f (a : b) | f a = a : (filter' f b)
                  | otherwise = filter' f b

foldl' :: (a -> b -> a) -> a -> [b] -> a
foldl' f z [] = z
foldl' f z (a : b) = foldl' f (f z a) b

concat' :: [a] -> [a] -> [a]
concat' [] b = b
concat' (l : r) b = l : (concat' r b)

quickSort' :: Ord a => [a] -> [a]
quickSort' [] = []
quickSort' a = let partition = head' a
               in concat' (concat' (quickSort' (filter' (< partition) a)) (filter' (== partition) a)) (quickSort' (filter' (> partition) a))
