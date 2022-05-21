package writer

import (
	"fmt"
	"prova_tecnica/linestruct"
	"reflect"
	"testing"
)

func TestNewWriter(t *testing.T) {
	w := NewWriter()
	if w == nil {
		t.Error("Falha ao criar Writer")
	}
}

func TestByteToStruct(t *testing.T) {
	source := []byte(`	{
		"Cpf": "041.091.641-25",
		"CpfValido": false,
		"Private": false,
		"Incompleto": false,
		"DataUltimaCompra": "NULL",
		"TicketMedio": 0,
		"TicketUltimaCompra": 0,
		"LojaMaisFrequente": "NULL",
		"LojaMaisFrequenteValido": false,
		"LojaUltimaCompra": "NULL",
		"LojaUltimaCompraValido": false
	}`)

	want := &linestruct.Line{
		Cpf:                     "041.091.641-25",
		CpfValido:               false,
		Private:                 false,
		Incompleto:              false,
		DataUltimaCompra:        "NULL",
		TicketMedio:             0,
		TicketUltimaCompra:      0,
		LojaMaisFrequente:       "NULL",
		LojaMaisFrequenteValido: false,
		LojaUltimaCompra:        "NULL",
		LojaUltimaCompraValido:  false,
	}

	got, _ := byteToStruct(source)

	if !reflect.DeepEqual(want, got) {
		t.Error("Erro na separação na conversão")
		fmt.Println("Esperado:", want)
		fmt.Println("Recebido:", got)
	}

}
