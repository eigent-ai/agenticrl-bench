module SceneGraph
  ( SceneGraph
  , buildGraph
  , lookupEdge
  , allEdges
  , uniEdges
  , neighbors
  , navigate
  ) where

import Data.Map.Strict (Map)
import qualified Data.Map.Strict as Map
import Types
import Dual

data SceneGraph = SceneGraph
  { sgUniEdges :: [Edge]
  , sgAllEdges :: [Edge]
  , sgAdjMap   :: Map (RoomId, Direction) RoomId
  } deriving (Show, Eq)

buildGraph :: [Edge] -> SceneGraph
buildGraph uni =
  let allE = makeBidirectional uni
      adj  = Map.fromList [((edgeFrom e, edgeDirection e), edgeTo e) | e <- allE]
  in  SceneGraph uni allE adj

lookupEdge :: SceneGraph -> RoomId -> Direction -> Maybe RoomId
lookupEdge sg rid dir = Map.lookup (rid, dir) (sgAdjMap sg)

allEdges :: SceneGraph -> [Edge]
allEdges = sgAllEdges

uniEdges :: SceneGraph -> [Edge]
uniEdges = sgUniEdges

neighbors :: SceneGraph -> RoomId -> [(Direction, RoomId)]
neighbors sg rid =
  [ (d, to') | d <- [N, S, E, W]
             , Just to' <- [lookupEdge sg rid d]
  ]

navigate :: SceneGraph -> RoomId -> [Direction] -> Maybe RoomId
navigate _ current [] = Just current
navigate sg current (d:ds) =
  case lookupEdge sg current d of
    Nothing   -> Nothing
    Just next -> navigate sg next ds
