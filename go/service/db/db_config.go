package db

import (
	"log"

	"github.com/caarlos0/env"
)

type config struct {
	POSTGRES_HOST     string `env:"POSTGRES_HOST"`
	POSTGRES_NAME     string `env:"POSTGRES_NAME"`
	POSTGRES_USER     string `env:"POSTGRES_USER"`
	POSTGRES_PORT     string `env:"POSTGRES_PORT"`
	POSTGRES_PASSWORD string `env:"POSTGRES_PASSWORD"`
}

func ReadConfig() *config {
	cfg := config{}
	if err := env.Parse(&cfg); err != nil {
		log.Fatal(err)
	}
	return &cfg
}
