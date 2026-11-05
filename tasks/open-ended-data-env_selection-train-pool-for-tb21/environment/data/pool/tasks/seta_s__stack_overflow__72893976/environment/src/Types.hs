module Types
  ( Direction(..)
  , RoomId
  , Room(..)
  , Edge(..)
  , Entity(..)
  , EntityType(..)
  , ItemId
  , GameWorld(..)
  , GameError(..)
  , GameFlag(..)
  ) where

import Data.Map.Strict (Map)
import Data.Text (Text)
import Data.Set (Set)

data Direction = N | S | E | W
  deriving (Show, Read, Eq, Ord, Enum, Bounded)

type RoomId = Text

data Room = Room
  { roomId          :: RoomId
  , roomName        :: Text
  , roomDescription :: Text
  , roomEntities    :: [Entity]
  } deriving (Show, Eq)

data Edge = Edge
  { edgeFrom      :: RoomId
  , edgeDirection  :: Direction
  , edgeTo        :: RoomId
  } deriving (Show, Eq, Ord)

data EntityType = ItemType | SceneryType | ContainerType
  deriving (Show, Read, Eq, Ord)

type ItemId = Text

data Entity = Entity
  { entityId   :: ItemId
  , entityName :: Text
  , entityType :: EntityType
  , entityDesc :: Text
  } deriving (Show, Eq, Ord)

data GameFlag = GameFlag Text
  deriving (Show, Read, Eq, Ord)

data GameWorld = GameWorld
  { worldRooms     :: Map RoomId Room
  , worldEdges     :: [Edge]
  , worldInventory :: Map ItemId RoomId
  , worldPlayerInv :: Set ItemId
  , worldPlayerLoc :: RoomId
  , worldFlags     :: Set GameFlag
  } deriving (Show, Eq)

data GameError
  = NoSuchRoom RoomId
  | NoSuchDirection Direction
  | NoSuchItem ItemId
  | InvalidAction Text
  | SerializationError Text
  deriving (Show, Eq)
