package main
 
import "fmt"

// Defined any type to make generic function
type any = interface{}
 
// A generic function that returns any type
// dummy function for Church funtions type
type fn func(any) any
 
// Church type is a function that returns a function
type Church func(fn) fn
 
// Zero funtion that represents the zero value of Church numerals
// It's a constant function
func Zero(f fn) fn {
    return func(x any) any {
        return x
    }
}
 
// Successor Church numerals, all Church numerals are represented by functions
// When aplied to a Church numeral, it returns the representation of the next Church numeral
func (c Church) Suc() Church {
    return func(f fn) fn {
        return func(x any) any {
            return f(c(f)(x))
        }
    }
}
 
// litle demostration of Church numerals
func main() {
    zero := Church(Zero)
    three := zero.Suc().Suc().Suc()
    four := three.Suc()
    fmt.Printf("The type of four is %T\n", four)
}