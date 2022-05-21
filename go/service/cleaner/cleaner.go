package cleaner

import (
	"encoding/json"
	"log"
	"prova_tecnica/cleaner/processor"
	"prova_tecnica/linestruct"
	"strconv"

	"github.com/klassmann/cpfcnpj"
)

type cleaner struct {
	cleanData [][]byte
}

func newLineStruct(data []string) *linestruct.Line {

	tcktMedio, _ := strconv.ParseFloat(data[4], 64)
	tcktUltCompra, _ := strconv.ParseFloat(data[5], 64)
	private, _ := strconv.ParseBool(data[1])
	incompleto, _ := strconv.ParseBool(data[2])

	return &linestruct.Line{
		Cpf:                     data[0],
		CpfValido:               cpfcnpj.ValidateCPF(data[0]),
		Private:                 private,
		Incompleto:              incompleto,
		DataUltimaCompra:        data[3],
		TicketMedio:             tcktMedio,
		TicketUltimaCompra:      tcktUltCompra,
		LojaMaisFrequente:       data[6],
		LojaMaisFrequenteValido: cpfcnpj.ValidateCNPJ(data[6]),
		LojaUltimaCompra:        data[7],
		LojaUltimaCompraValido:  cpfcnpj.ValidateCNPJ(data[7]),
	}
}

func NewCleaner() *cleaner {
	return &cleaner{
		cleanData: make([][]byte, 0),
	}
}

func (c *cleaner) CleanData(data []string) [][]byte {

	var line []string

	for _, v := range data[1:] {

		line = processor.SplitAndRemoveOnlySpaces(v, " ")
		line = processor.SwitchIntForBool(line)
		line = processor.SwitchCommaForDot(line)
		line = processor.SwitchNullForZeroInFloatFields(line, []int{4, 5})

		lineStruct := newLineStruct(line)
		lineJson, err := json.Marshal(lineStruct)

		if err != nil {
			log.Fatal(err)
		}

		c.cleanData = append(c.cleanData, lineJson)
	}
	return c.cleanData
}
