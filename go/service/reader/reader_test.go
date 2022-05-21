package reader

import (
	"path/filepath"
	"testing"
)

func TestNewReader(t *testing.T) {
	absPath, _ := filepath.Abs("test.txt")
	_, err := NewReader(absPath)
	if err != nil {
		t.Error("Falha ao abrir arquivo:", absPath)
	}
}

func TestFileCloser(t *testing.T) {
	absPath, _ := filepath.Abs("test.txt")
	r, _ := NewReader(absPath)
	if r.CloseFile() != nil {
		t.Error("Falhar ao fechar arquivo")
	}
}
