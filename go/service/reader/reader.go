package reader

import (
	"bufio"
	"os"
)

type reader struct {
	filePointer *os.File
}

func NewReader(path string) (*reader, error) {

	file, err := os.Open(path)

	if err != nil {
		return nil, err
	}

	return &reader{
		filePointer: file,
	}, nil
}

func (r *reader) CloseFile() error {
	return r.filePointer.Close()
}

func (r *reader) ReadFile() []string {
	var content []string
	scanner := bufio.NewScanner(r.filePointer)
	for scanner.Scan() {
		content = append(content, scanner.Text())
	}
	return content
}
