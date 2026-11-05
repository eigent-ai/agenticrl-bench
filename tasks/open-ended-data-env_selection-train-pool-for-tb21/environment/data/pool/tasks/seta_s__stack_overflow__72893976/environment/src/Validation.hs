module Validation
  ( ValidationError(..)
  , validateGraph
  , validateEdges
  , validateRoomRefs
  ) where

import Types
import SceneGraph
import Data.Map.Strict (Map)
import qualified Data.Map.Strict as Map
import Data.Text (Text)
import qualified Data.Text as T
import Data.List (group, sort)

data ValidationError
  = DuplicateEdge RoomId Direction
  | MissingRoom RoomId
  | ConflictingEdges RoomId Direction RoomId RoomId
  deriving (Show, Eq)

validateEdges :: SceneGraph -> [ValidationError]
validateEdges sg =
  let edges = uniEdges sg
      grouped = Map.toList $ Map.fromListWith (++)
        [((edgeFrom e, edgeDirection e), [edgeTo e]) | e <- edges]
      conflicts = [ ConflictingEdges room dir (head dests) (dests !! 1)
                   | ((room, dir), dests) <- grouped
                   , length dests > 1
                   ]
  in  conflicts

validateRoomRefs :: SceneGraph -> Map RoomId Room -> [ValidationError]
validateRoomRefs sg rooms =
  let edges = allEdges sg
      allRoomIds = concatMap (\e -> [edgeFrom e, edgeTo e]) edges
      missing = filter (\rid -> not (Map.member rid rooms)) allRoomIds
  in  map MissingRoom (map head . group . sort $ missing)

validateGraph :: SceneGraph -> Map RoomId Room -> [ValidationError]
validateGraph sg rooms = validateEdges sg ++ validateRoomRefs sg rooms
