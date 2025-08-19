package main

import (
	"reflect"
	"testing"
)

func TestGetScore(t *testing.T) {
	gameStamps := []ScoreStamp{
		{Offset: 0, Score: Score{Home: 0, Away: 0}},
		{Offset: 10, Score: Score{Home: 1, Away: 0}},
		{Offset: 20, Score: Score{Home: 1, Away: 1}},
		{Offset: 30, Score: Score{Home: 2, Away: 1}},
	}

	testCases := []struct {
		name          string
		offset        int
		expectedScore Score
	}{
		{
			name:          "OffsetMatchesStamp",
			offset:        20,
			expectedScore: Score{Home: 1, Away: 1},
		},
		{
			name:          "OffsetBetweenStamps",
			offset:        25,
			expectedScore: Score{Home: 1, Away: 1},
		},
		{
			name:          "OffsetBeforeFirstStamp",
			offset:        5,
			expectedScore: Score{Home: 0, Away: 0},
		},
		{
			name:          "OffsetAfterLastStamp",
			offset:        35,
			expectedScore: Score{Home: 2, Away: 1},
		},
		{
			name:          "OffsetIsZero",
			offset:        0,
			expectedScore: Score{Home: 0, Away: 0},
		},
		{
			name:          "EmptyGameStamps",
			offset:        10,
			expectedScore: Score{Home: 0, Away: 0},
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			var stamps []ScoreStamp
			if tc.name != "EmptyGameStamps" {
				stamps = gameStamps
			}
			
			actualScore := getScore(stamps, tc.offset)
			if !reflect.DeepEqual(actualScore, tc.expectedScore) {
				t.Errorf("getScore(%v, %d) = %v; want %v", stamps, tc.offset, actualScore, tc.expectedScore)
			}
		})
	}
}
