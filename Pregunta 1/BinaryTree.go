package main

import (
	"math/rand"
	"reflect"
	"time"
)

// Binary Tree
type BinaryTree struct {
	Value int
	leaf  bool
	Left  interface{} // Puede ser un BinaryTree o un int
	Right interface{}
}

// NewBinaryTree returns a new BinaryTree
func NewBinaryTree(value int) *BinaryTree {
	return &BinaryTree{Value: value}
}

// Insert inserts a new value into the BinaryTree
func (t *BinaryTree) Insert(value int, branch ...bool) {
	if t.Left == nil {
		t.Left = NewBinaryTree(value)
		return
	}
	if t.Right == nil {
		t.Right = NewBinaryTree(value)
		return
	}
	if branch[0] {
		t.Left.(*BinaryTree).Insert(value, branch[0])
	} else {
		t.Right.(*BinaryTree).Insert(value, branch[0])
	}

}

// InsertLeaf inserts information into the leaf of the BinaryTree
func (t *BinaryTree) InsertLeaf(value int, branch ...bool) {
	if t.Left == nil {
		t.Left = value
		t.leaf = true
		return
	}
	if t.Right == nil {
		t.Right = value
		t.leaf = true
		return
	}
	if branch[0] {
		t.Left.(*BinaryTree).InsertLeaf(value, branch[0])
	} else {
		t.Right.(*BinaryTree).InsertLeaf(value, branch[0])
	}
}

// preOrder traverses the BinaryTree in pre-order and returns a slice of int
func (t *BinaryTree) preOrder() []int {
	var result []int
	if t == nil {
		return result
	}
	result = append(result, t.Value)
	if t.Left != nil {
		if tl, ok := t.Left.(*BinaryTree); ok {
			result = append(result, tl.preOrder()...)
		} else {
			result = append(result, t.Left.(int))
		}
	}
	if t.Right != nil {
		if tr, ok := t.Right.(*BinaryTree); ok {
			result = append(result, tr.preOrder()...)
		} else {
			result = append(result, t.Right.(int))
		}
	}
	return result
}

// postOrder traverses the BinaryTree in post-order and returns a slice of int
func (t *BinaryTree) postOrder() []int {
	var result []int
	if t == nil {
		return result
	}
	if t.Left != nil {
		if tl, ok := t.Left.(*BinaryTree); ok {
			result = append(result, tl.postOrder()...)
		} else {
			result = append(result, t.Left.(int))
		}
	}
	if t.Right != nil {
		if tr, ok := t.Right.(*BinaryTree); ok {
			result = append(result, tr.postOrder()...)
		} else {
			result = append(result, t.Right.(int))
		}
	}
	result = append(result, t.Value)
	return result
}

// isMaxHeap checks if the BinaryTree is a max heap
func (t *BinaryTree) isMaxHeap() bool {
	r1 := true
	r2 := true
	if t == nil {
		return true
	}
	if t.Left != nil {
		if tl, ok := t.Left.(*BinaryTree); ok {
			if t.Value < t.Left.(*BinaryTree).Value {
				return false
			}
			r1 = tl.isMaxHeap()
		} else {
			if t.Value < t.Left.(int) {
				return false
			}
		}
	}
	if t.Right != nil {
		if tr, ok := t.Right.(*BinaryTree); ok {
			if t.Value < t.Right.(*BinaryTree).Value {
				return false
			}
			r2 = tr.isMaxHeap()
		} else {
			if t.Value < t.Right.(int) {
				return false
			}
		}
	}
	return r1 && r2
}

// isSimetric checks if the BinaryTree is simetric
func (t *BinaryTree) isSimetric() bool {
	if t == nil {
		return true
	}
	preOrd := t.preOrder()
	postOrd := t.postOrder()
	if reflect.DeepEqual(preOrd, postOrd) {
		return true
	}
	return false
}

func (t *BinaryTree) isMaxHeapSimetric() bool {
	if t.isMaxHeap() && t.isSimetric() {
		return true
	}
	return false
}

func main() {
	s1 := rand.NewSource(time.Now().UnixNano())
    rand := rand.New(s1)
	var root = NewBinaryTree(rand.Intn(100))
	root.Insert(rand.Intn(100))
	root.Insert(rand.Intn(100))
	root.Insert(rand.Intn(100),true)
	root.Insert(rand.Intn(100),false)
	root.InsertLeaf(rand.Intn(100),true)
	root.InsertLeaf(rand.Intn(100),false)
	println(root.isMaxHeapSimetric())

	root = NewBinaryTree(100)
	root.Insert(50)
	root.Insert(75)
	root.Insert(25, true)
	root.Insert(35, false)
	root.InsertLeaf(15, true)
	root.InsertLeaf(20, false)
	println(root.isMaxHeapSimetric())

	root = NewBinaryTree(10)
	root.Insert(10)
	root.Insert(10)
	root.Insert(10, true)
	root.Insert(10, false)
	root.InsertLeaf(10, true)
	println(root.isMaxHeapSimetric())
	root.InsertLeaf(10, false)
}