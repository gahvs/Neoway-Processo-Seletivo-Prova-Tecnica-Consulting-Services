package processor

import (
	"fmt"
	"reflect"
	"testing"
)

func TestSplitAndRemoveOnlySpaces(t *testing.T) {
	source, sep := "A B  C   D    E     F", " "

	want := []string{"A", "B", "C", "D", "E", "F"}
	got := SplitAndRemoveOnlySpaces(source, sep)

	if !reflect.DeepEqual(want, got) {
		t.Error("Erro na separação da linha")
		fmt.Println("Esperado:", want)
		fmt.Println("Recebido:", got)
	}
}

func TestSwitchIntForBool(t *testing.T) {
	source := []string{"041.091.641-25", "0", "1", "NULL", "NULL", "NULL", "NULL", "NULL"}
	want := []string{"041.091.641-25", "false", "true", "NULL", "NULL", "NULL", "NULL", "NULL"}

	got := SwitchIntForBool(source)

	if !reflect.DeepEqual(want, got) {
		t.Error("Erro na separação na conversão \"0\"->\"false\" | \"1\"->\"true\"")
		fmt.Println("Esperado:", want)
		fmt.Println("Recebido:", got)
	}

}

func TestSwitchCommaForDot(t *testing.T) {
	source := []string{"691.987.489-04", "0", "0", "2011-12-15", "1799,00", "1799,00", "79.379.491/0001-83", "79.379.491/0001-83"}
	want := []string{"691.987.489-04", "0", "0", "2011-12-15", "1799.00", "1799.00", "79.379.491/0001-83", "79.379.491/0001-83"}

	got := SwitchCommaForDot(source)

	if !reflect.DeepEqual(want, got) {
		t.Error("Erro na separação na conversão")
		fmt.Println("Esperado:", want)
		fmt.Println("Recebido:", got)
	}
}

func TestSwitchNullForZeroInFloatFields(t *testing.T) {
	floatFields := []int{4, 5}
	source := []string{"041.091.641-25", "0", "1", "NULL", "NULL", "NULL", "NULL", "NULL"}
	want := []string{"041.091.641-25", "0", "1", "NULL", "0.0", "0.0", "NULL", "NULL"}

	got := SwitchNullForZeroInFloatFields(source, floatFields)

	if !reflect.DeepEqual(want, got) {
		t.Error("Erro na separação na conversão")
		fmt.Println("Esperado:", want)
		fmt.Println("Recebido:", got)
	}

}
