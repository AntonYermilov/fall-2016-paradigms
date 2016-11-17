import Prelude hiding (lookup)


data BinaryTree k v = None | Node {
	key    :: k,
	value  :: v,
	left   :: BinaryTree k v,
	right  :: BinaryTree k v
} deriving (Eq)

lookup :: Ord k => k -> BinaryTree k v -> Maybe v
merge  :: Ord k => BinaryTree k v -> BinaryTree k v -> BinaryTree k v
insert :: Ord k => k -> v -> BinaryTree k v -> BinaryTree k v
delete :: Ord k => k -> BinaryTree k v -> BinaryTree k v

lookup key' None = Nothing
lookup key' node | (key node) > key' = lookup key' (left node)
                 | (key node) < key' = lookup key' (right node)
				 | otherwise = Just (value node)

merge None node2 = node2
merge node1 None = node1
merge node1 node2 | (key node1) < (key node2) = Node (key node1) (value node1) (left node1) (merge (right node1) node2)
                  | otherwise = Node (key node2) (value node2) (merge node1 (left node2)) (right node2)

insert key' value' None = Node key' value' None None
insert key' value' node | (key node) > key' = Node (key node) (value node) (insert key' value' (left node)) (right node)
                        | (key node) < key' = Node (key node) (value node) (left node) (insert key' value' (right node))
						| otherwise = Node key' value' (left node) (right node)

delete key' None = None
delete key' node | (key node) > key' = Node (key node) (value node) (delete key' (left node)) (right node)
				 | (key node) < key' = Node (key node) (value node) (left node) (delete key' (right node))
				 | otherwise = merge (left node) (right node)
