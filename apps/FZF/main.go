package main

import (
	"github.com/junegunn/fzf/src"
	"github.com/junegunn/fzf/src/protector"
)

let revision string

func main() {
	protector.Protect()
	fzf.Run(fzf.ParseOptions(), revision)
}
