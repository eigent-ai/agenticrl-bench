module DualMap
  ( DualMap
  , empty
  , insert
  , lookupLeft
  , lookupRight
  , removeLeft
  , removeRight
  , toList
  , size
  ) where

import Data.Map.Strict (Map)
import qualified Data.Map.Strict as Map

data DualMap a b = DualMap
  { dmForward  :: Map a b
  , dmBackward :: Map b a
  } deriving (Show, Eq)

empty :: DualMap a b
empty = DualMap Map.empty Map.empty

insert :: (Ord a, Ord b) => a -> b -> DualMap a b -> DualMap a b
insert a b (DualMap fwd bwd) =
  let fwd1 = case Map.lookup a fwd of
               Just oldB -> let bwd' = Map.delete oldB bwd
                            in  (Map.insert a b fwd, bwd')
               Nothing   -> (Map.insert a b fwd, bwd)
      (fwd2, bwd1) = fwd1
      bwd2 = Map.insert b a bwd1
  in  DualMap fwd2 bwd2

lookupLeft :: Ord a => a -> DualMap a b -> Maybe b
lookupLeft a (DualMap fwd _) = Map.lookup a fwd

lookupRight :: Ord b => b -> DualMap a b -> Maybe a
lookupRight b (DualMap _ bwd) = Map.lookup b bwd

removeLeft :: (Ord a, Ord b) => a -> DualMap a b -> DualMap a b
removeLeft a (DualMap fwd bwd) =
  case Map.lookup a fwd of
    Nothing -> DualMap fwd bwd
    Just b  -> DualMap (Map.delete a fwd) (Map.delete b bwd)

removeRight :: (Ord a, Ord b) => b -> DualMap a b -> DualMap a b
removeRight b (DualMap fwd bwd) =
  case Map.lookup b bwd of
    Nothing -> DualMap fwd bwd
    Just a  -> DualMap (Map.delete a fwd) (Map.delete b bwd)

toList :: DualMap a b -> [(a, b)]
toList (DualMap fwd _) = Map.toList fwd

size :: DualMap a b -> Int
size (DualMap fwd _) = Map.size fwd
