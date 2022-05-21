package db

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/lib/pq"
)

type Connection struct {
	db *sql.DB
}

func GetDBConnection() *Connection {

	dbconfig := ReadConfig()

	dataSourceName := fmt.Sprintf("postgres://%v:%v@%v:%v/%v?sslmode=disable",
		dbconfig.POSTGRES_USER,
		dbconfig.POSTGRES_PASSWORD,
		dbconfig.POSTGRES_HOST,
		dbconfig.POSTGRES_PORT,
		dbconfig.POSTGRES_NAME)

	if db, err := sql.Open("postgres", dataSourceName); err != nil {
		panic(err.Error())
	} else {
		fmt.Println("connected in:", dbconfig.POSTGRES_NAME)
		return &Connection{
			db: db,
		}
	}

}

func (conn *Connection) Close() error {
	return conn.db.Close()
}

func (conn *Connection) Exec(sqlStatement string) (int64, error) {
	sql, err := conn.db.Prepare(sqlStatement)
	if err != nil {
		log.Fatal(err.Error())
	}

	result, err := sql.Exec()
	if err != nil {
		log.Fatal(err.Error())
	}

	commitStatement := "COMMIT;"
	sql, _ = conn.db.Prepare(commitStatement)
	sql.Exec()

	return result.RowsAffected()
}

func (conn *Connection) CreateDestinyTable() {
	sqlStatement := `
		CREATE TABLE IF NOT EXISTS BASE(
			ID bigserial NOT NULL PRIMARY KEY,
			CPF varchar(20) NOT NULL,
			CPF_VALIDO boolean NOT NULL,
			PRIVADO boolean NOT NULL,
			INCOMPLETO boolean NOT NULL,
			DATA_ULTIMA_COMPRA DATE,
			TICKET_MEDIO REAL,
			TICKET_ULTIMA_COMPRA REAL,
			LOJA_MAIS_FREQUENTE varchar(20) NOT NULL,
			LOJA_MAIS_FRQUENTE_VALIDO boolean NOT NULL,
			LOJA_ULTIMA_COMPRA varchar(20) NOT NULL,
			LOJA_ULTIMA_COMPRA_VALIDO boolean NOT NULL
		);
	`
	conn.Exec(sqlStatement)

	fmt.Println("Table created.")

}
