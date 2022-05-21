package cleaner

import "testing"

func TestNewCleaner(t *testing.T) {
	if NewCleaner() == nil {
		t.Error("Falha ao criar Cleaner")
	}
}
