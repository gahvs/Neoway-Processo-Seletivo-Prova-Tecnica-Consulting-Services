package processor

import (
	"strings"
)

func SplitAndRemoveOnlySpaces(source, sep string) []string {
	result := make([]string, 0)
	splited := strings.Split(source, sep)

	for _, item := range splited {
		if !(strings.TrimSpace(item) == "") {
			result = append(result, item)
		}
	}

	return result
}

func SwitchIntForBool(line []string) []string {
	result := make([]string, len(line))

	for i, v := range line {
		if v == "0" {
			result[i] = "false"
		} else if v == "1" {
			result[i] = "true"
		} else {
			result[i] = v
		}
	}

	return result
}

func SwitchCommaForDot(line []string) []string {
	result := make([]string, len(line))
	for i, v := range line {
		if strings.Contains(v, ",") {
			v = strings.ReplaceAll(v, ",", ".")
		}
		result[i] = v
	}
	return result
}

func SwitchNullForZeroInFloatFields(line []string, floatFields []int) []string {

	for _, v := range floatFields {
		if line[v] == "NULL" {
			line[v] = "0.0"
		}
	}

	return line
}
