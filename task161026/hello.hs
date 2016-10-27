module Main where
import Data.Char (digitToInt, ord)

first' :: [Int] -> [Int]
last' :: [Int] -> [Int]

first' [] = []
first' (x : y) = [x]

last' [] = []
last' (x : y) = y

index :: Int -> [Int] -> Int
index k l = helper 1 k l
	where helper id' k l | l == [] = -1
					 	 | (first' l) == [k] = id'
					 	 | True = helper (id' + 1) k (last' l)

numberOfDigits :: Integer -> Int
numberOfDigits x = helper x x
	where helper a b | b == 0 = 1
					 | a == 0 = 0
					 | True = 1  + (helper (div a 10) b)

sumOfDigits :: Integer -> Integer
sumOfDigits x | x == 0 = 0
			  | True = (mod x 10) + (sumOfDigits (div x 10))


listOfDigits :: Integer -> [Int]
listOfDigits x = reverse (helper x x)
	where helper a b | b == 0 = [0]
					 | a == 0 = []
					 | True = ((fromIntegral(mod a 10))::Int) : (helper (div a 10) b)


isPalindrom x = (listOfDigits x) == (reverse (listOfDigits x))
