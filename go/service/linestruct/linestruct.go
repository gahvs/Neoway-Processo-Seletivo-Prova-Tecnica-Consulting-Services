package linestruct

type Line struct {
	Cpf                     string
	CpfValido               bool
	Private                 bool
	Incompleto              bool
	DataUltimaCompra        string
	TicketMedio             float64
	TicketUltimaCompra      float64
	LojaMaisFrequente       string
	LojaMaisFrequenteValido bool
	LojaUltimaCompra        string
	LojaUltimaCompraValido  bool
}
