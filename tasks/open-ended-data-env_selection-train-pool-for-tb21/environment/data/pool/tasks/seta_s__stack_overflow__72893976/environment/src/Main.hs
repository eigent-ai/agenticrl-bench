{-# LANGUAGE OverloadedStrings #-}
module Main where

import System.Environment (getArgs)
import qualified Data.Text.IO as TIO
import qualified Data.Text as T
import qualified Data.Map.Strict as Map
import Types
import SceneGraph
import TestMap
import Validation
import Interactable

main :: IO ()
main = do
  args <- getArgs
  case args of
    ["--test-map"]       -> runTestMap
    ["--test-inventory"] -> testInventoryOps
    ["--test-save-load"] -> testSaveLoad
    _                    -> TIO.putStrLn "Usage: adventure-engine [--test-map|--test-inventory|--test-save-load]"

runTestMap :: IO ()
runTestMap = do
  let sg = buildTestGraph
  TIO.putStrLn "=== Navigation Test ==="

  -- Test: go East from R1 to R2, then West back to R1
  let nav1 = navigate sg "R1" [E, W]
  TIO.putStrLn $ T.concat ["R1 -> E -> W = ", T.pack (show nav1), " (expected: Just R1)"]

  -- Test: go South from R1 to R4, then North back to R1
  let nav2 = navigate sg "R1" [S, N]
  TIO.putStrLn $ T.concat ["R1 -> S -> N = ", T.pack (show nav2), " (expected: Just R1)"]

  -- Test: longer path R1 -> E -> E -> S -> S (should reach R7 via R2->R3->R6->R7)
  let nav3 = navigate sg "R1" [E, E, S, S]
  TIO.putStrLn $ T.concat ["R1 -> E -> E -> S -> S = ", T.pack (show nav3), " (expected: Just R7)"]

  -- Test: reverse the long path
  let nav4 = navigate sg "R7" [N, N, W, W]
  TIO.putStrLn $ T.concat ["R7 -> N -> N -> W -> W = ", T.pack (show nav4), " (expected: Just R1)"]

  -- Print all neighbors
  TIO.putStrLn "\n=== Room Neighbors ==="
  mapM_ (\rid -> do
    let ns = neighbors sg rid
    TIO.putStrLn $ T.concat [rid, ": ", T.pack (show ns)]
    ) ["R1", "R2", "R3", "R4", "R5", "R6", "R7"]

  -- Print all edges
  TIO.putStrLn "\n=== All Edges ==="
  mapM_ (TIO.putStrLn . T.pack . show) (allEdges sg)

  -- Entity interactions
  TIO.putStrLn "\n=== Entity Interactions ==="
  let book = Entity "book" "Ancient Book" ItemType "A leather-bound tome."
      chest = Entity "chest" "Wooden Chest" ContainerType "A sturdy oak chest."
      fountain = Entity "fountain" "Stone Fountain" SceneryType "A flowing fountain."

  TIO.putStrLn $ T.concat ["Examine book: ", T.pack (show (examineEntity book))]
  TIO.putStrLn $ T.concat ["Examine chest: ", T.pack (show (examineEntity chest))]
  TIO.putStrLn $ T.concat ["Use fountain: ", T.pack (show (useEntity fountain))]
  TIO.putStrLn $ T.concat ["Combine book+chest: ", T.pack (show (combineEntities book chest))]

  -- Validation
  TIO.putStrLn "\n=== Validation ==="
  let errors = validateGraph sg testRooms
  TIO.putStrLn $ T.concat ["Validation errors: ", T.pack (show errors)]

  TIO.putStrLn "\n=== Test Map Complete ==="
