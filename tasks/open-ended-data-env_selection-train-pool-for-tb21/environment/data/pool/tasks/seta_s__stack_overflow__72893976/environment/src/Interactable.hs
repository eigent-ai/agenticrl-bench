{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE OverloadedStrings #-}
module Interactable
  ( Interactable(..)
  , InteractResult(..)
  , examineEntity
  , useEntity
  , combineEntities
  ) where

import Types
import Data.Text (Text)
import qualified Data.Text as T

data InteractResult
  = ExamineResult Text
  | UseResult Text Bool
  | CombineResult Text (Maybe Entity)
  deriving (Show, Eq)

class Interactable a where
  examine :: a -> InteractResult
  use     :: a -> InteractResult
  combine :: a -> a -> InteractResult

-- Instance for generic entities based on their type
-- This handles ItemType and SceneryType
instance Interactable Entity where
  examine e = case entityType e of
    ItemType      -> ExamineResult (T.concat ["You look at the ", entityName e, ". ", entityDesc e])
    SceneryType   -> ExamineResult (T.concat ["You observe the ", entityName e, ". ", entityDesc e])
    ContainerType -> ExamineResult (T.concat ["You examine the ", entityName e, ". ", entityDesc e])

  use e = case entityType e of
    ItemType    -> UseResult (T.concat ["You use the ", entityName e, "."]) True
    SceneryType -> UseResult (T.concat ["The ", entityName e, " cannot be used."]) False
    ContainerType -> UseResult (T.concat ["You open the ", entityName e, "."]) True

  combine a b = case (entityType a, entityType b) of
    (ItemType, ItemType) ->
      CombineResult
        (T.concat ["You combine the ", entityName b, " with the ", entityName a, "."])
        (Just Entity
          { entityId   = T.concat [entityId b, "_", entityId a]
          , entityName = T.concat [entityName b, " and ", entityName a]
          , entityType = ItemType
          , entityDesc = T.concat ["A combination of ", entityName b, " and ", entityName a, "."]
          })
    _ -> CombineResult (T.concat ["You can't combine the ", entityName a, " with the ", entityName b, "."]) Nothing

newtype ContainerEntity = ContainerEntity Entity

instance Interactable ContainerEntity where
  examine (ContainerEntity e) =
    ExamineResult (T.concat ["You peer inside the ", entityName e, ". ", entityDesc e, " It looks like it can hold things."])
  use (ContainerEntity e) =
    UseResult (T.concat ["You rummage through the ", entityName e, "."]) True
  combine (ContainerEntity a) (ContainerEntity b) =
    CombineResult
      (T.concat ["You nest the ", entityName a, " inside the ", entityName b, "."])
      Nothing

examineEntity :: Entity -> InteractResult
examineEntity = examine

useEntity :: Entity -> InteractResult
useEntity = use

combineEntities :: Entity -> Entity -> InteractResult
combineEntities = combine
