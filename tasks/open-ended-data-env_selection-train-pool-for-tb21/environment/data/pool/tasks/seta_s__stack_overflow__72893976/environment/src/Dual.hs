module Dual
  ( HasDual(..)
  , makeBidirectional
  ) where

import Types

class HasDual a where
  dual :: a -> a

instance HasDual Direction where
  dual N = N
  dual S = S
  dual E = W
  dual W = E

instance HasDual Edge where
  dual (Edge from dir to') = Edge to' (dual dir) from

makeBidirectional :: [Edge] -> [Edge]
makeBidirectional es = es ++ map dual es
