package writer

import (
	"encoding/json"
	"fmt"
	"log"
	"prova_tecnica/db"
	"prova_tecnica/linestruct"
)

type writer struct {
	data []linestruct.Line
}

func NewWriter() *writer {
	return &writer{}
}

func byteToStruct(data []byte) (*linestruct.Line, error) {

	var line linestruct.Line
	err := json.Unmarshal(data, &line)

	if err != nil {
		return nil, err
	}

	return &line, nil
}

func (w *writer) LoadData(data [][]byte) {
	for _, v := range data {
		line, err := byteToStruct(v)
		if err != nil {
			log.Fatal(err)
		}
		w.data = append(w.data, *line)
	}
}

func sqlInsertStatement(l linestruct.Line) string {
	if l.DataUltimaCompra != "NULL" {
		return fmt.Sprintf(`
		INSERT INTO BASE
		(CPF, CPF_VALIDO, PRIVADO, INCOMPLETO, DATA_ULTIMA_COMPRA, 
		TICKET_MEDIO, TICKET_ULTIMA_COMPRA, LOJA_MAIS_FREQUENTE, LOJA_MAIS_FRQUENTE_VALIDO, 
		LOJA_ULTIMA_COMPRA,LOJA_ULTIMA_COMPRA_VALIDO) 
		values ('%v', '%v', '%v', '%v', '%v', '%v', '%v', '%v', '%v', '%v', '%v');`,
			l.Cpf, l.CpfValido, l.Private, l.Incompleto, l.DataUltimaCompra, l.TicketMedio, l.TicketUltimaCompra,
			l.LojaMaisFrequente, l.LojaMaisFrequenteValido, l.LojaUltimaCompra, l.LojaUltimaCompraValido)
	} else {
		return fmt.Sprintf(`
		INSERT INTO BASE
		(CPF, CPF_VALIDO, PRIVADO, INCOMPLETO, DATA_ULTIMA_COMPRA, 
		TICKET_MEDIO, TICKET_ULTIMA_COMPRA, LOJA_MAIS_FREQUENTE, LOJA_MAIS_FRQUENTE_VALIDO, 
		LOJA_ULTIMA_COMPRA,LOJA_ULTIMA_COMPRA_VALIDO) 
		values ('%v', '%v', '%v', '%v', %v, '%v', '%v', '%v', '%v', '%v', '%v');`,
			l.Cpf, l.CpfValido, l.Private, l.Incompleto, l.DataUltimaCompra, l.TicketMedio, l.TicketUltimaCompra,
			l.LojaMaisFrequente, l.LojaMaisFrequenteValido, l.LojaUltimaCompra, l.LojaUltimaCompraValido)
	}
}

func (w *writer) WriteData(conn *db.Connection) {
	var sqlStatement string

	for _, v := range w.data {
		sqlStatement += sqlInsertStatement(v)
	}

	conn.Exec(sqlStatement)

	fmt.Println("Sucesso ao inserir")
}
