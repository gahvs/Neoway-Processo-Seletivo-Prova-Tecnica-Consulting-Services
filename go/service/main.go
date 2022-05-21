package main

import (
	"fmt"
	"log"
	"path/filepath"
	"prova_tecnica/cleaner"
	"prova_tecnica/db"
	"prova_tecnica/reader"
	"prova_tecnica/writer"
)

func main() {

	absPath, err := filepath.Abs("./base/base.txt")
	if err != nil {
		log.Fatal(err)
	}

	reader, err := reader.NewReader(absPath)
	if err != nil {
		log.Fatal(err)
	}
	defer reader.CloseFile()

	fmt.Println("-> Lendo arquivo base ...")
	content := reader.ReadFile()

	fmt.Println("-> Tratando dados lidos ...")
	cleaner := cleaner.NewCleaner()
	cleanData := cleaner.CleanData(content)

	conn := db.GetDBConnection()
	defer conn.Close()

	conn.CreateDestinyTable()

	fmt.Println("-> Escrevendo dados no banco ...")
	writer := writer.NewWriter()
	writer.LoadData(cleanData[1:])

	writer.WriteData(conn)

	fmt.Println("-> Processo finalizado")
}
