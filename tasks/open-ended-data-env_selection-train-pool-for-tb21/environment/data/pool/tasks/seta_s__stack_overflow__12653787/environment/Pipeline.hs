module Pipeline where

import ListUtils
import Stats

processData :: [Int] -> (Summary Int, Summary Int)
processData xs = (evenStats, oddStats)
  where
    evenNums  = myFilter even xs
    oddNums   = myFilter odd xs
    doubled   = myMap (* 2) evenNums
    tripled   = myMap (* 3) oddNums
    evenStats = computeSummary doubled
    oddStats  = computeSummary tripled
